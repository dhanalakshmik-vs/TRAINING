
"""Configure application logging."""

import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "employee_orm.log"


def setup_logging() -> None:
    """Configure logging to write application events to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )
