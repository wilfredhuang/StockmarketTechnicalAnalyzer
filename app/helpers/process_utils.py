from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# import matplotlib.pyplot as plt

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

def train_linear_model(csvFile):
    df = pd.read_csv(f"app/static/data/{csvFile}")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    
    stockList = df['Symbol'].unique() #Split dataset by company
    frames = []
    for stock in stockList:
        x = df.loc[df['Symbol'] == stock] 
        x['Close'] = df.Close.shift(-10) #Shift close price (so the row for 1 Jan 2024 will contain the closing price for 11 Jan 2024)
        x.drop(x.tail(10).index,inplace=True) # drop last 10 rows
        frames.append(x)
    prepDf = pd.concat(frames)

    trainSet = prepDf.loc[(prepDf['Date'] >= '2010-01-01') & (prepDf['Date'] < '2023-01-01')]
    xTrain = trainSet[['Open','High','Low','Volume']]
    yTrain = trainSet['Close']
    lr = LinearRegression()
    linearModel = lr.fit(xTrain, yTrain)
    return linearModel

# Take in company of choice, date (starting 10 days earlier) csvFile to read and the trained model
# predict_linear_model("AAPL", '2024-09-11', "stock_data_20240925_121820.csv", model)
def predict_linear_model(company, date, csvFile, model):

    df = pd.read_csv(f"app/static/data/{csvFile}")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    predictSet = df.loc[df['Symbol'] == company]
    predictSet = predictSet.loc[predictSet['Date'] >= date]
    xPredict = predictSet[['Open','High','Low','Volume']]

    yScore = model.predict(xPredict)

    beginDate = datetime.now()
    resultDf = pd.DataFrame({'Date':pd.date_range(beginDate, periods=10), 'Results':yScore}) # <- This is wrong since it dosent take into account weekends
    
    return(resultDf)

def test_linear_model(company, date, csvFile, model):
    df = pd.read_csv(f"app/static/data/{csvFile}")

    testSet = df.loc[df['Symbol'] == company]
    testSet['Date'] = pd.to_datetime(testSet['Date'], format='%Y-%m-%d') 
    testSet['Close'] = testSet.Close.shift(-10) 
    testSet.drop(testSet.tail(10).index,inplace=True)    
    testSet = testSet.loc[testSet['Date'] >= date]

    xTest = testSet[['Open','High','Low','Volume']]
    yTest = testSet['Close']
    print(f'{model.score(xTest,yTest)}\n-----------------')
    pass
