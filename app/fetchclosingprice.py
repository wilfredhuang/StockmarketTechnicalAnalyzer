from flask import current_app
import yfinance as yf
from datetime import datetime, timedelta
from app.db import db  # Import db from the new module
from app.models import User, StockTicker  # This should remain unchanged
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
    while True:
        previous_date = today - timedelta(days=days_back)
        hist_previous = stock.history(start=previous_date, end=previous_date + timedelta(days=1))

        if not hist_previous.empty:
            return hist_previous['Close'].iloc[0]  # Return the most recent closing price

        days_back += 1  # Move to the next day back

        # Optional: Add a safeguard to prevent infinite loops (e.g., after checking a set number of days)
        if days_back > 5:  # Limit to 30 days back
            break

    return None  # If no closing price is found after the loop, return None

def save_ticker_to_db(ticker, user_id, new_shares, new_price):
    # Check if the ticker already exists for this user
    existing_ticker = StockTicker.query.filter_by(ticker=ticker, user_id=user_id).first()

    if existing_ticker:
        # If the ticker exists, update the shares and price
        old_shares = existing_ticker.shares
        old_price = existing_ticker.price

        total_shares = old_shares + int(new_shares)  # Total shares after adding new ones

        # Weighted average price formula
        weighted_price = ((old_shares * old_price) + (int(new_shares) * float(new_price))) / total_shares

        # Round the weighted price to 2 decimal places
        weighted_price = round(weighted_price, 2)

        # Update the existing ticker with new values
        existing_ticker.shares = total_shares
        existing_ticker.price = weighted_price


        flash(f'Updated {ticker} with {new_shares} additional shares. New total: {existing_ticker.shares}', 'info')
    else:
        # If the ticker does not exist, add it as a new record
        new_ticker = StockTicker(ticker=ticker, user_id=user_id, shares=int(new_shares), price=float(new_price))

        try:
            db.session.add(new_ticker)
            flash(f'Successfully added new ticker {ticker} with {new_shares} shares at {new_price} per share!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ticker: {str(e)}', 'danger')

    # Commit the changes
    db.session.commit()

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
                flash(f'Sold {sell_shares} of {ticker}. New total: {existing_ticker.shares}', 'info')
            elif total_shares == 0:
                # Delete the entry if shares reach 0
                db.session.delete(existing_ticker)
                flash(f'All shares of {ticker} sold. Removed from portfolio.', 'info')
            else:
                flash(f'Cannot sell {sell_shares} shares. You only own {existing_ticker.shares} shares of {ticker}.', 'warning')

        else:
            flash(f"{ticker} is not in you're portfolio", 'info')
    except Exception as e:
        flash(f'Error selling ticker: {str(e)}', 'danger')

    # Commit the changes
    db.session.commit()