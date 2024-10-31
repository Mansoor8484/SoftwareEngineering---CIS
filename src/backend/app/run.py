from .init import create_app
from .models import db

app = create_app()

with app.app_context():
    db.create_all()  # Create the database tables

if __name__ == "__main__":
    app.run(debug=True)

# $env:FLASK_APP="backend.app.run"; $env:PYTHONPATH="src"; flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade