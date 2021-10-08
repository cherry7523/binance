from re import I
import ccxt 
import pprint
import time
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

# USDT의 잔고 조회
balance = binance.fetch_balance(params={"type":"future"})
print("선물" ,balance['USDT'])


print(  balance['total']['USDT'])

btc= binance.fetch_ticker("BTC/USDT")
pprint.pprint(btc['last'])


btc = binance.fetch_ohlcv(
    symbol="BTC/USDT", 
    timeframe='1h', 
    since=None, 
    limit=10)

df = pd.DataFrame(btc, columns=['datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
# print(df)

symbol="BTC/USDT"
order_book= binance.fetch_order_book(
    symbol=symbol)

print(type(order_book))


open_orders = binance.fetch_open_orders(
    symbol = symbol
    )

pprint.pprint(type(open_orders))


# balance = binance.fetch_balance()
# positions = balance['info']['positions']
# for position in positions:
#     if position['positionAmt'] == 0:
#         pprint.pprint(position)





# print(order_book.keys())
# asks = order_book['asks']
# bids = order_book['bids']

# number=[0,1,2,3,4,]
# for num in number:
#     num2 = 4-num
#     print('매도호가',num2 ,asks[num2][0], ' 수량 ',  asks[(num2)][1])


# for num in number:
#     print('매수호가',num ,bids[num][0], ' 수량 ',  bids[num][1])




# resp= binance.create_limit_buy_order(
#     symbol=symbol, amount= 0.001,price= 45000)

# pprint.pprint (resp['id'])










# markets= binance.load_markets()
# print(type(markets))
# print(len(markets))

# pprint.pprint(markets)




# print(type(binance))
# order = binance.create_limit_buy_order(
#     symbol="BTC/USDT", 
#     amount=0.001, 
#     price=40000
# )

# pprint.pprint(order)

# order_id = order['info']['orderId']
# symbol = order['symbol']

# print(order_id)

# resp = binance.cancel_order(
#     id=order_id,
#     symbol=symbol
# )

# pprint.pprint(resp)