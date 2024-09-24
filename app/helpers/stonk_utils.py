# DC
import yfinance as yf
import pandas as pd
# DA
import pandas_ta as ta
# DV
import matplotlib.pyplot as plt
import plotly.express as px
# ML
from sklearn.metrics import mean_squared_error
# SVM
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# Random Forest
from sklearn.ensemble import RandomForestRegressor
# Logistics Regression
from sklearn.linear_model import LogisticRegression

# Step 0
def sampleFunc():
    print("Hello World")
    return None

# Step 1
def fetch_stock_data(tickers, period='10y', save_path='../static/data/ohlcv_stock_data.csv'):
    data_frames = []
    tickers = [
    'XOM', 'CVX',    # Energy
    'DOW', 'DD',     # Materials
    'GE', 'CAT',     # Industrials
    'TSLA', 'HD',    # Consumer Discretionary
    'PG', 'KO',      # Consumer Staples
    'JNJ', 'PFE',    # Healthcare
    'JPM', 'GS',     # Financials
    'AAPL', 'MSFT',  # Information Technology
    'GOOGL', 'DIS',  # Communication Services
    'NEE', 'DUK',    # Utilities
    'AMT', 'PLD'     # Real Estate
]
    for ticker in tickers:
        stock_data = yf.download(ticker, period=period)
        stock_data['Ticker'] = ticker  # Add stock ticker for identification
        data_frames.append(stock_data)
    
    combined_df = pd.concat(data_frames)
    combined_df.to_csv(save_path)
    return combined_df

# Step 2
def clean_stock_data(data_path='../static/data/ohlcv_stock_data.csv'):
    df = pd.read_csv(data_path)
    df = df.dropna()  # Remove rows with missing data
    df.to_csv(data_path, index=False)  # Save cleaned data
    return df

# Step 3
def calculate_indicators(df):
    indicators = {
        'SMA': df.ta.sma(length=50),  # Simple Moving Average
        'EMA': df.ta.ema(length=50),  # Exponential Moving Average
        'RSI': df.ta.rsi(),           # Relative Strength Index
        'MACD': df.ta.macd(),         # Moving Average Convergence Divergence
        'BB': df.ta.bbands(),         # Bollinger Bands
        'ADX': df.ta.adx()            # Average Directional Index
    }
    
    for key, value in indicators.items():
        df = pd.concat([df, value], axis=1)
    
    return df

# Step 4
def analyze_trends(df):
    trend_statements = []
    
    if df['Close'].iloc[-1] > df['SMA'].iloc[-1]:
        trend_statements.append("The stock is in an uptrend as the price is above the SMA.")
    else:
        trend_statements.append("The stock is in a downtrend as the price is below the SMA.")
    
    if df['RSI'].iloc[-1] > 70:
        trend_statements.append("The stock is overbought according to RSI.")
    elif df['RSI'].iloc[-1] < 30:
        trend_statements.append("The stock is oversold according to RSI.")
    
    # More conditions for other indicators (MACD, Bollinger Bands, etc.)
    
    return trend_statements

# Step 5
def predict_stocks(df):
    # Example of a simple method using moving averages to predict rise
    df['MA_diff'] = df['EMA'] - df['SMA']
    df['Prediction'] = df['MA_diff'].apply(lambda x: 'Buy' if x > 0 else 'Sell')
    
    # Ranking stocks based on "Buy" signals
    ranked_stocks = df[df['Prediction'] == 'Buy'].sort_values(by='MA_diff', ascending=False)
    
    return ranked_stocks[['Ticker', 'MA_diff']].head(10)  # Top 10 stocks to consider


# Step 6
def plot_stock_data(df, ticker, dynamic=False):
    stock_df = df[df['Ticker'] == ticker]

    if dynamic:
        fig = px.line(stock_df, x=stock_df.index, y='Close', title=f'{ticker} Stock Price')
        return fig.to_html()
    else:
        plt.figure(figsize=(10,6))
        plt.plot(stock_df.index, stock_df['Close'], label='Close Price')
        plt.title(f'{ticker} Stock Price')
        plt.legend()
        plt.savefig(f'static/{ticker}_stock.png')  # Save the plot as an image
        return f'static/{ticker}_stock.png'
    
# Step 7
def test_predictions(df, tickers):
    accuracy_scores = {}
    
    for ticker in tickers:
        stock_df = df[df['Ticker'] == ticker]
        train_data = stock_df[:-365]  # First 9 years
        test_data = stock_df[-365:]   # Last 1 year
        
        # Assume we have a function to make predictions (e.g., using moving averages)
        predicted = train_data['EMA'][-365:]  # Example prediction using EMA
        
        mse = mean_squared_error(test_data['Close'], predicted)
        accuracy_scores[ticker] = mse
    
    return accuracy_scores

# Step 8
def validate_data(df):
    assert not df.isnull().values.any(), "Data contains missing values!"
    assert len(df) > 0, "No data found!"
    return "Data validation passed!"

# Step 9
def svm_stock_prediction(df):
    # Preparing data
    features = df[['SMA', 'EMA', 'RSI', 'MACD_hist', 'BB_upper', 'BB_lower', 'ADX']]
    df['Label'] = (df['Close'].shift(-1) > df['Close']).astype(int)  # Binary label: stock rise or fall
    labels = df['Label']

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train SVM model
    model = SVC()
    model.fit(X_train, y_train)

    # Predict stock movements
    predictions = model.predict(X_test)
    return predictions, y_test


# Step 10
def random_forest_stock_prediction(df):
    # Prepare features and labels
    features = df[['SMA', 'EMA', 'RSI', 'MACD_hist', 'BB_upper', 'BB_lower', 'ADX']]
    labels = df['Close'].shift(-1)  # Next day’s closing price

    # Drop missing labels (NaN values after shifting)
    df = df.dropna()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict stock prices
    predictions = model.predict(X_test)

    # Calculate accuracy (e.g., using mean squared error or R²)
    mse = mean_squared_error(y_test, predictions)
    r2 = model.score(X_test, y_test)

    return predictions, mse, r2


# Step 11
def logistic_regression_prediction(df):
    # Preparing data
    features = df[['SMA', 'EMA', 'RSI', 'MACD_hist', 'BB_upper', 'BB_lower', 'ADX']]
    df['Label'] = (df['Close'].shift(-1) > df['Close']).astype(int)  # Binary label: stock rise or fall
    labels = df['Label']

    # Drop missing values
    df = df.dropna()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict stock movements
    predictions = model.predict(X_test)

    return predictions, model.score(X_test, y_test)  # Return predictions and accuracy