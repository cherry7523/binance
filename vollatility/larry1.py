# import ccxt 
# import pprint
# import time
# import datetime
import pandas as pd
import math

#수량계산 
def cal_amount(usdt_balance, cur_price):
    portion = 0.2
    usdt_trade = usdt_balance* portion
    amount = math.floor((usdt_trade *1000000) /cur_price )/1000000
    #버림 계산 가우스 함수 floor
    return amount


def cal_target(exchange,symbol):
    # 일봉 ccxt 에서 얻기
    data = exchange.fetch_ohlcv(
        symbol=symbol, 
        timeframe='1d', 
        since=None, 
        limit=10
    )
    #일봉데이터 프레임으로 변환
    df = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open']+ (yesterday['high'] - yesterday['low'])*0.5
    short_target = today['open']- (yesterday['high'] - yesterday['low'])*0.5
    return (long_target, short_target)


def enter_position(exchange, symbol, cur_price, long_target, short_target ,amount, position ):
    if cur_price >= long_target:
        position['type']= 'long'
        position['amount'] = amount
        exchange.create_market_buy_order(symbol= symbol, amount= amount)
    elif cur_price < short_target :
        position['type']= 'short'
        position['amount'] = amount
        exchange.create_market_sell_order(symbol= symbol, amount= amount)

def exit_position(exchange,symbol,position):
    amount = position['amount']

    if position['type']== 'long' : 
        exchange.create_market_sell_order(symbol= symbol, amount= amount)
        position['type'] = None
    elif position['type'] == 'short' : 
        exchange.create_market_buy_order(symbol= symbol, amount= amount)
        position['type'] = None