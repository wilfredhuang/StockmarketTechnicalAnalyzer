"""
Module Name: market_utils.py
============================

Description:
------------
This module provides functionality for fetching, processing, and analyzing stock market data. 
It uses various technical indicators to support different trading strategies and visualizations. 
The module includes functions to retrieve historical stock data, add technical indicators, and apply trading strategies such as Exponential Moving Average (EMA) crossover, EMA with Relative Strength Index (RSI), RSI with Average Directional Index (ADX), and a Machine Learning-enhanced indicator strategy.

Functions:
----------
1. `fetch_stock_data(TICKERS, START_DATE, END_DATE) -> None`:
    Fetches historical stock data for the given tickers and saves it to CSV files for further processing.

2. `process_data() -> pd.DataFrame`:
    Processes the raw data to generate technical indicators such as moving averages, RSI, ADX, and Bollinger Bands.

3. `construct_indicators(group: pd.DataFrame) -> pd.DataFrame`:
    Constructs various technical indicators for the given data group, including simple moving averages, exponential moving averages, RSI, ADX, and Bollinger Bands.

4. `log_returns(group: pd.DataFrame, periods: List[int]) -> pd.DataFrame`:
    Calculates daily log returns for the given group.

5. `ema_crossover_strategy(TICKER: str) -> List`:
    Implements an EMA crossover strategy where a signal is generated when the 21-period EMA crosses above the 50-period EMA.

6. `ema_crossover_rsi_strategy(TICKER: str) -> List`:
    Implements an EMA crossover with RSI filter strategy. An additional condition is included where the RSI must be below 50 to generate a buy signal.

7. `rsi_adx_strategy(TICKER: str) -> List`:
    Implements a strategy combining RSI and ADX indicators. A signal is generated when RSI is below 45 and ADX is above 30.

8. `indicator_ml_strategy(TICKER: str) -> List`:
    Uses a machine learning model (RandomForestClassifier) to enhance the EMA crossover strategy by filtering signals based on additional indicator features.

9. `visualise_pricechart() -> None`:
    Generates a price chart with optional indicators for a selected ticker.

Dependencies:
-------------
- numpy: For mathematical calculations.
- pandas: For data manipulation and time-series analysis.
- matplotlib and seaborn: For visualizing strategy performance.
- yfinance: For fetching stock data.
- pandas_ta: For calculating technical indicators.
- plotly: For generating interactive price charts.
- sklearn: For implementing machine learning-based filtering of trading signals.
"""



# === Libraries ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from typing import List

import sys
import os

# Add the path to the folder containing utils.py
sys.path.append(os.path.abspath('../app/helpers'))

# Import utils and reload when necessary
from . import metric_utils
import importlib
importlib.reload(metric_utils)

# Wilfred's Portion

# === Data Retrieval ===
def fetch_stock_data(TICKERS, START_DATE, END_DATE):
    df = yf.download(tickers=TICKERS, interval="1d", start=START_DATE, end=END_DATE, auto_adjust=True, group_by='ticker')
    # reformat for easy read from store
    df = df.stack(level='Ticker')
    df.columns = [s.lower() for s in df.columns]
    df.index.names = [s.lower() for s in df.index.names]
    df.reset_index(inplace=True)

    # download the benchmark data for reference later
    spy = yf.download(tickers='SPY', interval="1d", start=START_DATE, end=END_DATE, auto_adjust=True)
    spy.reset_index(inplace=True)
    spy.columns = [c.lower() for c in spy.columns]
    if not spy.isnull().sum().any():
        spy.to_csv('./app/static/data/spy.csv', index=False)
        print("Saved to data/spy.csv")
    spy = pd.read_csv('./app/static/data/spy.csv', parse_dates=['date'])
    spy.set_index('date', inplace=True)

    # just a performance statistic of buying and holding the S&P 500 for the entire period
    metric_utils.benchmark_performance(spy, START_DATE, END_DATE)
    # === Data Cleaning ===
    df.info()
    df.isnull().sum()
    # format is just a csv file with column names above
    df.to_csv('./app/static/data/ohlcv.csv', index=False)
    print("[helpers/market_utils.py]: Data Fetched! Should see both files downloaded")

