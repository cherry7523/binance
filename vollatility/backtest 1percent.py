import numpy as np
import pyupbit
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_ohlcv(ticker):
    dfs=[]
    df = pyupbit.get_ohlcv(ticker, interval= "minute5", to="20211004 23:00:00")
    dfs.append(df)

    for i in range(20):
        df = pyupbit.get_ohlcv(ticker, interval= "minute5", to=df.index[0])
        dfs.append(df)
        time.sleep(0.2)

    df = pd.concat(dfs)
    df = df.sort_index()
    return df
  


def short_trading_for_1percent(df):

    ma15 = df['close'].rolling(15).mean().shift(1)
    ma50 = df['close'].rolling(50).mean().shift(1)
    ma120 = df['close'].rolling(120).mean().shift(1)

    cond_0 = df['high'] >= df['open'] * 1.01
    cond_1 = (ma15>= ma50) & (ma15<= ma50 *1.03)
    cond_2 = ma50 >ma120
    cond_buy = cond_0 & cond_1





    acc_ror = 1
    sell_date = None

    ax_ror = []
    ay_ror = []

    # 매수일자 판별
    cond = df['high'] >= df['open'] * 1.01
    # print(df.index[cond])

    #2 매도조건 탐색 수익율 계산
    for buy_date in df.index[cond]:
        if sell_date != None and buy_date <= sell_date:
            continue

        target = df.loc[buy_date : ]
        cond = target['high'] >= df.loc[buy_date, 'open'] * 1.02
        sell_candidate = target.index[cond] 

        if len(sell_candidate) == 0:
            buy_price = df.loc[buy_date, 'open'] *1.01
            sell_price = df.iloc[-1,3]
            acc_ror *= (sell_price/ buy_price)
            ax_ror.append(df.index[-1])
            ay_ror.append(acc_ror)

            break
        else:
            sell_date= sell_candidate[0]
            acc_ror *= 1.005
            ax_ror.append(sell_date)
            ay_ror.append(acc_ror)


    candle = go.Candlestick(
        x = df.index,
        open = df['open'],
        high = df['high'],
        low = df['low'],
        close = df['close'],
    )

    ror_chart = go.Scatter(
        x = ax_ror,
        y = ay_ror
    )

    fig = make_subplots(specs= [  [{ "secondary_y":True}] ])
    fig.add_trace(candle)
    fig.add_trace(ror_chart, secondary_y = True)
    fig.show()




    return acc_ror


# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
#     df = get_ohlcv(ticker)
#     df.to_excel(f"{ticker}.xlsx")

for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
# for ticker in ["KRW-BTC"]:
    df = pd.read_excel(f"{ticker}.xlsx", index_col= 0 )
    ror = short_trading_for_1percent(df)
    기간수익률 = df.iloc[-1,3] / df.iloc[0,0]
    print(ticker, f"{ror:.4f}", f"{기간수익률:.4f}")

# tickers = pyupbit.get_tickers(fiat="KRW")
# print(tickers)





# pat = [100, 90,80,70,90,120,140]

# tickers = pyupbit.get_tickers(fiat="KRW")[:50]

# dfs = []
# for ticker in tickers:
#     df = pyupbit.get_ohlcv(ticker, count=7)
#     dfs.append(df['close'])
#     time.sleep(0.2)

# df = pd.concat(dfs, axis=1)
# df.columns = tickers
# df['target'] = pat
# corr = df.corr()
# print(corr.loc['target'].sort_values())

# btc= pyupbit.get_ohlcv("KRW-BTC")
# ltc= pyupbit.get_ohlcv("KRW-LTC")

# df = pd.concat([btc['close'], ltc['close']], axis=1)
# df.columns = ["BTC", "LTC"]
# print(df.corr().iloc[0,1])
# print (df)
# val = np.corrcoef([1,2,3],[9,6,1])
# print (val[0,1])

# co = go.Scatter(
#     x = btc['close'],
#     y = ltc['close'],
#     mode = "markers"
# )

# fig = go.Figure([co])
# fig.show()