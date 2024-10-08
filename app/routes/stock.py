from flask import Flask, current_app, render_template, send_file, jsonify, request, flash
import pandas as pd
import yfinance as yf
from dash import Dash, dcc, html
import plotly.express as px
import plotly
import json
from flask import Blueprint
from app.helpers.market_utils import (ema_crossover_rsi_strategy, ema_crossover_strategy,
    fetch_stock_data, indicator_ml_strategy, rsi_adx_strategy)
from app.helpers.validation_utils import (validate_dates, validate_ticker_list)

stock_bp = Blueprint('stock', __name__)

# Wilfred's Portion

# Main Page
@stock_bp.route('/stock-analyzer')
def stock_page():
    # Define render variables
    render_variables = {
    }
    return render_template('stock_analyzer.html', **render_variables)

# Simply a POST request used to test form retrieval with javascript, redundant to web app
@stock_bp.route('/sandbox-test-request', methods=['POST'])
def sandbox_request():
    # Retrieve Input from Web App
    data = request.get_json()
    sandbox_list = data.get('data')
    print(sandbox_list)
    errors = {"foobar":"Some Foobar Error occured"}
    #return jsonify(success=True, message="Form submitted successfully!")
    return jsonify(success=False, errors=errors)

# Fetch Stock Data Request
@stock_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data_request():
    # Retrieve Input from Web App
    data = request.get_json()
    errors = {}
    tickers = data.get('tickers')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    # --Input Validation--
    ticker_valid, ticker_msg = validate_ticker_list(data.get('tickers'))
    date_valid, date_msg = validate_dates(data.get('start_date'), data.get('end_date'))
    # Transform Web App Form Input to proper list data type for yfinance api call
    if date_valid & ticker_valid: 
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        # ---Hardcoded Inputs Sample---
        # TICKERS = [
        # 'KO','PEP','WMT', # consumer staples
        # 'SBUX','MCD', # consumer discretionary
        # 'AAL','DAL','F', # industrials
        # 'VZ', 'T', 'DIS', # communication services
        # 'BAC','JPM','MA','V', # financials
        # 'ORCL','AMD','NVDA','AAPL','MSFT', # information technology
        # ] 
        # START_DATE = "2000-01-01"
        # END_DATE = "2024-07-31"
        # fetch_stock_data(TICKERS, START_DATE, END_DATE)
        fetch_stock_data(tickers_list, start_date, end_date)
        return jsonify(success=True, message="Data Fetched to CSV File!", tickers_list=tickers_list)
    else:
        if ticker_valid == False:
            errors["ticker_msg"] = ticker_msg
        if date_valid == False:
            errors["date_msg"] = date_msg
        return jsonify(success=False, errors=errors)

# Process Stock Data Request
@stock_bp.route('/process-stock-data', methods=['POST'])
def process_stock_data_request():
    data = request.get_json() 
    strategy = data.get('strategy')
    ticker = data.get('ticker')

    if not strategy:
        return jsonify({"error": "Strategy not provided"}), 400  # Return error if no strategy
    
    match strategy:
        case "1":
            print("=== Using Strategy 1: EMA Crossover ===")
            data_statistics = ema_crossover_strategy(ticker)
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return jsonify(image_url='static/data/plot_strategy_ema.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "2":
            print("=== Using Strategy 2: EMA Crossover with RSI filter ===")
            data_statistics = ema_crossover_rsi_strategy(ticker)
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return jsonify(image_url='static/data/plot_strategy_ema_rsi.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "3":
            print("=== Using Strategy 3: ADX with RSI ===")
            data_statistics = rsi_adx_strategy(ticker)
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return jsonify(image_url='static/data/plot_strategy_rsi_adx.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "4":
            print("=== Using Strategy 4: ML ===")
            data_statistics = indicator_ml_strategy(ticker)
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            #fig = data_statistics[2]
            #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return jsonify(image_url='static/data/plot_strategy_ml_indicator.png', image_url_second='static/data/plot_strategy_ml_indicator_comparison.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data)
        case _:
            print("No option selected")

    # Respond with the default image path
    return jsonify(image_url='static/data/plot.png')



