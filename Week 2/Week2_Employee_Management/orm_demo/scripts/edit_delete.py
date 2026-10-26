
"""Provide a CLI to edit or delete an employee."""

from getpass import getpass

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from employee_management.models import Employee


def main() -> None:
    """Connect to PostgreSQL and edit or delete an employee."""
    password: str = getpass("Enter PostgreSQL password: ")

    database_url: URL = URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_demo",
    )

    engine: Engine = create_engine(database_url)

    try:
        employee_id: str = input("Enter employee ID: ").strip()

        with Session(engine) as session:
            with session.begin():
                employee: Employee | None = session.get(
                    Employee, employee_id
                )

                if employee is None:
                    print("Employee not found.")
                    return

                print(
                    f"Current details: {employee.name}, "
                    f"age {employee.age}, salary {employee.salary}"
                )

                action: str = input(
                    "Choose edit or delete: "
                ).strip().lower()

                if action == "edit":
                    print("\nWhich field do you want to update?")
                    print("1. Name")
                    print("2. Age")
                    print("3. Salary")

                    choice: str = input("Enter your choice: ").strip()

                    if choice == "1":
                        new_name: str = input(
                            "Enter new name: "
                        ).strip()

                        if not new_name:
                            raise ValueError("Name cannot be empty.")

                        employee.name = new_name

                    elif choice == "2":
                        new_age: int = int(
                            input("Enter new age: ")
                        )

                        if not 20 <= new_age <= 60:
                            raise ValueError(
                                "Age must be between 20 and 60."
                            )

                        employee.age = new_age

                    elif choice == "3":
                        new_salary: float = float(
                            input("Enter new salary: ")
                        )

                        if new_salary <= 0:
                            raise ValueError(
                                "Salary must be positive."
                            )

                        employee.salary = new_salary

                    else:
                        print("Invalid field choice.")
                        return

                    print("Employee updated successfully.")

                elif action == "delete":
                    confirm: str = input(
                        "Type YES to confirm deletion: "
                    ).strip().upper()

                    if confirm == "YES":
                        session.delete(employee)
                        print("Employee deleted successfully.")
                    else:
                        print("Deletion cancelled.")

                else:
                    print("Invalid action. Choose edit or delete.")

    except (ValueError, TypeError) as error:
        print(f"Invalid input: {error}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
