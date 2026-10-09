"""Unit tests for employee input validation functions."""

import unittest

from validators import (
    validate_employee_id,
    validate_employee_name,
    validate_employee_age,
    validate_employee_email,
    validate_employee_department,
    validate_employee_salary,
)


class TestEmployeeValidation(unittest.TestCase):
    """Test validation functions used by the employee management app."""

    def test_valid_employee_id(self) -> None:
        """Test that a correctly formatted employee ID is accepted."""
        self.assertTrue(validate_employee_id("EMP001"))

    def test_invalid_employee_id(self) -> None:
        """Test that incorrectly formatted employee IDs are rejected."""
        self.assertFalse(validate_employee_id("ABC001"))
        self.assertFalse(validate_employee_id(""))

    def test_valid_employee_name(self) -> None:
        """Test that a valid employee name is accepted."""
        self.assertTrue(validate_employee_name("Rahul"))

    def test_invalid_employee_name(self) -> None:
        """Test that invalid employee names are rejected."""
        self.assertFalse(validate_employee_name("12345"))
        self.assertFalse(validate_employee_name(""))

    def test_valid_employee_age(self) -> None:
        """Test valid ages, including the minimum and maximum boundaries."""
        self.assertTrue(validate_employee_age(20))
        self.assertTrue(validate_employee_age(25))
        self.assertTrue(validate_employee_age(60))

    def test_invalid_employee_age(self) -> None:
        """Test that ages outside the allowed range are rejected."""
        self.assertFalse(validate_employee_age(19))
        self.assertFalse(validate_employee_age(61))

    def test_valid_employee_email(self) -> None:
        """Test that valid email formats are accepted."""
        self.assertTrue(validate_employee_email("rahul@gmail.com"))
        self.assertTrue(validate_employee_email("anjali123@yahoo.in"))
        self.assertTrue(validate_employee_email("sree.kutty@company.org"))

    def test_invalid_employee_email(self) -> None:
        """Test that invalid email formats are rejected."""
        self.assertFalse(validate_employee_email("rahulgmail.com"))
        self.assertFalse(validate_employee_email("rahul@"))
        self.assertFalse(validate_employee_email("@gmail.com"))
        self.assertFalse(validate_employee_email(""))

    def test_valid_employee_department(self) -> None:
        """Test that an accepted department is valid."""
        self.assertTrue(validate_employee_department("IT"))

    def test_invalid_employee_department(self) -> None:
        """Test that an empty department is rejected."""
        self.assertFalse(validate_employee_department(""))

    def test_valid_employee_salary(self) -> None:
        """Test that a positive employee salary is accepted."""
        self.assertTrue(validate_employee_salary(30000))
        self.assertTrue(validate_employee_salary(0.01))

    def test_invalid_employee_salary(self) -> None:
        """Test that zero and negative salaries are rejected."""
        self.assertFalse(validate_employee_salary(0))
        self.assertFalse(validate_employee_salary(-5000))


if __name__ == "__main__":
    unittest.main()