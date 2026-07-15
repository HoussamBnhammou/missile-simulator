from flask import Flask
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from database import configure_database
from routes.expenses import expenses_bp
from database import db

app = Flask(__name__)

configure_database(app)

app.register_blueprint(expenses_bp)

# database connection
with app.app_context():
    try:
        result = db.session.execute(text("SELECT current_database()"))
    except OperationalError as exc:
        raise ConnectionError("Database is not connected, If you want to run the app without database connection please comment the database connection from main.tf") from exc
    print("Connected to:", result.scalar())

if __name__ == "__main__":
    app.run(debug=True)