# === Data Processing ===
def process_data():
    # load the data into proper format for processing
    df = pd.read_csv('./app/static/data/ohlcv.csv', parse_dates=['date'])
    df.set_index(['date', 'ticker'], inplace=True)
    df.head()
    df_returns = df.groupby('ticker', group_keys=False).apply(log_returns)
    df_indicators = df_returns.groupby('ticker', group_keys=False).apply(contruct_indicators)  # Update the ohlcv.csv with technical indicator data
    print(f"Hello World {df_indicators}")
    return df_indicators

# === Calculate Indicators ===
def contruct_indicators(group):
    # indicator: Simple Moving Averages
    group['sma_5'] = ta.sma(group['close'], length=5)
    group['sma_10'] = ta.sma(group['close'], length=10)
    group['sma_21'] = ta.sma(group['close'], length=21)
    group['sma_50'] = ta.sma(group['close'], length=50)
    group['sma_100'] = ta.sma(group['close'], length=100)
    group['sma_200'] = ta.sma(group['close'], length=200)

    # indicator: Exponential Moving Averages
    group['ema_5'] = ta.ema(group['close'], length=5)
    group['ema_10'] = ta.ema(group['close'], length=10)
    group['ema_21'] = ta.ema(group['close'], length=21)
    group['ema_50'] = ta.ema(group['close'], length=50)
    group['ema_100'] = ta.ema(group['close'], length=100)
    group['ema_200'] = ta.ema(group['close'], length=200)

    # indicator: normalized volume
    group['norm_volume_3'] = group['volume'] / group['volume'].rolling(3).median()
    group['norm_volume_5'] = group['volume'] / group['volume'].rolling(5).median()
    group['norm_volume_10'] = group['volume'] / group['volume'].rolling(10).median()
    group['norm_volume_21'] = group['volume'] / group['volume'].rolling(21).median()
    group['norm_volume_50'] = group['volume'] / group['volume'].rolling(50).median()

    # indicator: Relative Strength Index
    group['rsi_7'] = ta.rsi(group['close'], length=7)
    group['rsi_9'] = ta.rsi(group['close'], length=9)
    group['rsi_10'] = ta.rsi(group['close'], length=10)
    group['rsi_14'] = ta.rsi(group['close'], length=14)
    

    # indicator: Average Directional Index
    adx_result = ta.adx(group['high'], group['low'], group['close'], length=3)
    group['adx_3'] = adx_result['ADX_3']
    group['+DI_3'] = adx_result['DMP_3']  # +DI
    group['-DI_3'] = adx_result['DMN_3']  # -DI

    adx_result = ta.adx(group['high'], group['low'], group['close'], length=5)
    group['adx_5'] = adx_result['ADX_5']
    group['+DI_5'] = adx_result['DMP_5']  # +DI
    group['-DI_5'] = adx_result['DMN_5']  # -DI

    adx_result = ta.adx(group['high'], group['low'], group['close'], length=7)
    group['adx_7'] = adx_result['ADX_7']
    group['+DI_7'] = adx_result['DMP_7']  # +DI
    group['-DI_7'] = adx_result['DMN_7']  # -DI

    adx_result = ta.adx(group['high'], group['low'], group['close'], length=14)
    group['adx_14'] = adx_result['ADX_14']
    group['+DI_14'] = adx_result['DMP_14']  # +DI
    group['-DI_14'] = adx_result['DMN_14']  # -DI

    # indicator: Bollinger Bands
    bband_result = ta.bbands(group['close'])
    group['bb_5_lb'] = bband_result['BBL_5_2.0']
    group['bb_5_mb'] = bband_result['BBM_5_2.0']
    group['bb_5_ub'] = bband_result['BBU_5_2.0']
    group['bb_5_bw'] = bband_result['BBB_5_2.0']
    group['bb_5_p'] = bband_result['BBP_5_2.0']

    group['Crossings'] = 0

    return group

def log_returns(group, periods=[1]):
    # daily log return
    group['log_return'] = np.log(group['close']) -  np.log(group['close'].shift(1))
    return group

# === ===

