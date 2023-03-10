import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yahoofinance as yf
import re
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
import statsmodels.api as sm
from prophet import Prophet
# Désolé je vais rajouter les commentaires asap
def app():
    ### Create Title
    st.title("Prédiction")
    ### Add a picture
    st.header('Paramètres de prédiction')
    st.markdown('### Choix du modèle et optimisation')
    st.write("Dans un premier temps, nous avons fait fonctionner la totalité des algorithmes disponibles par périodes.")
    st.write("Puis, nous avons dressé un tableau, résumant pour chaque algorithme les métriques calculées  (ratio de Sharpe et rendement cumulatif) :")

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

    senar = st.selectbox("Senari_list", senari_list)
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

    ### using Markdown
    st.markdown("## Visualisation des scénarios")
    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=[0])
    close_list = []
    for j in df.columns:
        if "Close" in j:
            close_list.append(j)
    liste_actions = st.selectbox("Choisir le marché",
                                   close_list)
    df_crypto_close = df[liste_actions]
    niveau = st.slider("selectionner le pourcentage à conserver", 50, 90)
    x = int(len(df_crypto_close.index)/100*niveau)
    st.write("Nous pouvons remarquer que vers 70-80% de conservation de nos datas Prophet arrive à trouver l'évolution de notre série")

    # Prophet à besoin d'une column avec des dates au format dtimeserie donc on importons deux DF
    df_i = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", parse_dates=[0])
    df_j = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", parse_dates=[0], index_col=0)
    df_pro = df_i[[liste_actions, "Date"]]
    df_pro.columns = ["y", "ds"]
    serie_j = df_j[liste_actions]
    m = Prophet(interval_width=0.95, daily_seasonality=True)
    model = m.fit(df_pro.iloc[: int(x)])
    future = m.make_future_dataframe(periods=df_j.shape[0]-x, freq='D')
    forecast = m.predict(future)

    serie_forecast = pd.Series(forecast['yhat'].values, index=forecast['ds'])
    plot1 = m.plot(forecast)
    plt.plot(serie_j, label = 'Real Serie')
    plt.plot(serie_forecast.iloc[:x], label = 'Serie Forecast')
    plt.xticks(rotation=60)
    plt.legend()
    st.pyplot()