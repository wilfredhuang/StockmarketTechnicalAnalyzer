from flask import Blueprint, render_template, current_app

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

@main_bp.route('/grid')
def grid_page():
    # Define render variables
    render_variables = {
    }
    return render_template('grid.html', **render_variables)








