import streamlit as st
import numpy as np
import pandas as pd
from universal import tools, algos
from universal.algos import *

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



    algorithmes = [ algos.Anticor(), algos.BAH(), algos.BCRP(), algos.BestMarkowitz(), algos.BestSoFar(), algos.BNN(),
                 algos.CORN(), algos.CRP(), algos.CWMR(), algos.DynamicCRP(), algos.EG(), algos.OLMAR(), algos.ONS(),
                 algos.PAMR(), algos.RMR()]
    noms_algos = ['Anticor', 'BAH', 'BCRP', 'BestMarkowitz', 'BestSoFar', 'BNN', 'CORN', 'CRP', 'CWMR', 'DynamicCRP',
           'EG', 'OLMAR', 'ONS', 'PAMR', 'RMR']
    metric_name = ['Ratio de Sharpe',  'beta']
    #Mesure de performance
    def perform(result):
        return result.sharpe , result.alpha_beta()[1]


    def summary_table(path, nom):
        '''Fonction qui va retourner un DataFrame pour chaque scenari et chaque algos avec le sharpe et le beta
        path : chemin du fichier
        nom : nom du scénari
        '''

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

    S = pd.read_csv(f"assets/{mrkt}/{snr}.csv", index_col=0, parse_dates=True) # je charge le premier
    liste = []
    for clo in S.columns:
        if "Close" in clo:
            liste.append(clo)
    S = S[liste]
    S = S.dropna(axis=1)

        # lancer les algos
    for algo in algorithmes:
            result = algo.run(S)
            sharp = [perform(result)[0], perform(result)[1]]
            metrics.append(sharp)
            sharpe = []

    # Création et affichage dataframes
    st.write('************ ' + snr + ' **********') # je charge le premier
    X = pd.DataFrame(data=np.array(metrics), columns=metric_name, index=noms_algos)
    Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
    Y = Y[Y['Ratio de Sharpe'] > 1].head(4)
    st.write(X)
    #Affichage meilleurs algos
    st.write('===========>>>>> ' + 'Meilleures performances pour : ', list(Y.index))
"""    def summaries(scenari, nom):
        for a,b in zip(scenari, nom):
            summary_table(a,b)
    summaries(f"{mrkt}/{snr}.csv", snr)"""
    #summaries(Scenar_nasdaq_path[1], Scenar_nasdaq[1])
