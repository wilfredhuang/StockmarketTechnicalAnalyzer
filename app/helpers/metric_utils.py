"""
Module Name: metric_utils.py
=============================================

Description:
------------
This module contains functions for analyzing and visualizing stock performance. It provides utilities 
for calculating benchmark buy-and-hold performance, strategy performance metrics, and generating 
interactive price charts using Plotly.

Functions:
----------
1. `benchmark_performance(data: pd.DataFrame, start: str, end: str) -> dict`:
    Computes performance metrics for a buy-and-hold strategy over a given date range.

2. `strategy_performance(data: pd.DataFrame) -> dict`:
    Calculates strategy-specific performance metrics based on trade signals.

3. `visualise_pricechart(df: pd.DataFrame, start: Optional[str], end: Optional[str], 
   ticker: Optional[str], indicators: List[str], signal_marker: bool) -> go.Figure`:
    Generates an interactive price chart with optional indicators and trade signals.

benchmark_performance(data: pd.DataFrame, start: str, end: str) -> dict:
-------------------------------------------------------------------------
Computes various benchmark performance metrics for a buy-and-hold strategy over a specified date range, 
such as cumulative returns, annualized volatility, maximum drawdown, and profit factor.

Parameters:
    data (pd.DataFrame): The stock price data with 'close' prices and a DateTime index.
    start (str): The start date for the analysis (format: 'YYYY-MM-DD').
    end (str): The end date for the analysis (format: 'YYYY-MM-DD').

Returns:
    dict: A dictionary containing the calculated performance metrics like total return, 
    annualized volatility, maximum drawdown, profit factor, etc.

Example Usage:
    performance_dict = benchmark_performance(stock_data, '2023-01-01', '2023-12-31')

strategy_performance(data: pd.DataFrame) -> dict:
-------------------------------------------------
Computes performance metrics for a trading strategy based on trade signals and returns. 
Includes statistics like total trades, profit factor, average profit/loss, and maximum drawdown.

Parameters:
    data (pd.DataFrame): The strategy data, where 'signal' indicates trades (1 for buy, -1 for sell), 
    and 'returns' contains the percentage returns.

Returns:
    dict: A dictionary with performance metrics, including total trades, profit factor, 
    average profit, average loss, maximum drawdown, etc.

Example Usage:
    strategy_perf_dict = strategy_performance(strategy_data)

visualise_pricechart(df: pd.DataFrame, start: Optional[str], end: Optional[str], ticker: Optional[str], 
indicators: List[str], signal_marker: bool) -> go.Figure:
-------------------------------------------------------------------------------------------------
Generates an interactive price chart with candlestick representation and optional technical indicators 
(e.g., SMA, EMA, Bollinger Bands). Optionally, trade signals can be displayed on the chart.

Parameters:
    df (pd.DataFrame): The stock data with columns for 'open', 'high', 'low', 'close', 'rsi_14', etc.
    start (Optional[str]): The start date for the chart (format: 'YYYY-MM-DD').
    end (Optional[str]): The end date for the chart (format: 'YYYY-MM-DD').
    ticker (Optional[str]): The ticker symbol of the stock (if multiple tickers exist in the DataFrame).
    indicators (List[str]): A list of technical indicators to display (options: ['SMA', 'EMA', 'RSI', 'BB']).
    signal_marker (bool): If True, displays markers where trades were made on the price chart.

Returns:
    go.Figure: A Plotly Figure object with the generated price chart and optional indicators.

Example Usage:
    fig = visualise_pricechart(stock_data, '2023-01-01', '2023-12-31', 'AAPL', ['SMA', 'EMA'], signal_marker=True)
    fig.show()

Dependencies:
-------------
- pandas: Used for data manipulation and indexing.
- numpy: For mathematical operations like standard deviation and cumulative returns.
- plotly: Used for generating interactive charts and figures.
- typing: Provides type hints for optional parameters and lists.
"""



from typing import List, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# import warnings
# warnings.filterwarnings("ignore")

