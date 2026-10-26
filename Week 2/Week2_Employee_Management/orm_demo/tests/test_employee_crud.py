
"""Unit tests for the Employee Management ORM CRUD operations."""

import os
import unittest
from decimal import Decimal
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from typing import ClassVar

from sqlalchemy import URL, Engine, create_engine, select
from sqlalchemy.orm import Session

from employee_management import main
from employee_management.models import Base, Department, Employee


class TestEmployeeCRUD(unittest.TestCase):
    """Test employee CRUD operations and input validation."""

    engine: ClassVar[Engine]

    @classmethod
    def setUpClass(cls) -> None:
        """Create the database engine and database tables for testing."""
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

    def setUp(self) -> None:
        """Remove the sample employee before each test."""
        with Session(self.engine) as session, session.begin():
            existing: Employee | None = session.get(Employee, "EMP001")

            if existing is not None:
                session.delete(existing)

    def add_sample_employee(self) -> None:
        """Insert a sample employee and its department for testing."""
        with Session(self.engine) as session, session.begin():
            department: Department | None = session.scalar(
                select(Department).where(Department.name == "Testing")
            )

            if department is None:
                department = Department(name="Testing")
                session.add(department)
                session.flush()

            employee = Employee(
                employee_id="EMP001",
                name="Ravi",
                age=30,
                salary=Decimal("35000.00"),
                department=department,
            )
            session.add(employee)

    def test_add_employee(self) -> None:
        """Verify that an employee can be added successfully."""
        answers: list[str] = ["EMP001", "Ravi", "30", "35000", "Testing"]

        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(StringIO()):
                main.add_employee(self.engine)

        with Session(self.engine) as session:
            employee: Employee | None = session.get(Employee, "EMP001")

            self.assertIsNotNone(employee)
            assert employee is not None
            self.assertEqual(employee.name, "Ravi")
            self.assertEqual(employee.age, 30)
            self.assertEqual(employee.salary, Decimal("35000.00"))
            self.assertEqual(employee.department.name, "Testing")

    def test_list_employees(self) -> None:
        """Verify that listing employees displays their details."""
        self.add_sample_employee()

        output: StringIO = StringIO()
        with redirect_stdout(output):
            main.list_employees(self.engine)

        self.assertIn("EMP001", output.getvalue())
        self.assertIn("Ravi", output.getvalue())
        self.assertIn("Testing", output.getvalue())

    def test_search_employee(self) -> None:
        """Verify that an employee can be found using a partial name."""
        self.add_sample_employee()

        with patch("builtins.input", return_value="Rav"):
            output: StringIO = StringIO()
            with redirect_stdout(output):
                main.search_employee(self.engine)

        self.assertIn("EMP001", output.getvalue())
        self.assertIn("Ravi", output.getvalue())

    def test_edit_employee(self) -> None:
        """Verify that an employee's name can be updated."""
        self.add_sample_employee()

        answers: list[str] = ["EMP001", "1", "Rahul"]
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(StringIO()):
                main.edit_employee(self.engine)

        with Session(self.engine) as session:
            employee: Employee | None = session.get(Employee, "EMP001")

            self.assertIsNotNone(employee)
            assert employee is not None
            self.assertEqual(employee.name, "Rahul")

    def test_delete_employee(self) -> None:
        """Verify that an employee can be deleted after confirmation."""
        self.add_sample_employee()

        answers: list[str] = ["EMP001", "YES"]
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(StringIO()):
                main.delete_employee(self.engine)

        with Session(self.engine) as session:
            employee: Employee | None = session.get(Employee, "EMP001")
            self.assertIsNone(employee)

    def test_invalid_employee_id(self) -> None:
        """Verify that an invalid employee ID raises ValueError."""
        with patch("builtins.input", return_value="ABC123"):
            with self.assertRaises(ValueError):
                main.read_employee_id()


if __name__ == "__main__":
    unittest.main()
