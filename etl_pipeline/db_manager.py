import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def setup_database(conf: dict) -> None:
    """
    Set up database from the .env if it doesn't exists already.

    Args:
        conf (dict): The dict containing .csv filepath and database configurations.
    """

    try:
        if not database_exists(conf["engine"].url):
            create_database(conf["engine"].url)
            logger.info("Database created successully.")

        else:
            logger.info("Database already exists.")

    except:
        logger.exception("Couldn't create database.")
        raise


def data_loading(df: pd.DataFrame, conf: dict) -> None:
    """
    Load the data to database, if failed load it into .csv and .xlsx instead.

    Args:
        df (pd.DataFrame): Contains the cleaned transactions data.
        conf (dict): The dict containing the configurating data and authentications.
    """

    try:
        df.to_sql("transactions_temp", conf["engine"], index=True, if_exists="replace")

    except:
        logger.exception("Couldn't write to SQL server, exported to csv and xlsx")
        df.to_csv("transaction_temp_substitution.csv")
        df.to_excel("transaction_temp.xlsx")


def run_sql_file(filepath: str, conf: dict) -> None:
    """
    Run a .sql file.

    Args:
        filepath (str): Contains the filepath to the .sql file.
        conf (dict): The dict containing .csv filepath and database configurations.
    """

    try:
        with open(filepath, "r") as f:
            sql = f.read()

        with conf["engine"].connect() as connection:
            connection.execute(sa.text(sql))
            connection.commit()

    except:
        logger.exception(f"Couldn't run SQL file ({filepath}).")
        raise

    else:
        logger.info(f"SQL file read successfully ({filepath}).")
