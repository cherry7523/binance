import yfinance as yf
import matplotlib.pyplot as plt

import ccxt 
import pprint
import time
import datetime
import pandas as pd

df = yf.download('AAPL', start ='2019-03-08',interval= '1wk',end = '2021-03-01' )

def MACD(df):
    df['EMA12'] = df.Close.ewm(span=12).mean()
    df['EMA26'] = df.Close.ewm(span=26).mean()
    df['MACD'] = df.EMA12 - df.EMA26
    df['signal'] = df.MACD.ewm(span=9).mean()
    df['histo'] = df.MACD - df.signal
    print("indicators added")

MACD(df)

Buy, Sell = [],[]

for i in range(3,len(df)):
    if df.histo.iloc[i] > df.histo.iloc[i-1] and df.histo.iloc[i-1] < df.histo.iloc[i-2]:
        Buy.append(i)

    elif df.histo.iloc[i] < df.histo.iloc[i-1] and df.histo.iloc[i-1] > df.histo.iloc[i-2]:
        Sell.append(i)





# for i in range(2,len(df)):
#     if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
#         Buy.append(i)

#     elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
#         Sell.append(i)

plt.scatter(df.iloc[Buy].index, df.iloc[Buy].Close, marker="^", color='green')
plt.scatter(df.iloc[Sell].index, df.iloc[Sell].Close, marker="v", color='red')
plt.plot(df.Close, label='Tesla Close', color = 'k')
plt.legend()
plt.plot(((df.histo)*20)+40, label= 'histo', color = 'blue')

Realbuys = [i for i in Buy]
Realsells = [i for i in Sell]

Buyprices = df.Close.iloc[Realbuys]
Sellprices = df.Close.iloc[Realsells]

if Sellprices.index[0] < Buyprices.index[0]:
    Sellprices = Sellprices.drop(Sellprices.index[0])
elif Buyprices.index[-1] > Sellprices.index[-1]:
    Buyprices = Buyprices.drop(Buyprices.index[0])

profitsrel = []

for i in range(len(Sellprices)):
    profitsrel.append(((Sellprices[i] - Buyprices[i])/Buyprices[i])-0.005)

profit = sum(profitsrel)/len(profitsrel)
print(profit)
plt.show()


# print (Buyprices)
# print (Sellprices)