
"""Import employee records from the Week 1 JSON file."""

import json
import sys
from decimal import Decimal, InvalidOperation
from getpass import getpass
from pathlib import Path

from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session

from models import Department, Employee


JSON_FILE = Path(__file__).resolve().parent.parent / "employee.json"


def get_database_url():
    password = getpass("Enter PostgreSQL password: ")

    return URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_demo",
    )


def validate_employee(record, row_number):
    """Validate and convert one JSON record."""

    if not isinstance(record, dict):
        raise ValueError(f"Record {row_number} must be a JSON object.")

    required = {"id", "name", "age", "department", "salary"}

    missing = required - record.keys()
    if missing:
        raise ValueError(
            f"Record {row_number} is missing: {', '.join(sorted(missing))}"
        )

    employee_id = record["id"]
    name = record["name"]
    department_name = record["department"]

    if (
        not isinstance(employee_id, str)
        or not employee_id.startswith("EMP")
        or not employee_id[3:].isdigit()
    ):
        raise ValueError(f"Record {row_number} has an invalid employee ID.")

    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Record {row_number} has an invalid name.")

    if (
        not isinstance(department_name, str)
        or not department_name.strip()
    ):
        raise ValueError(f"Record {row_number} has an invalid department.")

    age = record["age"]
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValueError(f"Record {row_number} age must be an integer.")

    if not 20 <= age <= 60:
        raise ValueError(f"Record {row_number} age must be between 20 and 60.")

    try:
        salary = Decimal(str(record["salary"]))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError(
            f"Record {row_number} has an invalid salary."
        ) from error

    if not salary.is_finite() or salary <= 0:
        raise ValueError(f"Record {row_number} salary must be positive.")

    if salary.as_tuple().exponent < -2:
        raise ValueError(
            f"Record {row_number} salary cannot have more than 2 decimals."
        )

    salary = salary.quantize(Decimal("0.01"))

    return {
        "employee_id": employee_id,
        "name": name.strip(),
        "age": age,
        "salary": salary,
        "department_name": department_name.strip(),
    }


def import_employees(engine, json_file):
    with json_file.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("The JSON file must contain a list of employees.")

    inserted = 0
    skipped = 0
    imported_salary_total = Decimal("0.00")

    # All changes in this block commit together.
    # Any error rolls back inserts and department changes in this batch.
    with Session(engine) as session:
        with session.begin():
            for row_number, record in enumerate(records, start=1):
                employee_data = validate_employee(record, row_number)
                employee_id = employee_data["employee_id"]

                # Keep existing employees unchanged.
                if session.get(Employee, employee_id) is not None:
                    print(f"SKIPPED: {employee_id} already exists.")
                    skipped += 1
                    continue

                department_name = employee_data.pop("department_name")

                department = session.scalar(
                    select(Department).where(
                        Department.name.ilike(department_name)
                    )
                )

                if department is None:
                    department = Department(name=department_name)
                    session.add(department)
                    session.flush()

                employee = Employee(
                    **employee_data,
                    department=department,
                )
                session.add(employee)
                session.flush()

                inserted += 1
                imported_salary_total += employee.salary

                print(f"IMPORTED: {employee.employee_id}")

    print("\nImport completed successfully.")
    print(f"Source records: {len(records)}")
    print(f"Inserted: {inserted}")
    print(f"Skipped existing IDs: {skipped}")
    print(f"Imported salary total: {imported_salary_total:.2f}")


def main():
    engine = None

    try:
        # engine = create_engine(get_database_url(), pool_pre_ping=True)
        # import_employees(engine, JSON_FILE)
        json_file = Path(sys.argv[1]) if len(sys.argv) > 1 else JSON_FILE

        engine = create_engine(get_database_url(), pool_pre_ping=True)
        import_employees(engine, json_file)

    except (ValueError, InvalidOperation, json.JSONDecodeError) as error:
        print(f"Import rejected; transaction rolled back: {error}")
        sys.exit(1)

    except OSError as error:
        print(f"File error: {error}")
        sys.exit(1)

    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()
