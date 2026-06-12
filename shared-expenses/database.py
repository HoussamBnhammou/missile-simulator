import oracledb
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

pool = None

##these next 2 functions are not related to the db connection but rather just to resolve the env variables form .env file.
def _required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _resolve_path_from_env(name):
    path = Path(_required_env(name)).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()


def init_db_pool():
    global pool
    wallet_dir = _resolve_path_from_env("TNS_ADMIN")
    wallet_password = os.getenv("WALLET_PASSWORD") or None

    pool = oracledb.create_pool(
        user=_required_env("DB_USER"),
        password=_required_env("DB_PASSWORD"),
        dsn=_required_env("DB_DSN"),
        config_dir=str(wallet_dir),
        wallet_location=str(wallet_dir),
        wallet_password=wallet_password,
        min=1,
        max=10,
        increment=1,
    )


def get_connection():
    if pool == None:
        raise RuntimeWarning("Database connection pool has not been initialized yet")
    else:
        return pool.acquire()
    

def test_db_connection():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM DUAL")
                result = cursor.fetchone()

        return True, result[0]

    except Exception as error:
        return False, str(error)
