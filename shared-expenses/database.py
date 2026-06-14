import os
from dotenv import load_dotenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

db = SQLAlchemy()
SCHEMA_NAME = os.getenv("SCHEMA_NAME")


##these next 2 functions are not related to the db connection but rather just to resolve the env variables form .env file.
## this is good for debugging, we should catch if the credential exist or not otherwise. you will get just a vague  db connection failure
def _required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise RuntimeError(f"Missing required environment variable: {' or '.join(names)}")

## resolvine the path of the wallet, in production we should fetch it directly from a vault.
def _resolve_path_from_env(*names):
    path = Path(_required_env(*names)).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()
#############################################


## the database connection engine is stored in the flask app instanciation thanks to the library flask_sqlalchemy/
def configure_database(app):
    wallet_dir = _resolve_path_from_env("DB_WALLET_DIR", "TNS_ADMIN")
    wallet_password = os.getenv("DB_WALLET_PASSWORD") or os.getenv("WALLET_PASSWORD")

    app.config["SQLALCHEMY_DATABASE_URI"] = "oracle+oracledb://"

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "user": _required_env("DB_USER"),
            "password": _required_env("DB_PASSWORD"),
            "dsn": _required_env("DB_DSN"),
            "wallet_location": str(wallet_dir),
            "wallet_password": wallet_password,
        }
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
