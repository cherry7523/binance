
# import matplotlib.pyplot as plt

import ccxt 
import pprint
import time
import datetime
import pandas as pd
import ta

import math

from pandas.core.tools.datetimes import to_datetime

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


def get_ohlcv(ticker,timef):
    # since = "2021-09-28"
    # since = int(pd.to_datetime(since).timestamp() *1000)  #since 인트값으로 변경하기
    coin1m = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timef, 
        since=None,         
        limit=1000)

    df = pd.DataFrame(coin1m, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

def get_ohlcv_2(ticker,timef):
    coin1m = binance.fetch_ohlcv(
        symbol=ticker, 
        timeframe=timef, 
        since=None,         
        limit=1)
    df = pd.DataFrame(coin1m, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

def MACD(df):
    df['histo'] = ta.trend.macd_diff(df.close)
    df['histodf'] = df['histo'] - df['histo'].shift(1)
    # df['histodfrabs'] = df['histodf'].abs()
    meanhisto = df['histodf'].std()
    df['histodfr'] = df['histodf']/ meanhisto *10
    # df['histodfr'] = df['histodf']/df['close'] *1000
    df['rsi'] = ta.momentum.rsi(df.close, window=14)
    df['rsidf'] = df['rsi'] - df['rsi'].shift(1)

# dfs= pd.DataFrame(columns=['symbol','leverage','period', 'portion', 'type','maxcount','maxsoldtime', 'amount', 'high','low', 'counter','soldtime','rehistodf' ])
# dfs.to_excel(f"dfsym.xlsx")
dfs = pd.read_excel(f"dfsym.xlsx")


# dfs.loc[0,'period'] = '15m'  #설정바꾸기
# dfs.loc[1, 'period'] = '1h'
# dfs.loc[2, 'period'] = '8h'
# dfs.loc[3, 'period'] = '8h'
# dfs.loc[4, 'period'] = '8h'

# dfs.loc[0, 'type' ] = 0   #1h 롱
# dfs.loc[1, 'type' ] = 1   #8h 롱
# dfs.loc[2, 'type' ] = 1    #3d 롱
# dfs.loc[3, 'type' ] = 0   #eth3d 롱
# dfs.loc[4, 'type' ] = 0    #bnb8h 롱
# dfs.loc[0, 'portion'] = 0.15 #1h 
# dfs.loc[1, 'portion'] = 0.2  #8h
# dfs.loc[2, 'portion'] = 0.15   #3d
# dfs.loc[3, 'portion'] = 0.2   #eth3d
# # dfs.loc[4, 'portion'] = 0.1  #bnb8h
# dfs.loc[0, 'maxcount'] = 40 #1h 
# dfs.loc[1, 'maxcount'] = 60  #8h
# dfs.loc[2, 'maxcount'] = 60   #3d
# dfs.loc[3, 'maxcount'] = 60  #eth3d
# dfs.loc[4, 'maxcount'] = 50  #bnb8h
# dfs.loc[0, 'leverage'] = 20 #1h 
# dfs.loc[1, 'leverage'] = 20  #8h
# dfs.loc[2, 'leverage'] = 20   #3d
# dfs.loc[3, 'leverage'] = 60  #eth3d
# dfs.loc[4, 'leverage'] = 50  #bnb8h
# dfs.loc[0, 'maxsoldtime'] = 100 #1h 
# dfs.loc[1, 'maxsoldtime'] = 300  #8h
# dfs.loc[2, 'maxsoldtime'] = 1000   #3d
# dfs.loc[3, 'maxsoldtime'] = 500  #eth3d
# dfs.loc[4, 'maxsoldtime'] = 500  #bnb8h
# dfs.loc[0, 'soldtime'] = 0 #1h 
# dfs.loc[1, 'soldtime'] = 0  #8h
# dfs.loc[2, 'soldtime'] = 0   #3d
# dfs.loc[3, 'soldtime'] = 0  #eth3d
# dfs.loc[4, 'soldtime'] = 0  #bnb8h





df1 = get_ohlcv(dfs.symbol[0],dfs.period[0])
df2 = get_ohlcv(dfs.symbol[1],dfs.period[1])
df3 = get_ohlcv(dfs.symbol[2],dfs.period[2])
df4 = get_ohlcv(dfs.symbol[3],dfs.period[3])
df5 = get_ohlcv(dfs.symbol[4],dfs.period[4])

MACD(df1)
MACD(df2)
MACD(df3)
MACD(df4)
MACD(df5)





print(len(dfs))
print(df1.index[-1])

def MACD_2(dfa, i):
    dfb = get_ohlcv_2(dfs.symbol[i] ,dfs.period[i])
    if dfa.index[-1] == dfb.index[-1] :
        dfa.close[-1] = dfb.close[-1]
    elif dfa.index[-1] != dfb.index[-1] :
        dfa = dfa.append(dfb)
    MACD(dfa)
    return dfa
    # df1 = MACD_2(df1, 0)

def cal_amount(usdt_balance, cur_price, portion,leverage):
    usdt_trade = usdt_balance* portion *leverage
    amount = math.floor((usdt_trade *1000) /cur_price )/1000 #  0.001이하 버림 계산 가우스 함수 floor
    return amount

def cal_amount_2(usdt_balance, cur_price, portion,leverage):
    usdt_trade = usdt_balance* portion *leverage
    amount = math.floor((usdt_trade * 10 ) /cur_price )/10  #1이하 버림 계산 가우스 함수 floor
    return amount

def buy_position(exchange, symbol, amount, df ):
    exchange.create_market_buy_order(symbol= symbol, amount= amount)

def sell_position(exchange, symbol, amount, df ):
    exchange.create_market_sell_order(symbol= symbol, amount= amount)

def judge(df_1,  i, usdt):
    coin = binance.fetch_ticker(symbol=dfs.symbol[i])
    cur_price = coin['last']
  

    if df_1['histodfr'][-1] > 2 and (dfs['type'][i] == 0):
        dfs.loc[i,'counter'] += 1
        if dfs.loc[i,'counter'] >= dfs['maxcount'][i] :
            amount = cal_amount(usdt, cur_price, dfs.portion[i], dfs.leverage[i])
            if dfs['symbol'][i] == 'BNB/USDT' :
                amount = cal_amount_2(usdt, cur_price, dfs.portion[i], dfs.leverage[i])

            buy_position(binance, dfs['symbol'][i], amount, dfs)
            dfs.loc[i,'counter'] = 0
            dfs.loc[i,'type'] = 1
            dfs.loc[i,'soldtime'] = dfs['maxsoldtime'][i]
            dfs.loc[i,'amount'] = amount
            print(dfs.symbol[i],dfs.period[i],' buy! ' , amount, cur_price)

    elif df_1['histodfr'][-1] < 2 and (dfs['type'][i] == 0):
        if dfs.loc[i,'counter'] >0 :
            dfs.loc[i,'counter'] -= 1

    elif df_1['histodfr'][-1] < -2 and (dfs['type'][i] == 1):
        dfs.loc[i,'counter'] -= 1 
        if dfs.loc[i,'counter'] <= -(dfs['maxcount'][i]) :
            amount = dfs.loc[i,'amount']
            if dfs.loc[i,'amount']==0 :
                amount = cal_amount(usdt, cur_price, dfs.portion[i], dfs.leverage[i])
                if dfs['symbol'][i] == 'BNB/USDT' :
                    amount = cal_amount_2(usdt, cur_price, dfs.portion[i], dfs.leverage[i])
            sell_position(binance, dfs.symbol[i], amount, dfs)
            dfs.loc[i,'counter'] = 0
            dfs.loc[i,'type'] = 0
            dfs.loc[i,'amount'] = 0
            dfs.loc[i,'soldtime'] = (dfs['maxsoldtime'][i] * 1.5)
            print(dfs.symbol[i],dfs.period[i],' sell! ' , amount, cur_price)

    elif df_1['histodfr'][-1] > -2 and (dfs['type'][i] == 1):
        if dfs.loc[i,'counter'] < 0 :
            dfs.loc[i,'counter'] += 1

for i in range(len(dfs)):
    print(dfs.symbol[i], dfs.period[i],dfs.loc[i,'type'] ,dfs.amount[i])



# print(df1.iloc[-60:] ,'\n','absmean',df1['histodfr'].abs().mean(),'\n','std', df1['histodf'].std() )
# print(df2.iloc[-40:] ,'\n','absmean',df2['histodfr'].abs().mean(),'\n','std', df2['histodf'].std() )
# print(df3.iloc[-30:] ,'\n','absmean',df3['histodfr'].abs().mean(),'\n','std', df3['histodf'].std() )
# print(df4.iloc[-30:] ,'\n','absmean',df4['histodfr'].abs().mean(),'\n','std', df4['histodf'].std() )
# print(df5.iloc[-40:] ,'\n','absmean',df5['histodfr'].abs().mean(),'\n','std', df5['histodf'].std() )

op_mode = True

for i in range(len(dfs)):
    binance.set_leverage(leverage = dfs.leverage[i], symbol = dfs.symbol[i]) #레버리지설정


while True:

    now = datetime.datetime.now()
    
 
    df1 = MACD_2(df1, 0)              #1시간4시간 단위 macd 계산하기
    time.sleep(0.2)
    df2 = MACD_2(df2, 1)
    time.sleep(0.2)
    df3 = MACD_2(df3, 2)              #1시간4시간 단위 macd 계산하기
    time.sleep(0.2)
    df4 = MACD_2(df4, 3)
    time.sleep(0.2) 
    df5 = MACD_2(df5, 4)
    time.sleep(0.2) 
    
    if (55<= now.second < 60):
        dfs.to_excel(f"dfsym.xlsx")     #엑셀에 1분에 한번씩 저장하기
    
    balance = binance.fetch_balance(params={"type":"future"})
    usdt = balance['total']['USDT']  
    coin = binance.fetch_ticker(symbol='BTC/USDT')
    cur_price = coin['last']

    if op_mode and (dfs['soldtime'][0] <= 0):
        judge(df1, 0, usdt)
        time.sleep(0.1)
    if op_mode and (dfs['soldtime'][1] <= 0):
        judge(df2, 1, usdt)
        time.sleep(0.1)
    if op_mode and (dfs['soldtime'][2] <= 0):
        judge(df3, 2, usdt)
        time.sleep(0.1)
    if op_mode and (dfs['soldtime'][3] <= 0):
        judge(df4, 3, usdt)
        time.sleep(0.1)
    if op_mode and (dfs['soldtime'][4] <= 0):
        judge(df5, 4, usdt)
        time.sleep(0.1)


    print(now, cur_price, round(df1['histodfr'][-1],3),dfs['counter'][0],dfs['soldtime'][0], 
                          round(df2['histodfr'][-1],3),dfs['counter'][1],dfs['soldtime'][1],
                          round(df3['histodfr'][-1],3),dfs['counter'][2],dfs['soldtime'][2], 
                          round(df4['histodfr'][-1],3),dfs['counter'][3],dfs['soldtime'][3],
                          round(df5['histodfr'][-1],3),dfs['counter'][4],dfs['soldtime'][4])
    
    for i in range(len(dfs)) :
        if (dfs.soldtime[i] > 0):
            dfs.loc[i,'soldtime'] -= 1
            if (i == 1) and ((now.hour == 0) or (now.hour == 8) or (now.hour == 16)) and (now.minute == 59):
                dfs.loc[i,'soldtime'] = 0

    time.sleep(2.3)











# # df1['histodfrabs'] = df1['histodf'].abs()
# # print(df1.iloc[-20:])
# mean1 = df1['histodfrabs'].mean()
# mean2 = df1['histodf'].std()
# print(mean1, mean2,'\n')

# print(dfs.symbol[1], dfs.period[1],dfs.loc[1,'type'])
# # print(df2.iloc[-20:])
# # df2['histodfrabs'] = df2['histodf'].abs()
# mean1 = df2['histodfrabs'].mean()
# print(mean1,'\n')

# print(dfs.symbol[2], dfs.period[2],dfs.loc[2,'type'])
# # print(df3.iloc[-20:])
# # df3['histodfrabs'] = df3['histodf'].abs()
# mean1 = df3['histodfrabs'].mean()
# print(mean1,'\n')

# print(dfs.symbol[3], dfs.period[3],dfs.loc[3,'type'])
# # print(df4.iloc[-20:])
# # df4['histodfrabs'] = df4['histodf'].abs()
# mean1 = df4['histodfrabs'].mean()
# print(mean1,'\n')

# print(dfs.symbol[4], dfs.period[4],dfs.loc[4,'type'])
# # print(df5.iloc[-20:])
# # df5['histodfrabs'] = df5['histodf'].abs()
# mean1 = df5['histodfrabs'].mean()
# print(mean1,'\n')

        # coin = binance.fetch_ticker(symbol=dfs.symbol[0])
        # cur_price = coin['last']
        # balance = binance.fetch_balance(params={"type":"future"})
        # usdt = balance['total']['USDT']    

        # if df1['histodf'][-1] > 0 and (dfs['type'][0] == None):
        #     dfs['count'][0] =  dfs['count'][0] + 1
        #     if dfs['count'][0] >= dfs['maxcount'][0] :
        #         amount = cal_amount(usdt, cur_price, dfs.portion[0], dfs.leverage[0])
        #         buy_position(binance, symbol, amount, dfs)
        #         dfs['count'][0] = 0
        #         dfs['type'][0] = 1
        #         dfs['soldtime'][0] = dfs['maxsoldtime'][0]
        #         print(dfs.symbol[0],dfs.period[0],' buy! ' , amount, cur_price)

        # elif df1['histodf'][-1] <= 0 and (dfs['type'][0] == None):
        #     if dfs['count'][0] >0 :
        #         dfs['count'][0] =  dfs['count'][0] - 1

        # elif df1['histodf'][-1] <= 0 and (dfs['type'][0] == 1):
        #     dfs['count'][0] =  dfs['count'][0] -1 
        #     if dfs['count'][0] <= -(dfs['maxcount'][0]) :
        #         amount = cal_amount(usdt, cur_price, dfs.portion[0], dfs.leverage[0])
        #         sell_position(binance, symbol, amount, dfs)
        #         dfs['count'][0] = 0
        #         dfs['type'][0] = None
        #         dfs['soldtime'][0] = (dfs['maxsoldtime'][0] * 1.2)
        #         print(dfs.symbol[0],dfs.period[0],' sell! ' , amount, cur_price)

        # elif df1['histodf'][-1] > 0 and (dfs['type'][0] == 1):
        #     if dfs['count'][0] < 0 :
        #         dfs['count'][0] =  dfs['count'][0] + 1


    # if op_mode and (position['1wsoldtime'] <= 0):
    #     balance = binance.fetch_balance(params={"type":"future"})
    #     usdt = balance['total']['USDT']    
    #     if df1w['histodf'][-1] > 0 and (position['type1w'] == None):
    #         amount1w = cal_amount(usdt, cur_price, portion1w, leverage)
    #         buy_position(binance, symbol, amount1w, position)
    #         position['type1w'] = 1
    #         position['1wsoldtime'] = 240  
    #         print('1w buy! ' , amount1w, cur_price)

    #     elif df1w['histodf'][-1] <= 0 and (position['type1w'] == 1):
    #         amount1w = cal_amount(usdt, cur_price, portion1w, leverage)
    #         sell_position(binance, symbol, amount1w, position)
    #         position['type1w'] = None
    #         position['1wsoldtime'] = 350    
    #         print('1w sold! ' , amount1w, cur_price)

    # if op_mode and (position['15mesoldtime'] <= 0):
    #     balance = binance.fetch_balance(params={"type":"future"})
    #     usdt = balance['total']['USDT']
    #     coineth = binance.fetch_ticker(symbol=symbol_eth)
    #     cur_price = coineth['last']    
    #     if df15me['histodf'][-1] > 0 and (position['type15me'] == None):
    #         position['15mecount'] =  position['15mecount'] + 1
    #         if position['15mecount'] >= 30 :               
    #             amount15me = cal_amount(usdt, cur_price, portion15me, leverage_eth)
    #             buy_position(binance, symbol_eth, amount15me, position)
    #             position['15mecount'] = 0
    #             position['type15me'] = 1
    #             position['15mesoldtime'] = 120
    #             print('15me buy! ' , amount15me, cur_price)

    #     elif df15me['histodf'][-1] <= 0 and (position['type15me'] == None):
    #         if position['15mecount'] >0 :
    #             position['15mecount'] =  position['15mecount'] - 1



    #     elif df15me['histodf'][-1] <= 0 and (position['type15me'] == 1):
    #         position['15mecount'] =  position['15mecount'] -1 
    #         if position['15mecount'] == -30 :            
    #             amount15me = cal_amount(usdt, cur_price, portion15me, leverage_eth)
    #             sell_position(binance, symbol_eth, amount15me, position)
    #             position['15mecount'] = 0
    #             position['type15me'] = None
    #             position['15mesoldtime'] = 130
    #             print('15me sold! ' , amount15me, cur_price)

    #     elif df15me['histodf'][-1] > 0 and (position['type15me'] == 1):
    #         if position['15mecount'] < 0 :
    #             position['15mecount'] =  position['15mecount'] + 1

    # if op_mode and (position['4hbsoldtime'] <= 0):
    #     balance = binance.fetch_balance(params={"type":"future"})
    #     usdt = balance['total']['USDT']
    #     coineth = binance.fetch_ticker(symbol=symbol_b)
    #     cur_price = coineth['last']    
    #     if df4hb['histodf'][-1] > 0 and (position['type4hb'] == None):
    #         position['4hbcount'] =  position['4hbcount'] + 1
    #         if position['4hbcount'] >= 80 :               
    #             amount4hb = cal_amount_2(usdt, cur_price, portion4hb, leverage_b)
    #             buy_position(binance, symbol_b, amount4hb, position)
    #             position['4hbcount'] = 0
    #             position['type4hb'] = 'long'
    #             position['4hbsoldtime'] = 320
    #             print('4hb buy! ' , amount4hb, cur_price)

    #     elif df4hb['histodf'][-1] <= 0 and (position['type4hb'] == None):
    #         if position['4hbcount'] >0 :
    #             position['4hbcount'] =  position['4hbcount'] - 1



    #     elif df4hb['histodf'][-1] <= 0 and (position['type4hb'] == 'long'):
    #         position['4hbcount'] =  position['4hbcount'] -1 
    #         if position['4hbcount'] == -80 :            
    #             amount4hb = cal_amount_2(usdt, cur_price, portion4hb, leverage_b)
    #             sell_position(binance, symbol_b, amount4hb, position)
    #             position['4hbcount'] = 0
    #             position['type4hb'] = None
    #             position['4hbsoldtime'] = 310
    #             print('4hb sold! ' , amount4hb, cur_price)

    #     elif df4hb['histodf'][-1] > 0 and (position['type4hb'] == 'long'):
    #         if position['4hbcount'] < 0 :
    #             position['4hbcount'] =  position['4hbcount'] + 1












# #각종 설정들
# symbols =["BTC/USDT","ETH/USDT"]
# symbol = "BTC/USDT"
# leverage = 10
# portion1h = 0.15
# portion4h = 0.25
# portion1w = 0.35

# symbol_eth = "ETH/USDT"
# leverage_eth = 7
# portion15me = 0.2
# portion1he = 0.1
# portion1we = 0.3

# position = {
#     "type" : None,
#     "type1h" : None,
#     "type4h" : None,
#     "type1w" : 'long',
#     "type15me" : None,
#     "amount" : 0,
#     "high" : 0,
#     "1hcount" : 0,
#     "1hsoldtime" : 0,
#     "4hsoldtime" : 0,
#     "1wsoldtime" : 0,
#     "15mesoldtime" : 0,
#     "15mecount" : 0
# }
# #설정값

# df1m = get_ohlcv(symbol,'1m')
# df1 = get_ohlcv(symbol,dfs.time[0])
# df4h = get_ohlcv(symbol,'4h')
# df1d = get_ohlcv(symbol,'1d')
# df1w = get_ohlcv(symbol,'1w')
# df15me = get_ohlcv(symbol_eth,'2h')




# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
#     df = get_ohlcv(ticker)
#     df.to_excel(f"{ticker}.xlsx")

# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
# # for ticker in ["KRW-BTC"]:
#     df = pd.read_excel(f"{ticker}.xlsx", index_col= 0 )
#     ror = short_trading_for_1percent(df)
#     기간수익률 = df.iloc[-1,3] / df.iloc[0,0]
#     print(ticker, f"{ror:.4f}", f"{기간수익률:.4f}")



# balance = binance.fetch_balance(params={"type":"future"})
# usdt = balance['total']['USDT']
# usedusdt = balance['used']['USDT']

# print(usdt)
# print(usedusdt)

# coin = binance.fetch_ticker(symbol=symbol)
# cur_price = coin['last']
# print(cur_price)
# lastcoin = [df1['histodf'][-1],df4h['histodf'][-1],df1w['histodf'][-1]]
# print(lastcoin)

# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
#     df = get_ohlcv(ticker)
#     df.to_excel(f"{ticker}.xlsx")

# for ticker in ["KRW-BTC", "KRW-XRP","KRW-ETH","KRW-ADA"]:
# # for ticker in ["KRW-BTC"]:
#     df = pd.read_excel(f"{ticker}.xlsx", index_col= 0 )
#     ror = short_trading_for_1percent(df)
#     기간수익률 = df.iloc[-1,3] / df.iloc[0,0]
#     print(ticker, f"{ror:.4f}", f"{기간수익률:.4f}")




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
