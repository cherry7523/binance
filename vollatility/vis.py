from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pyupbit

pat = [100, 90,80,70,90,120,140]

df = pyupbit.get_ohlcv("KRW-POLY", count=7)
poly= go.Scatter(
    x= df.index,
    y= df.close,
    name = "poly"
)

df = pyupbit.get_ohlcv("KRW-OMG", count=7)
omg= go.Scatter(
    x= df.index,
    y= df.close,
    name = "omg"
)

df = pyupbit.get_ohlcv("KRW-ICX", count=7)
icx= go.Scatter(
    x= df.index,
    y= df.close,
    name = "icx"
)


target = go.Scatter(
    x= df.index,
    y= pat,
)

fig = make_subplots(rows=2, cols=2)
fig.add_trace(target ,row=1,col=1)
fig.add_trace(poly ,row=1,col=2)
fig.add_trace(omg ,row=2,col=1)
fig.add_trace(icx ,row=2,col=2)
fig.show()
