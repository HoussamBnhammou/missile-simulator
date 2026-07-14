import os
from dotenv import load_dotenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

db = SQLAlchemy()
SCHEMA_NAME = os.getenv("SCHEMA_NAME", "shared_expenses")


def _required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise RuntimeError(f"Missing required environment variable: {' or '.join(names)}")












def configure_database(app) -> None:
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=_required_env("DB_USER"),
        password=_required_env("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=_required_env("DB_NAME"),
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "options": f"-csearch_path={SCHEMA_NAME},public",
        },
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)