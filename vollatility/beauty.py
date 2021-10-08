import numpy as np
import pyupbit
import plotly.graph_objects as go
import pandas as pd
import time

pat = [100, 90,80,70,90,120,140]

tickers = pyupbit.get_tickers(fiat="KRW")[:50]

dfs = []
for ticker in tickers:
    df = pyupbit.get_ohlcv(ticker, count=7)
    dfs.append(df['close'])
    time.sleep(0.2)

df = pd.concat(dfs, axis=1)
df.columns = tickers
df['target'] = pat
corr = df.corr()
print(corr.loc['target'].sort_values())

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