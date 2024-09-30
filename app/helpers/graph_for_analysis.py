import pandas_ta as ta           
import pandas as pd  
import plotly.graph_objects as go 
from plotly import utils
import plotly
import plotly.express as px

from json import dumps

# from stock_utils import fetch_and_process_stock_data as data #change accordingly to where the data is 

#VISUALISATION FOR DATA ANALYSIS

#to include customised indicators like crossovers, buy/sell signals 

def visualise_analysis(csv_filename, company):
    #main graph 
    data = pd.read_csv(f"app/static/data/{csv_filename}")
    data = data.loc[data['Symbol'] == company]
    fig = go.Figure(data = 
                    [go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    increasing_line_color = "red",
                    decreasing_line_color = "green",
                    name="Closing Price")])


    #calculations (not sure if data['Close'] is the correct params for these feel free to change)
    data['SMA-10'] = ta.sma(data['Close'], length=10, append=True)
    data['EMA-50'] = ta.ema(data['Close'], length=50,append=True)
    data['RSI'] = ta.rsi(data['Close'], length=20,append=True)


    #technical indicators 
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA-10'],mode='lines',name='SMA10',line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA-50'],mode='lines',name='EMA50',line=dict(color='yellow')))
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'],mode='lines',name='RSI',line=dict(color='purple')))
    fig.update_layout(title=f'Stock Data for {company}',xaxis_title='Years',xaxis=dict(rangeslider=dict(visible=False)),yaxis_title='Closing Price')
    
    #Convert the graph into json so that it can be visualised in the template
    plot_json = plotly.io.to_json(fig, pretty=True)
    return plot_json

def visualise_prediction(prediction_data, historical_data):
    fig = px.line(prediction_data, x="Date", y="Results", title='Stock Prices')
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['Close'],mode='lines',name='Historical Data',line=dict(color='yellow')))

    plot_json = plotly.io.to_json(fig, pretty=True)
    
    return plot_json