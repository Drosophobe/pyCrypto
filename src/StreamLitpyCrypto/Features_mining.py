import streamlit as st
import numpy as np
import pandas as pd
from universal import tools, algos
from universal.algos import *
import matplotlib.pyplot as plt
from datetime import timedelta
import time
import os

def perform(result):
    return result.sharpe, result.alpha_beta()[1]
def volatility(data):
    # On crée une fonction qui retourne le volatilté de l'action dans une window définie plus bas
    return np.log(data/data.shift()).std()
def max_range(data):
    # On crée une fonction qui retourne l'amplitude max de la valeure
    return np.max(data)-np.min(data)
def create_Features(mrkt, snr, algos, nom_algos):

    metric_name = ['Ratio de Sharpe', 'beta']

    #Mesure de performance
    sharp = []
    metrics = []
    # On récupère le df en question
    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=True)
    # On les tweets du df
    df_len_cryto_tweets = pd.read_csv(f"../../data/cryptos/tweets/extract_dates/date_{snr}.csv", sep = '\t', parse_dates= [0], index_col=0)
    df_len_nasdaq_tweets = pd.read_csv(f"../../data/nasdaq/tweets/extract_dates/date_{snr}.csv", sep='\t', parse_dates=[0], index_col=0)
    # On supprime le ^VIX_vol car il est toujours à 0 c'est un indicateur
    df = df.drop(["^VIX_Vol"], axis = 1)
    # On fill les nan car si on travail avec la cryptos il est possible que la bourse ne soit pas ouverte
    df["^VIX_Close"] = df["^VIX_Close"].fillna(df["^VIX_Close"].mean())
    # On récupères les noms des col avec closes, vols ou vix pour faire plusieurs DF (SRQ)
    liste_close= []
    liste_vol = []
    liste_vix = []
    for clo in df.columns:
        if "^VIX_Close" in clo :
            liste_vix.append(clo)
        elif "Close" in clo:
            liste_close.append(clo)
        elif 'Vol' in clo:
            liste_vol.append(clo)
    S = df[liste_close]
    S = S.dropna(axis=1)
    R = df[liste_vol]
    R = R.dropna(axis=1)
    Q = df[liste_vix]
    Q = Q.dropna(axis = 1)
    # On set la window sur laquelle on veut faire du ML et on calcule le nombre de window par scenaris
    window = 10
    wndw_nbr = S.shape[0] // window
    T = S.copy()[[]]
    # On crée un DF T qui fait la même taille que nos autres df mais vide dans lequel on viendra mettres nos valeurs calculés
    T["Mean_Close_Volatility"] = 0
    T['Mean_Close_Range'] = 0
    T["Mean_Vol_Volatility"] = 0
    T['Mean_Vol_Range'] = 0
    # On crée des columns de ce qu'on veut que l'on viendra update plus tard
    for e in S.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0
        # Pour chaque close on ajoute une col volarility et range qu'on viendra update plus tard
    for i in np.arange(0, df.shape[0]+1, window):
        for e in S.columns:
            T[f"{e}_volatility"].iloc[i:i +window] = volatility(S[e].iloc[i:i +window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(S[e].iloc[i:i + window])
    # On calcule la volatilité et la range de chaque closes par windows et on update les cols
    for e in R.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0
        # Pour chaque volume on ajoute une col volarility et range qu'on viendra update plus tard
    T["VIX_range"] = 0
    T["VIX_mean"] = 0
    T['VIX_volatility'] = 0
    date_list = []
    # On crée Trois cols range, volati et mean pour le VIX qu'on viendra update plus tard
    for i in np.arange(0, df.shape[0]+1, window):
        for e in R.columns:
            T[f"{e}_volatility"].iloc[i:i +window] = volatility(R[e].iloc[i:i +window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(R[e].iloc[i:i + window])
        # On calcule la volatilité et la range de chaque volume par windows et on update les cols
        T["VIX_range"].iloc[i:i + window] = max_range(Q["^VIX_Close"].iloc[i:i+window])
        T["VIX_mean"].iloc[i:i + window] = np.mean(Q["^VIX_Close"].iloc[i:i + window])
        T["VIX_volatility"].iloc[i:i + window] = volatility(Q["^VIX_Close"].iloc[i:i + window])
        if i != 0:
            date_list.append(df.index[i-1])
        else :
            date_list.append(df.index[0])
    my_len_cryptos_tweets_list = []
    my_len_nasdaq_tweets_list = []

    for i in range(len(date_list)):
        my_len_cryptos_tweets_list.append(df_len_cryto_tweets.loc[date_list[i]:date_list[i+1]].sum(axis = 0).values[0])
        my_len_nasdaq_tweets_list.append(df_len_nasdaq_tweets.loc[date_list[i]:date_list[i + 1]].sum(axis=0).values[0])
        if i == len(date_list)-2:
            break

        # On calcule la volatilité, la mean et la range du  VIX par windows et on update les cols
    list_close_Vol_names = []
    list_close_Ran_names = []
    list_vol_Vol_names = []
    list_vol_Ran_names = []
    # On crée des listes vides des valeurs qu'on va utliser pour le ML
    for i in T.columns:
        if 'Close_volatility' in i:
            list_close_Vol_names.append(i)
        elif 'Close_range' in i:
            list_close_Ran_names.append(i)
        elif 'Vol_volatility' in i:
            list_vol_Vol_names.append(i)
        elif 'Vol_range' in i:
            list_vol_Ran_names.append(i)
    # On fait la moyennes des volatil et des ranges sur les closes et les volumes qu'on vient mettre dans notre df T
    T['Mean_Close_Volatility'] = T[list_close_Vol_names].mean(axis=1)
    T['Mean_Close_Range'] = T[list_close_Ran_names].mean(axis=1)
    T['Mean_Vol_Volatility'] = T[list_vol_Vol_names].mean(axis=1)
    T['Mean_Vol_Range'] = T[list_vol_Ran_names].mean(axis=1)
    # On update la valeur de mean_volatility avec les moyennes de chaques volatilty des actions par window
    #st.write(T)
    # On check notre df
    window_i = 10
    my_close_volatility_list = []
    my_close_range_list = []
    my_vol_volatility_list = []
    my_vol_range_list = []
    my_vix_volatility_list =[]
    my_vix_mean_list =[]
    my_vix_range_list = []
    for i in range(wndw_nbr):
        my_close_volatility_list.append(T['Mean_Close_Volatility'].iloc[window_i-1])
        my_close_range_list.append(T['Mean_Close_Range'].iloc[window_i - 1])
        my_vol_volatility_list.append(T['Mean_Vol_Volatility'].iloc[window_i-1])
        my_vol_range_list.append(T['Mean_Vol_Range'].iloc[window_i - 1])
        my_vix_volatility_list.append(T["VIX_range"].iloc[window_i - 1])
        my_vix_mean_list.append(T["VIX_mean"].iloc[window_i - 1])
        my_vix_range_list.append(T["VIX_volatility"].iloc[window_i - 1])
        window_i  += window







    #st.write("close volatility list\n", my_close_volatility_list)
    #st.write("close range list\n", my_close_range_list)
    #st.write("vol volatility list\n", my_vol_volatility_list)
    #st.write("vol range list\n", my_vol_range_list)
    # On afficher la liste des volatilties obtenues en prenant l'avant dernière valeurs de la window et on l'affiche
    list_metrics = []

    best_model_list = []
    for wd in range(wndw_nbr):
        for algo in algorithmes:
                result = algo.run(S.iloc[wd * window: (wd + 1) * window-1, :])
                sharp = [perform(result)[0], perform(result)[1]]
                metrics.append(sharp)
                sharpe = []
        #st.write('************ ' + snr + ' **********')
        X = pd.DataFrame(data=np.array(metrics[wd*len(algorithmes):(wd+1)*len(algorithmes)]), columns=metric_name, index=noms_algos)
        Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
        Y = Y[Y['Ratio de Sharpe'] > 1].head(1)
        # Selection du meilleur algo si il existe on le met dans notre liste
        if len(list(Y.index)) == 1:
            best_model_list.append(list(Y.index)[0])
        else:
            best_model_list.append('?')
        # On recupère le meilleur model si il existe sinon un "?"

    # On crée un df qui regroupe toutes les features calculés qu'on utilisera dans le problème de ML
    df_best_model = pd.DataFrame.from_dict({"algo": best_model_list, "close_volatility": my_close_volatility_list, 'close_range': my_close_range_list,
                                            "vol_volatility": my_vol_volatility_list, 'vol_range': my_vol_range_list, 'market': mrkt,
                                            "VIX_range": my_vix_range_list, "VIX_volatility" : my_vix_volatility_list, 'VIX_mean': my_vix_mean_list,
                                            "nbr_of_cryptos_tweets": my_len_cryptos_tweets_list, "nbr_of_nasdaq_tweets": my_len_nasdaq_tweets_list})

    os.makedirs(f'assets/best_models/{"_". join(noms_algos)}/{mrkt}', exist_ok=True)
    df_best_model.to_csv(f'assets/best_models/{"_". join(noms_algos)}/{mrkt}/{snr}.csv')

    """plt.figure(figsize=(12, 6))
    plt.text(10, 10, 'Parabola $Y = x^2$', fontsize=22)
    plt.plot(df_best_model['close_volatility'])
    j = 0


    plt.xticks(rotation=60)
    plt.title(f'{snr}_{mrkt}')
    plt.ylabel('Mean Volatility')
    plt.xlabel('Windows (10 days)')
    plt.show()"""
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot(111)
    ax.plot(T['Mean_Close_Volatility'])
    t = ax.set_title(f'{snr}_{mrkt}')
    i = 0
    print(mrkt)
    print(snr)
    print(len(T['Mean_Close_Volatility'].unique()))
    print(df_best_model['algo'])
    if mrkt == 'cryptos':
        values = T['Mean_Close_Volatility'].unique()
    elif mrkt =='nasdaq':
        values = T['Mean_Close_Volatility'].unique()
        values = np.resize(values, values.size - 1)
    '''if mrkt =='nasdaq' and snr == 'rdm2_DF':
        values = T['Mean_Close_Volatility'].unique()
        values = np.resize(values, values.size - 1)
    elif mrkt =='nasdaq' and  snr == 'rdm1_DF':
        values = T['Mean_Close_Volatility'].unique()
    elif mrkt =='nasdaq' and  snr == 'année_2018_flat_DF':
        values = T['Mean_Close_Volatility'].unique()
    elif mrkt =='nasdaq' and  snr == 'année_2018_DF':
        values = T['Mean_Close_Volatility'].unique()
    elif mrkt == 'cryptos':
        values = T['Mean_Close_Volatility'].unique()
    elif mrkt =='nasdaq':
        values = T['Mean_Close_Volatility'].unique()
        values = np.resize(values, values.size - 2)'''

    for j in values:
        textes = [ax.text(T['Mean_Close_Volatility'][T['Mean_Close_Volatility'] == j].index[len(T['Mean_Close_Volatility'][T['Mean_Close_Volatility'] == j])//2]- timedelta(days=5), j, df_best_model['algo'][i])]
        plt.setp(textes, color='blue', family='serif')
        if i == 35:
            continue
        i += 1
    plt.setp(t, fontsize=16, color='red')
    plt.xlabel('Windows')
    plt.ylabel('Volatility')
    plt.title(f'best_algos_for_{mrkt}_{snr}')
    os.makedirs(f'assets/best_models/graphs/{"_".join(noms_algos)}/{mrkt}', exist_ok=True)
    plt.savefig(f'assets/best_models/graphs/{"_". join(noms_algos)}/{mrkt}/{snr}.jpg')
    plt.show()
    # On récupère les meilleurs models et ses features dans un csv
scenari = ['année_2018_DF', 'année_2018_flat_DF','année_2019_flat_DF','année_2021_Nov_DF', 'année_2021_Oct_DF',
             'covid_DF', 'ukr_war_DF', 'rdm1_DF', 'rdm2_DF', 'rdm3_DF']
markets = ['cryptos', 'nasdaq']
# les algos utilisés peuvent être changé dans notre problème de ML nous en avons utilisé 2
algorithmes = [algos.BestMarkowitz()]
noms_algos = ['BestMarkowitz']


# Dans cette partie on instancie les algos avec leurs noms
# On a réduit le nombre d'algo pour plus de simplicité
for mrkt in markets:
    for sns in scenari:
        create_Features(mrkt, sns, algorithmes, noms_algos)