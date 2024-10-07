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
@stock_bp.route('/stock-page')
def stock_page():
    # Define render variables
    render_variables = {
    }
    return render_template('new_stonk.html', **render_variables)


@stock_bp.route('/sandbox-test-request', methods=['POST'])
def sandbox_request():
    data = request.get_json()
    # Retrieve Input from Web App
    sandbox_list = data.get('data')
    print(sandbox_list)
    errors = {"foobar":"Some Foobar Error occured"}
    #return jsonify(success=True, message="Form submitted successfully!")
    return jsonify(success=False, errors=errors)


@stock_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data_request():
    # --Retrieve Str Inputs from Web App--
    data = request.get_json()
    errors = {}
    tickers = data.get('tickers')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    # --Input Validation--
    # Validate ticker_list (Working)
    ticker_valid, ticker_msg = validate_ticker_list(data.get('tickers'))
    print(ticker_msg)
    print(ticker_valid)
    # Validate start_date and end_date (Works for leap years too)
    date_valid, date_msg = validate_dates(data.get('start_date'), data.get('end_date'))
    print(date_msg)
    print(date_valid)
    #print(f"Data is {data} \nTickers List: {tickers}\nStart Date: {start_date}\n End Date: {end_date}  {type(tickers)}")

    # Transform Web App Form Input to proper list data type for yfinance api call
    if date_valid & ticker_valid: 
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        print(tickers_list)
        # Sample List: KO, PEP, WMT, SBUX, MCD, AAL, DAL, F, VZ, T, DIS, BAC, JPM, MA, V, ORCL, AMD, NVDA, AAPL, MSFT
        # ---Hardcoded Inputs---
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

# Upload Stock Data File
@stock_bp.route('/upload-stock-data', methods=['POST'])
def upload_stock_data_request():
    data = request.get_json()

# Process Stock Data Post Request
@stock_bp.route('/process-stock-data', methods=['POST'])
def process_stock_data_request():
    data = request.get_json()  # Get the JSON data from the POST request
    strategy = data.get('strategy')  # Extract the 'strategy' value
    if not strategy:
        return jsonify({"error": "Strategy not provided"}), 400  # Return error if no strategy
    
    match strategy:
        case "1":
            print("1")
            data_statistics = ema_crossover_strategy()
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            # Convert the figure to JSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return jsonify(image_url='static/data/plot_strategy_ema.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "2":
            print("2")
            data_statistics = ema_crossover_rsi_strategy()
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            # Convert the figure to JSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return jsonify(image_url='static/data/plot_strategy_ema_rsi.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "3":
            print("3")
            data_statistics = rsi_adx_strategy()
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            fig = data_statistics[2]
            # Convert the figure to JSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return jsonify(image_url='static/data/plot_strategy_rsi_adx.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case "4":
            print("4")
            data_statistics = indicator_ml_strategy()
            benchmark_data = data_statistics[0]
            strat_perf_data = data_statistics[1]
            # === TODO ===
            ##fig = data_statistics[2]
            # Convert the figure to JSON
            #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return jsonify(image_url='static/data/plot_strategy_ml_indicator.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data)
        case _:
            print("No option selected")

    # Respond with the default image path
    return jsonify(image_url='static/data/plot.png')



