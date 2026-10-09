
import logging
import requests
from file_handler import save_to_csv, save_to_json
from logging_config import setup_logging
from transformer import transform_users
from validators import validate_users

def main() -> None:
    """Fetch, validate, transform, and save API user data."""
    setup_logging()
    logger = logging.getLogger(__name__)

    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        logger.info("API request successful.")

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        logger.exception("API request failed.")
        return

    except ValueError as error:
        print(f"API returned invalid JSON: {error}")
        logger.exception("API returned invalid JSON.")
        return

    errors = validate_users(data)

    if errors:
        print("Validation failed:")
        logger.warning("Validation failed.")

        for error in errors:
            print(f"- {error}")
            logger.warning("%s", error)

        return

    print(f"Validation successful. Received {len(data)} users.")
    logger.info("Validation successful for %d users.", len(data))

    transformed_data = transform_users(data)

    print(
        f"Transformation successful. "
        f"Processed {len(transformed_data)} users."
    )
    logger.info("Transformed %d users.", len(transformed_data))

    save_to_json(transformed_data)
    save_to_csv(transformed_data)


if __name__ == "__main__":
    main()