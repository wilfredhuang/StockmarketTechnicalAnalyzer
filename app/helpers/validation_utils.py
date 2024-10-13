
"""
Module Name: validation_utils.py
==========================================

Description:
------------
This module provides validation functions for a list of stock ticker symbols and date ranges. 
It uses the yfinance library to check if the given stock tickers are valid by ensuring they have historical data. 
Additionally, it validates start and end dates to ensure they are in the correct format and logical order.

Functions:
----------
- `validate_ticker_list(ticker_list)`: Validates a list of stock ticker symbols.
- `validate_dates(start_date, end_date)`: Validates the given start and end dates.

validate_ticker_list(ticker_list):
---------------------------------
Validates a comma-separated list of stock ticker symbols. It ensures that the list does not exceed 
30 symbols and checks each ticker symbol's validity using yfinance.

Parameters:
    ticker_list (str): A comma-separated string of stock ticker symbols.

Returns:
    tuple: A tuple containing:
        - (bool): True if all tickers are valid, False otherwise.
        - (str): A message indicating the validation result. If invalid tickers are found, they are listed.

Example Usage:
    is_valid, message = validate_ticker_list('AAPL, MSFT, GOOG')
    if is_valid:
        print("Ticker list is valid")
    else:
        print(f"Validation failed: {message}")

validate_dates(start_date, end_date):
-----------------------------------
Validates the given start and end dates. It ensures that the dates are in the correct format ('YYYY-MM-DD'), 
the start date is not later than the end date, and both dates are not in the future.

Parameters:
    start_date (str): The start date in 'YYYY-MM-DD' format.
    end_date (str): The end date in 'YYYY-MM-DD' format.

Returns:
    tuple: A tuple containing:
        - (bool): True if the dates are valid, False otherwise.
        - (str): A message indicating the validation result.

Example Usage:
    is_valid, message = validate_dates('2023-01-01', '2023-12-31')
    if is_valid:
        print("Dates are valid")
    else:
        print(f"Validation failed: {message}")

Dependencies:
-------------
- yfinance: Used to validate ticker symbols by checking their historical data.
- datetime: Used to parse and validate dates.
"""


import yfinance as yf
from datetime import datetime




def validate_ticker_list(ticker_list):
    # Split ticker_list by commas and strip extra spaces
    tickers = [ticker.strip() for ticker in ticker_list.split(',')]
    # Check if the number of tickers exceeds 30
    if len(tickers) > 30:
        return False, "The list contains more than 30 ticker symbols, which is not allowed." # this can be adjusted for higher/lesser values
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