# === Data Analysis / Visualisation ===
# Strategy One
# def ema_crossover_strategy(TICKER,DEFAULT_COLUMNS,K):
def ema_crossover_strategy(TICKER):
    df_indicators = process_data()
    data = df_indicators.xs(level='ticker', key=TICKER)
    DEFAULT_COLUMNS = ['open', 'high', 'low', 'close']
    # required indicators
    strategy = data[DEFAULT_COLUMNS + ['rsi_14', 'log_return','ema_21', 'ema_50']].dropna().copy()
    # strategy signal
    strategy['signal'] = (strategy ['ema_21'] > strategy['ema_50']).astype(np.int32)
    strategy['2d_log_return'] = strategy['log_return'].rolling(2).sum()
    strategy['3d_log_return'] = strategy['log_return'].rolling(3).sum()
    strategy['4d_log_return'] = strategy['log_return'].rolling(4).sum()
    strategy['5d_log_return'] = strategy['log_return'].rolling(5).sum()
    strategy['7d_log_return'] = strategy['log_return'].rolling(7).sum()
    strategy['10d_log_return'] = strategy['log_return'].rolling(10).sum()
    strategy.dropna(inplace=True)
    K = 7 # can change the number here as desired
    strategy['target'] = strategy[f'{K}d_log_return'].shift(-K)  
    strategy.dropna(inplace=True)
    strategy['log_returns'] = (strategy['signal'] * strategy['target'])
    strategy['returns'] = np.exp(strategy.log_returns) - 1
    # print the performance statistic of the strategy and the buy-and-hold
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    benchmark_performance_stat = metric_utils.benchmark_performance(data, start_date, end_date)
    strategy_performance_stat = metric_utils.strategy_peformance(strategy.loc[start_date:end_date])
    
    # visualize the performance of the strategy
    plt.switch_backend('Agg')  # Use non-interactive backend
    ax = (strategy.loc[start_date:end_date].returns + 1).cumprod().plot(kind='line', label='EMA Crossover', title='Strategy Performances', ylabel='Total Return (multiples)', figsize=(10,6))
    (np.exp(strategy.loc[start_date:end_date].log_return.cumsum())).plot(kind='line', label='Buy and Hold', grid=True, ax=ax)
    ax.xaxis.set_major_locator(mdates.YearLocator())  # set ticks for each year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # format of the year label
    plt.legend(loc='upper left');
    plt.savefig(os.path.join('./app/static/data', 'plot_strategy_ema.png'))
    plt.close()

    # Price Chart
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    price_chart = metric_utils.visualise_pricechart(strategy, start=start_date, end=end_date, indicators=['EMA'], buy_sell_01=True)

    return [benchmark_performance_stat, strategy_performance_stat, price_chart]

# Strategy Two
# def ema_crossover_strategy(TICKER,DEFAULT_COLUMNS,K, RSI_K):
def ema_crossover_rsi_strategy(TICKER):
    df_indicators = process_data()
    data = df_indicators.xs(level='ticker', key=TICKER)
    
    DEFAULT_COLUMNS = ['open', 'high', 'low', 'close']
    # required indicators
    strategy = data[DEFAULT_COLUMNS + 
        [
            'volume', 'log_return',
            'ema_5', 'ema_10','ema_21', 'ema_50',
            'rsi_7', 'rsi_9', 'rsi_10', 'rsi_14',
        ]
    ].dropna()

    K = 7 # using the same K=7 as before
    RSI_K = 14

    # strategy idea
    # by adding more indicators as a filters, we should expect lesser trades and perhaps less volatility than previous strategy
    strategy['signal'] = (
        (strategy['ema_21'] > strategy['ema_50']) & 
        (strategy[f'rsi_{RSI_K}'] < 50)
    ).astype(np.int32)

    strategy['target'] = strategy['log_return'].rolling(K).sum().shift(-K)
    strategy.dropna(inplace=True)
    strategy['log_returns'] = (strategy['signal'] * strategy['target'])
    strategy['returns'] = np.exp(strategy.log_returns) - 1
    # print the performance statistic of the strategy and the buy-and-hold
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    benchmark_performance_stat = metric_utils.benchmark_performance(data, start_date, end_date)
    strategy_performance_stat = metric_utils.strategy_peformance(strategy.loc[start_date:end_date])
    # visualize the performance of the strategy
    plt.switch_backend('Agg')  # Use non-interactive backend
    ax = (strategy.loc[start_date:end_date].returns + 1).cumprod().plot(kind='line', label='EMA Crossover + RSI', title='Strategy Performances', ylabel='Total Return (multiples)', figsize=(10,6))
    (np.exp(strategy.loc[start_date:end_date].log_return.cumsum())).plot(kind='line', label='Buy and Hold', grid=True, ax=ax)
    ax.xaxis.set_major_locator(mdates.YearLocator())  # set ticks for each year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # format of the year label
    plt.legend(loc='upper left');
    plt.savefig(os.path.join('./app/static/data', 'plot_strategy_ema_rsi.png'))
    plt.close()

    # Price Chart
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    price_chart = metric_utils.visualise_pricechart(strategy, start=start_date, end=end_date, indicators=['EMA'], buy_sell_02=True)

    return [benchmark_performance_stat, strategy_performance_stat, price_chart]


    
