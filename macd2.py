import yfinance as yf
import matplotlib.pyplot as plt

import ccxt 
import pprint
import time
import datetime
import pandas as pd

def get_ohlcv(ticker):

    df = yf.download(ticker, start ='2019-03-01')

    def MACD(df):
        df['EMA12'] = df.Close.ewm(span=24).mean()
        df['EMA26'] = df.Close.ewm(span=52).mean()
        df['MACD'] = df.EMA12 - df.EMA26
        df['signal'] = df.MACD.ewm(span=9).mean()
        df['histo'] = df.MACD - df.signal
        df['histodf'] = df.MACD - df.signal
        # print("indicators added")
        
        for i in range(1, len(df)):
            df.histodf.iloc[i] = df.histo.iloc[i] - df.histo.iloc[i-1]

    MACD(df)

    return df




def macd_trading(df):



    buy_state= 0

    Buy, Sell = [],[]

    for i in range(1,len(df)):
        if (df.histodf.iloc[i] > 0) and (buy_state == 0):
            buy_state = 1
            Buy.append(i)
            

        elif (df.histodf.iloc[i] < 0) and (buy_state == 1):
            buy_state = 0
            Sell.append(i)
            

        # 매수 원칙 macd histo df 가 - 에서 +로 갈때 매수
        # 매수 이후시점으로 고가 체크 

        # 매도 조건 macd histo df 가  +에서 -로 바뀌면 매도 or
        # histodf - 이고 and
        # histo 값이 + 이면 histo 전날대비 90%  작을때 매도 
        # histo 값이 - 이면 histo 전날대비 110% 작을때 매도
        # or 
        # 고가 df.buyhigh 대비 df.low 값이 
        # high_dif(약 3에서 5) 
        # 퍼센트 만큼 떨어졌을시 df.buyhigh * (1-high_dif/100)
        # 가격으로 트레일링 오프 매도 

        # 10분단위로 가격은 검색하되 buy high 값만들때 
        # 매수 매도는 
        # 일봉단위를 기준선으로 정함.

    # plt.scatter(df.iloc[Buy].index, df.iloc[Buy].Close, marker="^", color='green')
    # plt.scatter(df.iloc[Sell].index, df.iloc[Sell].Close, marker="v", color='red')
    # plt.plot(df.Close, label='Tesla Close', color = 'k')
    # plt.legend()
    # plt.plot(((df.histo)*20)+40, label= 'histo', color = 'blue')

    Realbuys = [i for i in Buy]
    Realsells = [i for i in Sell]

    Buyprices = df.Close.iloc[Buy]
    Sellprices = df.Close.iloc[Sell]

    # if Sellprices.index[0] < Buyprices.index[0]:
    #     Sellprices = Sellprices.drop(Sellprices.index[0])
    # elif Buyprices.index[-1] > Sellprices.index[-1]:
    #     Buyprices = Buyprices.drop(Buyprices.index[0])

    profitsrel = []
    profit = 1


    for i in range(len(Sellprices)):
        profit = profit * ((Sellprices[i]/Buyprices[i])-0.005) #슬리피지 


    return profit



for ticker in ["TSLA", "AAPL","GOOG","MSFT", "AMZN", "MRNA"]:
    df = get_ohlcv(ticker)
    ror = macd_trading(df)

    period_ror = df.iloc[-1,3] / df.iloc[0,0]
    print(ticker,"1d", "알고리즘수익율",ror, "존버수익율",period_ror)
    print(ticker, ror)
    time.sleep(0.2)

    # print(df)
    # print(Buyprices)
    # print(Sellprices)
 



# print (Buyprices)
# print (Sellprices)