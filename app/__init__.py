from flask import Flask, render_template
from dotenv import load_dotenv
from .config import get_config
from .routes import main_bp, stock_bp
from .middleware.logger import logger_middleware
import os, logging


from .config.db import db  # Import db from the new db module
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from .models.User import User


def create_app():
    # Load environment variables
    load_dotenv()
    # Create Flask app instance
    app = Flask(__name__, static_folder='static')

    # Logger Stuff, can ignore
    # Suppress Werkzeug's (Flask's built in logger) request logs
    # Comment out these lines if you want to use the default logger as it suppresses it
    # Configure werkzeug logging
    # logging.basicConfig(level=logging.ERROR)  # This sets the root logger to show ERROR messages only
    # werkzeug_logger = logging.getLogger('werkzeug')
    # werkzeug_logger.setLevel(logging.ERROR)  # Only log ERROR messages for Werkzeug

    # Load configuration
    app.config.from_object(get_config())


    # Login Stuff
    app.jinja_env.globals.update(current_user=current_user)
    db.init_app(app)  # Initialize the database
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        from .routes import main_bp  # Import the blueprint here, inside the app context
        app.register_blueprint(main_bp)  # Register the blueprint
        db.create_all()  # Create database tables if they do not exist
    # === ===

    # Register blueprints
    #app.register_blueprint(main_bp)

    app.register_blueprint(main_bp)
    app.register_blueprint(stock_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    @app.before_request
    def before_request():
        pass
        # Custom logger middleware
        logger_middleware()
    
    return app





