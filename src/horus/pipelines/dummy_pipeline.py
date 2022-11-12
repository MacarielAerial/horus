from logging import Logger


def dummy_pipeline(logger: Logger) -> None:
    logger.info("This is a dry run of an empty pipeline")


if __name__ == "__main__":
    import argparse
    import logging

    from horus.nodes.project_logging import default_logging

    default_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Demonstration of an empty pipeline")

    args = parser.parse_args()

    dummy_pipeline(logger=logger)
