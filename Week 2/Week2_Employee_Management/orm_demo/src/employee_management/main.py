"""Menu-driven employee management application using SQLAlchemy ORM."""

from collections.abc import Callable
import logging
from decimal import Decimal, InvalidOperation
from getpass import getpass

from sqlalchemy import URL, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from employee_management.logging_config import setup_logging
from employee_management.models import Department, Employee

logger = logging.getLogger(__name__)


def get_database_url() -> URL:
    """Build and return the PostgreSQL connection URL from user input."""
    password: str = getpass("Enter PostgreSQL password: ")

    return URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_demo",
    )


def read_employee_id() -> str:
    """Read and validate an employee ID in EMP001 format."""
    employee_id: str = input(
        "Enter employee ID (e.g. EMP001): "
    ).strip().upper()

    if not employee_id.startswith("EMP") or not employee_id[3:].isdigit():
        raise ValueError("Employee ID must use a format such as EMP001.")

    return employee_id


def read_name() -> str:
    """Read and return a non-empty employee name."""
    name: str = input("Enter employee name: ").strip()

    if not name:
        raise ValueError("Employee name cannot be empty.")

    return name


def read_age() -> int:
    """Read and return an employee age between 20 and 60."""
    try:
        age: int = int(input("Enter employee age (20-60): "))
    except ValueError as error:
        raise ValueError("Age must be a whole number.") from error

    if not 20 <= age <= 60:
        raise ValueError("Age must be between 20 and 60.")

    return age


def read_salary() -> Decimal:
    """Read and return a positive salary with two decimal places."""
    try:
        salary: Decimal = Decimal(input("Enter employee salary: ").strip())
    except InvalidOperation as error:
        raise ValueError("Salary must be a valid number.") from error

    if not salary.is_finite() or salary <= 0:
        raise ValueError("Salary must be a positive finite number.")

    return salary.quantize(Decimal("0.01"))


def choose_department(session: Session) -> Department:
    """Find an existing department or create a new one."""
    name: str = input("Enter department name: ").strip()

    if not name:
        raise ValueError("Department name cannot be empty.")

    department: Department | None = session.scalar(
        select(Department).where(Department.name.ilike(name))
    )

    if department is None:
        department = Department(name=name)
        session.add(department)
        session.flush()

    return department


def add_employee(engine: Engine) -> None:
    """Add a new employee within a database transaction."""
    employee_id: str = read_employee_id()
    name: str = read_name()
    age: int = read_age()
    salary: Decimal = read_salary()

    with Session(engine) as session, session.begin():
        if session.get(Employee, employee_id) is not None:
            print("An employee with this ID already exists.")
            return

        department: Department = choose_department(session)

        employee = Employee(
            employee_id=employee_id,
            name=name,
            age=age,
            salary=salary,
            department=department,
        )
        session.add(employee)

    logger.info("Employee %s was added.", employee_id)
    print("Employee added successfully.")


def list_employees(engine: Engine) -> None:
    """Display all employees together with their department names."""
    with Session(engine) as session:
        statement = (
            select(Employee)
            .options(joinedload(Employee.department))
            .order_by(Employee.employee_id)
        )
        employees: list[Employee] = list(session.scalars(statement).all())

        if not employees:
            print("No employees found.")
            return

        print("\nID | Name | Age | Salary | Department")
        print("-" * 65)

        for employee in employees:
            print(
                f"{employee.employee_id} | {employee.name} | "
                f"{employee.age} | {employee.salary} | "
                f"{employee.department.name}"
            )


def search_employee(engine: Engine) -> None:
    """Search for employees by employee ID or partial name."""
    term: str = input("Enter employee ID or name to search: ").strip()

    if not term:
        raise ValueError("Search text cannot be empty.")

    with Session(engine) as session:
        statement = (
            select(Employee)
            .options(joinedload(Employee.department))
            .where(
                Employee.employee_id.ilike(f"%{term}%")
                | Employee.name.ilike(f"%{term}%")
            )
            .order_by(Employee.employee_id)
        )
        employees: list[Employee] = list(session.scalars(statement).all())

        if not employees:
            print("No matching employees found.")
            return

        for employee in employees:
            print(
                f"{employee.employee_id} | {employee.name} | "
                f"{employee.age} | {employee.salary} | "
                f"{employee.department.name}"
            )


def edit_employee(engine: Engine) -> None:
    """Update one selected field of an existing employee."""
    employee_id: str = read_employee_id()

    with Session(engine) as session, session.begin():
        employee: Employee | None = session.get(Employee, employee_id)

        if employee is None:
            print("Employee not found.")
            return

        print(
            f"Current details: {employee.name}, age {employee.age}, "
            f"salary {employee.salary}"
        )
        print("1. Name")
        print("2. Age")
        print("3. Salary")

        choice: str = input("Choose a field to update: ").strip()

        if choice == "1":
            employee.name = read_name()
        elif choice == "2":
            employee.age = read_age()
        elif choice == "3":
            employee.salary = read_salary()
        else:
            print("Invalid field choice.")
            return

    logger.info("Employee %s was updated.", employee_id)
    print("Employee updated successfully.")


def delete_employee(engine: Engine) -> None:
    """Delete an employee only after explicit confirmation."""
    employee_id: str = read_employee_id()

    with Session(engine) as session, session.begin():
        employee: Employee | None = session.get(Employee, employee_id)

        if employee is None:
            print("Employee not found.")
            return

        print(f"Employee: {employee.name} ({employee.employee_id})")
        confirmation: str = input(
            "Type YES to confirm deletion: "
        ).strip().upper()

        if confirmation != "YES":
            print("Deletion cancelled.")
            return

        session.delete(employee)

    logger.info("Employee %s was deleted.", employee_id)
    print("Employee deleted successfully.")


def main() -> None:
    """Initialize the database connection and run the CLI menu."""
    setup_logging()
    engine: Engine | None = None

    try:
        engine = create_engine(get_database_url(), pool_pre_ping=True)

        with engine.connect():
            logger.info("Connected to PostgreSQL.")

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

            action(engine)
            
            try:
                # The selected action receives the database engine.
                action(engine)  # type: ignore[operator]
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

    except SQLAlchemyError:
        logger.exception("Could not connect to PostgreSQL.")
        print("Could not connect to PostgreSQL. Check your settings.")
    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()