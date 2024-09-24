# This file simplify import of blueprints if there are additional folders (e.g /products , /login, /visualiation)
# so in app/__init__.py i can do get it like this 'from .routes import main_bp' instead of 'from .routes.main import main_bp'
from .main import main_bp
from .stock import stock_bp
from .example import example_bp