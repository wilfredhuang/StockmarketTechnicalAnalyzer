from flask import Blueprint, render_template, current_app, request, redirect, flash, url_for

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

# @main_bp.route('/fetch-stock-data', methods=['POST'])
# def fetch_stock_data():
#     try:
#         csv_filename = fetch_and_process_stock_data()
#         flash(f'Stock data successfully fetched and saved as {csv_filename}', 'success')
#         present_csv_filename = csv_filename
#     except Exception as e:
#         flash(f'Error fetching stock data: {str(e)}', 'danger')
#     return redirect(url_for('main.index'))

@main_bp.route('/grid')
def grid_page():
    # Define render variables
    render_variables = {
    }
    return render_template('grid.html', **render_variables)

# # Retrieve historical data for analysis
# @main_bp.route('/get-analysis', methods=['POST'])
# def get_analysis():
#     try:
#         company = request.form['company']
#         csv_file = request.form['dataset']
#         # company = 'AAPL'
#         # csv_file = 'stock_data_20240925_124231.csv'
#         analysis_graph = ga.visualise_analysis(csv_file, company)
#         render_variables = {
#             'analysis_graph': analysis_graph,
#         }
#         return render_template('analysis.html', **render_variables)
#     except Exception as e:
#         flash(f'Error fetching stock data: {str(e)}', 'danger')
#     return render_template('analysis.html', **render_variables)


# @main_bp.route('/train-model', methods=['GET'])
# def train_linear():
#     try:
#         linear_model = pu.train_linear_model(present_csv_filename)
#         flash(f'Model Successfully Trained', 'success')
#     except Exception as e:
#         flash(f'Error training model: {str(e)}', 'danger')
#     return redirect(url_for('main.index'))
    
# # Predict data using linear model for now trains the model everytime
# @main_bp.route('/prediction', methods=['POST'])
# def predict_linear():
#     try:
#         company = request.form['company']
#         csv_file = f"stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
#         linear_model = pu.train_linear_model(csv_file)
#         date = ''
#         prediction_data, historical_data = pu.predict_linear_model(company, date, csv_file, linear_model)
#         prediction_graph = ga.visualise_prediction(prediction_data, historical_data)

#         render_variables = {
#             'prediction_graph': prediction_graph,
#         }

#         return render_template('prediction.html', **render_variables)
#     except Exception as e:
#         flash(f'Error with prediction: {str(e)}', 'danger')
#     return redirect(url_for('main.index'))








