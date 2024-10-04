# Packages
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, session
from flask_login import login_user, logout_user, login_required, current_user
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Config
from app.config.db import db  # Import db from the new module
# Helpers
from app.helpers.stock_utils import fetch_and_process_stock_data
import app.helpers.process_utils as pu
import app.helpers.graph_for_analysis as ga
from app.helpers.fetchclosingprice import get_closing_price, sell_share_to_db, save_ticker_to_db
# Models
from app.models.User import User
from app.models.StockTicker import StockTicker 


global linear_model


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


@main_bp.route('/stock')
def stock_page():
    secret_key = current_app.config.get('SECRET_KEY', 'default123')
    # Define render variables
    render_variables = {
        'secret_key': secret_key,
        'user_name': 'John Doe',
    }
    print("Hello World")

    return render_template('index_stock.html', **render_variables)


@main_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data():
    try:
        csv_filename = fetch_and_process_stock_data()
        flash(f'Stock data successfully fetched and saved as {csv_filename}', 'success')
        present_csv_filename = csv_filename
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'danger')
    return redirect(url_for('main.index'))

@main_bp.route('/grid')
def grid_page():
    # Define render variables
    render_variables = {
    }
    return render_template('grid.html', **render_variables)

# Retrieve historical data for analysis
@main_bp.route('/get-analysis', methods=['POST'])
def get_analysis():
    try:
        company = request.form['company']
        csv_file = request.form['dataset']
        # company = 'AAPL'
        # csv_file = 'stock_data_20240925_124231.csv'
        analysis_graph = ga.visualise_analysis(csv_file, company)
        render_variables = {
            'analysis_graph': analysis_graph,
        }
        return render_template('analysis.html', **render_variables)
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'danger')
    return render_template('analysis.html', **render_variables)


# @main_bp.route('/train-model', methods=['GET'])
# def train_linear():
#     try:
#         linear_model = pu.train_linear_model(present_csv_filename)
#         flash(f'Model Successfully Trained', 'success')
#     except Exception as e:
#         flash(f'Error training model: {str(e)}', 'danger')
#     return redirect(url_for('main.index'))
    
# Predict data using linear model for now trains the model everytime
@main_bp.route('/prediction', methods=['POST'])
def predict_linear():
    try:
        company = request.form['company']
        csv_file = f"stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        linear_model = pu.train_linear_model(csv_file)
        date = ''
        prediction_data, historical_data = pu.predict_linear_model(company, date, csv_file, linear_model)
        prediction_graph = ga.visualise_prediction(prediction_data, historical_data)

        render_variables = {
            'prediction_graph': prediction_graph,
        }

        return render_template('prediction.html', **render_variables)
    except Exception as e:
        flash(f'Error with prediction: {str(e)}', 'danger')
    return redirect(url_for('main.index'))

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
    for ticker in user_tickers:
        # Fetch the current closing price using the get_closing_price function
        closing_price = get_closing_price(ticker.ticker)
        
        # Calculate profit and loss if closing price is available
        if closing_price is not None:
            ticker.profit_loss = round((closing_price - ticker.price) * ticker.shares, 2)  # Calculate P&L
            ticker.current_price = round(closing_price, 2)  # Store current price for display
        else:
            ticker.profit_loss = None  # Handle the case where the price is not available

    return render_template('profile.html', tickers=user_tickers, chart_data_ticker=chart_data_ticker, chart_data_shares=chart_data_shares)

@main_bp.route('/add_ticker', methods=['POST'])
@login_required
def add_ticker():
    ticker = request.form.get('ticker') or request.form.get('new_ticker')
    shares = request.form.get('shares')
    price = request.form.get('price')

    # Access the current user's ID
    if current_user.is_authenticated:
        user_id = current_user.id
        print(f"Current user ID: {user_id}")
        
        # Logic to save the ticker to the database or process it
        if ticker and shares and price:
            # Save the ticker, shares, and price to the database
            save_ticker_to_db(ticker, user_id, shares, price)
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