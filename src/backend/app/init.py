from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from .config import Config
from .models import db, User, Reminder, BankAccount, Transaction, ChatbotInteraction, Budget, Message
from flask_migrate import Migrate
'''
______________________________________________________________________________________________________________________________________________________________________________
API Reference
Comprehensive reference for integrating with Plaid API endpoints
API endpoints and webhooks
For documentation on specific API endpoints and webhooks, use the navigation menu or search.

API access
To gain access to the Plaid API, create an account on the Plaid Dashboard. Once you’ve completed the signup process and acknowledged our terms, we’ll provide a live client_id and secret via the Dashboard.

API protocols and headers
The Plaid API is JSON over HTTP. Requests are POST requests, and responses are JSON, with errors indicated in response bodies as error_code and error_type (use these in preference to HTTP status codes for identifying application-level errors). All responses come as standard JSON, with a small subset returning binary data where appropriate. The Plaid API is served over HTTPS TLS v1.2+ to ensure data privacy; HTTP and HTTPS with TLS versions below 1.2 are not supported. Clients must use an up to date root certificate bundle as the only TLS verification path; certificate pinning should never be used. All requests must include a Content-Type of application/json and the body must be valid JSON.

Almost all Plaid API endpoints require a client_id and secret. These may be sent either in the request body or in the headers PLAID-CLIENT-ID and PLAID-SECRET.

Every Plaid API response includes a request_id, either in the body or (in the case of endpoints that return binary data, such as /asset_report/pdf/get) in the response headers. For faster support, include the request_id when contacting support regarding a specific API call.

API host
https://sandbox.plaid.com (Sandbox)
https://production.plaid.com (Production)
Plaid has two environments: Sandbox and Production. Items cannot be moved between environments. The Sandbox environment supports only test Items. You can request Production API access via the Dashboard.
____________________________________________________________________________________________________________________________________________________________________________
'''

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database and migrations
    db.init_app(app)
    Migrate(app, db)

    # Enable CORS
    CORS(app)

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Configure ORM registry
    from sqlalchemy.orm import registry
    mapper_registry = registry()
    mapper_registry.configure()

    # Serve the frontend folder
    @app.route('/<path:filename>')
    def serve_frontend(filename):
        frontend_path = os.path.abspath('../frontend')  # Adjust if necessary
        return send_from_directory(frontend_path, filename)

    return app


# cd src\backend\app
# python start_smtp.py
# $env:FLASK_APP="backend.app.run"
# $env:PYTHONPATH="src"
# flask run --debug