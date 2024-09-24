# Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# [Data Retrieval]
# user to decide this parameters
TICKERS = [
    'KO','PEP','WMT', # consumer staples
    'SBUX','MCD', # consumer discretionary
    'AAL','DAL','F', # industrials
    'VZ', 'T', 'DIS', # communication services
    'BAC','JPM','MA','V', # financials
    'ORCL','AMD','NVDA','AAPL','MSFT', # information technology
] 
START_DATE = "2010-01-01"
END_DATE = "2024-07-31"

# Documentation: yfinance
df = yf.download(tickers=TICKERS, interval="1d", start=START_DATE, end=END_DATE, auto_adjust=True, group_by='ticker')
df.head() # see how the raw data format looks

# reformat for easy read from store
df = df.stack(level='Ticker')
df.columns = [s.lower() for s in df.columns]
df.index.names = [s.lower() for s in df.index.names]
df.reset_index(inplace=True)
#df.head()

# [Data Cleaning]
# df.info()
# df.isnull().sum()

# format is just a csv file with column names above
df.to_csv('../app/static/data/ohlcv.csv', index=False)


# [Data Processing]
# load the data into proper format for processing
df = pd.read_csv('../app/static/data/ohlcv.csv', parse_dates=['date'])
df.set_index(['date', 'ticker'], inplace=True)
#df.head()

def contruct_indicators(group):

    # indicator: Simple Moving Averages
    group['sma_10'] = ta.sma(group['close'], length=10)
    group['sma_21'] = ta.sma(group['close'], length=21)
    group['sma_50'] = ta.sma(group['close'], length=50)
    group['sma_100'] = ta.sma(group['close'], length=100)
    group['sma_200'] = ta.sma(group['close'], length=200)

    # indicator: Relative Strength Index
    group['rsi_7'] = ta.rsi(group['close'], length=7)
    group['rsi_9'] = ta.rsi(group['close'], length=9)
    group['rsi_14'] = ta.rsi(group['close'], length=14)
    group['rsi_21'] = ta.rsi(group['close'], length=21)
    
    # TO BE CONTINUED:
    # indicator: Exponential Moving Averages
    # indicator: Average Directional Index
    # indicator: Bollinger Bands
    # indicator: 
    # ...
    # ...

    return group

df_indicators = df.groupby('ticker', group_keys=False).apply(contruct_indicators)
df_indicators

# [Data Visualisation and Analysis]

# possibly a dropdown to let user select ticker to visualize
TICKER = 'KO'
data = df_indicators.xs(level='ticker', key=TICKER)
data

# TO BE REFINED LATER ON:

# Create subplots: 2 rows, 1 column with shared x-axis
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.7, 0.3],  # Relative heights of the subplots
    subplot_titles=[f'Candlestick with SMA for {TICKER}', 'RSI and ADX']
)

# Add candlestick trace to the first row
fig.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Candlestick'
    ),
    row=1, col=1
)

# Add moving average trace to the first row
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['sma_10'],
        mode='lines',
        name='SMA(10)',
        line=dict(color='green', width=1)
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['sma_21'],
        mode='lines',
        name='SMA(21)',
        line=dict(color='blue', width=1)
    ),
    row=1, col=1
)

# Add RSI trace to the second row
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['rsi_7'],
        mode='lines',
        name='RSI 7',
        line=dict(color='purple', width=2)
    ),
    row=2, col=1
)

# # Add ADX trace to the second row
# fig.add_trace(
#     go.Scatter(
#         x=df_ticker.index,
#         y=df_ticker['ADX_14'],
#         mode='lines',
#         name='ADX 14',
#         line=dict(color='green', width=2)
#     ),
#     row=2, col=1
# )

# Update layout for the subplots
fig.update_layout(
    title=f'OHLC with SMA and Indicators for {TICKER}',
    xaxis2_title='Date',  # Title for the second subplot's x-axis
    yaxis=dict(title='OHLC'),
    width=1200,
    height=800,
    yaxis2=dict(title='RSI & ADX (0-100)', range=[0, 100]),  # Set the y-axis range for RSI and ADX
    xaxis_rangeslider_visible=False,  # Hide range slider
    legend=dict(x=0.01, y=0.99)
)
fig.show()
