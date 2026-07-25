from pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)

def main() -> None:

    logger.info("_" * 30)
    logger.info("Finance analytics pipeline started")
    pipeline = Pipeline()
    pipeline.run()
    logger.info("Finance analytics pipeline finished")
    logger.info("_" * 30)


if __name__ == "__main__":
    main()