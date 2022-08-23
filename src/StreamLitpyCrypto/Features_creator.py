from universal import tools, algos
from universal.algos import *
import matplotlib.pyplot as plt
from datetime import timedelta
import time
import os
from math import *
import warnings
warnings.filterwarnings('ignore')

def perform(result):
    return result.sharpe, result.alpha_beta()[1]
def volatility(data):
    # On crée une fonction qui retourne le volatilté de l'action dans une window définie plus bas
    return np.log(data/data.shift()).std()
def max_range(data):
    # On crée une fonction qui retourne l'amplitude max de la valeure
    return np.max(data)-np.min(data)
def create_features(snr, mrkt, window, algos, noms_algos, show = False):
    metric_name = ['Ratio de Sharpe', 'beta']
    #Mesure de performance
    sharp = []
    metrics = []
    df = pd.read_csv(f"../../data/{mrkt}/{snr}.csv", index_col=0, parse_dates=True)
    start_date = df.index[0]
    end_date = df.index[-1]
    df_size= df.shape[0]
    df_len_cryto_tweets = pd.read_csv(f"../../data/cryptos/tweets/extract_dates/date_{snr}.csv", sep = '\t', parse_dates= [0], index_col=0)
    df_len_nasdaq_tweets = pd.read_csv(f"../../data/nasdaq/tweets/extract_dates/date_{snr}.csv", sep='\t', parse_dates=[0], index_col=0)
    liste_close= []
    liste_vol = []
    for clo in df.columns:
        if "Close" in clo:
            liste_close.append(clo)
        elif 'Vol' in clo:
            liste_vol.append(clo)
    S = df[liste_close]
    S = S.dropna(axis=1)
    R = df[liste_vol]
    R = R.dropna(axis=1)
    wndw_nbr = S.shape[0] // window

    T = S.copy()[[]]

    T["Mean_Close_Volatility"] = 0
    T['Mean_Close_Range'] = 0
    T["Mean_Vol_Volatility"] = 0
    T['Mean_Vol_Range'] = 0

    for e in S.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0

    for i in np.arange(0, wndw_nbr*window+1, window):
        for e in S.columns:
            T[f"{e}_volatility"].iloc[i:i + window]= volatility(S[e].iloc[i:i + window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(S[e].iloc[i:i + window])

    T = T.iloc[0: wndw_nbr*window]

    for e in R.columns:
        T[f"{e}_range"] = 0
        T[f"{e}_volatility"] = 0
    date_list =[]
    for i in np.arange(0, wndw_nbr*window+1, window):
        for e in R.columns:
            T[f"{e}_volatility"].iloc[i:i +window] = volatility(R[e].iloc[i:i +window])
            T[f"{e}_range"].iloc[i:i + window] = max_range(R[e].iloc[i:i + window])
        # On calcule la volatilité et la range de chaque volume par windows et on update les cols
        if i != 0:
            date_list.append(df.index[i-1])
        else:
            date_list.append(df.index[i])

    my_len_cryptos_tweets_list = []
    my_len_nasdaq_tweets_list = []
    for i in range(len(date_list)):
        if i == 0:
            days = 0
        else :
            days = 1
        my_len_cryptos_tweets_list.append(df_len_cryto_tweets.loc[date_list[i]+timedelta(days=days):date_list[i + 1]].sum(axis=0).values[0])
        my_len_nasdaq_tweets_list.append(df_len_nasdaq_tweets.loc[date_list[i]+timedelta(days=days):date_list[i + 1]].sum(axis=0).values[0])
        if i == len(date_list) - 2:
            break

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

    my_close_volatility_list = []
    my_close_range_list = []
    my_vol_volatility_list = []
    my_vol_range_list = []
    for i in range(wndw_nbr):
        my_close_volatility_list.append(T['Mean_Close_Volatility'].iloc[((i+1)*window) - 2])
        my_close_range_list.append(T['Mean_Close_Range'].iloc[((i+1)*window) - 2])
        my_vol_volatility_list.append(T['Mean_Vol_Volatility'].iloc[((i+1)*window) - 2])
        my_vol_range_list.append(T['Mean_Vol_Range'].iloc[((i+1)*window) - 2])

    df_features = pd.read_csv("../../data/csv_features/Features.csv", index_col=0, parse_dates=True)

    for l in range(wndw_nbr):
        if l ==0:
            days = 0
        else:
            days = 1

    T['Volatility_Gold_Close'] = 0
    T['Volatility_Gold_Vol'] = 0
    T['Volatility_Oil_Close'] = 0
    T['Volatility_Oil_Vol'] = 0
    T['Volatility_Gas_Close'] = 0
    T['Volatility_Gas_Vol'] = 0
    T['Range_Gold_Close'] = 0
    T['Range_Gold_Vol'] = 0
    T['Range_Oil_Close'] = 0
    T['Range_Oil_Vol'] = 0
    T['Range_Gas_Close'] = 0
    T['Range_Gas_Vol'] = 0
    T['Mean_FED'] = 0
    T['Mean_PMI'] = 0
    T['Mean_Unemploy'] = 0
    T['Volatility_VIX'] = 0
    T['Range_VIX'] = 0
    for m in range(wndw_nbr):
        if m ==0:
            days = 0
        else:
            days = 1
        #print(df_features[date_list[m]+timedelta(days=days): date_list[m+1]])
        T['Volatility_Gold_Close'][date_list[m]+timedelta(days=days): date_list[m+1]] = volatility(df_features['Gold_Close'][date_list[m]+timedelta(days=days): date_list[m+1]])
        T['Volatility_Gold_Vol'][date_list[m] + timedelta(days=days): date_list[m+1]] = volatility(df_features['Gold_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Volatility_Oil_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]] = volatility(
            df_features['Oil_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Volatility_Oil_Vol'][date_list[m] + timedelta(days=days): date_list[m + 1]] = volatility(
            df_features['Oil_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Volatility_Gas_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]] = volatility(
            df_features['Gas_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Volatility_Gas_Vol'][date_list[m] + timedelta(days=days): date_list[m + 1]] = volatility(
            df_features['Gas_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])

        T['Range_Gold_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Gold_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_Gold_Vol'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Gold_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_Oil_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Oil_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_Oil_Vol'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Oil_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_Gas_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Gas_Close'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_Gas_Vol'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['Gas_Volume'][date_list[m] + timedelta(days=days): date_list[m + 1]])

        T['Mean_FED'][date_list[m] + timedelta(days=days): date_list[m + 1]] = np.mean(
            df_features['FED'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Mean_PMI'][date_list[m] + timedelta(days=days): date_list[m + 1]] = np.mean(
            df_features['PMI'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Mean_Unemploy'][date_list[m] + timedelta(days=days): date_list[m + 1]] = np.mean(
            df_features['Unemploy'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Volatility_VIX'][date_list[m] + timedelta(days=days): date_list[m + 1]] = volatility(
            df_features['VIX'][date_list[m] + timedelta(days=days): date_list[m + 1]])
        T['Range_VIX'][date_list[m] + timedelta(days=days): date_list[m + 1]] = max_range(
            df_features['VIX'][date_list[m] + timedelta(days=days): date_list[m + 1]])
    my_Volatility_Gold_Close = []
    my_Volatility_Gold_Vol = []
    my_Volatility_Oil_Close = []
    my_Volatility_Oil_Vol = []
    my_Volatility_Gas_Close = []
    my_Volatility_Gas_Vol = []
    my_Range_Gold_Close = []
    my_Range_Gold_Vol = []
    my_Range_Oil_Close = []
    my_Range_Oil_Vol = []
    my_Range_Gas_Close = []
    my_Range_Gas_Vol = []
    my_Mean_FED = []
    my_Mean_PMI = []
    my_Mean_Unemploy = []
    my_Volatility_VIX = []
    my_Range_VIX = []
    for i in range(wndw_nbr):
        my_Volatility_Gold_Close.append(T['Volatility_Gold_Close'].iloc[((i+1)*window) - 2])
        my_Volatility_Gold_Vol.append(T['Volatility_Gold_Vol'].iloc[((i+1)*window) - 2])
        my_Volatility_Oil_Close.append(T['Volatility_Oil_Close'].iloc[((i+1)*window) - 2])
        my_Volatility_Oil_Vol.append(T['Volatility_Oil_Vol'].iloc[((i+1)*window) - 2])
        my_Volatility_Gas_Close.append(T['Volatility_Gas_Close'].iloc[((i+1)*window) - 2])
        my_Volatility_Gas_Vol.append(T['Volatility_Gas_Vol'].iloc[((i+1)*window) - 2])
        my_Range_Gold_Close.append(T['Range_Gold_Close'].iloc[((i+1)*window) - 2])
        my_Range_Gold_Vol.append(T['Range_Gold_Vol'].iloc[((i+1)*window) - 2])
        my_Range_Oil_Close.append(T['Range_Oil_Close'].iloc[((i+1)*window) - 2])
        my_Range_Oil_Vol.append(T['Range_Oil_Vol'].iloc[((i+1)*window) - 2])
        my_Range_Gas_Close.append(T['Range_Gas_Close'].iloc[((i+1)*window) - 2])
        my_Range_Gas_Vol.append(T['Range_Gas_Vol'].iloc[((i+1)*window) - 2])
        my_Mean_FED.append(T['Mean_FED'].iloc[((i+1)*window) - 2])
        my_Mean_PMI.append(T['Mean_PMI'].iloc[((i+1)*window) - 2])
        my_Mean_Unemploy.append(T['Mean_Unemploy'].iloc[((i+1)*window) - 2])
        my_Volatility_VIX.append(T['Volatility_VIX'].iloc[((i+1)*window) - 2])
        my_Range_VIX.append(T['Range_VIX'].iloc[((i+1)*window) - 2])
    best_model_list = []
    if noms_algos == ["CRP_mom", "CRP_rev"]:
        for w in range(wndw_nbr):
            V = S.iloc[w * window: (w + 1) * window , :] / S.iloc[w * window: (w + 1) * window , :].shift(1)
            highest_return_symbol = V.idxmax(axis=1).shift(1)
            lower_return_symbol = V.idxmin(axis=1).shift(1)
            W_mom = S.iloc[w * window: (w + 1) * window , :] * 0
            for col in V.columns:
                W_mom.loc[highest_return_symbol == col, col] = 1
            W_rev = S.iloc[w * window: (w + 1) * window , :] * 0
            for col in V.columns:
                W_rev.loc[lower_return_symbol == col, col] = 1
            for algo in [CRP(W_mom), CRP(W_rev)]:
                #print(S.iloc[w * window: (w + 1) * window, :])
                result = algo.run(S.iloc[w * window: (w + 1) * window , :])
                sharp = [perform(result)[0], perform(result)[1]]
                metrics.append(sharp)
                sharpe = []
            # st.write('************ ' + snr + ' **********')
            X = pd.DataFrame(data=np.array(metrics[w * len(algos):(w + 1) * len(algos)]), columns=metric_name,
                             index=noms_algos)
            Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
            Y = Y[Y['Ratio de Sharpe'] > 1].head(1)
            # Selection du meilleur algo si il existe on le met dans notre liste
            if len(list(Y.index)) == 1:
                best_model_list.append(list(Y.index)[0])
            else:
                best_model_list.append('?')
    else :
        for w in range(wndw_nbr):
            #print((w + 1) * window - 1 - w * window)
            for algo in algos:
                    result = algo.run(S.iloc[w * window: (w + 1) * window-1, :])
                    sharp = [perform(result)[0], perform(result)[1]]
                    metrics.append(sharp)
                    sharpe = []
                #st.write('************ ' + snr + ' **********')
            X = pd.DataFrame(data=np.array(metrics[w*len(algos):(w+1)*len(algos)]), columns=metric_name, index=noms_algos)
            Y = X.sort_values(by='Ratio de Sharpe', ascending=False)
            Y = Y[Y['Ratio de Sharpe'] > 1].head(1)
            # Selection du meilleur algo si il existe on le met dans notre liste
            if len(list(Y.index)) == 1:
                best_model_list.append(list(Y.index)[0])
            else:
                best_model_list.append('?')

    df_best_model = pd.DataFrame.from_dict({"algo": best_model_list, "close_volatility": my_close_volatility_list, 'close_range': my_close_range_list,
                                                "vol_volatility": my_vol_volatility_list, 'vol_range': my_vol_range_list, 'market': mrkt,
                                                "nbr_of_cryptos_tweets": my_len_cryptos_tweets_list, "nbr_of_nasdaq_tweets": my_len_nasdaq_tweets_list,
                                            "Volatility_Gold_Close": my_Volatility_Gold_Close, "Volatility_Gold_Vol":my_Volatility_Gold_Vol, "Volatility_Oil_Close": my_Volatility_Oil_Close,
                                            "Volatility_Oil_Vol": my_Volatility_Oil_Vol, "Volatility_Gas_Close": my_Volatility_Gas_Close, "Volatility_Gas_Vol": my_Volatility_Gas_Vol,
                                            "Range_Gold_Close ": my_Range_Gold_Close , "Range_Gold_Vol": my_Range_Gold_Vol, "Range_Oil_Close": my_Range_Oil_Close,
                                            "Range_Oil_Vol": my_Range_Oil_Vol, "Range_Gas_Close": my_Range_Gas_Close, "Range_Gas_Vol": my_Range_Gas_Vol,
                                            "Mean_FED": my_Mean_FED, "Mean_PMI" : my_Mean_PMI, "Mean_Unemploy": my_Mean_Unemploy,"Volatility_VIX": my_Volatility_VIX,
                                            "Range_VIX": my_Range_VIX})

    os.makedirs(f'assets/best_models/datas/{"_". join(noms_algos)}/full/{mrkt}', exist_ok=True)
    df_best_model.to_csv(f'assets/best_models/datas/{"_". join(noms_algos)}/full/{mrkt}/{snr}.csv')
    values = T['Mean_Close_Volatility'].unique()
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot(111)
    ax.plot(T['Mean_Close_Volatility'])
    t = ax.set_title(f'{snr}_{mrkt}')
    i = 0
    #print(len(T['Mean_Close_Volatility'].unique()))
    #print(df_best_model['algo'])
    for j in values:
        textes = [ax.text(T['Mean_Close_Volatility'][T['Mean_Close_Volatility'] == j].index[
                              len(T['Mean_Close_Volatility'][T['Mean_Close_Volatility'] == j]) // 2] - timedelta(days=5), j,
                          df_best_model['algo'][i])]
        plt.setp(textes, color='blue', family='serif')
        if i == 35:
            continue
        i += 1
    # on montre les graphiques correspondants à la volatilité par window avec le meilleur algo correspondant
    plt.setp(t, fontsize=16, color='red')
    plt.xlabel('Windows')
    plt.xticks(rotation = 60)
    plt.ylabel('Volatility')
    plt.title(f'best_algos_for_{mrkt}_{snr}')
    # On récupère les graphs dans un dossier que l'on crée
    os.makedirs(f'assets/best_models/graphs/{"_".join(noms_algos)}/full/{mrkt}', exist_ok=True)
    plt.savefig(f'assets/best_models/graphs/{"_".join(noms_algos)}/full/{mrkt}/{snr}.jpg')
    if show == True:
        plt.show()
algorithmes = [algos.CRP(), algos.CRP()]
noms_algos = ['CRP_mom', 'CRP_rev']
snr_list = ["covid_DF", "ukr_war_DF", "année_2018_DF", "année_2018_flat_DF", "année_2019_flat_DF", "année_2021_Nov_DF",
                       "année_2021_Oct_DF", "rdm1_DF", "rdm2_DF", "rdm3_DF"]
year_list = ["année_2017_full_DF", "année_2018_full_DF", "année_2019_full_DF", "année_2020_full_DF", "année_2021_full_DF"]
mrkt_list = ["cryptos", "nasdaq"]
for i in mrkt_list:
    for j in year_list:
        create_features(snr=j, mrkt=i, algos= algorithmes, noms_algos= noms_algos, window=7, show = False)