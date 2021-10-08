import ccxt
import pprint 

binance = ccxt.binance()
markets= binance.load_markets()

# print(markets.keys())
# print(len(markets))

btc= binance.fetch_ticker("BTC/USDT")
pprint.pprint(btc)

a = 0

for market_usdt in markets.keys():


    if market_usdt.endswith("/USDT"):
        print(market_usdt)
        a= a+1



print(a)

print("현재 ", btc['last'])