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
from fbprophet import Prophet
# Désolé je vais rajouter les commentaires asap
def app():
    st.title('APP2')
    st.write('Welcome to app2')
    st.sidebar.header('Paramètres de prediction')
    tech_list = ["SARIMA", "prophet", "RNN"]
    techno = st.sidebar.radio("Sélectionner un type de techno", tech_list)

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

    ### using Markdown
    st.markdown("## Let's have a look into our Senari")
    df_crypto = pd.read_csv(f"assets/{mrkt}/{snr}.csv", index_col=0, parse_dates=[0])
    close_list = []
    for j in df_crypto.columns:
        if "Close" in j:
            close_list.append(j)
    liste_actions = st.selectbox("Choisir le marché",
                                   close_list)
    df_crypto_close = df_crypto[liste_actions]
    st.write(liste_actions)
    niveau = st.slider("selectionner le pourcentage à conserver", 50, 90)
    x = int(len(df_crypto_close.index)/100*niveau)
    if techno == tech_list[0]:
        #st.write(df_crypto_close.iloc[:x])
        plt.plot(df_crypto_close.iloc[:x])
        plt.xticks(rotation=60)
        plt.xlabel("Time")
        plt.ylabel('Close')
        plt.title(mrkt)
        plt.legend()
        st.pyplot()
        mult_add_list = ["Additive", "Multiplicative"]
        mult_add = st.radio("Sélectionner un un type", mult_add_list)
        if mult_add == mult_add_list[0]:
            seas = seasonal_decompose(df_crypto_close.iloc[:x], model="additive")
            seas.plot()
            st.pyplot()
            plt.xticks(rotation=60)
            serie_train = df_crypto_close.iloc[:x]
            mult = seasonal_decompose(serie_train)
            cvs = serie_train - mult.seasonal
            x_cvs = cvs
        else:
            seas = seasonal_decompose(df_crypto_close.iloc[:x], model="multiplicative")
            seas.plot()
            st.pyplot()
            plt.xticks(rotation=60)
            serie_train = np.log(df_crypto_close.iloc[:x])
            mult = seasonal_decompose(serie_train)
            cvs = serie_train - mult.seasonal
            x_cvs = np.exp(cvs)

        plt.plot(serie_train, label='Série originale')
        plt.plot(x_cvs, label='Série corrigée')
        plt.title('Graphique de la série originale et la série corrigée')
        plt.xlabel('Date')
        plt.ylabel('Nb passagers')
        plt.legend()
        st.pyplot()
        diff_lvl = st.slider("selectionner le nombre de diff", 0, 3)
        for i in range (diff_lvl):
            serie_train = serie_train.diff(1).dropna()

        pd.plotting.autocorrelation_plot(serie_train)
        st.pyplot()

        lag = st.slider("selectionner le pourcentage à conserver", 1, 12)
        plot_acf(serie_train, lags=lag)
        st.pyplot()

        model = sm.tsa.SARIMAX(serie_train, order=(1, 1, 0), seasonal_order=(0, 1, 0, 5))
        sarima = model.fit()
        st.markdown(sarima.summary())
    elif techno == tech_list[1]:
        df_i = pd.read_csv(f"assets/{mrkt}/{snr}.csv", parse_dates=[0])
        df_crypto = pd.read_csv(f"assets/{mrkt}/{snr}.csv", parse_dates=[0], index_col=0)
        df_pro = df_i[[liste_actions, "Date"]]
        df_pro.columns = ["y", "ds"]
        serie_j = df_crypto[liste_actions]
        m = Prophet(interval_width=0.95, daily_seasonality=True)
        model = m.fit(df_pro.iloc[: int(x)])
        future = m.make_future_dataframe(periods=100, freq='D')
        forecast = m.predict(future)

        serie_forecast = pd.Series(forecast['yhat'].values, index=forecast['ds'])
        plot1 = m.plot(forecast)
        plt.plot(serie_j)
        plt.plot(serie_forecast.iloc[:df_pro.shape[0]])
        plt.xticks(rotation=60)
        st.pyplot()