"""Advanced unit tests for the Employee Management SQLAlchemy ORM."""

import os
import unittest
from collections.abc import Callable
from decimal import Decimal
from typing import Any

from sqlalchemy import URL, create_engine, event, func, select, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from employee_management.models import Base, Department, Employee


class TestEmployeeAdvanced(unittest.TestCase):
    """Test advanced ORM behavior against a PostgreSQL database."""

    engine: Engine

    @classmethod
    def setUpClass(cls) -> None:
        """Create the database engine and ensure ORM tables exist."""
        password: str | None = os.getenv("TEST_DB_PASSWORD")

        if not password:
            raise RuntimeError(
                "Set TEST_DB_PASSWORD to your PostgreSQL password."
            )

        url: URL = URL.create(
            drivername="postgresql+psycopg",
            username="postgres",
            password=password,
            host="localhost",
            port=5432,
            database="employee_orm_demo",
        )

        cls.engine = create_engine(url)
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """Dispose of the database engine after all tests finish."""
        cls.engine.dispose()

    def test_transaction_rollback(self) -> None:
        """Verify that a failed insert is rolled back completely."""
        employee_id: str = "ADVROLLBACK"

        try:
            with Session(self.engine) as session:
                with session.begin():
                    employee = Employee(
                        employee_id=employee_id,
                        name="Rollback Test",
                        age=30,
                        salary=Decimal("25000.00"),
                        department_id=-999999999,
                    )
                    session.add(employee)
                    session.flush()
        except IntegrityError:
            pass
        else:
            self.fail("Expected a foreign-key error.")

        with Session(self.engine) as session:
            employee: Employee | None = session.get(
                Employee, employee_id
            )
            self.assertIsNone(employee)

    def test_persistence_across_sessions(self) -> None:
        """Verify that committed employee data persists across sessions."""
        employee_id: str = "ADVPERSIST"
        department_name: str = "ADV_PERSIST_DEPT"

        try:
            with Session(self.engine) as session, session.begin():
                department = Department(name=department_name)
                session.add(department)
                session.flush()

                employee = Employee(
                    employee_id=employee_id,
                    name="Persistence Test",
                    age=28,
                    salary=Decimal("30000.00"),
                    department=department,
                )
                session.add(employee)

            # Open a separate session to verify persistence.
            with Session(self.engine) as session:
                employee = session.get(Employee, employee_id)

                self.assertIsNotNone(employee)
                assert employee is not None

                self.assertEqual(employee.name, "Persistence Test")
                self.assertEqual(
                    employee.salary, Decimal("30000.00")
                )
                self.assertEqual(
                    employee.department.name, department_name
                )

        finally:
            # Remove test records so repeated runs remain safe.
            with Session(self.engine) as session, session.begin():
                employee = session.get(Employee, employee_id)
                if employee is not None:
                    session.delete(employee)

                department = session.scalar(
                    select(Department).where(
                        Department.name == department_name
                    )
                )
                if department is not None:
                    session.delete(department)

    def test_missing_department_is_rejected(self) -> None:
        """Verify that an employee cannot reference a missing department."""
        employee_id: str = "ADVNODEPT"

        try:
            with Session(self.engine) as session:
                with session.begin():
                    session.add(
                        Employee(
                            employee_id=employee_id,
                            name="Missing Department",
                            age=25,
                            salary=Decimal("20000.00"),
                            department_id=-999999998,
                        )
                    )
                    session.flush()
        except IntegrityError:
            pass
        else:
            self.fail("Expected a foreign-key error.")

        with Session(self.engine) as session:
            self.assertIsNone(session.get(Employee, employee_id))

    def test_sql_injection_like_input_is_data(self) -> None:
        """Verify that SQL-like text is stored as ordinary employee data."""
        employee_id: str = "ADVSQLSAFE"
        department_name: str = "ADV_SQL_DEPT"
        unusual_name: str = "' OR 1=1 --"

        try:
            with Session(self.engine) as session, session.begin():
                department = Department(name=department_name)
                session.add(department)
                session.flush()

                session.add(
                    Employee(
                        employee_id=employee_id,
                        name=unusual_name,
                        age=26,
                        salary=Decimal("22000.00"),
                        department=department,
                    )
                )

            with Session(self.engine) as session:
                results = session.scalars(
                    select(Employee).where(
                        Employee.name == unusual_name
                    )
                ).all()

                self.assertEqual(len(results), 1)
                self.assertEqual(results[0].employee_id, employee_id)
                self.assertEqual(results[0].name, unusual_name)

        finally:
            with Session(self.engine) as session, session.begin():
                employee = session.get(Employee, employee_id)
                if employee is not None:
                    session.delete(employee)

                department = session.scalar(
                    select(Department).where(
                        Department.name == department_name
                    )
                )
                if department is not None:
                    session.delete(department)

    def test_sql_and_orm_aggregates_match(self) -> None:
        """Verify that ORM aggregates match equivalent raw SQL results."""
        department_name: str = "ADV_AGG_DEPT"
        employee_ids: list[str] = ["ADVAGG001", "ADVAGG002"]

        try:
            with Session(self.engine) as session, session.begin():
                department = Department(name=department_name)
                session.add(department)
                session.flush()

                session.add_all(
                    [
                        Employee(
                            employee_id=employee_ids[0],
                            name="Aggregate One",
                            age=25,
                            salary=Decimal("20000.00"),
                            department=department,
                        ),
                        Employee(
                            employee_id=employee_ids[1],
                            name="Aggregate Two",
                            age=30,
                            salary=Decimal("30000.00"),
                            department=department,
                        ),
                    ]
                )

            # Calculate using SQLAlchemy ORM.
            with Session(self.engine) as session:
                orm_result = session.execute(
                    select(
                        Department.name,
                        func.count(Employee.employee_id),
                        func.coalesce(func.sum(Employee.salary), 0),
                    )
                    .outerjoin(Department.employees)
                    .where(Department.name == department_name)
                    .group_by(Department.name)
                ).one()

            # Calculate the same values using raw SQL.
            with Session(self.engine) as session:
                sql_result = session.execute(
                    text(
                        """
                        SELECT
                            d.name,
                            COUNT(e.employee_id),
                            COALESCE(SUM(e.salary), 0)
                        FROM departments AS d
                        LEFT JOIN employees AS e
                            ON e.department_id = d.department_id
                        WHERE d.name = :department_name
                        GROUP BY d.name
                        """
                    ),
                    {"department_name": department_name},
                ).one()

            self.assertEqual(orm_result[0], sql_result[0])
            self.assertEqual(orm_result[1], sql_result[1])
            self.assertEqual(
                Decimal(str(orm_result[2])),
                Decimal(str(sql_result[2])),
            )

            self.assertEqual(orm_result[1], 2)
            self.assertEqual(
                Decimal(str(orm_result[2])),
                Decimal("50000.00"),
            )

        finally:
            with Session(self.engine) as session, session.begin():
                for employee_id in employee_ids:
                    employee = session.get(Employee, employee_id)
                    if employee is not None:
                        session.delete(employee)

                department = session.scalar(
                    select(Department).where(
                        Department.name == department_name
                    )
                )
                if department is not None:
                    session.delete(department)

    def test_lazy_loading_vs_joinedload(self) -> None:
        """Compare SELECT query counts for lazy and eager loading."""
        department_names: list[str] = [
            "ADV_LAZY_DEPT1",
            "ADV_LAZY_DEPT2",
        ]
        employee_ids: list[str] = [
            "ADVLAZY001",
            "ADVLAZY002",
        ]

        try:
            # Create two departments, each with one employee.
            with Session(self.engine) as session, session.begin():
                departments = [
                    Department(name=name)
                    for name in department_names
                ]
                session.add_all(departments)
                session.flush()

                session.add_all(
                    [
                        Employee(
                            employee_id=employee_ids[0],
                            name="Lazy One",
                            age=25,
                            salary=Decimal("20000.00"),
                            department=departments[0],
                        ),
                        Employee(
                            employee_id=employee_ids[1],
                            name="Lazy Two",
                            age=28,
                            salary=Decimal("25000.00"),
                            department=departments[1],
                        ),
                    ]
                )

            lazy_queries: list[str] = []
            eager_queries: list[str] = []

            def count_selects(
                target_list: list[str],
            ) -> Callable[
                [Connection, Any, str, Any, Any, bool], None
            ]:
                """Create a SQLAlchemy event listener that records SELECTs."""

                def listener(
                    connection: Connection,
                    cursor: Any,
                    statement: str,
                    parameters: Any,
                    context: Any,
                    executemany: bool,
                ) -> None:
                    """Record a statement when it begins with SELECT."""
                    if statement.lstrip().upper().startswith("SELECT"):
                        target_list.append(statement)

                return listener

            # Lazy loading: fetch departments, then employees separately.
            lazy_listener = count_selects(lazy_queries)
            event.listen(
                self.engine,
                "before_cursor_execute",
                lazy_listener,
            )

            try:
                with Session(self.engine) as session:
                    departments = session.scalars(
                        select(Department).where(
                            Department.name.in_(department_names)
                        )
                    ).all()

                    employee_count: int = sum(
                        len(department.employees)
                        for department in departments
                    )
                    self.assertEqual(employee_count, 2)
            finally:
                event.remove(
                    self.engine,
                    "before_cursor_execute",
                    lazy_listener,
                )

            # Eager loading: fetch departments and employees together.
            eager_listener = count_selects(eager_queries)
            event.listen(
                self.engine,
                "before_cursor_execute",
                eager_listener,
            )

            try:
                with Session(self.engine) as session:
                    departments = session.scalars(
                        select(Department)
                        .options(joinedload(Department.employees))
                        .where(
                            Department.name.in_(department_names)
                        )
                    ).unique().all()

                    employee_count = sum(
                        len(department.employees)
                        for department in departments
                    )
                    self.assertEqual(employee_count, 2)
            finally:
                event.remove(
                    self.engine,
                    "before_cursor_execute",
                    eager_listener,
                )

            self.assertGreater(len(lazy_queries), len(eager_queries))
            self.assertEqual(len(lazy_queries), 3)
            self.assertEqual(len(eager_queries), 1)

        finally:
            with Session(self.engine) as session, session.begin():
                for employee_id in employee_ids:
                    employee = session.get(Employee, employee_id)
                    if employee is not None:
                        session.delete(employee)

                for department_name in department_names:
                    department = session.scalar(
                        select(Department).where(
                            Department.name == department_name
                        )
                    )
                    if department is not None:
                        session.delete(department)


if __name__ == "__main__":
    unittest.main()
