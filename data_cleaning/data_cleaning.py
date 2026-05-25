import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from pandas.util import hash_pandas_object
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatting = logging.Formatter(
    "%(asctime)s--%(levelname)s--%(name)s--%(funcName)s--%(message)s"
)
file = logging.FileHandler("python_logs/data_cleaning.log")
file.setFormatter(formatting)
logger.addHandler(file)

console_log = logging.StreamHandler()
console_log.setFormatter(formatting)
logger.addHandler(console_log)


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
            "engine": sa.create_engine(
                f"mssql+pyodbc://{os.environ.get("db_user")}:{os.environ.get("db_passw")}@localhost\\SQLEXPRESS/{os.environ.get("db_name")}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
            ),
        }

    except:
        logger.exception("Couldn't read .env file.")
        raise

    else:
        logger.info("Config read successfully from .env file.")
        return conf


def extract_data(file_path: str) -> pd.DataFrame:
    """
    Fetch data from .csv file.

    Args:
        file_path (str): Containing the path for the .csv file.

    Returns:
        pd.DataFrame: Containing the data of the .csv file.
    """

    try:
        df = pd.read_csv(file_path, sep=";")

    except Exception as e:
        logger.exception("Couldn't extract data.")
        raise

    else:
        logger.info("Data extracted successfully.")
        return df


def transactions_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the DataFrame containing the transactions.

    Args:
        df (pd.DataFrame): Containing the transactions.

    Returns:
        pd.DataFrame: Containing the transformed and cleaned transactions.
    """

    try:
        df = df.drop_duplicates()

        # Deleted redundant columns and switched to english names for readability
        df.drop(
            columns=[
                "Pénznem",
                "Könyvelés dátuma",
                "Bejövő/Kimenő",
                "Számla név",
                "Számla szám",
            ],
            inplace=True,
        )
        df.columns = [
            "Transaction_date",
            "Type",
            "Partner_name",
            "Partner_account",
            "Spending_category",
            "Description",
            "Amount",
        ]

        # Had to format for appropriate data types
        df["Amount"] = df["Amount"].str.replace(",", ".").str.replace(" ", "")
        df["Amount"] = df["Amount"].astype(float)

        df["Transaction_date"] = pd.to_datetime(
            df["Transaction_date"], format="%Y-%m-%d %H:%M:%S"
        )
        df.sort_values("Transaction_date", inplace=True, ignore_index=True)
        df.insert(1, "Date_only", df["Transaction_date"].dt.date)

        # Switched Nulls to Unknown in case of future use in visualization
        df["Partner_account"] = df["Partner_account"].fillna("Unknown")
        df["Partner_account"] = df["Partner_account"].astype(str)

        # Description column had some HTML spacing
        df["Description"] = df["Description"].str.replace("&nbsp;", " ")

        df.insert(
            1,
            "Transaction_id",
            hash_pandas_object(df, index=False).values.view("int64"),
        )
        df = df.set_index("Transaction_id")

    except:
        logger.exception("Data cleaning failed.")
        raise

    else:
        logger.info("Data cleaning was successful.")
        return df


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


def main() -> None:
    logger.info("_" * 30)
    logger.info("Finance analytics pipeline started")
    conf = get_conf()
    raw_data = extract_data(conf["filename"])
    clean_data = transactions_cleaning(raw_data)
    setup_database(conf)
    data_loading(clean_data, conf)
    run_sql_file("data_modeling/transactions_main_table.sql", conf)
    run_sql_file("data_modeling/transactions_upsert.sql", conf)
    run_sql_file("data_modeling/date_dimension.sql", conf)
    run_sql_file("data_modeling/v_date_dimension.sql", conf)
    run_sql_file("data_modeling/v_balance.sql", conf)
    run_sql_file("data_modeling/v_transaction_master.sql", conf)
    logger.info("Finance analytics pipeline finished")
    logger.info("_" * 30)


if __name__ == "__main__":
    main()
