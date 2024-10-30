from flask import Blueprint, render_template

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/index')
def index():
    return 'Index Page'

# @main.route('/')
# def home():
#     return render_template('home.html')