"""Menu and user interaction for the employee management application."""

from collections.abc import Callable
import logging

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from employee_management.services.employee_service import (
    add_employee,
    list_employees,
    search_employee,
    edit_employee,
    delete_employee,
)

logger = logging.getLogger(__name__)


def run_cli(engine: Engine) -> None:
    """Run the employee management menu."""

    actions: dict[str, Callable[[Engine], None]] = {
        "1": add_employee,
        "2": list_employees,
        "3": search_employee,
        "4": edit_employee,
        "5": delete_employee,
    }

    while True:
        print("\n===== Employee Management CLI =====")
        print("1. Add employee")
        print("2. List employees")
        print("3. Search employee")
        print("4. Edit employee")
        print("5. Delete employee")
        print("6. Exit")

        choice: str = input("Enter your choice: ").strip()

        if choice == "6":
            print("Exiting Employee Management CLI.")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid choice. Select a number from 1 to 6.")
            continue

        try:
            action(engine)
        except ValueError as error:
            logger.warning("Invalid input: %s", error)
            print(f"Invalid input: {error}")
        except IntegrityError:
            logger.exception("A database integrity constraint failed.")
            print("Operation rejected because of a database constraint.")
        except SQLAlchemyError:
            logger.exception("Database operation failed.")
            print("Database operation failed. Check employee_orm.log.")
        except (OSError, EOFError):
            logger.exception("Input or file operation failed.")
            print("An input or file operation failed.")
        except Exception:
            logger.exception("Unexpected application error.")
            print("An unexpected error occurred. Check employee_orm.log.")
