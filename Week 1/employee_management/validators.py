import re

def validate_employee_id(employee_id):
    """Check whether the employee ID follows the EMP001 format."""
    pattern = r"^EMP\d{3}$"
    return bool(re.fullmatch(pattern, employee_id))


def validate_employee_name(employee_name):
    """Check whether the employee name contains letters and spaces."""
    if not employee_name or not employee_name.strip():
        return False

    return employee_name.replace(" ", "").isalpha()


def validate_employee_age(employee_age):
    """Check whether the employee age is between 20 and 60."""
    return 20 <= employee_age <= 60


def validate_employee_email(email):
    """Check whether the email has a basic valid format."""
    pattern = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

def validate_employee_department(employee_department):
    """Check whether the department contains letters and spaces."""
    if not employee_department or not employee_department.strip():
        return False

    return employee_department.replace(" ", "").isalpha()


def validate_employee_salary(employee_salary):
    """Check whether the salary is greater than zero."""
    return employee_salary > 0