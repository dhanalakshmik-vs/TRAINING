
from getpass import getpass

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

from models import Department, Employee


def main():
    password = getpass("Enter PostgreSQL password: ")

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_demo",
    )

    engine = create_engine(database_url)

    try:
        with Session(engine) as session:
            department = session.query(Department).filter_by(
                name="IT"
            ).first()

            if department is None:
                department = Department(name="IT")
                session.add(department)
                session.flush()

            employee_data = [
                ("EMP001", "Sreekutty", 20, 25000.00),
                ("EMP002", "Rahul", 30, 32000.00),
            ]

            for employee_id, name, age, salary in employee_data:
                existing = session.get(Employee, employee_id)

                if existing is None:
                    session.add(
                        Employee(
                            employee_id=employee_id,
                            name=name,
                            age=age,
                            salary=salary,
                            department=department,
                        )
                    )
                    print(f"Added {employee_id}")
                else:
                    print(f"{employee_id} already exists; skipped")

            session.commit()
            print("Employee records saved successfully.")

    except Exception:
        print("Operation failed. The transaction was rolled back.")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
