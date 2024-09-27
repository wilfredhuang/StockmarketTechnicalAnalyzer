import pandas_ta as ta             
import plotly.graph_objects as go 
from stock_utils import fetch_and_process_stock_data as data #change accordingly to where the data is 

#VISUALISATION FOR DATA ANALYSIS

#main graph 
fig = go.Figure(data = 
                [go.Candlestick(x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                increasing_line_color = "red",
                decreasing_line_color = "green",
                name="Closing Price")])


#calculations
data['SMA-10'] = ta.sma(length=10, append=True)
data['EMA-50'] = ta.ema(length=50,append=True)
data['RSI'] = ta.rsi(length=20,append=True)


#technical indicators 
fig.add_trace(go.Scatter(x=data.index, y=data['SMA-10'],mode='lines',name='SMA10',line=dict(color='orange')))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA-50'],mode='lines',name='EMA50',line=dict(color='yellow')))
fig.add_trace(go.Scatter(x=data.index, y=data['RSI'],mode='lines',name='RSI',line=dict(color='purple')))
fig.update_layout(title=f'Stock Data for IBM',xaxis_title='Years',xaxis=dict(rangeslider=dict(visible=False)),yaxis_title='Closing Price')
fig.show()

#to include customised indicators like crossovers, buy/sell signals 




