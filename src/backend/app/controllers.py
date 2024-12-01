from flask import jsonify, request, current_app
from .models import db, User, BankAccount, Transaction, Reminder, Budget, Message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta
from .chatbot import Chatbot
import matplotlib.pyplot as plt
import io
import base64

# ================================
# Utility Functions
# ================================

SECRET_KEY = "68d2374fc6aaaa84349a78ce5af4aaef50110b0b2df8592d2315f976944f9dc5"  # Replace with your secret key

def generate_token(user):
    """Generate a JSON Web Token for the user."""
    try:
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None


def error_response(message, status_code=400):
    """Error response helper function."""
    return jsonify({'error': message}), status_code


# ================================
# User Authentication
# ================================

def user_register(data):
    """Register a new user."""
    try:
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Validate input fields
        if not username or not email or not password:
            return jsonify({"error": "All fields are required."}), 400

        # Check for existing user
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists."}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists."}), 409

        # Create and save user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        # Return success response
        return jsonify({
            "message": "User registered successfully.",
            "user_id": new_user.id,
            "token": generate_token(new_user)
        }), 201

    except Exception as e:
        # Log errors for debugging
        print("Error in user_register:", str(e))
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

def user_login(data):
    """Authenticate user and return token."""
    try:
        username = data.get('username')
        password = data.get('password')

        print("Authenticating user:", username)

        # Query user from database
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Generate token
        token = generate_token(user)
        if not token:
            return jsonify({"error": "Failed to generate token"}), 500

        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        print(f"Error in user_login: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

def user_logout(user_id):
    """Logout user."""
    # Here you could invalidate a JWT token or remove sessions if using sessions
    return jsonify({'message': 'Logged out successfully'}), 200

def send_password_reset_email(email):
    # Assuming you have a way to send a reset email (e.g., using Flask-Mail)
    user = User.query.filter_by(email=email).first()
    if user:
        # Send email logic here
        return True
    return False

def reset_password(token, new_password):
    # Assuming you have a method to verify the token and reset the password
    try:
        decoded_token = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        user = User.query.get(decoded_token['user_id'])
        if user:
            user.set_password(new_password)
            db.session.commit()
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except Exception as e:
        return False

# ================================
# User Profile & Account Management
# ================================

def user_profile(user_id):
    """Get user profile information."""
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)

        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 200

    except Exception as e:
        return error_response(f'Error fetching user profile: {str(e)}', 500)


def edit_user_profile(user_id):
    """Edit user profile (username, email, password)."""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        new_username = data.get('username')
        new_email = data.get('email')
        new_password = data.get('password')

        if new_username and new_username != user.username:
            user.username = new_username  # Update username

        if new_email and new_email != user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                return jsonify({'error': 'Email is already in use'}), 400
            user.email = new_email  # Update email

        if new_password:
            user.set_password(new_password)  # Update password

        db.session.commit()

        return jsonify({'message': 'User profile updated successfully'}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error, please try again'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


def user_get_accounts(user_id):
    """Get all bank accounts linked to a user."""
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)

        accounts = BankAccount.query.filter_by(user_id=user.id).all()
        return jsonify([{
            'account_id': account.id,
            'account_name': account.name,
            'balance': account.balance
        } for account in accounts]), 200

    except Exception as e:
        return error_response(f'Error fetching accounts: {str(e)}', 500)


def link_account(account_name, account_id, user_id):
    """Link a new bank account to a user."""
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)

        account = BankAccount(name=account_name, account_id=account_id, user_id=user.id)
        db.session.add(account)
        db.session.commit()
        return jsonify({'message': 'Account linked successfully'}), 201

    except Exception as e:
        return error_response(f'Error linking account: {str(e)}', 500)


# ================================
# Transactions
# ================================

def user_add_transaction(account_id, amount, transaction_type, transaction_date):
    """Add a new transaction for a user."""
    try:
        transaction = Transaction(
            account_id=account_id,
            amount=amount,
            transaction_type=transaction_type,
            transaction_date=datetime.strptime(transaction_date, '%Y-%m-%dT%H:%M:%S')
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction added successfully', 'transaction_id': transaction.id}), 201
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error adding transaction: {str(e)}', 500)


def user_get_all_transactions(user_id):
    """Get all transactions for a user."""
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)

        transactions = Transaction.query.filter_by(user_id=user.id).all()
        return jsonify([{
            'transaction_id': t.id,
            'account_id': t.account_id,
            'amount': t.amount,
            'transaction_type': t.transaction_type,
            'transaction_date': t.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
        } for t in transactions]), 200

    except Exception as e:
        return error_response(f'Error fetching transactions: {str(e)}', 500)

