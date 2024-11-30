from flask import current_app

print("Secret Key:", current_app.app.config['SECRET_KEY'])
