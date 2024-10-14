from flask import Flask
from .config import Config

def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Import and register blueprints here
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize other components (like database, login manager, etc.)
    # from .extensions import db, login_manager
    # db.init_app(app)
    # login_manager.init_app(app)

    return app
