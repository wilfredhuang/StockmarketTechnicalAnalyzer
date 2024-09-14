from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from app.helpers.stock_utils import fetch_and_process_stock_data
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Initialize variable with env value
    #secret_key = os.getenv('SECRET_KEY', 'default')
    secret_key = current_app.config.get('SECRET_KEY', 'default123')
    
    # Define render variables
    render_variables = {
        'secret_key': secret_key,
        'user_name': 'John Doe',
    }
    print("Hello World")

    return render_template('index.html', **render_variables)

@main_bp.route('/fetch-stock-data', methods=['POST'])
def fetch_stock_data():
    try:
        csv_filename = fetch_and_process_stock_data()
        flash(f'Stock data successfully fetched and saved as {csv_filename}', 'success')
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'danger')
    return redirect(url_for('main.index'))

@main_bp.route('/grid')
def grid_page():
    # Define render variables
    render_variables = {
    }

    return render_template('grid.html', **render_variables)



