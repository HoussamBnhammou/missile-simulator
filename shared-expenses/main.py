from flask import Flask
from database import configure_database
from routes.expenses import expenses_bp


app = Flask(__name__)

configure_database(app)

app.register_blueprint(expenses_bp)


if __name__ == "__main__":
    app.run(debug=True)