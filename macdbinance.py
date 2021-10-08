import yfinance as yf
import matplotlib.pyplot as plt
from re import I
import ccxt 
import pprint
import time
import datetime
import pandas as pd

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


balance = binance.fetch_balance(params={"type":"future"})
print("선물" ,balance['USDT'])

btc= binance.fetch_ticker("BTC/USDT")
pprint.pprint(btc['last'])

def get_ohlcv(ticker,timep):

    btc = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timep, 
        since=None, 
        limit=50)

    df = pd.DataFrame(btc, columns=['datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    return df
# print(df)


def macd_trading(df):


    # df = yf.download(ticker, start ='2019-03-01') # 이건 미국 주식 받을때 쓰는  yf

    def MACD(df):
        df['EMA12'] = df.Close.ewm(span=12).mean()
        df['EMA26'] = df.Close.ewm(span=26).mean()
        df['MACD'] = df.EMA12 - df.EMA26
        df['signal'] = df.MACD.ewm(span=9).mean()
        df['histo'] = df.MACD - df.signal
        df['histodf'] = df.MACD - df.signal
        # print("indicators added")
        for i in range(1, len(df)):
            df.histodf.iloc[i] = df.histo.iloc[i] - df.histo.iloc[i-1]    
 
    MACD(df)



    # print (df)

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
    # plt.show()

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
    lever = 4


    # for i in range(len(Sellprices)):
    #     profit = profit * ((((Sellprices[i]/Buyprices[i]) - 1)*lever + 1)-0.005) #슬리피지  롱만 계산할때 


    for i in range(len(Sellprices)):
        profit = profit * ((((Sellprices[i]/Buyprices[i]) - 1)*lever + 1)-0.005) #슬리피지 롱 숏 다 먹을때 
    # for i in range(len(Sellprices)-1):
    #     profit = profit * ((((Sellprices[i]/Buyprices[i+1]) - 1)*lever + 1)-0.005)
# 바이 0 = 100  셀 0  120 바이 1 은 110   (( 셀 0 - 바이 1 ) / 바이1 * 레버) +1 -0.005

    return profit



# for ticker in ["TSLA", "AAPL","GOOG","MSFT", "AMZN", "MRNA"]:
# for ticker in ["BTC/USDT","ETH/USDT", "SOL/USDT", "1000SHIB/USDT"]:
for ticker in ["BTC/USDT","ETH/USDT"]:    
    for timef in ["1m","5m","15m","30m","1h","4h","8h","1d","3d","1w","1M"]:
    # timef = "1w"
        df = get_ohlcv(ticker, timef)
        ror = macd_trading(df)
        period_ror = df.iloc[-1,3] / df.iloc[0,0]
        print(ticker, timef, "알고리즘수익율",ror, "존버수익율",period_ror)
        time.sleep(0.2)

# for timep in ["1m","5m","15m","30m","1h","4h","8h","1d","3d","1w","1M"]:
    
#     df = get_ohlcv("ETH/USDT",timep)
#     ror = macd_trading(df)
#     period_ror = df.iloc[-1,3] / df.iloc[0,0]
#     print("ETH/USDT",timep, "알고리즘수익율",ror, "존버수익율",period_ror)
#     time.sleep(0.2)







    # print(df)
    # print(Buyprices)
    # print(Sellprices)
 



# print (Buyprices)
# print (Sellprices)