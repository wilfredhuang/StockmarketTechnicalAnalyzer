from flask import current_app
import yfinance as yf
from datetime import datetime, timedelta
from app.config.db import db  # Import db from the new module
from app.models.User import User  # This should remain unchanged
from app.models.StockTicker import StockTicker
from flask import flash

def get_closing_price(ticker):
    # Fetch historical data for the ticker
    stock = yf.Ticker(ticker)

    # Get today's date
    today = datetime.today().date()
    
    # Attempt to get today's closing price
    hist_today = stock.history(start=today, end=today + timedelta(days=1))

    if not hist_today.empty:
        return hist_today['Close'].iloc[0]  # Return today's closing price

    # Loop back through previous days until a closing price is found
    days_back = 1  # Start with yesterday
    while days_back <= 5:
        previous_date = today - timedelta(days=days_back)
        hist_previous = stock.history(start=previous_date, end=previous_date + timedelta(days=1))

        if not hist_previous.empty:
            return hist_previous['Close'].iloc[0]  # Return the most recent closing price

        days_back += 1  # Move to the next day back

    return None  # If no closing price is found after the loop, return None

def save_ticker_to_db(ticker, user_id, shares, price):
    # Check if the ticker already exists for this user
    existing_ticker = StockTicker.query.filter_by(ticker=ticker, user_id=user_id).first()

    if not existing_ticker:
        # If the ticker does not exist, add it as a new record
        new_ticker = StockTicker(ticker=ticker, user_id=user_id, shares=int(shares), price=float(price))

        try:
            db.session.add(new_ticker)
            # Commit the changes
            db.session.commit()
            flash(f'Successfully added new ticker {ticker} with {shares} shares at {price} per share!', 'success')
        except Exception as e:
            # Rollback the session in case of error
            db.session.rollback()
            flash(f'Error adding ticker: {str(e)}', 'danger')

    else:
        flash(f'{ticker} is already in your portfolio!', 'warning')



def update_ticker_to_db(ticker, user_id, additional_shares, new_price):
    try:
        # Check if the ticker already exists for this user
        existing_ticker = StockTicker.query.filter_by(ticker=ticker, user_id=user_id).first()
        if existing_ticker:
            # If the ticker exists, update the shares and price
            existing_shares = existing_ticker.shares
            existing_price = existing_ticker.price

            total_shares = existing_shares + int(additional_shares)  # Total shares after adding new ones

            # Weighted average price formula
            weighted_price = ((existing_shares * existing_price) + (int(additional_shares) * float(new_price))) / total_shares

            # Round the weighted price to 2 decimal places
            weighted_price = round(weighted_price, 2)

            # Update the existing ticker with new values
            existing_ticker.shares = total_shares
            existing_ticker.price = weighted_price

            # Commit the changes
            db.session.commit()

            flash(f'Updated {ticker} with {additional_shares} additional shares. New total: {existing_ticker.shares}', 'info')
        else:
            flash(f'Ticker {ticker} not found for user {user_id}', 'warning')
    except Exception as e:
        db.session.rollback()  # Rollback the session if any error occurs
        flash(f'Error updating {ticker}: {str(e)}', 'error')

def sell_share_to_db(ticker, user_id, sell_shares):
    # Check if the ticker already exists for this user
    existing_ticker = StockTicker.query.filter_by(ticker=ticker, user_id=user_id).first()

    try:
        if existing_ticker:
            # If the ticker exists, update the shares and price
            total_shares = int(existing_ticker.shares)-int(sell_shares)

            #check if there are remaining shares
            if total_shares > 0:
                # Update the existing ticker with new values
                existing_ticker.shares = total_shares
                # Commit the changes
                db.session.commit()
                flash(f'Sold {sell_shares} of {ticker}. New total: {existing_ticker.shares}', 'info')
            elif total_shares == 0:
                # Delete the entry if shares reach 0
                db.session.delete(existing_ticker)
                # Commit the changes
                db.session.commit()
                flash(f'All shares of {ticker} sold. Removed from portfolio.', 'info')
            else:
                flash(f'Cannot sell {sell_shares} shares. You only own {existing_ticker.shares} shares of {ticker}.', 'warning')

        else:
            flash(f"{ticker} is not in you're portfolio", 'info')
    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        flash(f'Error selling ticker: {str(e)}', 'danger')

def calculate_profit_loss(user_id):
    total_invested = 0
    total_current_value = 0

    allexisting_tickers = StockTicker.query.filter_by(user_id=user_id).all()

    for ticker in allexisting_tickers:
        closingprice = get_closing_price(ticker.ticker)
        shares = ticker.shares # Number of shares owned
        purchase_price = ticker.price  # Initial purchase price

        # Skip calculation if closing price is None or invalid
        if closingprice is None:
            continue  # Skip this ticker if there is no closing price

        # Calculate current value
        current_value = shares * closingprice
        total_current_value += current_value

        # Calculate total invested amount
        total_invested += shares * purchase_price

    total_profit_loss = total_current_value - total_invested
    return round(total_profit_loss, 2), round(total_invested, 2)

def is_valid_stock_ticker(ticker):
    """
    Checks if a stock ticker is valid using the yfinance library.
    
    Args:
        ticker (str): The stock ticker to validate.
    
    Returns:
        bool: True if the ticker is valid, False otherwise.
    """
    try:
        stock_info = yf.Ticker(ticker)
        # Check if the stock has a 'longName' or any relevant field to validate
        if stock_info.info.get('longName') is not None:
            return True
        else:
            flash(f"{ticker} is not a valid stock ticker.", 'danger')
            return False
    except Exception as e:
        flash(f"Error fetching data for {ticker}. Please check the ticker or try again later.", 'danger')
        return False