def benchmark_performance(data: pd.DataFrame, start: str, end: str):

    df = data.loc[start:end].copy()
    returns = df.close.pct_change().dropna()

    days = len(returns)
    up = (returns > 0).sum()
    down = (returns < 0).sum()

    # returns
    cumulative_rets = (1 + returns).cumprod()
    total_ret = cumulative_rets.iloc[-1] - 1

    # volatility
    daily_vol = returns.std()
    annual_vol = daily_vol * np.sqrt(252)

    # maximum drawdown
    cumulative_peaks = cumulative_rets.cummax()
    drawdowns = (cumulative_rets - cumulative_peaks) / cumulative_peaks
    mdd = drawdowns.min()

    # average P/L
    log_returns = (np.log(df.close) - np.log(df.close.shift(1))).dropna()
    gross_profit = log_returns[log_returns > 0].sum()
    gross_loss = -log_returns[log_returns < 0].sum()
    avg_profit = gross_profit / up
    avg_loss = gross_loss / down

    # profit factor
    pf = gross_profit / gross_loss
    print("======================= BENCHMARK BUY-N-HOLD PERFORMANCE =======================")
    print(f"Trading Days: {days}")
    print(f"'Up' days: {up} ({up/days * 100:.2f}%)")
    print(f"'Down' days: {down} ({down/days * 100:.2f}%)")
    print(f"Total Return: {total_ret * 100:.2f}%")
    print(f"Annualised Volatility: {annual_vol * 100:.2f}%")
    print(f"Maximum Drawdown: {mdd * 100:.2f}%")
    print(f"Profit Factor: {pf:.3f}")
    print(f"Average Profit: {avg_profit:.3f}")
    print(f"Average Loss: {avg_loss:.3f}")


    up_days_percentage = f"{up/days * 100:.2f}"
    down_days_percentage = f"{down/days * 100:.2f}"
    total_return_display = f"{total_ret * 100:.2f}"
    annualised_volatility_display = f"{annual_vol * 100:.2f}"
    maximum_drawdown_display = f"{mdd * 100:.2f}"
    profit_factor_display = f"{pf:.3f}"
    average_profit_display = f"{avg_profit:.3f}"
    average_loss_display = f"{avg_loss:.3f}"

    benchmark_performance_dict = {
        "trade_days": str(days),
        "up_days": str(up),
        "up_days_percentage":up_days_percentage, 
        "down_days":str(down),
        "down_days_percentage":down_days_percentage,
        "total_return": total_return_display,
        "annualised_volatility": annualised_volatility_display,
        "maximum_drawdown": maximum_drawdown_display,
        "profit_factor":profit_factor_display,
        "average_profit":average_profit_display,
        "average_loss_display":average_loss_display
    }

    print(f"Benchmark performance dict = {benchmark_performance_dict}")
    return benchmark_performance_dict

def strategy_peformance(data: pd.DataFrame):
    """
    columns in `data` should contain 'signal' and 'returns'
    'returns': simple return for taking a trade (signal != 0)
    """
    signals = data.signal
    returns = data.returns

    days = len(returns)
    trades = signals.sum()
    up = (returns > 0).sum()
    down = (returns < 0).sum()

    # returns
    cumulative_rets = (1 + returns).cumprod()
    total_ret = cumulative_rets.iloc[-1] - 1

    # volatility
    daily_vol = returns.std()
    annual_vol = daily_vol * np.sqrt(252)

    # maximum drawdown
    cumulative_peaks = cumulative_rets.cummax()
    drawdowns = (cumulative_rets - cumulative_peaks) / cumulative_peaks
    mdd = drawdowns.min()

    # average P/L
    log_returns = np.log(1 + returns)
    gross_profit = log_returns[log_returns > 0].sum()
    gross_loss = -log_returns[log_returns < 0].sum()
    avg_profit = gross_profit / up
    avg_loss = gross_loss / down

    # profit factor
    pf = gross_profit / gross_loss   
    print("=========================== STRATEGY PERFORMANCE ===========================")
    print(f"Trades: {trades}")
    print(f"'Up' days: {up} ({up/trades * 100:.2f}%)")
    print(f"'Down' days: {down} ({down/trades * 100:.2f}%)")
    print(f"Total Return: {total_ret * 100:.2f}%")
    print(f"Annualised Volatility: {annual_vol * 100:.2f}%")
    print(f"Maximum Drawdown: {mdd * 100:.2f}%")
    print(f"Profit Factor: {pf:.3f}")
    print(f"Average Profit: {avg_profit:.3f}")
    print(f"Average Loss: {avg_loss:.3f}")


    up_days_percentage = f"{up/trades * 100:.2f}"
    down_days_percentage = f"{down/trades * 100:.2f}"
    total_return_display = f"{total_ret * 100:.2f}"
    annualised_volatility_display = f"{annual_vol * 100:.2f}"
    maximum_drawdown_display = f"{mdd * 100:.2f}"
    profit_factor_display = f"{pf:.3f}"
    average_profit_display = f"{avg_profit:.3f}"
    average_loss_display = f"{avg_loss:.3f}"

    strat_performance_dict = {
        "trades":str(trades), 
        "up_days":str(up), 
        "up_days_percentage":up_days_percentage, 
        "down_days": str(down),
        "down_days_percentage":down_days_percentage,
        "total_return": total_return_display,
        "annualised_volatility": annualised_volatility_display,
        "maximum_drawdown": maximum_drawdown_display,
        "profit_factor":profit_factor_display,
        "average_profit":average_profit_display,
        "average_loss_display":average_loss_display
    }

    
    print(f"Strategy performance dict = {strat_performance_dict}")

    return strat_performance_dict

