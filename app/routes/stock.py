from flask import Flask, current_app, render_template, send_file, jsonify, request
import pandas as pd
import yfinance as yf
from dash import Dash, dcc, html
import plotly.express as px
import plotly
import json
from flask import Blueprint

from app.helpers.market_utils import (ema_crossover_rsi_strategy, ema_crossover_strategy,
    fetch_stock_data, indicator_ml_strategy, rsi_adx_strategy)

stock_bp = Blueprint('stock', __name__)

# 
@stock_bp.route('/stock-page')
def stock_page():
    # Define render variables
    render_variables = {
    }
    return render_template('new_stonk.html', **render_variables)

@stock_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data_request():
    # Hardcode the input for now
    TICKERS = [
    'KO','PEP','WMT', # consumer staples
    'SBUX','MCD', # consumer discretionary
    'AAL','DAL','F', # industrials
    'VZ', 'T', 'DIS', # communication services
    'BAC','JPM','MA','V', # financials
    'ORCL','AMD','NVDA','AAPL','MSFT', # information technology
    ] 
    START_DATE = "2000-01-01"
    END_DATE = "2024-07-31"
    fetch_stock_data(TICKERS, START_DATE, END_DATE)
    return "Stock Data Fetched"

@stock_bp.route('/process-stock-data', methods=['POST'])
def process_stock_data_request():
    #process_data()
    #ema_crossover_strategy()
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
            indicator_ml_strategy()
            return jsonify(image_url='static/data/plot_strategy_ml_indicator.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data, graphJSON=graphJSON)
        case _:
            print("No option selected")

    # Respond with the default image path
    return jsonify(image_url='static/data/plot.png', benchmark_data=benchmark_data, strat_perf_data=strat_perf_data)



