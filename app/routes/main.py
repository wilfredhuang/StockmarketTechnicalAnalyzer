# Packages
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, session
from flask_login import login_user, logout_user, login_required, current_user
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Config
from app.config.db import db  # Import db from the new module
# Helpers
from app.helpers.stock_utils import fetch_and_process_stock_data, fetch_portfolio_stock_data
import app.helpers.process_utils as pu
from app.helpers.fetchclosingprice import get_closing_price, sell_share_to_db, save_ticker_to_db, update_ticker_to_db, calculate_profit_loss, is_valid_stock_ticker
# Models
from app.models.User import User
from app.models.StockTicker import StockTicker 



main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    # Initialize variable with env value [the direct way from .env file]
    # secret_key = os.getenv('SECRET_KEY', 'default')
    # Initialize variable with env value [get a variable value from the current config set]
    secret_key = current_app.config.get('SECRET_KEY', 'default123')
    # Define render variables
    render_variables = {
        'secret_key': secret_key,
        'user_name': 'John Doe',
    }
    print("Hello World")

    return render_template('index.html', **render_variables)

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user:
        flash('No user found with that email address.', 'danger')
        return redirect(url_for('main.login'))
    
    if not check_password_hash(user.password, password):
        flash('Incorrect password. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    # Set session based on the "remember" flag
    if remember:
        session.permanent = True  # Session will persist even after browser close
    else:
        session.permanent = False  # Session will expire when the browser is closed

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@main_bp.route('/signup')
def signup():
    return render_template('register.html')

@main_bp.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Check if any of the fields are empty
    if not email or not name or not password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('main.signup'))

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user:
        flash('Email already registered. Please try again.', 'danger')
        return redirect(url_for('main.signup'))

    # Hash the password before saving it
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create new user
    new_user = User(email=email, name=name, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error occurred: {str(e)}', 'danger')

    return redirect(url_for('main.login'))

@main_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # This logs the user out by clearing their session
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))  # Redirect the user to the login page


@main_bp.route('/profile')
@login_required
def profile():
    # Print the current user object and user_id for debugging
    user_tickers = StockTicker.query.filter_by(user_id=current_user.id).all()
    chart_data_ticker = []
    chart_data_shares = []
    for i in range(len(user_tickers)):
        chart_data_ticker.append([user_tickers[i].ticker])
        chart_data_shares.append([user_tickers[i].shares])

    # Calculate profit/loss here
    total_profit_loss, total_invested = calculate_profit_loss(current_user.id)
    
    for ticker in user_tickers:
        # Fetch the current closing price using the get_closing_price function
        closing_price = get_closing_price(ticker.ticker)
        #Calculate total price for each stock
        ticker.total_price = round(ticker.shares*ticker.price, 2)
        # Calculate profit and loss if closing price is available
        if closing_price is not None:
            ticker.profit_loss = round((closing_price - ticker.price) * ticker.shares, 2)  # Calculate P&L
            ticker.current_price = round(closing_price, 2)  # Store current price for display
        else:
            ticker.profit_loss = None  # Handle the case where the price is not available

    return render_template('profile.html', tickers=user_tickers, chart_data_ticker=chart_data_ticker, chart_data_shares=chart_data_shares, total_profit_loss=total_profit_loss, total_invested=total_invested)

@main_bp.route('/add_ticker', methods=['POST'])
@login_required
def add_ticker():
    ticker = request.form.get('new_ticker')
    shares = request.form.get('shares')
    price = request.form.get('price')

    # Access the current user's ID
    if current_user.is_authenticated:
        user_id = current_user.id
        print(f"Current user ID: {user_id}")
        
        # Validate form inputs
        if ticker and shares and price:
            # Convert ticker to uppercase and validate it using the module function
            ticker = ticker.upper()
            if is_valid_stock_ticker(ticker):
                # Save the ticker, shares, and price to the database
                save_ticker_to_db(ticker, user_id, shares, price)
            else:
                return redirect(url_for('main.profile'))

        else:
            flash('Failed to add ticker. Please provide valid inputs.', 'danger')
    
    return redirect(url_for('main.profile'))  # Redirect to an appropriate page

