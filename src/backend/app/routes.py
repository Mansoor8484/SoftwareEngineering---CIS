from flask import Blueprint, render_template
from .controllers import register, user_login

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return 'Dashboard - Template Coming SOOOOOOOON'

@main.route('/transactions')
def transactions():
    return 'Transactions - Template Coming SOOOOOOON'

@main.route('/budgeting')
def budgeting():
    return 'Budgeting - Template Coming SOOOOOOON'

@main.route('/contact')
def contact():
    return 'Contact - Template Coming SOOOOOOON'

@main.route('/register', methods=['POST'])
def register():
    return register()  # Call the controller function

@main.route('/login', methods=['POST'])
def login():
    return user_login()  # Call the controller function

@main.route('/contact/message', methods=['POST'])
def message():
    return message()  # Call the controller function



# Later, when templates are ready
# @main.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html', data=my_data)