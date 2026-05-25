import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from pandas.util import hash_pandas_object
from dotenv import load_dotenv


def get_conf() -> dict:

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

    return conf


def extract_data(file_path: str) -> pd.DataFrame:

    try:
        df = pd.read_csv(file_path, sep=";")

    except Exception as e:
        print("Couldn't load data, error:", e)
        raise

    return df


def transactions_cleaning(df: pd.DataFrame) -> pd.DataFrame:

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
        1, "Transaction_id", hash_pandas_object(df, index=False).values.view("int64")
    )
    df = df.set_index("Transaction_id")

    return df


def setup_database(conf: dict) -> None:

    if not database_exists(conf["engine"].url):
        create_database(conf["engine"].url)


def data_loading(df: pd.DataFrame, conf: dict) -> None:
    # Extracting to SQL, if failed then extracting into .csv and .xlsx instead
    try:
        df.to_sql("transactions_temp", conf["engine"], index=True, if_exists="replace")

    except Exception as e:
        print("Couldn't write to SQL server, exported to csv and xlsx", e)
        df.to_csv("finance_table_substitution.csv")
        df.to_excel("finance_table.xlsx")


def run_sql_file(filepath: str, conf: dict) -> None:

    with open(filepath, "r") as f:
        sql = f.read()

    with conf["engine"].connect() as connection:
        connection.execute(sa.text(sql))
        connection.commit()


if __name__ == "__main__":
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
