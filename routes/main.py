from flask import Blueprint, render_template, flash, redirect, url_for
from helpers.stock_utils import fetch_and_process_stock_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data():
    try:
        csv_filename = fetch_and_process_stock_data()
        flash(f'Stock data successfully fetched and saved as {csv_filename}', 'success')
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'danger')
    return redirect(url_for('main.index'))


