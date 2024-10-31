from flask import Blueprint, request, jsonify, render_template
from models import db, User, Transaction, ChatbotInteraction

#initilizing blueporint
controllers = Blueprint('main',__name__)

#route to the register user page
@controllers.route('/registration_page', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')


    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@controllers.route('/login_page', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')

    password = data.get('password')

    user = User.query.filter_by(username=User).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate token (implementation depends on your authentication method)
    token = 'some_generated_token'

    return jsonify({'token': token}), 200
