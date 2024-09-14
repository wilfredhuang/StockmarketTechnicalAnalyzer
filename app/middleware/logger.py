from flask import Flask, request
from colorama import Fore, Style, init
import logging

# This logger may or may not be needed, as Flask already has its built in one before every request.
# Initialize colorama for Windows and other platforms
init(autoreset=True)

app = Flask(__name__)

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Custom logger function
def logger_middleware():
    # Skip logging for static files
    if request.path.startswith('/static'):
        return
    method_colors = {
        'GET': Fore.GREEN,
        'POST': Fore.BLUE,
        'PUT': Fore.YELLOW,
        'DELETE': Fore.RED
    }

    method = request.method
    color = method_colors.get(method, Fore.WHITE)
    
    log_message = f"{method} {request.url}"
    # Use logging instead of print
    logging.info(f"{color}{log_message}{Style.RESET_ALL}")


