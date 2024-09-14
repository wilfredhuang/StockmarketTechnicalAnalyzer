# Entry point to the app

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get the debug mode variable based on current configuration
    debug_mode = app.config.get('DEBUG', False,)
    app.run(debug=debug_mode)

