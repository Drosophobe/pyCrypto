import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from universal import tools, algos
from universal.algos import *

def app():

    ### Create Title
    st.title("PyCrypto")
    ### Add a picture
    st.header('Paramètres de prediction')
    st.markdown('### Choix du modèle et Optimisation')
    st.write("Dans un premier temps, nous avons fait fonctionner la totalité des algorithmes disponibles par périodes.")
    st.write("Puis, nous avons dressé un tableau, résumant pour chaque algorithme les métriques calculées  (ratio de Sharpe et rendement cumulatif) :")
    st.write("Nous avons remarqué que l’algorithme Best_Markowitz et BCRP avait tendance à surperformer les autres.") 

    pred = pd.read_csv(f"./data_csv/cryptos/X_val_crypto_pred_Thresholded2.csv", index_col= -1, parse_dates=True)
    btc = pd.read_csv(f"./data_csv/cryptos/année_2022_full_DF.csv", index_col= 0, parse_dates=[0])
    weight = pd.read_csv(f"./data_csv/cryptos/poids.csv", index_col= 0, parse_dates=True)
  
    plt.plot(weight, label=weight.columns)
    plt.legend()
    st.pyplot()

    btc = btc["2022-01-31":"2022-08-07"]
    pred = pred.rename(columns= {"Prediction" : "prediction"})
    pred = pred.drop("Unnamed: 0", axis = 1)
    pred = pred.replace([True, False], [1,0])
    T = btc.copy()[[]]
    
    T["prédiction"] = pred
    T = T.fillna(method = "ffill")

    fig, ax = plt.subplots(constrained_layout=True)
    x = btc.index
    y = btc["BNB-USD_Close"]
    ax.plot(x, y)
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.set_title('BTC')

    ax2 = ax.twinx()
    ax2.plot(x, T["prédiction"], '-r', label = 'temp')
    ax2.set_ylabel('Prédiction')
    ax2.set_yticks([0,1])
    ax.legend(loc=0)
    plt.xticks(rotation=60)
    st.pyplot()
    