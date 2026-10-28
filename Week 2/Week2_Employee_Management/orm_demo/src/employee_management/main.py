"""Application entry point for employee management."""

import logging

from sqlalchemy.exc import SQLAlchemyError

from employee_management.cli import run_cli
from employee_management.database import engine
from employee_management.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Initialize and run the employee management application."""

    setup_logging()

    try:
        with engine.connect():
            logger.info("Connected to PostgreSQL.")

        run_cli(engine)

    except (SQLAlchemyError, RuntimeError):
        logger.exception("Could not initialize the database connection.")
        print("Could not connect to PostgreSQL. Check your settings.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
