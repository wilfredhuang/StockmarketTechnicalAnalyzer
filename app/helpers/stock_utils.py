import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Very basic version, just fetches data

def fetch_and_process_stock_data():
    # List of 20 U.S. stocks (you can modify this list)
    stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK-B', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'MA', 'NVDA', 'HD', 'DIS', 'BAC', 'ADBE', 'CRM', 'NFLX']
    
    end_date = datetime.now()  # Current date OR datetime(2024, 1, 1) - 01/01/24
    start_date = end_date - timedelta(days=3652)  # Approximately 10 years
    
    all_data = []
    
    for stock in stocks:
        ticker = yf.Ticker(stock)
        data = ticker.history(start=start_date, end=end_date)
        data['Symbol'] = stock
        all_data.append(data)
    
    combined_data = pd.concat(all_data)
    combined_data.reset_index(inplace=True)
    
    # Ensure datetime column is properly formatted
    combined_data['Date'] = pd.to_datetime(combined_data['Date']).dt.strftime('%Y-%m-%d')
    
    # Save to CSV
    csv_filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    combined_data.to_csv(f"static/data/{csv_filename}", index=False)
    
    return csv_filename


