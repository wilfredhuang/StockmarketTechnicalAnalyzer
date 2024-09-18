from flask import Flask, render_template
from dotenv import load_dotenv
import os
from .config import get_config
from .routes import main_bp
import logging
from .middleware.logger import logger_middleware

def create_app():
    # Load environment variables
    load_dotenv()

    # Create Flask app instance
    app = Flask(__name__, static_folder='static')

    # --- ---
    # Comment out these lines if you want to use the default logger as it suppresses it
    # Configure werkzeug logging
    logging.basicConfig(level=logging.ERROR)  # This sets the root logger to show ERROR messages only
    # # Suppress Werkzeug's (Flask's built in logger) request logs
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)  # Only log ERROR messages for Werkzeug
    # --- ---
    
    # Load configuration
    app.config.from_object(get_config())

    # Register blueprints
    app.register_blueprint(main_bp)


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



