from interfaces import DBManager
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from os import environ
from logging import getLogger
from pandas import DataFrame

logger = getLogger(__name__)

class MssqlDB(DBManager):

    def __init__(self, db_user: str = environ.get('db_user'), db_password: str = environ.get('db_passw'), db_name: str = environ.get('db_name')) -> None:

        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.engine = create_engine(
                f"mssql+pyodbc://{self.db_user}:{self.db_password}@mssqlserver/{self.db_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")

    def setup_engine_database(self) -> None:
        """
        Set up the database of the instance if it doesn't exists already.
        """

        try:
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
                logger.info("Database created successully.")

            else:
                logger.info("Database already exists.")

        except:
            logger.exception("Couldn't create database.")
            raise

    def load_data(self, data: DataFrame, table_name: str, if_exists: str) -> None:
        """
        Load the given data to instance database, if failed load it into .csv and .xlsx instead.

        Args:
            data (DataFrame): Contains the data that needs to be loaded.
            table_name (str): Name of the table the data needs to be loaded into.
            if_exists (str): Decides how to laod data if the table already exists.
        """

        try:
            data.to_sql(table_name, self.engine, index=True, if_exists=if_exists)

        except:
            logger.exception("Couldn't write to SQL server, exported to csv and xlsx")
            data.to_csv(f"{table_name}.csv")
            data.to_excel(f"{table_name}.xlsx")

        else:
            logger.info(f"Data loaded successfully into '{table_name}'.")

    def run_sql_file(self, filepath: str) -> None:
        """
        Run a .sql file on the instance database.

        Args:
            filepath (str): Contains the filepath to the .sql file.
        """

        try:
            with open(filepath, "r") as f:
                sql = f.read()

            with self.engine.connect() as connection:
                connection.execute(text(sql))
                connection.commit()

        except:
            logger.exception(f"Couldn't run SQL file ({filepath}).")
            raise

        else:
            logger.info(f"SQL file read successfully ({filepath}).")