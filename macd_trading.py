
# import matplotlib.pyplot as plt

import ccxt 
import pprint
import time
import datetime
import pandas as pd
import ta

import math

from pandas.core.tools.datetimes import to_datetime

api_key = "
secret = "

# binance 객체 생성
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit':True,
    'options': {
        'defaultType': 'future'
    }
})

 
def get_ohlcv(ticker,timef):
    # since = "2021-09-28"
    # since = int(pd.to_datetime(since).timestamp() *1000)  #since 인트값으로 변경하기
    coin1m = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timef, 
        since=None,         
        limit=500)

    df = pd.DataFrame(coin1m, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

  
def MACD(df):
    df['histo'] = ta.trend.macd_diff(df.close)
    df['histodf'] = df['histo'] - df['histo'].shift(1)
    df['histodfr'] = df['histodf']/df['close'] *1000
    df['rsi'] = ta.momentum.rsi(df.close, window=14)
    df['rsidf'] = df['rsi'] - df['rsi'].shift(1)


#각종 설정들
symbols =["BTC/USDT","ETH/USDT"]
symbol = "BTC/USDT"
leverage = 25
portion1h = 0.1
portion4h = 0.4
portion1w = 0.4

symbol_eth = "ETH/USDT"
leverage_eth = 10
portion15me = 0.2
portion1he = 0.1
portion1we = 0.3


symbol_b = "BNB/USDT"
leverage_b = 15
portion4hb = 0.15
portion1he = 0.1
portion1we = 0.3
position = {
    "type" : None,
    "type1h" : None,
    "type4h" : None,
    "type1w" : 'long',
    "type15me" : 'long',
    "type4hb" : None,
    "amount" : 0,
    "high" : 0,
    "1hcount" : 0,
    "4hcount" : 0,
    "1wcount" : 0,
    "15mecount" : 0,
    "4hbcount" : 0,
    "1hsoldtime" : 0,
    "4hsoldtime" : 0,
    "1wsoldtime" : 0,
    "15mesoldtime" : 0,
    "4hbsoldtime" : 0
}
#설정값

df1m = get_ohlcv(symbol,'1m')
df1h = get_ohlcv(symbol,'1h')
df4h = get_ohlcv(symbol,'8h')
df1d = get_ohlcv(symbol,'1d')
df1w = get_ohlcv(symbol,'3d')
df15me = get_ohlcv(symbol_eth,'3d')
df4hb = get_ohlcv(symbol_b,'8h')

MACD(df1m)
MACD(df1h)
MACD(df4h)
MACD(df1d)
MACD(df1w)
MACD(df15me)
MACD(df4hb)



# print (df4h.iloc[-20:])
# print(df15me.iloc[-20:])
# print(df4hb.iloc[-20:])

def cal_amount(usdt_balance, cur_price, portion,leverage):
  
    usdt_trade = usdt_balance* portion *leverage
    amount = math.floor((usdt_trade *1000) /cur_price )/1000
    #버림 계산 가우스 함수 floor
    return amount

def cal_amount_2(usdt_balance, cur_price, portion,leverage):
  
    usdt_trade = usdt_balance* portion *leverage
    amount = math.floor((usdt_trade * 10 ) /cur_price )/10
    #버림 계산 가우스 함수 floor
    return amount

def buy_position(exchange, symbol, amount, position ):
    position['type']= 'long'
    position['amount'] = amount
    exchange.create_market_buy_order(symbol= symbol, amount= amount)

def sell_position(exchange, symbol, amount, position ):
    position['type']= 'short'
    position['amount'] = amount
    exchange.create_market_sell_order(symbol= symbol, amount= amount)


op_mode = False

balance = binance.fetch_balance(params={"type":"future"})
usdt = balance['total']['USDT']
usedusdt = balance['used']['USDT']

print(usdt)
print(usedusdt)

coin = binance.fetch_ticker(symbol=symbol)
cur_price = coin['last']
print(cur_price)
lastcoin = [df1h['histodf'][-1],df4h['histodf'][-1],df1w['histodf'][-1]]
print(lastcoin)

binance.set_leverage(leverage = leverage, symbol = symbol) 
binance.set_leverage(leverage = leverage_eth, symbol = symbol_eth) #레버리지설정
binance.set_leverage(leverage = leverage_b, symbol = symbol_b)


while True:

    now = datetime.datetime.now()
    
    if (0 <= now.second <25) or (35<= now.second <55) :
        # df1h = get_ohlcv(symbol,'1h')
        # MACD(df1h)


        op_mode = True     #1시간4시간 단위 macd 계산하기 op모드 온
      
    if (0 <= now.second < 5) or (30 <= now.second < 35):
        df1w = get_ohlcv(symbol,'3d')
        MACD(df1w)
        time.sleep(0.8)
        df15me = get_ohlcv(symbol_eth,'3d')
        MACD(df15me)
        time.sleep(0.8)

    if (5 <= now.second < 15) or (20 <= now.second < 35) or (40<= now.second < 60):    
        df4h = get_ohlcv(symbol,'8h')
        MACD(df4h)
        time.sleep(0.8)
        df4hb = get_ohlcv(symbol_b,'8h')
        MACD(df4hb)
        time.sleep(0.8)


    # if op_mode and (position['1hsoldtime'] <= 0):
    #     balance = binance.fetch_balance(params={"type":"future"})
    #     usdt = balance['total']['USDT']    
    #     if df1h['histodf'][-1] > 0 and (position['type1h'] == None):
    #         position['1hcount'] =  position['1hcount'] + 1
    #         if position['1hcount'] >= 40 :
    #             amount1h = cal_amount(usdt, cur_price, portion1h, leverage)
    #             buy_position(binance, symbol, amount1h, position)
    #             position['1hcount'] = 0
    #             position['type1h'] = 'long'
    #             position['1hsoldtime'] = 120
    #             print('1h buy! ' , amount1h, cur_price)
    #     elif df1h['histodf'][-1] <= 0 and (position['type1h'] == None):
    #         if position['1hcount'] >0 :
    #             position['1hcount'] =  position['1hcount'] - 1


    #     elif df1h['histodf'][-1] <= 0 and (position['type1h'] == 'long'):
    #         position['1hcount'] =  position['1hcount'] -1 
    #         if position['1hcount'] == -40 :
    #             amount1h = cal_amount(usdt, cur_price, portion1h, leverage)
    #             sell_position(binance, symbol, amount1h, position)
    #             position['1hcount'] = 0
    #             position['type1h'] = None
    #             position['1hsoldtime'] = 150
    #             print('1h sold! ' , amount1h, cur_price)
    #     elif df1h['histodf'][-1] > 0 and (position['type1h'] == 'long'):
    #         if position['1hcount'] < 0 :
    #             position['1hcount'] =  position['1hcount'] + 1

    if op_mode and (position['4hsoldtime'] <= 0):
        balance = binance.fetch_balance(params={"type":"future"})
        usdt = balance['total']['USDT']    
        if df4h['histodf'][-1] > 0 and (position['type4h'] == None):
            position['4hcount'] =  position['4hcount'] + 1
            if position['4hcount'] >= 80 :
                amount4h = cal_amount(usdt, cur_price, portion4h, leverage)
                buy_position(binance, symbol, amount4h, position)
                position['4hcount'] = 0
                position['type4h'] = 'long'
                position['4hsoldtime'] = 200
                print('4h buy! ' , amount4h, cur_price)
        elif df4h['histodf'][-1] <= 0 and (position['type4h'] == None):
            if position['4hcount'] >0 :
                position['4hcount'] =  position['4hcount'] - 1

        elif df4h['histodf'][-1] <= 0 and (position['type4h'] == 'long'):
            position['4hcount'] =  position['4hcount'] -1 
            if position['4hcount'] == -80 :
                amount4h = cal_amount(usdt, cur_price, portion4h, leverage)
                sell_position(binance, symbol, amount4h, position)
                position['4hcount'] = 0
                position['type4h'] = None
                position['4hsoldtime'] = 250
                print('4h sold! ' , amount4h, cur_price)

        elif df4h['histodf'][-1] > 0 and (position['type4h'] == 'long'):
            if position['4hcount'] < 0 :
                position['4hcount'] =  position['4hcount'] + 1


    if op_mode and (position['1wsoldtime'] <= 0):
        balance = binance.fetch_balance(params={"type":"future"})
        usdt = balance['total']['USDT']    
        if df1w['histodf'][-1] > 0 and (position['type1w'] == None):
            amount1w = cal_amount(usdt, cur_price, portion1w, leverage)
            buy_position(binance, symbol, amount1w, position)
            position['type1w'] = 'long'
            position['1wsoldtime'] = 600  
            print('1w buy! ' , amount1w, cur_price)

        elif df1w['histodf'][-1] <= 0 and (position['type1w'] == 'long'):
            amount1w = cal_amount(usdt, cur_price, portion1w, leverage)
            sell_position(binance, symbol, amount1w, position)
            position['type1w'] = None
            position['1wsoldtime'] = 750    
            print('1w sold! ' , amount1w, cur_price)

    if op_mode and (position['15mesoldtime'] <= 0):
        balance = binance.fetch_balance(params={"type":"future"})
        usdt = balance['total']['USDT']
        coineth = binance.fetch_ticker(symbol=symbol_eth)
        cur_price = coineth['last']    
        if df15me['histodf'][-1] > 0 and (position['type15me'] == None):
            position['15mecount'] =  position['15mecount'] + 1
            if position['15mecount'] >= 50 :               
                amount15me = cal_amount(usdt, cur_price, portion15me, leverage_eth)
                buy_position(binance, symbol_eth, amount15me, position)
                position['15mecount'] = 0
                position['type15me'] = 'long'
                position['15mesoldtime'] = 120
                print('15me buy! ' , amount15me, cur_price)

        elif df15me['histodf'][-1] <= 0 and (position['type15me'] == None):
            if position['15mecount'] >0 :
                position['15mecount'] =  position['15mecount'] - 1



        elif df15me['histodf'][-1] <= 0 and (position['type15me'] == 'long'):
            position['15mecount'] =  position['15mecount'] -1 
            if position['15mecount'] == -60 :            
                amount15me = cal_amount(usdt, cur_price, portion15me, leverage_eth)
                sell_position(binance, symbol_eth, amount15me, position)
                position['15mecount'] = 0
                position['type15me'] = None
                position['15mesoldtime'] = 130
                print('15me sold! ' , amount15me, cur_price)

        elif df15me['histodf'][-1] > 0 and (position['type15me'] == 'long'):
            if position['15mecount'] < 0 :
                position['15mecount'] =  position['15mecount'] + 1


    if op_mode and (position['4hbsoldtime'] <= 0):
        balance = binance.fetch_balance(params={"type":"future"})
        usdt = balance['total']['USDT']
        coineth = binance.fetch_ticker(symbol=symbol_b)
        cur_price = coineth['last']    
        if df4hb['histodf'][-1] > 0 and (position['type4hb'] == None):
            position['4hbcount'] =  position['4hbcount'] + 1
            if position['4hbcount'] >= 80 :               
                amount4hb = cal_amount_2(usdt, cur_price, portion4hb, leverage_b)
                buy_position(binance, symbol_b, amount4hb, position)
                position['4hbcount'] = 0
                position['type4hb'] = 'long'
                position['4hbsoldtime'] = 320
                print('4hb buy! ' , amount4hb, cur_price)

        elif df4hb['histodf'][-1] <= 0 and (position['type4hb'] == None):
            if position['4hbcount'] >0 :
                position['4hbcount'] =  position['4hbcount'] - 1



        elif df4hb['histodf'][-1] <= 0 and (position['type4hb'] == 'long'):
            position['4hbcount'] =  position['4hbcount'] -1 
            if position['4hbcount'] == -80 :            
                amount4hb = cal_amount_2(usdt, cur_price, portion4hb, leverage_b)
                sell_position(binance, symbol_b, amount4hb, position)
                position['4hbcount'] = 0
                position['type4hb'] = None
                position['4hbsoldtime'] = 310
                print('4hb sold! ' , amount4hb, cur_price)

        elif df4hb['histodf'][-1] > 0 and (position['type4hb'] == 'long'):
            if position['4hbcount'] < 0 :
                position['4hbcount'] =  position['4hbcount'] + 1



    coin = binance.fetch_ticker(symbol=symbol)
    cur_price = coin['last']



    print(now, cur_price, round(df1h['histodfr'][-1],3),position['1hcount'],position['1hsoldtime'],round(df4h['histodfr'][-1],3),position['4hcount'],position['4hsoldtime'],round(df1w['histodfr'][-1],3),position['1wsoldtime'],round(df15me['histodfr'][-1],6),position['15mecount'],position['15mesoldtime'],round(df4hb['histodfr'][-1],6),position['4hbcount'],position['4hbsoldtime'])
    if (position['1hsoldtime'] > 0) :
        position['1hsoldtime'] = position['1hsoldtime'] - 1 
    if (position['4hsoldtime'] > 0) :
        position['4hsoldtime'] = position['4hsoldtime'] - 1 
    if (position['1wsoldtime'] > 0) :
        position['1wsoldtime'] = position['1wsoldtime'] - 1 
    if (position['15mesoldtime'] > 0) :
        position['15mesoldtime'] = position['15mesoldtime'] - 1
    if (position['4hbsoldtime'] > 0) :
        position['4hbsoldtime'] = position['4hbsoldtime'] - 1
            

    time.sleep(4.3)






# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
#     df = get_ohlcv(ticker)
#     df.to_excel(f"{ticker}.xlsx")

# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
# # for ticker in ["KRW-BTC"]:
#     df = pd.read_excel(f"{ticker}.xlsx", index_col= 0 )
#     ror = short_trading_for_1percent(df)
#     기간수익률 = df.iloc[-1,3] / df.iloc[0,0]
#     print(ticker, f"{ror:.4f}", f"{기간수익률:.4f}")



# df['EMA12'] = df.close.ewm(span=12).mean()
# df['EMA26'] = df.close.ewm(span=26).mean()
# df['MACD'] = df.EMA12 - df.EMA26
# df['signal'] = df.MACD.ewm(span=9).mean()
# df['histo'] = df.MACD - df.signal
# df['histodf'] = df.MACD - df.signal
# # print("indicators added")
# for i in range(1, len(df)):
#     df.histodf.iloc[i] = df.histo.iloc[i] - df.histo.iloc[i-1]    

# def exit_position(exchange,symbol,position):
#     amount = position['amount']

#     if position['type']== 'long' : 
#         exchange.create_market_sell_order(symbol= symbol, amount= amount)
#         position['type'] = None
#     elif position['type'] == 'short' : 
#         exchange.create_market_buy_order(symbol= symbol, amount= amount)
#         position['type'] = None


# eth_position = {
#     "type" : None,
#     "amount" : 0,
#     "high" : 0,
#     "soldtime" : 0
# }


# def cal_target(exchange,symbol):
#     # 일봉 ccxt 에서 얻기
#     data = exchange.fetch_ohlcv(
#         symbol=symbol, 
#         timeframe='1m', 
#         since=None, 
#         limit=20
#     )
#     #일봉데이터 프레임으로 변환
#     df = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#     df.set_index('datetime', inplace=True)

#     yesterday = df.iloc[-2]
#     today = df.iloc[-1]
#     long_target = today['open']+ (yesterday['high'] - yesterday['low'])*0.5
#     short_target = today['open']- (yesterday['high'] - yesterday['low'])*0.5
#     return (long_target, short_target)


# def enter_position(exchange, symbol, cur_price, long_target, short_target ,amount, position ):
#     if cur_price >= long_target:
#         position['type']= 'long'
#         position['amount'] = amount
#         exchange.create_market_buy_order(symbol= symbol, amount= amount)
#     elif cur_price < short_target :
#         position['type']= 'short'
#         position['amount'] = amount
#         exchange.create_market_sell_order(symbol= symbol, amount= amount)




    # elif (position['soldtime'] == 0) :

   
    # amount = cal_amount(usdt, cur_price,portion1h)

    # if op_mode and position['type'] is None:
    #     enter_position(binance, symbol, cur_price, amount, position)


    # amount = cal_amount(usdt, cur_price,portion1h)

    # if op_mode and position['type'] is None:
    #     enter_position(binance, symbol, cur_price, amount, position)
    # if op_mode and position['type'] is None:
    #     exit_position(binance, symbol, position)
    #     op_mode = False
    
    # #내일 목표가 갱신
    # if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
    #     long_target,short_target = cal_target(binance,symbol)
    #     balance = binance.fetch_balance(params={"type":"future"})
    #     usdt = balance['total']['USDT']
    #     op_mode = True
    #     time.sleep(10)

    
# def get_ohlcv_1d(ticker):  
#     coin1d = binance.fetch_ohlcv(
#         symbol=ticker, 
#         timeframe='1d', 
#         since=None, 
#         limit=2000)

#     df = pd.DataFrame(coin1d, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#     df.set_index('datetime', inplace=True)
#     return df    #1일 짜리 ohlcv 함수

# def get_ohlcv(ticker):
#     dfs=[]
#     df = pyupbit.get_ohlcv(ticker, interval= "minute5", to="20211004 23:00:00")
#     dfs.append(df)

#     for i in range(20):
#         df = pyupbit.get_ohlcv(ticker, interval= "minute5", to=df.index[0])
#         dfs.append(df)
#         time.sleep(0.2)

#     df = pd.concat(dfs)
#     df = df.sort_index()
#     return df    #여러개 ohlcv 합할때 쓰는 함수

# 마켓 심볼 찾기
# markets = binance.load_markets()
# market = binance.market(symbol)
# print(market['id'])

# resp = binance.fapiPrivate_post_leverage({
#     'symbol' : market['id'],
#     'leverage' : leverage
# })
# print(resp)  #레버리지 설정 

# binance.set_leverage(leverage = leverage, symbol = 'ETH/USDT')
# binance.create_market_sell_order(symbol= 'ETH/USDT', amount= 0.01)
