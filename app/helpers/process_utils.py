from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import matplotlib.pyplot as plt


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

    #Split dataset by company
    stock_list = df['Symbol'].unique() 
    frames = []
    for stock in stock_list:
        x = df.loc[df['Symbol'] == stock] 
        
        #Shift close price (so the row for 1 Jan 2024 will contain the closing price for 11 Jan 2024)
        x['Close'] = df.Close.shift(-10) 
        # drop last 10 rows 
        x.drop(x.tail(10).index,inplace=True) 
        frames.append(x)
    pref_df = pd.concat(frames)


    train_set = pref_df.loc[(pref_df['Date'] >= '2010-01-01') & (pref_df['Date'] < '2023-01-01')]
    x_train = train_set[['Open','High','Low','Volume']]
    y_train = train_set['Close']
    lr = LinearRegression()
    linear_model = lr.fit(x_train, y_train)
    return linear_model

# Take in company of choice, date (starting 10 days earlier) csvFile to read and the trained model
# predict_linear_model("AAPL", '2024-09-11', "stock_data_20240925_121820.csv", model)
def predict_linear_model(company, date, csvFile, model):

    df = pd.read_csv(f"app/static/data/{csvFile}")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    predict_set = df.loc[df['Symbol'] == company]

    # Filter for historical data up to the previous day
    historical_set = predict_set[-20:]
    historical_set = historical_set[['Date','Close']]

    predict_set = predict_set[-10:]
    x_predict = predict_set[['Open','High','Low','Volume']]

    y_score = model.predict(x_predict)
    begin_date = datetime.today()

    # Add in date to the dataframe for visualising
    resultDf = pd.DataFrame({'Date':pd.bdate_range(begin_date, periods=10), 'Results':y_score}) 
    return(resultDf, historical_set)

def test_linear_model(company, date, csvFile, model):
    df = pd.read_csv(f"app/static/data/{csvFile}")
    test_set = df.loc[df['Symbol'] == company]
    test_set['Date'] = pd.to_datetime(test_set['Date'], format='%Y-%m-%d') 
    test_set['FutureClose'] = test_set.Close.shift(-10) 
    test_set.drop(test_set.tail(10).index,inplace=True)    
    test_set = test_set.loc[test_set['Date'] >= date]
    x_test = test_set[['Open','High','Low','Volume']]
    y_test = test_set['FutureClose']
    y_score = model.score(x_test,y_test)
    yPredict = model.predict(x_test)
    plt.figure(figsize=(20,6))
    plt.plot(test_set['Date'],y_test) 
    plt.plot(test_set['Date'],yPredict)
    plt.plot(test_set['Date'],test_set['Close'])
    plt.legend(['Future Price','Predicted Price','Actual Price'])
    plt.title('Predicted Closing Price of Apple 10 days ahead')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()
    pass

# model = train_linear_model('stock_data_20240925_124231.csv')
# predictions = predict_linear_model('AAPL','2023-08-02','stock_data_20240925_124231.csv', model)

