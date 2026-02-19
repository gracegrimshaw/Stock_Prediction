import numpy as np
import pandas as pd
import datetime
import yfinance as yf
import pandas_datareader.data as web
import requests
#from datetime import datetime, timedelta
import os
import sys

import os
import sys


# ... continue with your script ...

def extract_features():

    return_period = 5
    
    START_DATE = (datetime.date.today() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    END_DATE = datetime.date.today().strftime("%Y-%m-%d")
    stk_tickers = ['CRM', 'MSFT', 'ADBE', 'ORCL', 'SAP', '^IXIC']
    #ccy_tickers = []
    #idx_tickers = ['^IXIC']

    
    stk_data = yf.download(stk_tickers, start=START_DATE, end=END_DATE, auto_adjust=False)
    #stk_data = web.DataReader(stk_tickers, 'yahoo')
    #ccy_data = web.DataReader(ccy_tickers, 'fred', start=START_DATE, end=END_DATE)
    #idx_data = web.DataReader(idx_tickers, 'fred', start=START_DATE, end=END_DATE)

    Y = np.log(stk_data.loc[:, ('Adj Close', 'CRM')]).diff(return_period).shift(-return_period)
    Y.name = 'CRM_Future'
    
    X1 = np.log(stk_data.loc[:, ('Adj Close', ('MSFT', 'ADBE', 'ORCL', 'SAP'))]).diff(return_period)
    X1.columns = X1.columns.droplevel()
    X_stocks = X1
    X_ixic = np.log(stk_data.loc[:, ('Adj Close', '^IXIC')]).diff(return_period)
    X_ixic.name = 'NASDAQ_Return'
    
    X_mom = np.log(stk_data.loc[:, ('Adj Close', 'CRM')]).diff(return_period)
    X_mom.name = 'CRM_Momentum_5'
    
    X_spread = stk_data.loc[:, ('High', 'CRM')] - stk_data.loc[:, ('Low', 'CRM')]
    X_spread.name = 'CRM_HighLow_Spread'
    
    X = pd.concat([X_stocks, X_ixic, X_mom, X_spread], axis=1)
    
    dataset = pd.concat([Y, X], axis=1).dropna().iloc[::return_period, :]

    
    
    Y = dataset.loc[:, Y.name]
    X = dataset.loc[:, X.columns]
    dataset.index.name = 'Date'
    #dataset.to_csv(r"./test_data.csv")
    features = dataset.sort_index()
    features = features.reset_index(drop=True)
    features = features.iloc[:,1:]
    return features


def get_bitcoin_historical_prices(days = 60):
    
    BASE_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily' # Ensure we get daily granularity
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['Timestamp', 'Close Price (USD)'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.normalize()
    df = df[['Date', 'Close Price (USD)']].set_index('Date')
    return df




