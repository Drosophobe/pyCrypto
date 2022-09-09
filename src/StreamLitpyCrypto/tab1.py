import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yahoofinance as yf
import re
# Désolé je vais rajouter les commentaires asap
def app():


    ### Create Title
    st.title("Analyse exploratoire")
    st.markdown("## Cadre")
    st.write("Dans le but d’atteindre nos objectifs, nous avons choisi de nous concentrer sur 10 cryptos monnaies et  40 valeurs du NASDAQ qui nous semblaient les plus cohérentes avec le marché des cryptos monnaies.")
    st.markdown('### Selection des parametres d\'affichage')
    st.write("Nous avons rassemblé les données boursières issues du NASDAQ et des cryptos monnaies suivant divers scénarios représentatifs de l’ordre du mois :")
    
    market_list = ["Crypto", "Nasdaq"]
    market = st.radio("Sélectionner un type de marché", market_list)
    if market == market_list[0]:
        mrkt = "cryptos"
        senari_list = ["covid (date : 2019-11-11)", "ukr_war (date : 2022-02-24)", "année_2018 (date : 2017-12-1)", "année_2018_flat (date : 2018-09-01)", "année_2019_flat (date : 2019-1-1)", "année_2021_Nov",
                       "année_2021_Oct", "random1 (date : 2020-02-01)", "random2 (date : 2020-05-23)", "random3 (date : 2020-09-01)"]
    elif market == market_list[1]:
        mrkt = "nasdaq"
        senari_list = ["covid (date : 2019-11-11)", "ukr_war (date : 2022-02-24)", "année_2018 (date : 2017-12-1)", "année_2018_flat (date : 2018-09-01)", "année_2019_flat (date : 2019-1-1)", "année_2021_Nov",
                       "année_2021_Oct", "random1 (date : 2020-02-01)", "random2 (date : 2020-05-23)", "random3 (date : 2020-09-01)", "subprimes_DF (date : 2007-11-01)", "new_millennium_DF (date : 1999-06-06)"]
    

    senar = st.selectbox("Sélectionez un scénario", senari_list)
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
    vol_close_list = ["Close", "Volume", "Close & Vol"]
    vol_close = st.radio("Sélectionnez la Close ou le Volume", vol_close_list)
    if vol_close == vol_close_list[0]:
        vl_cl = ['Close']
    elif vol_close == vol_close_list[1]:
        vl_cl = ['Vol']
    else:
        vl_cl = ["Close", "Vol"]

    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=True)
    close_list = []
    for j in df.columns:
        if len(vl_cl) == 1:
            if vl_cl[0] in j:
                close_list.append(j)
        else:
            if vl_cl[0] or vl_cl[1] in j:
                close_list.append(j)

    if mrkt== "cryptos" :
        title= "Sélectionnez paire de devise"
    else:    
        title= "Sélectionnez une action"       
    liste_closes = st.multiselect(title,
                                   close_list)
    df_close = df[liste_closes]
    st.markdown("### Visualisation des scénarios")
    # r = re.compile(r"A-Za-z")
    my_string = ''
    plt.plot(df_close)
    plt.xticks(rotation=60)
    plt.xlabel("Time")
    plt.ylabel(my_string.join(vl_cl))
    plt.title(mrkt)
    plt.legend()
    st.pyplot()