# def rsi_adx_strategy(TICKER,DEFAULT_COLUMNS,K, RSI_K, ADX_K)):
def rsi_adx_strategy(TICKER):
    df_indicators = process_data()
    data = df_indicators.xs(level='ticker', key=TICKER)
    DEFAULT_COLUMNS = ['open', 'high', 'low', 'close']
    # required indicators
    strategy = data[DEFAULT_COLUMNS + 
        [
            'volume', 'log_return',
            'rsi_7', 'rsi_9', 'rsi_10', 'rsi_14',
            'adx_3', 'adx_5', 'adx_7', 'adx_14', 
            'ema_10', 'ema_21', 'ema_50'

        ]
    ].dropna()

    K = 7 # using the same K=7 as before
    RSI_K = 14
    ADX_K = 14

    # strategy idea
    # by adding more indicators as a filters, we should expect lesser trades and perhaps less volatility
    strategy['signal'] = (
        (strategy[f'rsi_{RSI_K}'] < 45) &
        (strategy[f'adx_{ADX_K}'] > 30)
    ).astype(np.int32)

    strategy['target'] = strategy['log_return'].rolling(K).sum().shift(-K)
    strategy.dropna(inplace=True)
    strategy['log_returns'] = (strategy['signal'] * strategy['target'])
    strategy['returns'] = np.exp(strategy.log_returns) - 1
    # print the performance statistic of the strategy and the buy-and-hold
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    benchmark_performance_stat = metric_utils.benchmark_performance(data, start_date, end_date)
    strategy_performance_stat = metric_utils.strategy_peformance(strategy.loc[start_date:end_date])
    # visualize the performance of the strategy
    plt.switch_backend('Agg')  # Use non-interactive backend
    ax = (strategy.loc[start_date:end_date].returns + 1).cumprod().plot(kind='line', label='EMA Crossover', title='Strategy Performances', ylabel='Total Return (multiples)', figsize=(10,6))
    (np.exp(strategy.loc[start_date:end_date].log_return.cumsum())).plot(kind='line', label='Buy and Hold', grid=True, ax=ax)
    ax.xaxis.set_major_locator(mdates.YearLocator())  # set ticks for each year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # format of the year label
    plt.legend(loc='upper left');
    plt.savefig(os.path.join('./app/static/data', 'plot_strategy_rsi_adx.png'))
    plt.close()

    # Price Chart
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    chart_url = metric_utils.visualise_pricechart(strategy, start=start_date, end=end_date, indicators=['EMA'], buy_sell_03=True)

    return [benchmark_performance_stat, strategy_performance_stat, chart_url]