def user_transaction_details(transaction_id):
    try:
        # Query the transaction by ID (adjust according to your DB model)
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return error_response(f"Transaction with ID {transaction_id} not found.", 404)

        # You can modify this to return the necessary details, depending on your transaction model
        transaction_data = {
            'transaction_id': transaction.id,
            'amount': transaction.amount,
            'transaction_type': transaction.transaction_type,
            'date': transaction.date,
            'account_id': transaction.account_id,
            'description': transaction.description,  # If applicable
            'status': transaction.status  # If applicable
        }

        return jsonify({'transaction': transaction_data})

    except Exception as e:
        return error_response(f"Error fetching transaction details: {str(e)}", 500)

# Filter transactions for a user
def user_filter_transactions(user_id, filter_params):
    try:
        # Assuming the filter_params is a dict with 'date_range', 'transaction_type', etc.
        transactions = Transaction.query.filter_by(user_id=user_id)

        if filter_params.get('transaction_type'):
            transactions = transactions.filter_by(transaction_type=filter_params['transaction_type'])

        if filter_params.get('start_date') and filter_params.get('end_date'):
            start_date = datetime.strptime(filter_params['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(filter_params['end_date'], "%Y-%m-%d")
            transactions = transactions.filter(Transaction.transaction_date.between(start_date, end_date))

        filtered_transactions = transactions.all()

        transaction_data = [
            {
                'transaction_id': txn.id,
                'amount': txn.amount,
                'transaction_type': txn.transaction_type,
                'transaction_date': txn.transaction_date,
                'account_id': txn.account_id
            } for txn in filtered_transactions
        ]

        return jsonify(transaction_data)
    except Exception as e:
        return error_response(f"Error filtering transactions: {str(e)}", 500)


def user_delete_manual_transaction(transaction_id):
    """Delete a manual transaction."""
    try:
        txn = Transaction.query.get(transaction_id)
        if txn:
            db.session.delete(txn)
            db.session.commit()
            return jsonify({'message': 'Transaction deleted successfully'}), 200
        else:
            return error_response('Transaction not found', 404)
    except Exception as e:
        return error_response(f"Error deleting transaction: {str(e)}", 500)


def transactions_graph(transaction_type=None, graph_type='bar'):
    """Generate a graph of transactions (bar or pie chart)."""
    try:
        query = Transaction.query
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type)

        transactions = query.all()
        data = {}

        for txn in transactions:
            if txn.transaction_type not in data:
                data[txn.transaction_type] = 0
            data[txn.transaction_type] += txn.amount

        types = list(data.keys())
        amounts = list(data.values())

        plt.figure(figsize=(10, 6))

        if graph_type == 'pie':
            plt.pie(amounts, labels=types, autopct='%1.1f%%', startangle=140)
        else:
            plt.bar(types, amounts)

        plt.title(f"Transaction Distribution by Type ({graph_type})")

        # Convert the plot to base64 for API response
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_data = base64.b64encode(img.getvalue()).decode('utf-8')

        return jsonify({'graph': graph_data})
    except Exception as e:
        return error_response(f"Error generating graph: {str(e)}", 500)


# ================================
# Budgeting
# ================================

def user_custom_budget():
    """Set or update a custom budget."""
    try:
        data = request.get_json()
        amount = data.get('amount')
        category = data.get('category')

        if not amount or not category:
            return error_response('Amount and category are required', 400)

        user_id = data.get('user_id')  # Ensure the user is authenticated
        existing_budget = Budget.query.filter_by(user_id=user_id, category=category).first()

        if existing_budget:
            # Update existing budget
            existing_budget.amount = amount
            db.session.commit()
            return jsonify({'message': 'Custom budget updated successfully'}), 200
        else:
            # Create new custom budget
            budget = Budget(user_id=user_id, amount=amount, category=category)
            db.session.add(budget)
            db.session.commit()
            return jsonify({'message': 'Custom budget created successfully'}), 201

    except Exception as e:
        return error_response(f'Error setting custom budget: {str(e)}', 500)

    # Budgeting Plan 1 - Basic Budgeting Plan
def user_plan_one():
    try:
        # You can define a specific budgeting plan structure for plan 1
        plan_data = {
            "plan_name": "Basic Budgeting Plan",
            "budget_categories": {
                "Housing": "30%",
                "Food": "15%",
                "Transportation": "10%",
                "Savings": "10%",
                "Entertainment": "5%",
                "Other": "30%"
            },
            "notes": "This is a basic budgeting plan to help with general expense tracking."
        }
        return jsonify(plan_data)
    except Exception as e:
        return error_response(f"Error fetching plan 1: {str(e)}", 500)

# Budgeting Plan 2 - Intermediate Budgeting Plan
def user_plan_two():
    try:
        plan_data = {
            "plan_name": "Intermediate Budgeting Plan",
            "budget_categories": {
                "Housing": "25%",
                "Food": "10%",
                "Transportation": "15%",
                "Savings": "15%",
                "Entertainment": "5%",
                "Other": "30%"
            },
            "notes": "This plan helps users set aside more for savings while still managing day-to-day expenses."
        }
        return jsonify(plan_data)
    except Exception as e:
        return error_response(f"Error fetching plan 2: {str(e)}", 500)

# Budgeting Plan 3 - Advanced Budgeting Plan
def user_plan_three():
    try:
        plan_data = {
            "plan_name": "Advanced Budgeting Plan",
            "budget_categories": {
                "Housing": "20%",
                "Food": "10%",
                "Transportation": "10%",
                "Savings": "30%",
                "Entertainment": "5%",
                "Other": "25%"
            },
            "notes": "This is an advanced budgeting plan focused on maximizing savings and investments."
        }
        return jsonify(plan_data)
    except Exception as e:
        return error_response(f"Error fetching plan 3: {str(e)}", 500)

# ================================
# Reminders
# ================================

def create_reminder(data):
    """Create a new reminder."""
    try:
        reminder_date = data.get('reminder_date')
        reminder_message = data.get('reminder_message')

        if not reminder_date or not reminder_message:
            return error_response('Missing required fields', 400)

        reminder = Reminder(
            reminder_date=datetime.strptime(reminder_date, '%Y-%m-%d'),
            reminder_message=reminder_message
        )
        db.session.add(reminder)
        db.session.commit()

        return jsonify({'message': 'Reminder created successfully'}), 201

    except Exception as e:
        return error_response(f'Error creating reminder: {str(e)}', 500)


def get_reminders_for_month_and_year(year, month):
    """Get all reminders for a specific month and year."""
    try:
        reminders = Reminder.query.filter(
            db.extract('year', Reminder.reminder_date) == year,
            db.extract('month', Reminder.reminder_date) == month
        ).all()

        return jsonify([{
            'reminder_id': r.id,
            'reminder_message': r.reminder_message,
            'reminder_date': r.reminder_date.strftime('%Y-%m-%d')
        } for r in reminders]), 200

    except Exception as e:
        return error_response(f'Error fetching reminders: {str(e)}', 500)


# ================================
# Chatbot
# ================================

chatbot_instance = Chatbot()

def chat_with_bot(data):
    """Interact with the chatbot."""
    return chatbot_instance.get_response(data)

from datetime import datetime

# ================================
# Messaging
# ================================

def send_message(sender_id, subject, message_content, message_type):
    """Send a message from the user to a designated team email, send an automated response to the user, and include a timestamp."""
    try:
        sender = User.query.get(sender_id)

        if not sender:
            return error_response('Sender not found', 404)

        # The recipient email is the designated team email (e.g., support@company.com)
        recipient_email = 'team@example.com'  # Change to your team or support email

        # Get the current timestamp when the message is sent
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Construct the message to send to the team
        team_message_subject = f'New Message from Contact Page: {subject}'
        team_message_body = f"""
        New message received from {sender.username} ({sender.email}) on {timestamp}:

        Message Type: {message_type}
        Subject: {subject}
        Message: {message_content}

        Timestamp: {timestamp}
        """

        # Send the message to the team email
        send_email(team_message_subject, team_message_body, recipient_email)

        # Send the automated response to the user (to their email address)
        response_subject = 'We Received Your Message'
        response_body = f"""
        Dear {sender.username},

        Thank you for reaching out! We received your message with the following details:

        Subject: {subject}
        Message: {message_content}

        Your message was sent on {timestamp}. Our team will get back to you shortly.

        Best regards,
        Your Support Team
        """

        send_email(response_subject, response_body, sender.email)

        return jsonify({'message': 'Message sent successfully. You will receive a response via email.'}), 201

    except Exception as e:
        return error_response(f'Error sending message: {str(e)}', 500)

def send_email(subject, body, recipient_email):
    """Send an email using Flask-Mail (or any email service)."""
    try:
        # Placeholder for email sending logic
        print(f"Sending email to {recipient_email} with subject: {subject}")
        print(f"Email body:\n{body}")
        # In a real application, integrate email sending service here (e.g., Flask-Mail, SendGrid)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
