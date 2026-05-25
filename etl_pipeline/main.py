import config as c
import extract_transform as el
import db_manager as dbm
import logging

logger = logging.getLogger(__name__)


def main() -> None:

    logger.info("_" * 30)
    logger.info("Finance analytics pipeline started")
    conf = c.get_conf()
    raw_data = el.extract_data(conf["filename"])
    clean_data = el.transactions_cleaning(raw_data)
    dbm.setup_database(conf)
    dbm.data_loading(clean_data, conf)
    dbm.run_sql_file("modeling/transactions_main_table.sql", conf)
    dbm.run_sql_file("modeling/transactions_upsert.sql", conf)
    dbm.run_sql_file("modeling/date_dimension.sql", conf)
    dbm.run_sql_file("modeling/v_date_dimension.sql", conf)
    dbm.run_sql_file("modeling/v_balance.sql", conf)
    dbm.run_sql_file("modeling/v_transaction_master.sql", conf)
    logger.info("Finance analytics pipeline finished")
    logger.info("_" * 30)


if __name__ == "__main__":
    main()
