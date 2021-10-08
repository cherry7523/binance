import ccxt 
import pandas as pd 

binance = ccxt.binance()
btc_ohlcv = binance.fetch_ohlcv(symbol="BTC/USDT", timeframe='1h', limit=100)

# 데이터 프레임 변환
df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
print(df)