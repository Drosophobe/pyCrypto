#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np 
import yfinance as yf
import os
import matplotlib.pyplot as plt
from datetime import  timedelta
import warnings 
warnings.filterwarnings('ignore')


# In[3]:


crypto_list = ['BTC-USD', 'ETH-USD', 'TRX-USD', 'BNB-USD', 'XRP-USD', 'DOGE-USD', 'ADA-USD', 'SOL-USD', 'SHIB-USD', 'LTC-USD']
nasdaq40 = ["AAPL", "TSLA", "ADBE", "ADI", "ADP", "ADSK", "AEP", "ALGN", "AMAT", "AMD", "NVDA",
           "AMGN", "AMZN", "ASML", "ATVI", "AVGO", "AZN", "BIDU", "BIIB", "BKNG", 
           "CDNS", "TMUS", "CHTR", "CMCSA", "COST", "GOOGL", "CRWD", "CSCO", "CSX", "CTAS",
           "CTSH", "DDOG", "DLTR", "DXCM", "EA", "EBAY", "EXC", "FAST", "FISV", "CSCO", "GOOG"]
other = ['^DJI']


# In[4]:


senar_dic_list = [
    {"name": "année_2018", 'start_date' : "2017-12-1", 'window' : 60, 'type': 'all'},
    {"name": "année_2019_flat", 'start_date' : "2019-1-1", 'window' : 60, 'type': 'all'},
    {"name": "année_2021_Nov", 'start_date' : "2021-11-1", 'window' : 30, 'type': 'all'},
    {"name": "année_2021_Oct", 'start_date' : "2021-9-28", 'window' : 30, 'type': 'all'},
    {"name": "covid", 'start_date' : "2019-11-11", 'window' : 365, 'type': 'all'},
    {"name": "ukr_war", 'start_date' : "2022-02-24", 'window' : 60, 'type': 'all'},
    {"name": "new_millennium", 'start_date' : "1999-06-06", 'window' : 60, 'type': 'old'},
    {"name": "subprimes", 'start_date' : "2007-11-01", 'window' : 60, 'type': 'old'},
    {"name": "rdm1", 'start_date' : "2020-02-01", 'window' : 30, 'type': 'all'},
    {"name": "rdm2", 'start_date' : "2020-05-23", 'window' : 30, 'type': 'all'},
    {"name": "rdm3", 'start_date' : "2021-09-01", 'window' : 30, 'type': 'all'},
    {"name": "année_2018_flat", 'start_date' : "2018-09-01", 'window' : 30, 'type': 'all'}
    
]


# In[6]:


df_holiday = pd.read_csv('../data/holidays_with_2022.csv', index_col=0, parse_dates=[0])
# Lecture du fichier vacances americaines 


# In[1]:


