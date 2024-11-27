from flask import Blueprint, request, jsonify, redirect, url_for, render_template, send_from_directory
import os
from .controllers import user_register
from .chatbot import Chatbot
from .models import db
from .controllers import (
    user_register, user_login, user_get_accounts, user_custom_budget,
    user_plan_one, user_plan_two, user_plan_three, send_message,
    user_profile, edit_user_profile, user_logout,
    user_filter_transactions, user_add_transaction, user_get_all_transactions,
    user_transaction_details, user_delete_manual_transaction,
    create_reminder, get_reminders_for_month_and_year, transactions_graph,
    link_account, send_password_reset_email, reset_password
)

# Blueprint setup
main = Blueprint('main', __name__)

FRONTEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))

@main.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the frontend folder."""
    return send_from_directory(FRONTEND_PATH, filename)

# Utility function for error handling
def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code

@main.route('/')
def home():
    return redirect(url_for('main.login_route'))
    #return "Welcome to the Software Engineering API! Use the /api/auth/login endpoint to log in."

# Authentication Routes
@main.route('/api/auth/register', methods=['GET', 'POST'])
def register_route():
    """Serve the registration page on GET and process user registration on POST."""
    if request.method == 'GET':
        return send_from_directory(FRONTEND_PATH, 'register.html')

    # POST request: Process user registration
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if not username or not email or not password or not confirm_password:
        return jsonify({'error': 'All fields are required'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Call the user_register controller
    return user_register({
        'username': username,
        'email': email,
        'password': password
    })

@main.route('/api/auth/login', methods=['GET', 'POST'])
def login_route():
    """Handle login page display (GET) and authentication (POST)."""
    if request.method == 'GET':
        return send_from_directory(FRONTEND_PATH, 'login.html')

    # Handle POST requests for login
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # Call the user_login function
    response = user_login(username, password)

    if response.status_code == 200:
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'error': 'Invalid login credentials'}), 401

@main.route('/static/walletwizard.png', methods=['GET'])
def serve_walletwizard():
    """Serve walletwizard.png."""
    return send_from_directory(FRONTEND_PATH, 'walletwizard.png')

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
    """Handle GET to serve the forgot password page and POST for password reset."""
    if request.method == 'GET':
        # Serve the forgotpassword.html file from the frontend folder
        return send_from_directory(FRONTEND_PATH, 'forgotpassword.html')

    # POST request logic: Handle password reset
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if send_password_reset_email(email):
        return jsonify({'message': 'Password reset email sent successfully'}), 200
    else:
        return jsonify({'error': 'Email address not found'}), 404

# Reset Password
@main.route('/api/auth/reset-password', methods=['POST'])
def reset_password_route():
    """Reset the password using the reset token."""
    data = request.json
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return error_response('Token and new password are required', 400)

    if reset_password(token, new_password):
        return jsonify({'message': 'Password reset successfully'}), 200
    else:
        return error_response('Invalid or expired token', 400)

# Dashboard
@main.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify({'message': 'Dashboard - Template Coming SOOOOOOOON'})

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