import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from universal import tools, algos
from universal.algos import *
import re
def app():
    trading_fee = 0.05 # en pourcent
    st.title('APP5')
    st.write('Welcome to app5')

    algorithmes = [algos.Anticor(), algos.BAH(), algos.BCRP(), algos.BestMarkowitz(), algos.BestSoFar(), algos.BNN(),
                   algos.CORN(), algos.CRP(), algos.CWMR(), algos.DynamicCRP(), algos.EG(), algos.OLMAR(), algos.ONS(),
                   algos.PAMR(), algos.RMR()]
    noms_algos = ['Anticor', 'BAH', 'BCRP', 'BestMarkowitz', 'BestSoFar', 'BNN', 'CORN', 'CRP', 'CWMR', 'DynamicCRP',
                  'EG', 'OLMAR', 'ONS', 'PAMR', 'RMR']
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
    best_algo = pd.read_csv(f"assets/best_models/{mrkt}/{snr}.csv", index_col = 0)
    st.write(best_algo)
    close_list = []
    for j in df_crypto.columns:
        if "Close" in j:
            close_list.append(j)
    S = df_crypto[close_list]
    S = S.dropna(axis=1)
    st.write(S)
    liste_actions = st.selectbox("Choisir le marché",
                                   close_list)
    window = 10
    wndw_nbr = S.shape[0] // window
    for j in S.columns:
        j_reg = j.replace("_Close", "")
        df_crypto[f'{j_reg}_Weight'] = 0
    j = 0
    st.write(df_crypto)
    for i in best_algo['algo']:
        #st.write('j : ', j)
        if i != "?":
            algo = algorithmes[noms_algos.index(i)]
        #st.write(algo)
            result = algo.run(S.iloc[j * window: (j + 1) * window, :])
        #st.write(result.weights['BTC-USD_Close'])
            for e in result.weights.columns:
                e_reg = e.replace("_Close", "")
            #st.write(e)
            #df_crypto[f'{e}_Weight'].iloc[j * window: (j + 1) * window +1, :] = result.weights[e]
                df_crypto[f"{e_reg}_Weight"].iloc[j * window:(j + 1) * window] = result.weights[e]
            # st.write(result.weights[e])

        j +=1
    st.write(df_crypto)
    def cash_update(c_start, c_end, csh_start, b_start, b_end, ft):
        gain = np.sum((c_end - c_start)* (b_start-b_end)*csh_start)
        return gain - gain*ft
    #def cash_update(c_start, c_end, csh_start, b_start, b_end, ft):
    l = 0

    for line in df_crypto.index:


        gain_list = []
        for k in S.columns:
            k_reg = k.replace("_Close", "")
            gain_i = ((df_crypto[f'{k_reg}_Close'].iloc[l+1] - df_crypto[f'{k_reg}_Close'].iloc[(l)]))/df_crypto[f'{k_reg}_Close'].iloc[(l)]* (df_crypto[f'{k_reg}_Weight'].iloc[l])*df_crypto['Cashback'].iloc[l]
            #st.write(gain)
            gain_reel = gain_i - gain_i*trading_fee
            gain_list.append(gain_reel)

        #st.write(sum(gain_list))
        df_crypto['Cashback'].iloc[l+1] = df_crypto['Cashback'].iloc[l] + sum(gain_list)
        l += 1
        if l == S.shape[0]-1:
            break
    st.write(df_crypto['Cashback'])