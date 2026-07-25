from interfaces import Extractor
from logging import getLogger
from pandas import DataFrame, read_csv
from os import environ

logger = getLogger(__name__)

class CSVExtractor(Extractor):

    def __init__(self, file_path: str = environ.get("filename"), separator: str = ";") -> None:

        self.file_path = file_path
        self.separator = separator

    def extract(self) -> DataFrame:
        """
        Fetch data from .csv file.

        Returns:
            DataFrame: Containing the data of the .csv file.
        """

        try:
            df = read_csv(self.file_path, sep=self.separator)

        except:
            logger.exception("Couldn't extract data.")
            raise

        else:
            logger.info("Data extracted successfully.")
            return df