import yfinance as yf
import numpy as np
import ta
import pandas as pd
import matplotlib.pyplot as plt

df = yf.download('ETH-USD', start = '2021-08-15', interval= '30m')

df['%K'] = ta.momentum.stoch(df.High,df.Low ,df.Close, window=14, smooth_window = 3)
df['%D'] = df['%K'].rolling(3).mean()
df['rsi'] = ta.momentum.rsi(df.Close, window=14)
df['macd'] = ta.trend.macd_diff(df.Close)

df.dropna(inplace=True)
def gettriggers(df, lags, buy= True):
    dfx = pd.DataFrame()
    for i in range(1, lags+1):
        if buy:
            mask = (df['%K'].shift(i) <20) & (df['%D'].shift(i) <20)
        else:
            mask = (df['%K'].shift(i) >80) & (df['%D'].shift(i) >80)
        dfx = dfx.append(mask, ignore_index=True)
    return dfx.sum(axis=0)

df['Buytrigger']= np.where(gettriggers(df,4,),1,0)
df['Selltrigger']= np.where(gettriggers(df,4,False),1,0)
df['Buy']= np.where((df.Buytrigger)&
                    (df['%K'].between(20,80)) & (df['%D'].between(20,80)) & (df.rsi>50) &
                    (df.macd>0),1,0)
df['Sell']= np.where((df.Selltrigger)&
                    (df['%K'].between(20,80)) & (df['%D'].between(20,80)) & (df.rsi<50) &
                    (df.macd<0),1,0)

Buying_dates , Selling_dates = [],[]
for i in range(len(df)-1):
    if df.Buy.iloc[i]:
        Buying_dates.append(df.iloc[i+1].name)
        for num,j in enumerate(df.Sell[i:]):
            if j:
                Selling_dates.append(df.iloc[i+num+1].name)
                break

cutit = len(Buying_dates) - len(Selling_dates)

if cutit:
    Buying_dates = Buying_dates[:-cutit]

frame = pd.DataFrame({'Buying_dates':Buying_dates, 'Selling_dates': Selling_dates})
actuals = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]
def profitcalc():
    Buyprices = df.loc[actuals.Buying_dates].Open
    Sellprices = df.loc[actuals.Selling_dates].Open
    return (Sellprices.values - Buyprices.values)/Buyprices.values
profits = profitcalc()
print(actuals)
prot= (profits +1).prod()

print(prot)

plt.figure(figsize=(20,10))
plt.plot(df.Close, color = 'k', alpha=  0.7)
plt.scatter(actuals.Buying_dates, df.Open[actuals.Buying_dates],marker='^', color='g', s=500)
plt.scatter(actuals.Selling_dates, df.Open[actuals.Selling_dates],marker='v', color='r', s=500)

plt.show()









 
  
  


# dfx = pd.DataFrame()
# for i in range(1,4):
#     mask = (df['%K'].shift(i) <20) & (df['%D'].shift(i) <20)
#     dfx = dfx.append(mask, ignore_index=True)

# dfx.sum(axis=0)

