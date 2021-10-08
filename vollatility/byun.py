import ccxt 
import pprint
import time
import datetime
import pandas as pd

# 파일로부터 apiKey, Secret 읽기 
# with open("api.txt") as f:
#     lines = f.readlines()
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

symbols = ['BTC/USDT' ,'ETH/USDT', 'SOL/USDT', 'LUNA/USDT']
while True:
    for sym in symbols:
        btc = binance.fetch_ticker(symbol=sym)
        cur_price= btc['last']
        now = datetime.datetime.now()
        print(now, "현재가격", sym, ":", cur_price)
    time.sleep(2)


