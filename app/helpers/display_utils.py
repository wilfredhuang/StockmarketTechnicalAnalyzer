import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots

# yfinance with plotly example

def fetch_stock_data(tickers, start_date, end_date):
    """Fetch stock data for given tickers and date range."""
    df = yf.download(tickers=tickers, interval="1d", start=start_date, end=end_date, auto_adjust=True, group_by='ticker')
    df = df.stack(level='Ticker')
    df.columns = [s.lower() for s in df.columns]
    df.index.names = [s.lower() for s in df.index.names]
    df.reset_index(inplace=True)
    return df

def save_data_to_csv(df, filename):
    """Save data to CSV file."""
    df.to_csv(filename, index=False)

def load_data_from_csv(filename):
    """Load data from CSV file."""
    df = pd.read_csv(filename, parse_dates=['date'])
    df.set_index(['date', 'ticker'], inplace=True)
    return df

def construct_indicators(group):
    """Construct technical indicators for a group of stock data."""
    group['sma_10'] = ta.sma(group['close'], length=10)
    group['sma_21'] = ta.sma(group['close'], length=21)
    group['sma_50'] = ta.sma(group['close'], length=50)
    group['sma_100'] = ta.sma(group['close'], length=100)
    group['sma_200'] = ta.sma(group['close'], length=200)
    group['rsi_7'] = ta.rsi(group['close'], length=7)
    group['rsi_9'] = ta.rsi(group['close'], length=9)
    group['rsi_14'] = ta.rsi(group['close'], length=14)
    group['rsi_21'] = ta.rsi(group['close'], length=21)
    return group

def process_data_with_indicators(df):
    """Process data and add technical indicators."""
    return df.groupby('ticker', group_keys=False).apply(construct_indicators)

def create_stock_chart(data, ticker):
    """Create a Plotly chart for a given stock ticker."""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        subplot_titles=[f'Candlestick with SMA for {ticker}', 'RSI']
    )

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

    for sma in ['sma_10', 'sma_21']:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[sma],
                mode='lines',
                name=f'SMA({sma.split("_")[1]})',
                line=dict(color='green' if sma == 'sma_10' else 'blue', width=1)
            ),
            row=1, col=1
        )

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

    fig.update_layout(
        title=f'OHLC with SMA and Indicators for {ticker}',
        xaxis2_title='Date',
        yaxis=dict(title='OHLC'),
        width=1200,
        height=800,
        yaxis2=dict(title='RSI (0-100)', range=[0, 100]),
        xaxis_rangeslider_visible=False,
        legend=dict(x=0.01, y=0.99)
    )

    return fig

def save_data_to_csv(df, filename):
    """Save data to CSV file, creating the directory if it doesn't exist."""
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_csv(filename, index=False)
