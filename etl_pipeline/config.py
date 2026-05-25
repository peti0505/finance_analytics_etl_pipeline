import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging

root_log = logging.getLogger()
root_log.setLevel(logging.INFO)
formatting = logging.Formatter(
    "%(asctime)s--%(levelname)s--%(name)s--%(funcName)s--%(message)s"
)
file = logging.FileHandler("python_logs/data_cleaning.log")
file.setFormatter(formatting)
root_log.addHandler(file)

console_log = logging.StreamHandler()
console_log.setFormatter(formatting)
root_log.addHandler(console_log)

logger = logging.getLogger(__name__)


def get_conf() -> dict:
    """
    Fetch the variables from .env file.

    Returns:
        dict: Containing .csv filepath and database configurations.
    """

    try:
        load_dotenv()
        conf = {
            "filename": os.environ.get("filename"),
            "server_name": os.environ.get("db_server", "localhost\\SQLEXPRESS"),
            "db_name": os.environ.get("db_name", "finance_project"),
            "db_user": os.environ.get("db_login_name"),
            "db_passw": os.environ.get("db_login_passw"),
            "engine": create_engine(
                f"mssql+pyodbc://{os.environ.get("db_user")}:{os.environ.get("db_passw")}@localhost\\SQLEXPRESS/{os.environ.get("db_name")}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
            ),
        }

    except:
        logger.exception("Couldn't read .env file.")
        raise

    else:
        logger.info("Config read successfully from .env file.")
        return conf
