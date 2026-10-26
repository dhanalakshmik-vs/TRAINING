
from getpass import getpass

from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session, joinedload

from employee_management.models import Employee


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
            print("\n--- All Employees ---")

            statement = select(Employee).options(
                joinedload(Employee.department)
            ).order_by(Employee.employee_id)

            employees = session.scalars(statement).all()

            for employee in employees:
                print(
                    f"{employee.employee_id} | "
                    f"{employee.name} | "
                    f"{employee.age} | "
                    f"{employee.salary} | "
                    f"{employee.department.name}"
                )

            search_name = input(
                "\nEnter employee name to search: "
            ).strip()

            statement = select(Employee).where(
                Employee.name.ilike(f"%{search_name}%")
            ).options(joinedload(Employee.department))

            results = session.scalars(statement).all()

            print("\n--- Search Results ---")

            if results:
                for employee in results:
                    print(
                        f"{employee.employee_id} | "
                        f"{employee.name} | "
                        f"{employee.department.name}"
                    )
            else:
                print("No matching employees found.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
