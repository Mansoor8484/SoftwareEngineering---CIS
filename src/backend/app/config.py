import os
from datetime import timedelta
from .models import db, User


class Config:
    """Base configuration class for the Flask application."""

    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY','68d2374fc6aaaa84349a78ce5af4aaef50110b0b2df8592d2315f976944f9dc5')
    """Key used for cryptographic operations, such as signing cookies and tokens."""

    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'your_password_salt_here'
    """Salt for hashing passwords, enhances security against rainbow table attacks."""

    SECURITY_TOKEN_AUTHENTICATE = True
    """Enable token-based authentication for user sessions."""

    SECURITY_SEND_REGISTER_EMAIL = False  # Not needed for local offline testing
    """Send confirmation email upon user registration to verify email address."""

    # Flask Debugging
    DEBUG = True  # Always set to True for local development
    """Set to True to enable debug mode; displays detailed error messages."""

    TESTING = False  # Not needed unless running unit tests
    """Set to True to enable testing mode; useful for running unit tests without starting the server."""

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use SQLite for local testing
    """Database connection URI for SQLAlchemy; supports various databases."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """Disables track modifications to reduce overhead; not needed unless tracking changes."""

    # User Roles
    USER_ROLES = ['admin', 'user']
    """List of roles available in the application."""

    # Localization Settings
    DEFAULT_CURRENCY = 'USD'
    """Default currency for financial transactions."""

    SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP']
    """List of supported currencies for user budgets."""

    # Email Configuration
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    # """SMTP server for sending emails."""

    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    # """Port for the email server; typically 587 for TLS, 465 for SSL, or 25 for non-secure."""

    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # """Whether to use TLS for secure email sending."""

    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # """Username for SMTP authentication; usually an email address."""

    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # """Password for the email account; ensure this is kept secret."""

    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@yourapp.com'
    # """Default sender address for outgoing emails."""

    # MAIL_MAX_EMAILS = int(os.environ.get('MAIL_MAX_EMAILS', 5))
    # """Limit the number of emails to be sent per hour to prevent abuse."""

    # Plaid API Configuration
    PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
    """Client ID for the Plaid API; used for authenticating API requests."""

    PLAID_SECRET = os.environ.get('PLAID_SECRET')
    """Secret key for Plaid API authentication; keep this confidential."""

    PLAID_ENV = os.environ.get('PLAID_ENV') or 'sandbox'
    """Environment for Plaid API; options include 'sandbox', 'development', and 'production'."""

    PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
    """Public key for frontend integration; used for generating link tokens."""

    PLAID_REDIRECT_URI = os.environ.get('PLAID_REDIRECT_URI') or 'http://localhost:5000/plaid/callback'
    """Redirect URI for OAuth flow; where users are sent after linking their bank accounts."""

    PLAID_WEBHOOK_URL = os.environ.get('PLAID_WEBHOOK_URL') or 'http://localhost:5000/plaid/webhook'
    """Webhook URL for receiving updates from Plaid about linked accounts."""

    # Assistant and Ollama API Keys
    ASSISTANT_API_KEY = os.environ.get('ASSISTANT_API_KEY')
    OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY')

    # Bank Data Configuration
    BANK_DATA_RETENTION_PERIOD = 365  # Days to retain bank transaction data
    """Period for retaining bank transaction data; helps comply with regulations."""

    BANK_ACCOUNT_TYPES = ['checking', 'savings', 'credit']
    """List of supported bank account types for users to link."""

    ALLOWED_BANKS = ['bank_1', 'bank_2']  # Replace with actual bank identifiers
    """List of banks that users are allowed to link; helps limit integrations."""

    # Rate Limits
    # RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', '1') == '1'
    # """Enable or disable rate limiting to prevent abuse of API endpoints."""

    # RATE_LIMIT = os.environ.get('RATE_LIMIT') or '100 per hour'
    # """Rate limit policy; defines how many requests a user can make in a time window."""

    # RATE_LIMITER_STORAGE = os.environ.get('RATE_LIMITER_STORAGE') or 'redis'
    # """Storage backend for rate limiting; options may include Redis or in-memory."""

    # RATE_LIMITER_STRATEGY = os.environ.get('RATE_LIMITER_STRATEGY') or 'fixed_window'
    # """Strategy used for rate limiting; options include 'fixed_window', 'sliding_window', etc."""

    # Logging Configuration
    LOGGING_LEVEL = 'DEBUG'  # Can keep this for local development
    """Global logging level; controls the verbosity of log messages."""

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    """Format for log messages, includes timestamps, log level, and the message itself."""

    LOGGING_LOCATION = 'logs/app.log'  # Local log storage is fine
    """File path where logs will be stored."""

    # Caching Configuration
    # CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'redis'
    # """Type of caching mechanism to use; Redis, Memcached, or in-memory."""

    # CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    # """Default timeout for cache entries; sets how long data is stored in cache."""

    # CACHE_KEY_PREFIX = os.environ.get('CACHE_KEY_PREFIX') or 'budgeting_tool'
    # """Prefix for cache keys to avoid collisions with other applications."""

    # Session Management
    SESSION_TYPE = 'filesystem'  # Local storage for sessions
    """Type of session storage; options include 'filesystem', 'redis', or 'memcached'."""

    SESSION_PERMANENT = False  # Not necessary for local use
    """Whether to use permanent sessions; if True, sessions will last until they expire."""

    # USER_PREFERENCES_ENABLED = os.environ.get('USER_PREFERENCES_ENABLED', '1') == '1'
    # """Enable user-specific preferences for personalized experiences."""

    # Frontend URL
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:3000'
    """Base URL for the frontend application; used for CORS and API requests."""

    # CORS Configuration
    # CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    # """Allowed origins for Cross-Origin Resource Sharing (CORS); can be set to specific domains or '*'. """

    # CORS_ALLOW_CREDENTIALS = True
    # """Allow credentials (cookies, authorization headers, etc.) to be included in cross-origin requests."""

    # CORS_ALLOW_HEADERS = os.environ.get('CORS_ALLOW_HEADERS', 'Content-Type,Authorization').split(',')
    # """List of allowed headers for CORS requests; important for security and functionality."""

    # CORS_ALLOW_METHODS = os.environ.get('CORS_ALLOW_METHODS', 'GET,POST,PUT,DELETE').split(',')
    # """List of allowed methods for CORS requests; defines what HTTP methods can be used."""

    # Monitoring and Analytics
    # MONITORING_ENABLED = os.environ.get('MONITORING_ENABLED', '1') == '1'
    # """Enable or disable application performance monitoring."""

    # ANALYTICS_TRACKING_ID = os.environ.get('ANALYTICS_TRACKING_ID')
    # """Tracking ID for Google Analytics or other analytics services."""

    # Backup Settings
    BACKUP_ENABLED = True
    """Enable automated backups for user data."""

    BACKUP_SCHEDULE = 'daily'
    """Frequency for data backups."""

    BACKUP_LOCATION = os.environ.get('BACKUP_LOCATION') or '/path/to/backup'
    """Directory for storing backup files; should have sufficient storage and security."""

    # Deployment Environment Configuration
    ENVIRONMENT = 'development'  # Set directly to development for local use
    """Current environment of the application; options include 'development', 'testing', and 'production'."""

    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    """List of hostnames or IP addresses allowed to access the application; limits access in production."""

    # API Versioning
    API_VERSION = 'v1'
    """Version of the API being used; helps manage changes and backward compatibility."""

    # External Services Integration
    # EXTERNAL_SERVICE_TIMEOUT = int(os.environ.get('EXTERNAL_SERVICE_TIMEOUT', 10))
    # """Timeout for requests to external services; prevents blocking the application on long requests."""

    # Feature Flags
    # FEATURE_FLAGS = {
    #     'new_feature_x': os.environ.get('FEATURE_FLAGS_NEW_FEATURE_X', '0') == '1',
    #     """Toggle for enabling/disabling new feature X."""
    # }

    # Health Check Configuration
    HEALTH_CHECK_URL = '/health'
    """Endpoint for health checks to monitor the application's status."""
