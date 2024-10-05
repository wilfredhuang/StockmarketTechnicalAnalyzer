from typing import List, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    # strat_performance_dict = {
    #     "trades":{trades}, 
    #     "up_days":{up}, 
    #     "up_days_percentage":{up_days_percentage}, 
    #     "down_days": {down},
    #     "down_days_percentage":down_days_percentage,
    #     "total_return": total_return_display,
    #     "annualised_volatility": annualised_volatility_display,
    #     "maximum_drawdown": maximum_drawdown_display,
    #     "profit_factor":profit_factor_display,
    #     "average_profit":average_profit_display,
    #     "average_loss_display":average_loss_display
    # }

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
        signal_marker: bool = False
    ):
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

    # select ticker from dataframe
    if ticker:
        data = df.xs(ticker, level='ticker').copy()
    else:
        data = df.copy()
    # using the given date range
    if start and end:
        data = data.loc[start:end]

    # visualisation: 2 rows, 1 column with shared x-axis(time)
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
    # default candlestick representation
    fig.add_trace(go.Candlestick(x=data.index, open=data['open'], high=data['high'], low=data['low'], close=data['close'], name='Candlestick'), row=1, col=1)
    
    # see which indicator to add
    for name in indicators:
        cols = indicators_to_columns[name]
        for c in cols:
            fig.add_trace(go.Scatter(x=data.index, y=data[c], mode='lines', name=f"{name}_{c}", line=dict(color='orange', width=1)), row=1, col=1)

    if signal_marker:
        trade_signals = go.Scatter(
            x=data[data.signal == 1].index, 
            y=data[data.signal == 1]['close'],  
            mode='markers',
            marker=dict(size=5, color='purple', symbol='triangle-up'),
            name='Trade Signal',
        )
        fig.add_trace(trade_signals, row=1, col=1)

    # add RSI by default
    fig.add_trace(go.Scatter(x=data.index, y=data['rsi_14'], mode='lines', name='RSI', line=dict(color='blue', width=2)), row=2, col=1)

    # update layout for the subplots
    fig.update_layout(
        title=f'',
        xaxis2_title='Date',  # Title for the second subplot's x-axis
        yaxis=dict(title='Price'),
        width=1200,
        height=800,
        yaxis2=dict(title='RSI', range=[0, 100]),  # Set the y-axis range for RSI and ADX
        xaxis_rangeslider_visible=False,  # Hide range slider
        legend=dict(x=0.01, y=0.99)
    )
    fig.show()


  