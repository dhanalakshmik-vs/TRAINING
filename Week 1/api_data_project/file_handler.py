
import csv
import json
import logging

logger = logging.getLogger(__name__)

def save_to_json(data: list[dict]) -> None:
    """Save transformed user data to a JSON file."""
    try:
        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Data saved to users.json successfully.")
        logger.info("Data saved to users.json successfully.")

    except OSError:
        print("Error saving JSON file.")
        logger.exception("Failed to save users.json.")


def save_to_csv(data: list[dict]) -> None:
    """Save transformed user data to a CSV file."""
    try:
        with open(
            "users.csv", "w", newline="", encoding="utf-8"
        ) as file:
            fieldnames = ["id", "name", "email", "city"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)

        print("Data saved to users.csv successfully.")
        logger.info("Data saved to users.csv successfully.")

    except OSError:
        print("Error saving CSV file.")
        logger.exception("Failed to save users.csv.")