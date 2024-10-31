from flask import Blueprint, render_template, request

# Create a blueprint for the main routes
bp = Blueprint('main', __name__)

@bp.route('/index')
def index():
    return render_template("#index paghe")
    

# @main.route('/')
# def home():
#     return render_template('home.html')