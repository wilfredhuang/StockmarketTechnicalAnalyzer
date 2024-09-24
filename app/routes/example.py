from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request, current_app
# API Package
import yfinance as yf
# Data Collection and Preparation Package
import pandas as pd
# Visualisation Packages
from dash import Dash, dcc, html
import plotly.express as px
import plotly.utils
# Other Packages
import json
# Utility Functions
from app.helpers.stock_utils import fetch_and_process_stock_data
from app.helpers.display_utils import (fetch_stock_data, save_data_to_csv, load_data_from_csv,
                         process_data_with_indicators, create_stock_chart)

example_bp = Blueprint('example', __name__)

# --- First Example (fetch data from yfinance into .csv) --
@example_bp.route('/first-example')
def first_example_page():
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

    return render_template('examples/first-example.html', **render_variables)

@example_bp.route('/example-fetch-stock-data', methods=['POST'])
def example_fetch_stock_data():
    try:
        csv_filename = fetch_and_process_stock_data()
        flash(f'Stock data successfully fetched and saved as {csv_filename}', 'success')
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'danger')
    return redirect(url_for('main.index'))
# --- end  --

# --- Second Example (render a normal flask webpage, insert Dash webpage with visualisation as an iframe) --
# Refer to dash_helpers.py
@example_bp.route('/dash-example')
def dash_test_page():
    # Define render variables
    render_variables = {
    }
    return render_template('examples/dash-example.html', **render_variables)
# --- end  --

# --- Third Example (Flask webpage with plotly visualisation via DOM) --
# --- 1) Fetch Data (Get File) ---
# --- 2) Process Data (Read File, Analyse File) ---
# --- 3) Get Chart (Visualise) ---
@example_bp.route('/plotly')
def plotly_test_page():
    # Define render variables
    render_variables = {
    }
    return render_template('examples/plotly-example.html', **render_variables)

@example_bp.route('/fetch_data', methods=['POST'])
def fetch_data():
    data = request.json
    tickers = data['tickers'].split(',')
    start_date = data['start_date']
    end_date = data['end_date']
    df = fetch_stock_data(tickers, start_date, end_date)
    save_data_to_csv(df, 'app/static/data/ohlcv_test.csv')
    return jsonify({"message": "Data fetched successfully"})

@example_bp.route('/process_data', methods=['POST'])
def process_data():
    df = load_data_from_csv('app/static/data/ohlcv_test.csv')
    df_processed = process_data_with_indicators(df)
    save_data_to_csv(df_processed.reset_index(), 'app/static/data/processed_data_test.csv')
    return jsonify({"message": "Data processed successfully"})

@example_bp.route('/get_chart', methods=['POST'])
def get_chart():
    data = request.json
    ticker = data['ticker']
    df = load_data_from_csv('app/static/data/processed_data_test.csv')
    data = df.xs(ticker, level='ticker')
    fig = create_stock_chart(data, ticker)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(json.loads(graphJSON))




