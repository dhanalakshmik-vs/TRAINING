
"""Configure application-wide logging for the employee management project."""

import logging

logging.basicConfig(
    filename="employee.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)