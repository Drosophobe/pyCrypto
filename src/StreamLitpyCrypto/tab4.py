import streamlit as st
import numpy as np
import pandas as pd
from universal import tools, algos
from universal.algos import *
import matplotlib.pyplot as plt
from datetime import  timedelta
# J'ai git clone le git en entier et j'ai changé son nom par universalPF
# Désolé je vais rajouter les commentaires asap
def app():
    Scenar_crypto_path = ['assets/cryptos/année_2018_DF.csv', 'assets/cryptos/année_2018_flat_DF.csv','assets/cryptos/année_2019_flat_DF.csv','assets/cryptos/année_2021_Nov_DF.csv',
                     'assets/cryptos/année_2021_Oct_DF.csv', 'assets/cryptos/covid_DF.csv', 'assets/cryptos/ukr_war_DF.csv']
    Scenar_nasdaq_path = ['assets/nasdaq/année_2018_DF.csv', 'assets/nasdaq/année_2018_flat_DF.csv','assets/nasdaq/année_2019_flat_DF.csv','assets/nasdaq/année_2021_Nov_DF.csv', 'assets/nasdaq/année_2021_Oct_DF.csv',
             'assets/nasdaq/covid_DF.csv', 'assets/nasdaq/new_millennium_DF.csv', 'assets/nasdaq/subprimes_DF.csv', 'assets/nasdaq/ukr_war_DF.csv']

    Scenar_crypto = ['année_2018_DF', 'année_2018_flat_DF','année_2019_flat_DF','année_2021_Nov_DF', 'année_2021_Oct_DF',
             'covid_DF', 'ukr_war_DF']
    Scenar_nasdaq = ['année_2018_DF', 'année_2018_flat_DF','année_2019_flat_DF','année_2021_Nov_DF', 'année_2021_Oct_DF',
             'covid_DF', 'new_millennium_DF', 'subprimes_DF' 'ukr_war_DF']
    # Dans cette partie on instancie les path des datas avec leurs noms

    algorithmes = [algos.BCRP(), algos.BestMarkowitz()]
    noms_algos = ['BCRP', 'BestMarkowitz']
    metric_name = ['Ratio de Sharpe', 'beta']

    # Dans cette partie on instancie les algos avec leurs noms
    # On a réduit le nombre d'algo pour plus de simplicité
    #Mesure de performance
    def perform(result):
        return result.sharpe , result.alpha_beta()[1]

    def volatility(data):
        # On crée une fonction qui retourne le volatilté de l'action dans une window définie plus bas
        return np.log(data/data.shift()).std()
    def max_range(data):
        return np.max(data)-np.min(data)
    market_list = ["Crypto", "Nasdaq", "Other"]
    market = st.sidebar.radio("Sélectionner un type de marché", market_list)
    if market == market_list[0]:
        mrkt = "cryptos"
        senari_list = ["covid", "ukr_war", "année_2018", "année_2018_flat", "année_2019_flat", "année_2021_Nov",
                       "année_2021_Oct", "random1", "random2", "random3"]
    elif market == market_list[1]:
        mrkt = "nasdaq"
        senari_list = ["covid", "ukr_war", "année_2018", "année_2018_flat", "année_2019_flat", "année_2021_Nov",
                       "année_2021_Oct", "random1", "random2", "random3", "subprimes_DF", "new_millennium_DF"]
    else:
        mrkt = 'other'
        senari_list = ["covid", "ukr_war", "année_2018", "année_2018_flat", "année_2019_flat", "année_2021_Nov",
                       "année_2021_Oct", "random1", "random2", "random3", "subprimes_DF", "new_millennium_DF"]
        st.write('only one value for Other can perform portefolio')
    senar = st.sidebar.selectbox("Senari_list", senari_list)
    if senar == senari_list[0]:
        snr = "covid_DF"
    elif senar == senari_list[1]:
        snr = "ukr_war_DF"
    elif senar == senari_list[2]:
        snr = "année_2018_DF"
    elif senar == senari_list[3]:
        snr = "année_2018_flat_DF"
    elif senar == senari_list[4]:
        snr = "année_2019_flat_DF"
    elif senar == senari_list[5]:
        snr = "année_2021_Nov_DF"
    elif senar == senari_list[6]:
        snr = "année_2021_Oct_DF"
    elif senar == senari_list[7]:
        snr = "rdm1_DF"
    elif senar == senari_list[8]:
        snr = "rdm2_DF"
    elif senar == senari_list[9]:
        snr = 'rdm3_DF'
    elif senar == senari_list[10]:
        snr = 'subprimes_DF'
    else:
        snr = 'new_millennium_DF'
    sharp = []
    metrics = []
    # nettoyage des données

    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=True)
    # je charge le premier
    df = df.drop(["^VIX_Vol"], axis = 1)
    df["^VIX_Close"] = df["^VIX_Close"].fillna(df["^VIX_Close"].mean())
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
    st.write(df)
    st.write(Q)
    # On crée un df avec uniquement les closes
    window = 10
    wndw_nbr = S.shape[0] // window
    # On choisi notre window et on crée un variable avec le nombre de window dans chaque senario
    T = S.copy()[[]]
    T["Mean_Close_Volatility"] = 0
    T['Mean_Close_Range'] = 0
    T["Mean_Vol_Volatility"] = 0
    T['Mean_Vol_Range'] = 0
    # On crée une column Mean_volatility que l'on viendra update plus tard
    for e in S.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0
        # Pour chaque close on ajoute une col volarility qu'on viendra update plus tard

    for i in np.arange(0, df.shape[0]+1, window):
        for e in S.columns:
            #st.write(df[f"{e}_volatility"][df[f"{e}_volatility"].index[0]: df[f"{e}_volatility"].index[0] + timedelta(days=window - 1)])
            #df[f"{e}_volatility"][df.index[i]: df.index[i] + timedelta(days= 10)] = volatility(S[e][df.index[i]: df.index[i] + timedelta(days= 10)])
            T[f"{e}_volatility"].iloc[i:i +window] = volatility(S[e].iloc[i:i +window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(S[e].iloc[i:i + window])
            #print("La volatitly de ", e, "pour le periode :", i - window, "-", i, 'est de ',
                  #volatility(S[e].iloc[i - window:i]))
    for e in R.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0
    T["VIX_range"] = 0
    T["VIX_mean"] = 0
    T['VIX_volatility'] = 0
    for i in np.arange(0, df.shape[0]+1, window):
        for e in R.columns:
            #st.write(df[f"{e}_volatility"][df[f"{e}_volatility"].index[0]: df[f"{e}_volatility"].index[0] + timedelta(days=window - 1)])
            #df[f"{e}_volatility"][df.index[i]: df.index[i] + timedelta(days= 10)] = volatility(S[e][df.index[i]: df.index[i] + timedelta(days= 10)])
            T[f"{e}_volatility"].iloc[i:i +window] = volatility(R[e].iloc[i:i +window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(R[e].iloc[i:i + window])
        T["VIX_range"].iloc[i:i + window] = max_range(Q["^VIX_Close"].iloc[i:i+window])
        T["VIX_mean"].iloc[i:i + window] = np.mean(Q["^VIX_Close"].iloc[i:i + window])
        T["VIX_volatility"].iloc[i:i + window] = volatility(Q["^VIX_Close"].iloc[i:i + window])
    st.write(df.columns)
    # Dans cette double boucle on vient changer la valeur de la volatilty (de base à 0) par la valeur calculé par la fonction pour chaques action
    list_close_Vol_names = []
    list_close_Ran_names = []
    list_vol_Vol_names = []
    list_vol_Ran_names = []
    for i in T.columns:
        if 'Close_volatility' in i:
            list_close_Vol_names.append(i)
        elif 'Close_range' in i:
            list_close_Ran_names.append(i)
        elif 'Vol_volatility' in i:
            list_vol_Vol_names.append(i)
        elif 'Vol_range' in i:
            list_vol_Ran_names.append(i)
    T['Mean_Close_Volatility'] = T[list_close_Vol_names].mean(axis=1)
    T['Mean_Close_Range'] = T[list_close_Ran_names].mean(axis=1)
    T['Mean_Vol_Volatility'] = T[list_vol_Vol_names].mean(axis=1)
    T['Mean_Vol_Range'] = T[list_vol_Ran_names].mean(axis=1)
    # On update la valeur de mean_volatility avec les moyennes de chaques volatilty des actions par window
    st.write(T)
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







    st.write("close volatility list\n", my_close_volatility_list)
    st.write("close range list\n", my_close_range_list)
    st.write("vol volatility list\n", my_vol_volatility_list)
    st.write("vol range list\n", my_vol_range_list)
    # On afficher la liste des volatilties obtenues en prenant l'avant dernière valeurs de la window et on l'affiche
    list_metrics = []

    best_model_list = []
    for wd in range(wndw_nbr):
        for algo in algorithmes:
                result = algo.run(S.iloc[wd * window: (wd + 1) * window-1, :])
                sharp = [perform(result)[0], perform(result)[1]]
                metrics.append(sharp)
                sharpe = []
        st.write('************ ' + snr + ' **********')
        X = pd.DataFrame(data=np.array(metrics[wd*len(algorithmes):(wd+1)*len(algorithmes)]), columns=metric_name, index=noms_algos)
        Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
        Y = Y[Y['Ratio de Sharpe'] > 1].head(1)
        # Selection du meilleur algo
        if len(list(Y.index)) == 1:
            best_model_list.append(list(Y.index)[0])
        else:
            best_model_list.append('?')
        # On recupère le meilleur model si il existe sinon un "?"
    plt.plot(T['Mean_Close_Volatility'])
    plt.xticks(rotation=60)
    st.pyplot()
    # On plot la volatility
    df_best_model = pd.DataFrame.from_dict({"algo": best_model_list, "close_volatility": my_close_volatility_list, 'close_range': my_close_range_list,
                                            "vol_volatility": my_vol_volatility_list, 'vol_range': my_vol_range_list, 'market': market,
                                            "VIX_range": my_vix_range_list, "VIX_volatility" : my_vix_volatility_list, 'VIX_mean': my_vix_mean_list})
    df_best_model.to_csv(f'assets/best_models/{mrkt}/{snr}.csv')
    st.write(df_best_model)
    # On récupère les meilleurs models dans un csv