class senari:
    def __init__(self, crypto_list, nasdaq_list , senar_dic_list, df_holiday, other):
        self._crypto_list = crypto_list
        self._nasdaq_list = nasdaq_list
        self._senar_dic_list = senar_dic_list
        self._df_holiday = df_holiday
        self._other = other
        
        
    def weekend(self, x):
        
    # Fonction Permettant la creation d'un column is Weekend
        if x == 5 or x == 6:
            return True
        else:
            return False
        
        
    def end_of_the_month(self, y):
        
    #Fonction permettants la creation de col end et beg of the month
        if y ==30 or y == 31 or y==29 or y==28:
            return True
        else:
            return False

        
    def beginning_of_the_month(self, z):
        if z ==1 or z == 2 or z==3 or z==4:
            return True
        else:
            return False
        
        
    def create_senari(self):
        os.makedirs('../data', exist_ok=True)
        for m in self._senar_dic_list:
            name = m['name']
            window = m['window']
            
            start_date = pd.to_datetime(m["start_date"])
            kind = m['type']
            if kind == 'all':
                df = pd.DataFrame()
                for i in self._crypto_list:
                    data = yf.Ticker(i)
                    df[f'{i}_Close']= data.history(start = start_date, end =start_date + timedelta(days = window))['Close']
                    df[f'{i}_Vol'] = data.history(start = start_date, end =start_date + timedelta(days = window))['Volume']
                    #print(df.head())
                    cashback = pd.Series(data=np.ones(df.shape[0]), index=df.index, name = 'Cashback')
                    df_with_csh = pd.concat([df,cashback],axis=1) 
                    df_final = df_with_csh[start_date: start_date+timedelta(days = window)]# On crée un column de 1
                    df_final["Day"] = df_final.index.day
                    df_final['weekday'] = df_final.index.dayofweek
                    df_final['is_weekend'] = df_final['weekday'].apply(self.weekend) # On rajoute une col is weekend
                    df_final['end_of_month'] = df_final['Day'].apply(self.end_of_the_month)# On rajoute une col end of mth
                    df_final['beginning_of_month'] = df_final['Day'].apply(self.beginning_of_the_month) # On rajoute une col beg of mth
                    df_final['is_holiday']= pd.Series([])
                    for a, b in enumerate(df_final.index):
                        if b in self._df_holiday.index.tolist():
                            df_final['is_holiday'].iloc[a] = True
                        else:
                            df_final['is_holiday'].iloc[a] =False # On rajoute une col end of mth  

                    os.makedirs('../data/cryptos', exist_ok=True)
                    df_final.to_csv(f'../data/cryptos/{name}_DF.csv')
            else:
                pass
            df = pd.DataFrame()
            for j in self._nasdaq_list:
                data = yf.Ticker(j)
                df[f'{j}_Close']= data.history(start = start_date, end =start_date + timedelta(days = window))['Close']
                df[f'{j}_Vol'] = data.history(start = start_date, end =start_date + timedelta(days = window))['Volume']
                #print(df.head())
                cashback = pd.Series(data=np.ones(df.shape[0]), index=df.index, name = 'Cashback')
                df_with_csh = pd.concat([df,cashback],axis=1) 
                df_final = df_with_csh[start_date: start_date+timedelta(days = window)]# On crée un column de 1
                df_final["Day"] = df_final.index.day
                df_final['weekday'] = df_final.index.dayofweek
                df_final['is_weekend'] = df_final['weekday'].apply(self.weekend) # On rajoute une col is weekend
                df_final['end_of_month'] = df_final['Day'].apply(self.end_of_the_month)# On rajoute une col end of mth
                df_final['beginning_of_month'] = df_final['Day'].apply(self.beginning_of_the_month) # On rajoute une col beg of mth
                df_final['is_holiday']= pd.Series([])
                for a, b in enumerate(df_final.index):
                    if b in self._df_holiday.index.tolist():
                        df_final['is_holiday'].iloc[a] = True
                    else:
                        df_final['is_holiday'].iloc[a] =False # On rajoute une col end of mth
                os.makedirs('../data/nasdaq', exist_ok=True)
                df_final.to_csv(f'../data/nasdaq/{name}_DF.csv')
            df = pd.DataFrame()
            for k in self._other:
                data = yf.Ticker(k)
                df[f'{k}_Close']= data.history(start = start_date, end =start_date + timedelta(days = window))['Close']
                df[f'{k}_Vol'] = data.history(start = start_date, end =start_date + timedelta(days = window))['Volume']
                #print(df.head())
                cashback = pd.Series(data=np.ones(df.shape[0]), index=df.index, name = 'Cashback')
                df_with_csh = pd.concat([df,cashback],axis=1) 
                df_final = df_with_csh[start_date: start_date+timedelta(days = window)]# On crée un column de 1
                df_final["Day"] = df_final.index.day
                df_final['weekday'] = df_final.index.dayofweek
                df_final['is_weekend'] = df_final['weekday'].apply(self.weekend) # On rajoute une col is weekend
                df_final['end_of_month'] = df_final['Day'].apply(self.end_of_the_month)# On rajoute une col end of mth
                df_final['beginning_of_month'] = df_final['Day'].apply(self.beginning_of_the_month) # On rajoute une col beg of mth
                df_final['is_holiday']= pd.Series([])
                for a, b in enumerate(df_final.index):
                    if b in self._df_holiday.index.tolist():
                        df_final['is_holiday'].iloc[a] = True
                    else:
                        df_final['is_holiday'].iloc[a] =False # On rajoute une col end of mth
                os.makedirs('../data/other', exist_ok=True)
                df_final.to_csv(f'../data/other/{name}_DF.csv')


# In[75]:


objet = senari(crypto_list = crypto_list, nasdaq_list = nasdaq40 , senar_dic_list= senar_dic_list, df_holiday= df_holiday, other = other)
objet.create_senari()

