import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    API_KEY = os.getenv('paypal_api_key', "default value")
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuration for development."""
    SECRET_KEY = os.getenv('SECRET_KEY_DEV', 'default_secret_key')
    DEBUG = True
class ProductionConfig(Config):
    """Configuration for production."""
    SECRET_KEY = os.getenv('SECRET_KEY_PROD', 'default_secret_key')
    DEBUG = False


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        print("Running on Production Config")
        return ProductionConfig
    else:
        print("Running on Development Config")
        return DevelopmentConfig
    
    