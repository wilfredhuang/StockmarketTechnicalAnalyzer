import pandas_ta as ta             
import plotly.graph_objects as go 
from stock_utils import fetch_and_process_stock_data as data #change accordingly to where the data is 

#VISUALISATION FOR DATA ANALYSIS


def visualisation_for_analysis():
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
    data['ema_21'] = ta.ema(data['close'],length = 21, append = True)
    data['ema_50'] = ta.ema(data['close'],length = 50, append = True)
    data['RSI_14'] = ta.rsi(data['close'],length = 14, append = True)
    adx_result = ta.adx(data['high'], data['low'], data['close'], length=14, append = True)
    data['adx_14'] = adx_result['ADX_14']


    #technical indicators 
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA-10'],mode='lines',name='SMA10',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index, y=data['ema_21'],mode='lines',name='EMA21',line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data['ema_50'],mode='lines',name='EMA50',line=dict(color='yellow')))
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'],mode='lines',name='RSI',line=dict(color='purple')))
    fig.add_trace(go.Scatter(x=data.index, y=data['ADX_14'] ,mode='lines',name='RSI',line=dict(color='pink')))

    fig.update_layout(title=f'Stock Data for IBM',xaxis_title='Years',xaxis=dict(rangeslider=dict(visible=False)),yaxis_title='Closing Price')
    fig.show()


def ema_crossovers_signals(): 
    data['Crossings'] = 0

    #compares both previous value of ema_21 and ema_50 as we just want the indicator to show when it intersects
    EMA21_above = ((data['ema_21'] > data['ema_50']) & (data['ema_21'].shift(-1) < data['ema_50'].shift(-1))) 
    EMA21_below = (data['ema_21'] < data['ema_50']) & (data['ema_21'].shift(-1) > data['ema_50'].shift(-1))  
    data.loc[EMA21_below, 'Crossings'] = -1
    data.loc[EMA21_above, 'Crossings'] = 1

    #plot buy and sell indicators for cross overs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[data['Crossings'] == -1].index, y=data[data['Crossings'] == -1]['ema_21'],
    mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=15),showlegend=True)) 

    fig.add_trace(go.Scatter(x=data[data['Crossings'] == 1].index, y=data[data['Crossings'] == 1]['ema_21'],
    mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=15), showlegend=True))
    pass

def ema_crossover_rsi_signals():

    #find bool of ema_21 and ema_50
    data['ema21_abv'] = data['ema_21'] > data['ema_50']
    data['ema21_bel'] = data['ema_21'] < data['ema_50']

    #plot buy/sell signals accordingly
    fig = go.Figure()
    #signals are plotted on the closing price
    fig.add_trace(go.Scatter(x=data[(data['RSI'] < 50) & data['ema21_abv']].index,  
                             y=data[(data['RSI'] < 50) & data['ema21_abv']]['close'], 
                             name='Buy', marker=dict(symbol='triangle-up', color='green', size=15), showlegend=True))

    fig.add_trace(go.Scatter(x=data[(data['RSI'] > 50) & data['ema21_bel']].index,  
                             y=data[(data['RSI'] > 50) & data['ema21_bel']]['close'], 
                             name='Sell', marker=dict(symbol='triangle-down', color='red', size=15),showlegend=True)) 
    pass

def rsi_adx_signals():
    #Condition for indicator 
    data['rsi_adx_buy_signal'] = (data['ADX_14'] > 30) & (data['RSI'] < 45)
    data['rsi_adx_sell_signal'] = (data['ADX_14'] > 30) & (data['RSI'] > 45) 

    #plot buy/sell signals accordingly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[data['rsi_adx_buy_signal']].index, 
                             y=data[data['rsi_adx_buy_signal']]['close'],
                             name='Buy', marker=dict(symbol='triangle-up', color='green', size=15), showlegend=True))

    fig.add_trace(go.Scatter(x=data[data['rsi_adx_sell_signal']].index,
                             y=data[data['rsi_adx_sell_signal']]['close'], 
                             name='Sell', marker=dict(symbol='triangle-down', color='red', size=15),showlegend=True)) 
    pass
