import yfinance as yf
from datetime import datetime

def validate_ticker_list(ticker_list):
    # Split ticker_list by commas and strip extra spaces
    tickers = [ticker.strip() for ticker in ticker_list.split(',')]
    
    # Check if the number of tickers exceeds 30
    if len(tickers) > 30:
        return False, "The list contains more than 30 ticker symbols, which is not allowed."
    
    invalid_tickers = []
    
    for ticker in tickers:
        # Validate each ticker using yfinance
        try:
            stock = yf.Ticker(ticker)
            # Check if the ticker has any historical data (if it's a valid symbol)
            if stock.history(period='1d').empty:
                invalid_tickers.append(ticker)
        except Exception as e:
            invalid_tickers.append(ticker)
    
    if invalid_tickers:
        return False, f"Invalid tickers: {', '.join(invalid_tickers)}"
    
    return True, "All tickers are valid."

def validate_dates(start_date, end_date):
    # Check if the date format is correct and valid
    date_format = "%Y-%m-%d"
    try:
        start_dt = datetime.strptime(start_date, date_format)
        end_dt = datetime.strptime(end_date, date_format)
        current_dt = datetime.now()
        
        # Ensure start_date is not later than end_date
        if start_dt > end_dt:
            return False, "Start date cannot be later than end date."
        
        # Ensure dates are not later than current date
        if start_dt > current_dt or end_dt > current_dt:
            return False, "Dates cannot be in the future."
    except ValueError:
        return False, "Invalid date format. Please use 'YYYY-MM-DD'."
    
    return True, "Dates are valid."