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



dfs = pd.read_excel(f"dfsym.xlsx")

start = datetime.datetime(2020,3,12)
end = datetime.datetime(2021,6,12)
df = web.DataReader("TSLA", "yahoo", start, end)

con = sqlite3.connect(f"dfdb.db")
df.to_sql('TSLA', con, if_exists='replace')
readed_df = pd.read_sql("SELECT * From TSLA", con, index_col=None)

print(readed_df)

# df = pd.read_sql("SELECT * From kakao", con, index_col=None)
# print(df)
# cursor = con.cursor()
# cursor.execute("SELECT * From kakao")

# cursor.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volume int)")
# cursor.execute("INSERT INTO kakao VALUES('16.06.03',97000,98600,96900,98000,321405)")
# cursor.execute("INSERT INTO kakao VALUES('16.06.02',99000,99300,96300,97500,556790)")
# con.commit()
# con.close()













