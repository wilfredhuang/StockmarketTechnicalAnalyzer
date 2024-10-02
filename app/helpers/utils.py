import numpy as np
import pandas as pd
# import warnings
# warnings.filterwarnings("ignore")

# For Notebook v3

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
  