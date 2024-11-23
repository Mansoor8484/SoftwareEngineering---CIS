from src.backend.app.init import create_app
from .models import db

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# $env:FLASK_APP="backend.app.run"; $env:PYTHONPATH="src"; flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade