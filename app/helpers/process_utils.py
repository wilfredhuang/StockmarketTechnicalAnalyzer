from typing import List
import pandas as pd

def load_data(tickers: List[str]) -> pd.DataFrame:
    pass

def visualize(ticker, indicators: List[str]):
    pass

def compute_indicators(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    pass

def rank_stocks(tickers: pd.DataFrame) -> pd.DataFrame:
    # TO DO: logic to rank the stocks according to some rule using information from the indicators
    # returns the tickers and their ranking 1 to N
    # to be shown to user as a suggestion
    pass

def test_stocks(tickers: List[str]) -> pd.DataFrame:
    # using the tickers that the user has chosen
    # mimic what happened if the user had bought/traded them (testing with the last one year data)
    # uses the backtest function
    pass

def backtest(tickers: pd.DataFrame):
    pass

# to be confirmed
def predict(df: pd.DataFrame):
    pass

