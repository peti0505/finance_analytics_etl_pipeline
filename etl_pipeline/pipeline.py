from dotenv import load_dotenv
load_dotenv()

from interfaces import DBManager, Extractor
from mssqldb import MssqlDB
from csvextractor import CSVExtractor
from transcaction_transform import transactions_transform
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

class Pipeline:

    def __init__(self, extractor: Extractor = CSVExtractor(), database: DBManager = MssqlDB()) -> None:

        self.extractor = extractor
        self.database = database

    def run(self) -> None:

        raw_data = self.extractor.extract()
        clean_data = transactions_transform(raw_data)
        self.database.setup_engine_database()
        self.database.load_data(clean_data, "transactions_temp", "replace")
        self._modeling()

    def _modeling(self) -> None:

        self.database.run_sql_file("modeling/transactions_main_table.sql")
        self.database.run_sql_file("modeling/transactions_upsert.sql")
        self.database.run_sql_file("modeling/date_dimension.sql")
        self.database.run_sql_file("modeling/v_date_dimension.sql")
        self.database.run_sql_file("modeling/v_balance.sql")
        self.database.run_sql_file("modeling/v_transaction_master.sql")