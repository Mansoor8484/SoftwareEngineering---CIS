from flask import Blueprint, jsonify, request
from .chatbot import Chatbot
from controllers import (register as user_register, user_login, user_get_accounts, user_custom_budget, \
                         user_plan_one, user_plan_two, user_plan_three, send_message, user_profile, \
                         edit_user_profile, user_logout, user_account_transactions, user_filter_transactions, \
                         user_add_transaction, user_get_all_transactions, user_transaction_detail, \
                         user_delete_manual_transaction)

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

# Authentication Routes
@main.route('/api/auth/register', methods=['POST'])
def register_route():
    return user_register()

@main.route('/api/auth/login', methods=['POST'])
def login_route():
    return user_login()

@main.route('/api/auth/logout', methods=['POST'])
def logout(user_id):
    return user_logout(user_id)

# Dashboard
@main.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify({'message': 'Dashboard - Template Coming SOOOOOOOON'})

@main.route('/api/accounts', methods=['GET'])
def get_user_accounts():
    """Get a list of accounts for the authenticated user."""
    return user_get_accounts()  # Implement this function in your controller

# Profile Management
@main.route('/api/profile/<int:user_id>', methods=['GET'])
def user_profile_route(user_id):
    return user_profile(user_id)

@main.route('/api/profile/<int:user_id>/edit', methods=['PUT'])
def edit_profile(user_id):
    return edit_user_profile(user_id)

# Transactions Management
@main.route('/api/transactions', methods=['GET'])
def transactions():
    """Get a list of all transactions."""
    return user_get_all_transactions()

@main.route('/api/transactions/filter', methods=['GET'])
def filter_transactions():
    """Filter transactions based on query parameters."""
    # Extract query parameters
    date = request.args.get('date')
    pay_to = request.args.get('pay_to')
    amount = request.args.get('amount', type=float)
    status = request.args.get('status')

    return user_filter_transactions(date, pay_to, amount, status)

@main.route('/api/transactions/<int:account_id>', methods=['GET'])
def account_transactions(account_id):
    """Get all transactions for a specific account."""
    return user_account_transactions(account_id)

@main.route('/api/transactions/<int:account_id>/add', methods=['POST'])
def manual_transaction(account_id):
    """Add a new manual transaction to a specific account."""
    return user_add_transaction(account_id)

@main.route('/api/transactions/<int:account_id>/<int:transaction_id>', methods=['GET'])
def transaction_detail(account_id, transaction_id):
    """Get details for a specific transaction of a specific account."""
    return user_transaction_detail(account_id, transaction_id)

@main.route('/api/transactions/<int:account_id>/delete/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(account_id, transaction_id):
    """Delete a specific transaction from an account, only if it was manually inputted."""
    return user_delete_manual_transaction(account_id, transaction_id)

# Budgeting
@main.route('/api/budgeting', methods=['GET'])
def budgeting():
    return jsonify({'message': 'Budgeting - Template Coming SOOOOOOON'})

@main.route('/api/budgeting/custom_budget', methods=['PUT'])
def custom_budget():
    return user_custom_budget()

@main.route('/api/budgeting/financial_plan/<int:plan_id>', methods=['GET'])
def financial_plan(plan_id):
    plans = {
        1: user_plan_one,
        2: user_plan_two,
        3: user_plan_three
    }
    plan_function = plans.get(plan_id)
    if plan_function:
        return plan_function()
    return jsonify({'error': 'Plan not found'}), 404

# Contact
@main.route('/api/contact', methods=['GET'])
def contact():
    return jsonify({'message': 'Contact - Template Coming SOOOOOOON'})

@main.route('/api/contact/message', methods=['POST'])
def message_route():
    return send_message()

# Chatbot
chatbot_instance = Chatbot()


@main.route('/api/chat', methods=['POST'])
def chat_with_bot():
    """Interact with the chatbot using user input."""
    data = request.get_json()

    if 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    user_message = data['message']
    response = chatbot_instance.get_response(user_message)

    return jsonify({'response': response})