@main_bp.route('/update_ticker', methods=['POST'])
@login_required
def update_ticker():
    ticker = request.form.get('existing_ticker')
    shares = request.form.get('shares')
    price = request.form.get('price')

    # Access the current user's ID
    if current_user.is_authenticated:
        user_id = current_user.id
        print(f"Current user ID: {user_id}")
        
        # Logic to save the ticker to the database or process it
        #check if ticker, shares or price is none
        if ticker and shares and price:
            # Save the ticker, shares, and price to the database
            update_ticker_to_db(ticker, user_id, shares, price)
        else:
            flash('Failed to add ticker. Please try again.', 'danger')
    
    return redirect(url_for('main.profile'))  # Redirect to an appropriate page

@main_bp.route('/sell_shares', methods=['POST'])
@login_required
def sell_shares():
    ticker = request.form.get('ticker')
    shares = request.form.get('shares')

    # Access the current user's ID
    if current_user.is_authenticated:
        user_id = current_user.id
        
        # Logic to save the ticker to the database or process it
        if ticker and shares:
            # Save the ticker, shares, and price to the database
            sell_share_to_db(ticker, user_id, shares)
    
    return redirect(url_for('main.profile'))  # Redirect to an appropriate page



@main_bp.route('/delete_ticker/<int:ticker_id>', methods=['POST'])
@login_required
def delete_ticker(ticker_id):
    ticker = StockTicker.query.get(ticker_id)
    
    if ticker:
        db.session.delete(ticker)
        db.session.commit()
        flash('Ticker deleted successfully!', 'success')

    return redirect(url_for('main.profile'))  # Redirect to the tickers page


@main_bp.route('/portfolio', methods=['GET'])
@login_required
def portfolio():
    try:
        predicted_prices, portfolio_data_ranked  = [], []

        # Fetch stock data from list of company
        company = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK-B', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'MA', 'NVDA', 'HD', 'DIS', 'BAC', 'ADBE', 'CRM', 'NFLX']
        stock_data = fetch_portfolio_stock_data(company)

        # Get user's stock information
        user_tickers = StockTicker.query.filter_by(user_id=current_user.id).all()

        # Get the predicted data
        for i in range(len(company)):
            for y in range(len(user_tickers)):
                if user_tickers[y].ticker == company[i]:
                    linear_model = pu.train_portfolio_linear_model(stock_data)
                    date = ''
                    prediction_data = pu.portfolio_predict_linear_model(company[i], date, stock_data, linear_model)
                    predicted_prices.append([company[i], prediction_data.Results[9]])

        # Check if stocks exists/matches
        for i in range(len(user_tickers)):
            for y in range(len(predicted_prices)):
                if user_tickers[i].ticker == predicted_prices[y][0]:
                    # Calculate Total Price of User stocks, predicted total price, projected profit & loss
                    user_share_total_price = user_tickers[i].price * user_tickers[i].shares
                    predicted_share_total_price = round(predicted_prices[y][1] * user_tickers[i].shares,2)
                    projected_profit_loss = round(predicted_share_total_price - user_share_total_price, 2)
                    portfolio_data_ranked.append([user_tickers[i].ticker, user_tickers[i].shares, user_tickers[i].price, user_share_total_price, round(predicted_prices[y][1], 2), predicted_share_total_price, projected_profit_loss])

        # Format the portfolio data such that it is ranked by profits & loss
        portfolio_data_ranked.sort(reverse = True, key=lambda x:x[5])

        return render_template('portfolio.html', portfolio_data=portfolio_data_ranked)
    except Exception as e:
        flash(f'Error with portfolio: {str(e)}', 'danger')
