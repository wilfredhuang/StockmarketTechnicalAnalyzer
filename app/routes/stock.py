from flask import Flask, current_app, render_template, send_file, jsonify, request
import pandas as pd
import yfinance as yf
from dash import Dash, dcc, html
import plotly.express as px
from flask import Blueprint

from ..helpers.stonk_utils import sampleFunc

stock_bp = Blueprint('stock', __name__)


# TODO WORK HERE
@stock_bp.route('/stock-page')
def stock_page():
    # Define render variables
    render_variables = {
    }
    return render_template('', **render_variables)


# 
@stock_bp.route('/stonk')
def stonk_page():
    # Define render variables
    render_variables = {
    }
    return render_template('stonk.html', **render_variables)

@stock_bp.route('/sample-post', methods=['POST'])
def sample_post():
    sampleFunc()
    return jsonify({"message": "Data fetched successfully"})

