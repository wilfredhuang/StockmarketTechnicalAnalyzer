from flask import Flask, render_template
from dotenv import load_dotenv
import os
from .config import get_config
from .routes import main_bp

def create_app():
    # Load environment variables
    load_dotenv()

    # Create Flask app instance
    app = Flask(__name__, static_folder='static')
    
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

    return app