def visualise_pricechart(
        df: pd.DataFrame,
        start: Optional[str] = None,
        end: Optional[str] = None,
        ticker: Optional[str] = None,
        indicators: List[str] = None,
        #signal_marker: bool = False,
        buy_sell_01: bool = False,
        buy_sell_02: bool = False,
        buy_sell_03: bool = False,
    ) -> go.Figure:
    """
    indicators can be any of ['SMA', 'EMA', 'RSI', 'ADX', 'Bollinger Band']
    signal_marker: <bool> False for Tab 1: Price Chart, True for Tab 2 to show where the trades were taken on the price chart
    (NOT TO BE CONFUSED WITH STRATEGY PERFORMANCE CHART, TAB 2 SHOWS 2 CHARTS AND 1 TABLE)
    TAB 2, CHART 1: PRICE CHART WITH MARKETS (signal = True)
    TAB 2, CHART 2: STRATEGY PERFORMANCE
    TAB 2, TABLE 1: PERFORMANCE METRICS
    """
    indicators_to_columns = {
        'SMA': ['sma_21', 'sma_50'],
        'EMA': ['ema_21', 'ema_50'],
        # 'RSI': ['rsi_14'], # show by default
        # 'ADX': ['adx_14'],
        'BB': ['bb_5_lb', 'bb_5_ub', 'bb_5_mb'],
    }
    columns = ['open', 'high', 'low', 'close', 'rsi_14']
    # Select ticker from dataframe
    if ticker:
        data = df.xs(ticker, level='ticker').copy()
    else:
        data = df.copy()
    # Using the given date range
    if start and end:
        data = data.loc[start:end]
    # Visualisation: 2 rows, 1 column with shared x-axis(time)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.75, 0.25],  # Relative heights of the subplots
        subplot_titles=[
            f'Price Chart: {ticker}',
            'RSI',
        ]
    )
   
    # Default candlestick representation
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Candlestick'), row=1, col=1
    )
   
    # See which indicator to add
    if indicators:
        for name in indicators:
            cols = indicators_to_columns.get(name, [])
            for c in cols:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[c],
                    mode='lines',
                    name=f"{name}_{c}",
                    line=dict(color='orange', width=1)
                ), row=1, col=1)

    #EMA crossover buy indicator
    if buy_sell_01:
        #data['Crossings'] = 0
        #conditions for indicator
        EMA21_above = ((data['ema_21'] > data['ema_50']) & (data['ema_21'].shift(-1) < data['ema_50'].shift(-1))) #compares both previous value of ema_21 and ema_50 and compare if ema21 is less than ema50 
        EMA21_below = (data['ema_21'] < data['ema_50']) & (data['ema_21'].shift(-1) > data['ema_50'].shift(-1))   #as we just want the indicator to show when it intersects
        data.loc[EMA21_below, 'Crossings'] = -1
        data.loc[EMA21_above, 'Crossings'] = 1

        #plot indicator
        fig.add_trace(go.Scatter(x=data[data['Crossings'] == 1].index, y=data[data['Crossings'] == 1]['ema_21'],
            mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='purple', size=15), showlegend=True))
    
    #ema + RSI buy indicator
    if buy_sell_02:
        #condition for indicator
        data['ema21_abv'] = data['ema_21'] > data['ema_50']
        data['ema21_bel'] = data['ema_21'] < data['ema_50']

        #plot indicator 
        fig.add_trace(go.Scatter(x=data[(data['rsi_14'] < 50) & data['ema21_abv']].index,  y=data[(data['rsi_14'] < 50) & data['ema21_abv']]['close'], 
                                name='Buy', mode='markers', marker=dict(symbol='triangle-up', color='purple', size=15), showlegend=True))
    #rsi_adx buy indicator
    if buy_sell_03:

        #Condition for indicator 
        data['rsi_adx_buy_signal'] = (data['adx_14'] > 30) & (data['rsi_14'] < 45)
        data['rsi_adx_sell_signal'] = (data['adx_14'] > 30) & (data['rsi_14'] > 45) 

        #plot indicator
        fig.add_trace(go.Scatter(x=data[data['rsi_adx_buy_signal']].index, y=data[data['rsi_adx_buy_signal']]['close'], 
                         name='Buy', mode='markers', marker=dict(symbol='triangle-up', color='purple', size=15), showlegend=True))

            
    '''
    if signal_marker:
        trade_signals = go.Scatter(
            x=data[data.signal == 1].index,
            y=data[data.signal == 1]['close'],  
            mode='markers',
            marker=dict(size=5, color='purple', symbol='triangle-up'),
            name='Trade Signal',
        )
        fig.add_trace(trade_signals, row=1, col=1)
    # Add RSI by default
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['rsi_14'],
        mode='lines',
        name='RSI',
        line=dict(color='blue', width=2)
    ), row=2, col=1)
    '''

    # Update layout for the subplots
    fig.update_layout(
        title='',
        xaxis2_title='Date',  # Title for the second subplot's x-axis
        yaxis=dict(title='Price'),
        width=1200,
        height=800,
        yaxis2=dict(title='RSI', range=[0, 100]),  # Set the y-axis range for RSI and ADX
        xaxis_rangeslider_visible=False,  # Hide range slider
        legend=dict(x=0.01, y=0.99)
    )
    # Return the Plotly figure object
    return fig




  