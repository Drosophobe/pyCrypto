import streamlit as st
import numpy as np
import pandas as pd
from universal import tools, algos
from universal.algos import *

def app():
    ### Create Title
    st.title("Summarize")
    ### Add a picture
    st.header('Paramètres de prédiction')
    st.markdown('### Choix du modèle et optimisation')
    st.write("Dans un premier temps, nous avons fait fonctionner la totalité des algorithmes disponibles par périodes.")
    st.write("Puis, nous avons dressé un tableau, résumant pour chaque algorithme les métriques calculées  (ratio de Sharpe et rendement cumulatif) :")
    st.write("Nous avons remarqué que l’algorithme Best_Markowitz et BCRP avait tendance à surperformer les autres.") 


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

    market_list = ["Crypto", "Nasdaq"]
    market = st.radio("Sélectionnez le marché souhaité", market_list)
    if market == market_list[0]:
        mrkt = "cryptos"
        senari_list = ["covid (date : 2019-11-11)", "ukr_war (date : 2022-02-24)", "année_2018 (date : 2017-12-1)", "année_2018_flat (date : 2018-09-01)", "année_2019_flat (date : 2019-1-1)", "année_2021_Nov",
                       "année_2021_Oct", "random1 (date : 2020-02-01)", "random2 (date : 2020-05-23)", "random3 (date : 2020-09-01)"]
    elif market == market_list[1]:
        mrkt = "nasdaq"
        senari_list = ["covid (date : 2019-11-11)", "ukr_war (date : 2022-02-24)", "année_2018 (date : 2017-12-1)", "année_2018_flat (date : 2018-09-01)", "année_2019_flat (date : 2019-1-1)", "année_2021_Nov",
                       "année_2021_Oct", "random1 (date : 2020-02-01)", "random2 (date : 2020-05-23)", "random3 (date : 2020-09-01)", "subprimes_DF (date : 2007-11-01)", "new_millennium_DF (date : 1999-06-06)"]
    senar = st.selectbox("Selectionnez le scénario souhaité", senari_list)

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

    # Création et affichage dataframes
    st.write('************ ' + snr + ' **********') # je charge le premier
    #X = pd.DataFrame(data=np.array(metrics), columns=metric_name, index=noms_algos)
    #Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
    #Y = Y[Y['Ratio de Sharpe'] > 1].head(4)
    

    X = pd.read_csv(f"./data_csv/{mrkt}/summary_table_{snr}.csv", index_col= 0)
    Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
    Y = Y[Y['Ratio de Sharpe'] > 1].head(4)
    

    #X.to_csv(f"./data_csv/{mrkt}/summary_table_{snr}.csv")
    st.write(X)

    #Affichage meilleurs algos
    st.write('===========>>>>> ' + 'Meilleures performances pour : ', list(Y.index))
"""    def summaries(scenari, nom):
        for a,b in zip(scenari, nom):
            summary_table(a,b)
    summaries(f"{mrkt}/{snr}.csv", snr)"""
    #summaries(Scenar_nasdaq_path[1], Scenar_nasdaq[1])
