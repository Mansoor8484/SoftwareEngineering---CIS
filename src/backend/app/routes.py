from flask import Blueprint, request, jsonify, redirect, url_for, render_template, send_from_directory
import os
from itsdangerous import URLSafeTimedSerializer
from .chatbot import Chatbot
from .config import Config
from .models import db, User
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
def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code

@main.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the frontend folder."""
    return send_from_directory(FRONTEND_PATH, filename)

@main.route('/static/walletwizard.png', methods=['GET'])
def serve_walletwizard():
    """Serve walletwizard.png."""
    return send_from_directory(FRONTEND_PATH, 'walletwizard.png')

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

        # Call the user_login function to authenticate the user
        response, status_code = user_login({'username': username, 'password': password})
        return response, status_code

    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

@main.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log the user out."""
    user_id = request.json.get('user_id')
    if not user_id:
        return error_response("User ID is required", 400)
    return user_logout(user_id)

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
    data = request.json
    return create_reminder(data)

@main.route('/api/dashboard/calendar/reminders', methods=['GET'])
def get_reminders_by_date():
    """Fetch reminders for a specific month and year."""
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    return get_reminders_for_month_and_year(year, month)

# Transactions Graph
@main.route('/api/dashboard/transactions/graph', methods=['GET'])
def transaction_graph_route():
    """Get transaction graph by type."""
    transaction_type = request.args.get('type', type=str)
    graph_type = request.args.get('graph_type', type=str, default='bar')
    return transactions_graph(transaction_type, graph_type)

# Profile Management
@main.route('/api/profile/<int:user_id>', methods=['GET'])
def user_profile_route(user_id):
    return user_profile(user_id)

@main.route('/api/profile/<int:user_id>/edit', methods=['PUT'])
def edit_profile(user_id):
    return edit_user_profile(user_id)

# Transactions
@main.route('/api/transactions', methods=['GET'])
def transactions():
    return user_get_all_transactions()

@main.route('/api/transactions', methods=['POST'])
def add_transaction():
    """Add a new transaction to the user's account."""
    data = request.json
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')
    transaction_date = data.get('transaction_date')  # e.g. "2024-11-01T15:30:00"
    account_id = data.get('account_id')

    if not amount or not transaction_type or not transaction_date or not account_id:
        return error_response('Missing required transaction data', 400)

    success = user_add_transaction(account_id, amount, transaction_type, transaction_date)

    if success:
        return jsonify({'message': 'Transaction added successfully'}), 201
    else:
        return error_response('Failed to add transaction', 500)

@main.route('/api/transactions/details/<int:transaction_id>', methods=['GET'])
def transaction_details(transaction_id):
    return user_transaction_details(transaction_id)

# Filter Transactions
@main.route('/api/transactions/filter/<int:user_id>', methods=['GET'])
def filter_transactions(user_id):
    filter_params = request.args.to_dict()  # Parse query parameters to dictionary
    return user_filter_transactions(user_id, filter_params)

# Delete Manual Transaction
@main.route('/api/transactions/delete/<int:transaction_id>', methods=['DELETE'])
def delete_manual_transaction(transaction_id):
    return user_delete_manual_transaction(transaction_id)

# Budgeting
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
    return jsonify({'message': 'Contact - Template Coming SOOOOOOON'})

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