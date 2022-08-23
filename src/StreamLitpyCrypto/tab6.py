import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yahoofinance as yf
import re
import datetime as dt
from scipy.stats import pearsonr, kstest
from wordcloud import WordCloud
from nltk.corpus import stopwords
import re
def app():
    stop_words = set(stopwords.words('english'))
    sw_i = st.text_input('Choisir un stop word à supprimer: ')
    stop_words.update([sw_i])
    stop_words.update(['cryptos', 'etherium', 'cryptocurrency', 'cryptocurrencies', 'https', 'bitcoin', 'crypto',
                       'ethereum', 'market', 'btc', 'markets', 'news', 'article', 'trade', 'example', 'stock',
                       'value', 'hours', 'trading', 'consumers', 'movement', 'looking', 'last', 'exchange', 'girl',
                       'per', 'cent', 'per cent', 'lot', 'analysis', 'asset', 'correlation', 'month', 'volume',
                       'information', 'also', 'saw', 'many', 'day', 'one', 'retail', 'mortgage rate', 'look',
                       'billion', 'said', 'think', 'last week'])
    r = re.compile(r"[^0-9]")

    def plot_word_cloud(text, background_color="black"):
        # Définir le calque du nuage des mots
        wc = WordCloud(background_color=background_color, max_words=200,
                       stopwords=stop_words,
                       max_font_size=50, random_state=42)
        # Générer et afficher le nuage de mots
        plt.figure(figsize=(13, 7))
        wc.generate(text)
        plt.imshow(wc)
        plt.axis("off")
        plt.show()

    # mesure de performance algo
    def perform(result):
        print('Le ratio de Sharpe est : ', result.sharpe)
        print('Le Beta est : ', result.alpha_beta()[1])
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
    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=[0])
    liste = []
    for clo in df.columns:
        if "Close" in clo:
            liste.append(clo)
    S = df[liste]
    S = S.dropna(axis=1)
    R = pd.read_csv(f'../../data/{mrkt}/articles/articles_{snr}.csv', on_bad_lines='skip',
                    index_col=0, parse_dates=True, sep='\t')
    T = pd.read_csv(f'../../data/{mrkt}/tweets/tweets_{snr}.csv', on_bad_lines='skip',
                    index_col=0, parse_dates=True, sep='\t')
    #R = R.index.astype("datetime64[ns]")
    R = R.dropna()
    T = T.dropna()
    R.index = R.index.astype("datetime64[ns]")
    T.index = T.index.astype("datetime64[ns]")
    niveau = 0
    niveau = st.slider("selectionner le début du wordcloud", 0, 100)
    niveau2= 99
    niveau2 = st.slider("selectionner la fin du wordcloud", niveau+1, 100)
    #st.write(S.index[S.shape[0]*niveau//100])
    date1 = str(S.index[S.shape[0] * niveau//100])
    date2 = str(S.index[(S.shape[0] * niveau2//100)-1])
    #st.write(S.index[S.shape[0] * niveau2//100])
    #st.write(S.shape[0]*niveau//100)
    #st.write(R[date1:date2])
    plt.plot(S)
    plt.axvline(S.index[S.shape[0]*niveau//100], color = "red")
    plt.axvline(S.index[S.shape[0] * niveau2 // 100-1], color = 'orange')
    plt.xticks(rotation = 60)
    st.pyplot()
    texte = " "
    for e in R['Text'][date1:date2]:
        texte += e
    for k in T['Tweet'][date1:date2]:
        texte += k
    texte = re.sub('num', texte, texte)
    plot_word_cloud(texte.lower(), 'white')
    st.pyplot()
    st.write('Nous remarquons que les mots qui resortent du Wordcloud ne peuvent être utilsier pour prédire quoi que ce soit')
    ### using Markdown