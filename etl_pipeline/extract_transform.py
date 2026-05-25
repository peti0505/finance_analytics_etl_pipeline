import pandas as pd
from pandas.util import hash_pandas_object
import logging

logger = logging.getLogger(__name__)


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
