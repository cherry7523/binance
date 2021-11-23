import ccxt 
import pprint
import time
import datetime
import pandas as pd
import pandas_datareader.data as web
import ta
import sqlite3
import math

from pandas.core.tools.datetimes import to_datetime

api_key = "1nP6bqPkQJXte3dKtx3yQz0yBUyQJnMsJ6EaXHh3qF3IwB1pDkGdQddSZzV41WAL"
secret = "ydWMSGJRC5ONLZ8NqRTP0UXK6cOpirXjFuuROEf0cs6QckVZonURReyERhAdADZb"
# binance 객체 생성
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit':True,
    'options': {
        'defaultType': 'future'
    }
})


def get_ohlcv(ticker,timef):
    # since = "2021-09-28"
    # since = int(pd.to_datetime(since).timestamp() *1000)  #since 인트값으로 변경하기
    coin1m = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timef, 
        since=None,         
        limit=1000)

    df = pd.DataFrame(coin1m, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

def get_ohlcv_2(ticker,timef):
    coin1m = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timef, 
        since=None,         
        limit=1)
    df = pd.DataFrame(coin1m, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

def MACD(df):
    df['histo'] = ta.trend.macd_diff(df.close)
    df['histodf'] = df['histo'] - df['histo'].shift(1)
    # df['histodfrabs'] = df['histodf'].abs()
    meanhisto = df['histodf'].std()
    df['histodfr'] = df['histodf']/ meanhisto *10
    # df['histodfr'] = df['histodf']/df['close'] *1000
    df['rsi'] = ta.momentum.rsi(df.close, window=14)
    df['rsidf'] = df['rsi'] - df['rsi'].shift(1)

