import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yahoofinance as yf
import re
# Désolé je vais rajouter les commentaires asap
def app():

    st.sidebar.header('Paramètres du Graphique')
    ### Create Title
    st.title("Streamlit Online PortFolio Web app with Streamlit for DataScientest")
    st.header("The beginning of a great adventure")
    st.subheader("By DataScientest team")
    ### Add a picture
    st.write("Below is a picture of a wonderful school made by the braves:")
    st.image("assets/DataScientest.jpeg")

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
    vol_close_list = ["Close", "Volume", "Close & Vol"]
    vol_close = st.sidebar.radio("Sélectionner la Close ou le Volumne", vol_close_list)
    if vol_close == vol_close_list[0]:
        vl_cl = ['Close']
    elif vol_close == vol_close_list[1]:
        vl_cl = ['Vol']
    else:
        vl_cl = ["Close", "Vol"]

    ### using Markdown
    st.markdown("## Let's have a look into our Senari")
    df_crypto = pd.read_csv(f"assets/{mrkt}/{snr}.csv", index_col=0, parse_dates=[0])
    close_list = []
    for j in df_crypto.columns:
        if len(vl_cl) == 1:
            if vl_cl[0] in j:
                close_list.append(j)
        else:
            if vl_cl[0] or vl_cl[1] in j:
                close_list.append(j)
    liste_actions = st.multiselect("liste d'action",
                                   close_list)
    df_crypto_close = df_crypto[liste_actions]
    # r = re.compile(r"A-Za-z")
    # close_list_regex = r.findall(close_list)
    plt.plot(df_crypto_close)
    plt.xticks(rotation=60)
    plt.xlabel("Time")
    plt.ylabel(vl_cl)
    plt.title(mrkt)
    plt.legend()
    st.pyplot()