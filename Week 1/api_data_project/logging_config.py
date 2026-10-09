
import logging

def setup_logging() -> None:
    """Configure application logging to write messages to app.log."""
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )