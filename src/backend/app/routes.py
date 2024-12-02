from datetime import timedelta, datetime
import jwt
from flask import Blueprint, request, jsonify, redirect, url_for, render_template, send_from_directory, session
from functools import wraps
import os
from itsdangerous import URLSafeTimedSerializer
from .chatbot import Chatbot
from .config import Config
from .models import db, User, Reminder
from .controllers import (
    user_register, user_login, user_get_accounts, user_custom_budget,
    user_plan_one, user_plan_two, user_plan_three, send_message,
    user_profile, edit_user_profile, user_logout,
    user_filter_transactions, user_add_transaction, user_get_all_transactions,
    user_transaction_details, user_delete_manual_transaction,
    create_reminder, get_reminders_for_month_and_year, transactions_graph,
    link_account, send_password_reset_email, reset_password, serializer
)

# Blueprint setup
main = Blueprint('main', __name__)

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)


FRONTEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))

# Utility function for error handling
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            token = token.split(" ")[1]  # Strip "Bearer" prefix
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']  # Attach user_id to the request
        except Exception as e:
            print(f"Token decoding error: {e}")
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code

@main.route('/test-logout-js')
def test_logout_js():
    return '<script src="/static/logout.js"></script>'


@main.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files (e.g., JavaScript, CSS).
    """
    try:
        return send_from_directory(f'FRONTEND_PATH/static', filename)
    except FileNotFoundError:
        return jsonify({'error': f'Static file {filename} not found'}), 404

@main.route('/static/walletwizard.png', methods=['GET'])
def serve_walletwizard():
    """Serve walletwizard.png."""
    return send_from_directory(FRONTEND_PATH, 'walletwizard.png')

@main.route('/static/mail.png', methods=['GET'])
def serve_mail():
    """Serve mail.png."""
    return send_from_directory(FRONTEND_PATH, 'mail.png')

@main.route('/')
def home():
    return redirect(url_for('main.login_route'))
    #return "Welcome to the Software Engineering API! Use the /api/auth/login endpoint to log in."

# Authentication Routes
@main.route('/api/auth/register', methods=['GET', 'POST'])
def register_route():
    """
    Serve the registration page on GET and process user registration on POST.
    """
    if request.method == 'GET':
        try:
            return send_from_directory(FRONTEND_PATH, 'register.html')
        except FileNotFoundError:
            return jsonify({'error': 'Registration page not found.'}), 404

    # POST: Handle JSON payload
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400

        # Extract fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm-password')

        # Validate fields
        if not username or not email or not password or not confirm_password:
            return jsonify({'error': 'All fields are required'}), 400
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        # Delegate to the user_register controller
        return user_register({
            'username': username,
            'email': email,
            'password': password
        })

    except Exception as e:
        # Log the full error trace for debugging
        print("Error during registration:", str(e))
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

@main.route('/api/auth/login', methods=['GET', 'POST'])
def login_route():
    """Handle login page display (GET) and authentication (POST)."""
    if request.method == 'GET':
        # Serve the login.html file from the frontend folder
        frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
        try:
            return send_from_directory(frontend_path, 'login.html')
        except FileNotFoundError:
            return jsonify({'error': 'Login page not found.'}), 404

    # Handle POST requests for login
    try:
        if not request.is_json:  # Ensure the request Content-Type is JSON
            return jsonify({'error': "Request must be JSON. Please set 'Content-Type: application/json'"}), 415

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Both username and password are required.'}), 400

        # Authenticate the user
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Generate a JWT token for token-based authentication
        try:
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
                Config.SECRET_KEY,
                algorithm='HS256'
            )
            print(f"Generated Token: {token}")  # Debug log for token generation
        except Exception as jwt_error:
            print(f"Error generating JWT token: {jwt_error}")
            return jsonify({'error': 'Failed to generate authentication token.'}), 500

        # Respond with the token and user ID
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user_id": user.id
        }), 200

    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

@main.route('/api/logout', methods=['POST'])
def logout_route():
    """
    Clears session or token and logs the user out.
    """
    session.clear()  # If using session-based authentication
    return jsonify({"message": "Logged out successfully"}), 200


# Forgot Password
@main.route('/api/auth/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle GET to serve forgotpassword.html and POST for password reset."""
    if request.method == 'GET':
        # Serve forgotpassword.html from the frontend folder
        try:
            return send_from_directory(FRONTEND_PATH, 'forgotpassword.html')
        except FileNotFoundError:
            return jsonify({'error': 'Forgot Password page not found'}), 404

    # POST request logic for password reset
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Logic to send a password reset email
        if send_password_reset_email(email):
            return jsonify({'message': 'Password reset email sent successfully'}), 200
        else:
            return jsonify({'error': 'Email address not found'}), 404

    except Exception as e:
        print(f"Error during password reset request: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500


# Reset Password
@main.route('/api/auth/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Handle the reset password process. Display the password reset form (GET)
    and process the new password submission (POST).
    """
    try:
        # Verify the token and retrieve the email
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT, max_age=1800)
    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 400

    if request.method == 'GET':
        # Serve the reset password page
        try:
            return send_from_directory(FRONTEND_PATH, 'createnewpassword.html')
        except FileNotFoundError:
            return jsonify({"error": "Reset password page not found"}), 404

    # Handle POST request: Process new password
    try:
        data = request.json

        new_password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate password fields
        if not new_password or not confirm_password:
            return jsonify({"error": "Both password fields are required"}), 400

        if new_password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        # Update the user's password
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"message": "Password reset successfully!"}), 200

    except Exception as e:
        print(f"Error during password reset: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
# Dashboard
@main.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Serve the dashboard page or JSON data."""
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
    try:
        return send_from_directory(frontend_path, 'dashboard.html')
    except FileNotFoundError:
        return jsonify({'error': 'Dashboard page not found.'}), 404

# Account Management
@main.route('/api/dashboard/accounts', methods=['GET'])
def list_linked_accounts():
    """Return a list of accounts linked to the authenticated user."""
    accounts = user_get_accounts()  # Assumes user is authenticated
    return jsonify({'accounts': accounts})

@main.route('/api/dashboard/accounts/link', methods=['POST'])
def link_new_account():
    """Link a new account to the authenticated user."""
    data = request.json
    account_name = data.get('account_name')
    account_id = data.get('account_id')

    if not account_name or not account_id:
        return error_response('Account name and ID are required', 400)

    if link_account(account_name, account_id):
        return jsonify({'message': 'Account linked successfully'}), 201
    else:
        return error_response('Failed to link account', 500)

# Calendar Routes
@main.route('/api/dashboard/calendar/reminder', methods=['POST'])
def create_reminder_route():
    """Endpoint to create a reminder."""
    try:
        data = request.json
        reminder_date = data.get('reminder_date')
        reminder_message = data.get('reminder_message')

        if not reminder_date or not reminder_message:
            return error_response('Both date and message are required', 400)

        reminder = Reminder(
            date=datetime.strptime(reminder_date, '%Y-%m-%d'),
            text=reminder_message
        )
        db.session.add(reminder)
        db.session.commit()

        return jsonify({'message': 'Reminder created successfully!'}), 201

    except Exception as e:
        return error_response(f"Error creating reminder: {str(e)}", 500)


@main.route('/api/dashboard/calendar/reminders', methods=['GET'])
def get_reminders_by_date():
    """Fetch reminders for a specific month and year."""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        if not year or not month:
            return error_response('Year and month are required', 400)

        reminders = Reminder.query.filter(
            db.extract('year', Reminder.date) == year,
            db.extract('month', Reminder.date) == month
        ).all()

        return jsonify([
            {'id': r.id, 'text': r.text, 'date': r.date.strftime('%Y-%m-%d')}
            for r in reminders
        ]), 200

    except Exception as e:
        return error_response(f"Error fetching reminders: {str(e)}", 500)


@main.route('/api/savings-expenses', methods=['GET'])
def savings_expenses():
    data = {
        "labels": ["January", "February", "March", "April", "May"],
        "expenses": [500, 700, 300, 400, 600],
        "savings": [1000, 800, 1200, 1000, 900]
    }
    return jsonify(data)

# Profile Route
@main.route('/api/profile', methods=['GET'])
def serve_profile_page():
    return send_from_directory(FRONTEND_PATH, 'profile.html')

@main.route('/api/profile/edit', methods=['GET'])
def serve_edit_profile_page():
    return send_from_directory(FRONTEND_PATH, 'edit_profile.html')


# Transactions
@main.route('/api/transactions', methods=['GET'])
def transactions():
    return send_from_directory(FRONTEND_PATH, 'Transactions.html')

transactions = [
    {"date": "2024-01-01", "amount": 500, "recipient": "Amazon", "status": "Completed"},
    {"date": "2024-02-01", "amount": 700, "recipient": "Netflix", "status": "Pending"},
    {"date": "2024-03-01", "amount": 300, "recipient": "Spotify", "status": "Completed"}
]
@main.route('/api/transaction', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

@main.route('/api/add-transaction', methods=['POST'])
def add_transaction():
    new_transaction = request.json
    transactions.append(new_transaction)
    return jsonify({"message": "Transaction added successfully"})

@main.route('/api/savings-expenses', methods=['GET'])
def get_savings_expenses():
    labels = [t["date"] for t in transactions]
    expenses = [t["amount"] for t in transactions]
    savings = [1000 - e for e in expenses]  # Example calculation
    return jsonify({"labels": labels, "expenses": expenses, "savings": savings})

# Budgeting
@main.route('/api/budgeting', methods=['GET'])
def budgeting():
    return send_from_directory(FRONTEND_PATH, 'Budgeting.html')

@main.route('/api/budgeting/custom_budget', methods=['PUT'])
def custom_budget():
    return user_custom_budget()

# Budgeting Plans
@main.route('/api/budgeting/plan/1', methods=['GET'])
def budgeting_plan_one():
    return user_plan_one()

@main.route('/api/budgeting/plan/2', methods=['GET'])
def budgeting_plan_two():
    return user_plan_two()

@main.route('/api/budgeting/plan/3', methods=['GET'])
def budgeting_plan_three():
    return user_plan_three()


# Contact
@main.route('/api/contact', methods=['GET'])
def contact():
    return send_from_directory(FRONTEND_PATH, 'Contact.html')

@main.route('/api/contact/message', methods=['POST'])
def message_route():
    """Send a message with a specific type (Request, Message, Complaint)."""
    data = request.get_json()
    message_type = data.get('type')
    message_content = data.get('message')

    if not message_type or not message_content:
        return error_response('Both type and message are required', 400)

    valid_types = ['Request', 'Message', 'Complaint']
    if message_type not in valid_types:
        return error_response(f'Invalid message type. Valid types are: {", ".join(valid_types)}', 400)

    success = send_message(message_type, message_content)

    if success:
        return jsonify({'message': 'Your message has been sent successfully'}), 200
    else:
        return error_response('Failed to send message', 500)

# Chatbot
chatbot_instance = Chatbot()

@main.route('/api/chat', methods=['POST'])
def chat_with_bot():
    data = request.get_json()
    return chatbot_instance.get_response(data)