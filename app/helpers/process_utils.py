from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import matplotlib.pyplot as plt

# Take in company of choice, date (starting 10 days earlier) csvFile to read and the trained model
# predict_linear_model("AAPL", '2024-09-11', "stock_data_20240925_121820.csv", model)
def train_portfolio_linear_model(stock_data):
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='%Y-%m-%d')

    #Split dataset by company
    stock_list = stock_data['Symbol'].unique() 
    frames = []
    for stock in stock_list:
        x = stock_data.loc[stock_data['Symbol'] == stock] 
        
        #Shift close price (so the row for 1 Jan 2024 will contain the closing price for 11 Jan 2024)
        x['Close'] = stock_data.Close.shift(-10) 
        # drop last 10 rows 
        x.drop(x.tail(10).index,inplace=True) 
        frames.append(x)
    pref_df = pd.concat(frames)

    train_set = pref_df.loc[(pref_df['Date'] >= '2010-01-01') & (pref_df['Date'] < '2023-01-01')]
    x_train = train_set[['Open','High','Low']]
    y_train = train_set['Close']
    lr = LinearRegression()
    linear_model = lr.fit(x_train, y_train)
    return linear_model

# Take in company of choice, date (starting 10 days earlier) dataframe to read and the trained model
# predict_linear_model("AAPL", '2024-09-11', dataframe, model)
def portfolio_predict_linear_model(company, date, stock_data, model):

    stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='%Y-%m-%d')
    predict_set = stock_data.loc[stock_data['Symbol'] == company]

    predict_set = predict_set[-10:]
    x_predict = predict_set[['Open','High','Low']]

    y_score = model.predict(x_predict)
    begin_date = datetime.today()

    # Add in date to the dataframe for visualising
    resultDf = pd.DataFrame({'Date':pd.bdate_range(begin_date, periods=10), 'Results':y_score}) 
    return(resultDf)

