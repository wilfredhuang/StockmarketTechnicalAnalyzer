from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='static')

from routes.main import main_bp

app.register_blueprint(main_bp)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