# === Analysis + Prediction Strategy ===
# def indicator_ml_strategy(TICKER, K, RSI_K, TRAIN_END, TEST_PERIOD_WEEKS, TEST_START, FEATURES):
def indicator_ml_strategy(TICKER):
    df_indicators = process_data()
    data = df_indicators.xs(level='ticker', key=TICKER)
    DEFAULT_COLUMNS = ['open', 'high', 'low', 'close']
    strategy = data[DEFAULT_COLUMNS +
        [
            'log_return',
            'ema_5', 'ema_10', 'ema_21','ema_50',
            'rsi_14',
            'adx_14',
            'norm_volume_5','norm_volume_10','norm_volume_21',
            'bb_5_lb', 'bb_5_ub', 'bb_5_mb', 'bb_5_bw', 'bb_5_p'
        ]
    ].dropna()

    strategy['x1'] = strategy['bb_5_ub'] - strategy['close']
    strategy['x2'] = strategy['close'] - strategy['bb_5_mb']
    strategy['x3'] = strategy['close'] - strategy['bb_5_lb'] 
    strategy['x4'] = strategy['close'] - strategy['ema_10']
    strategy['x5'] = strategy['ema_10'] - strategy['ema_21']
    strategy['x6'] = strategy['ema_21'] - strategy['ema_50']

    # create target variable to predict - idea is that since the default strategy would not be 100% accurate
    # we will use the machine learning model to learn and filter out the signals using information from other indicators
    K = 7 # using the same K=7 as before
    RSI_K = 14

    strategy['signal'] = (
        strategy['ema_21'] > strategy['ema_50']
    ).astype(np.int32)
    strategy['returns'] = np.exp(strategy['signal'] * strategy['log_return'].rolling(K).sum().shift(-K)) - 1
    strategy.dropna(inplace=True)

    dataset = strategy[strategy.signal == 1].copy()
    dataset['target'] = (dataset.returns > 0).astype(np.int32)

    # train-test split

    # We will use data from December 2013 to December 2022 as the training period (9 years of training data).
    # After the training period, we will apply a buffer period of 3 months (12 weeks) between training and testing sets.
    # This waiting period is suitable for our shorter-term strategies, which have a 7-day holding period.
    # Finally, the test period will start after the waiting period, i.e., from March 2023 onwards, until the current date.
    TRAIN_END = '2022-12-31' # define last period of training date
    TEST_PERIOD_WEEKS = 12 # Buffer Period
    TEST_START = str((pd.to_datetime(TRAIN_END) + pd.Timedelta(value=TEST_PERIOD_WEEKS, unit='W')).date())
    train = dataset.loc[:TRAIN_END] # Data from the start until the end of the training period
    test = dataset.loc[TEST_START:] # Data from the beginning of the test period (after the buffer) until the current date

    # train the model 
    FEATURES = ['rsi_14', 'adx_14', 'bb_5_bw', 'bb_5_p','norm_volume_5', 'norm_volume_10','x1', 'x2', 'x3', 'x4', 'x5', 'x6']
    train_X, train_y = train[FEATURES], train['target']
    model = RandomForestClassifier() # instantiate the model 
    model.fit(train_X, train_y) # this api call trains the model

    # evaluate the model accuracy
    test_X, test_y = test[FEATURES], test['target']
    y_pred = model.predict(test_X)
    acc = accuracy_score(test_y, y_pred)
    f1 = f1_score(test_y, y_pred)

    print(f"Model Accuracy: {acc*100:.2f}%")
    # print(f"Model F1-Score: {f1:.2f}")

    # strategy performance using the model
    # notice the large decrease in maximum drawdown, the model was able to filter our drastic false signals
    # winning rate has also improved a lot
    out_of_sample_with_model = strategy[strategy.signal == 1].loc[TEST_START:].copy()
    out_of_sample_with_model['signal'] = y_pred
    out_of_sample_with_model = out_of_sample_with_model[out_of_sample_with_model.signal == 1]
    strategy_peformance_stat = metric_utils.strategy_peformance(out_of_sample_with_model)
    # without using model
    out_of_sample_without_model = strategy[strategy.signal == 1].loc[TEST_START:]


    spy = pd.read_csv('./app/static/data/spy.csv', parse_dates=['date'])
    spy.set_index('date', inplace=True)

    benchmark_performance_stat = metric_utils.benchmark_performance(spy, '2023-03-25', '2024-07-25') # and we kind of beat the index as well
    # visualize the performance of the strategy using model - notice the fewer sharp drops throughout the period
    plt.switch_backend('Agg')  # Use non-interactive backend
    (out_of_sample_with_model.returns + 1).cumprod().plot(kind='line', grid=True, title='Strategy Performance', figsize=(10,6));
    plt.savefig(os.path.join('./app/static/data', 'plot_strategy_ml_indicator.png'))
    plt.close()
    # Strategy comparison
    ax = (out_of_sample_without_model.returns + 1).cumprod().plot(kind='line', label='Strategy 1: EMA Crossover', title='Strategy Performances', ylabel='Total Return (multiples)', figsize=(10,6))
    (out_of_sample_with_model.returns + 1).cumprod().plot(kind='line', label='Strategy 4: Strategy 1 + ML Filter', grid=True, ax=ax)
    # ax.xaxis.set_major_locator(mdates.YearLocator())  # set ticks for each year
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # format of the year label
    plt.legend(loc='upper left');
    plt.savefig(os.path.join('./app/static/data', 'plot_strategy_ml_indicator_comparison.png'))
    plt.close()

     # Price Chart
    strategy['signal'] = 0
    for datetime in out_of_sample_with_model.index:
        strategy.at[datetime, 'signal'] = 1
    chart_url = metric_utils.visualise_pricechart(strategy, start=str(test.index[0].date()), end=str(test.index[-1].date()), indicators=[], signal_marker=True)


    return [benchmark_performance_stat, strategy_peformance_stat, chart_url]