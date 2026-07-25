from abc import ABC, abstractmethod
from pandas import DataFrame

class DBManager(ABC):

    @abstractmethod
    def setup_engine_database(self) -> None:

        pass

    @abstractmethod
    def load_data(self, data: DataFrame, table_name: str, if_exists: str) -> None:

        pass

    @abstractmethod
    def run_sql_file(self, filepath: str) -> None:

        pass

class Extractor(ABC):

    @abstractmethod
    def extract(self) -> DataFrame:

        pass