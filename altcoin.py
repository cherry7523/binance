from binance.client import Client
import ta
import pandas as pd
import numpy as np
import time
client = Client("1nP6bqPkQJXte3dKtx3yQz0yBUyQJnMsJ6EaXHh3qF3IwB1pDkGdQddSZzV41WAL", "ydWMSGJRC5ONLZ8NqRTP0UXK6cOpirXjFuuROEf0cs6QckVZonURReyERhAdADZb")
# x= pd.DataFrame(client.get_ticker())

def getminutedata(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, 
                                                    interval, 
                                                    start_str=(lookback + ' min ago UTC') ))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit= 'ms')
    frame = frame.astype(float)
    return frame

df = getminutedata('BTCUSDT', '1m', '500')
# print(df)

def applytechnicals(df):
    df['%K'] = ta.momentum.stoch(df.High , df.Low, df.Close, window = 14, smooth_window = 3)
    df['%D'] = df['%K'].rolling(3).mean()
    df['rsi'] = ta.momentum.rsi(df.Close, window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df['macddf'] = df['macd'] - df['macd'].shift(1)
    # df.dropna(inplace=True)

applytechnicals(df)

print(df)
time.sleep(60)

df2 = getminutedata('BTCUSDT', '1m', '3')
print(df2)

dfout = df.append(df2.iloc[-1])
applytechnicals(dfout)
print(dfout)


class Signals:
    def __init__(self,df,lags):
        self.df = df
        self.lags = lags
    
    def gettrigger(self):
        dfx = pd.DataFrame()
        for i in range(self.lags +1):
            mask = (self.df['%K'].shift(i) <20) & (self.df['%D'].shift(i) <20)
            dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    def decide(self):
        self.df['trigger'] = np.where(self.gettrigger(), 1, 0)
        self.df['Buy'] = np.where((self.df.trigger) & (self.df['%K'].between(20,80)) 
                            & (self.df['%D'].between(20,80))
                            & (self.df.rsi >50) & ( self.df.macd >0), 1, 0)

inst = Signals(df, 25)
inst.decide()

def strategy(pair, qty, open_position=False):
    df = getminutedata(pair, '1m', '100')
    applytechnicals(df)
    inst = Signals(df, 25)
    inst.decide()
    print(f'current Close is '+str(df.Close.iloc[-1]))
    if df.Buy.iloc[-1]:
        order = client.create_order(symbol = pair, side='BUY', type='MARKET', quantity=qty)
        print(order)
        buyprice = float(order['fills'][0]['price'])
        open_position = True
