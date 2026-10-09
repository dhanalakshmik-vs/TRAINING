"""Employee management operations for the command-line application."""

import csv
import json
import logging
from typing import Any

import logging_config  # noqa: F401 - importing this module configures logging
from validators import (
    validate_employee_age,
    validate_employee_department,
    validate_employee_email,
    validate_employee_id,
    validate_employee_name,
    validate_employee_salary,
)

EMPLOYEE_FILE = "employee.json"
JSON_EXPORT_FILE = "employee_data.json"
CSV_EXPORT_FILE = "employees_export.csv"
Employee = dict[str, Any]
Employees = list[Employee]


def add_employee() -> None:
    """Prompt for employee details, validate them, and save a new record."""
    employees = load_employee()

    while True:
        employee_id = input("Enter the ID: ").strip()
        if not validate_employee_id(employee_id):
            print("Invalid employee ID. Use a format like EMP001.")
            logging.warning("Invalid employee ID format entered")
            continue
        if any(employee.get("id") == employee_id for employee in employees):
            print("Employee ID already exists. Please enter a different ID.")
            logging.warning("Duplicate employee ID attempted: %s", employee_id)
            continue
        break

    while True:
        employee_name = input("Enter the name: ").strip()
        if validate_employee_name(employee_name):
            break
        print("Please enter a valid name.")
        logging.warning("Invalid employee name entered")

    while True:
        try:
            employee_age = int(input("Enter the age: "))
            if validate_employee_age(employee_age):
                break
            print("Please enter an age between 20 and 60.")
            logging.warning("Employee age outside allowed range")
        except ValueError:
            print("Please enter a valid age.")
            logging.warning("Non-numeric employee age entered")

    while True:
        employee_email = input("Enter the email: ").strip()
        if validate_employee_email(employee_email):
            break
        print("Please enter a valid email, like rahul@gmail.com.")
        logging.warning("Invalid employee email format entered")

    while True:
        employee_department = input("Enter the department: ").strip()
        if validate_employee_department(employee_department):
            break
        print("Please enter a valid department.")
        logging.warning("Invalid employee department entered")

    while True:
        try:
            employee_salary = float(input("Enter the salary: "))
            if validate_employee_salary(employee_salary):
                break
            print("Salary must be greater than 0.")
            logging.warning("Non-positive employee salary entered")
        except ValueError:
            print("Please enter a valid salary.")
            logging.warning("Non-numeric employee salary entered")

    employee: Employee = {
        "id": employee_id,
        "name": employee_name,
        "age": employee_age,
        "email": employee_email,
        "department": employee_department,
        "salary": employee_salary,
    }

    employees.append(employee)
    
    if save_employee(employees):
        logging.info("Employee %s added successfully", employee_id)
        print("Employee added successfully.")
    else:
        print("Employee details were entered, but could not be saved.")


def save_employee(employees: Employees) -> bool:
    """Save employee records to the main JSON file.

    Args:
        employees: Employee records to write.

    Returns:
        True if saving succeeds; otherwise, False.
    """
    try:
        with open(EMPLOYEE_FILE, "w", encoding="utf-8") as file:
            json.dump(employees, file, indent=4)
        return True

    except (OSError, TypeError, ValueError) as error:
        logging.error("Error while saving employee data: %s", error)
        print("Error while saving employee data.")
        return False


def load_employee() -> Employees:
    """Load employee records from JSON, returning an empty list on read errors."""
    try:
        with open(EMPLOYEE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            logging.error("Employee file must contain a JSON list of objects")
            print("Employee file has an invalid format.")
            return []
        return data

    except FileNotFoundError:
        logging.info("Employee file does not exist yet")
        return []
    
    except json.JSONDecodeError as error:
        logging.error("Employee file contains invalid JSON: %s", error)
        print("Employee file contains invalid JSON.")
        return []

    except OSError as error:
        logging.error("Unable to read employee file: %s", error)
        print("Unable to read employee file.")
        return []

def show_employee_summary() -> None:

    """Display each employee's ID, name, and department."""
    employees = load_employee()

    if not employees:
        print("Employee list is empty. Please add employees.")
        return
    for employee in employees:
        print(
            f"ID: {employee.get('id', 'N/A')} | "
            f"Name: {employee.get('name', 'N/A')} | "
            f"Department: {employee.get('department', 'N/A')}"
        )


def show_employee() -> None:

    """Display the complete details of every employee."""
    employees = load_employee()

    if not employees:
        print("Employee list is empty. Please add employees.")
        return
    for employee in employees:
        print(
            f"ID: {employee.get('id', 'N/A')} | "
            f"Name: {employee.get('name', 'N/A')} | "
            f"Age: {employee.get('age', 'N/A')} | "
            f"Email: {employee.get('email', 'Not provided')} | "
            f"Department: {employee.get('department', 'N/A')} | "
            f"Salary: {employee.get('salary', 'N/A')}"
        )


def get_employee(employees: Employees, employee_id: str) -> Employee | None:

    """Return the employee matching an ID, or None if no match exists."""

    for employee in employees:
        if employee.get("id") == employee_id:
            return employee
    return None


def update_employee() -> None:
    """Update one field of an employee record and save the change."""
    employees = load_employee()

    if not employees:
        print("Employee list is empty. Please add employees.")
        return

    print("Below is the list of employees:")
    show_employee_summary()

    while True:
        employee_id = input("Enter the employee ID: ").strip()

        if validate_employee_id(employee_id):
            break

        print("Invalid employee ID. Use a format like EMP001.")
        logging.warning("Invalid employee ID format entered during update")

    employee = get_employee(employees, employee_id)

    if employee is None:
        print("Employee not found.")
        logging.warning("Update failed: employee %s not found", employee_id)
        return

    while True:
        print("\n1. Update name\n2. Update age\n3. Update email")
        print("4. Update department\n5. Update salary\n6. Exit")
        while True:
            try:
                choice = int(input("Enter the field number: "))
                if 1 <= choice <= 6:
                    break
                print("Please enter a number between 1 and 6.")
                logging.warning("Invalid update menu choice: %s", choice)
            except ValueError:
                print("Please enter a valid number.")
                logging.warning("Non-numeric input entered for update menu")

        if choice == 6:
            print("Update cancelled.")
            return
        if choice == 1:
            while True:
                value = input("Enter the new name: ").strip()
                if validate_employee_name(value):
                    employee["name"] = value
                    break
                print("Please enter a valid name.")
                logging.warning("Invalid name entered during update for %s", employee_id)
        elif choice == 2:
            while True:
                try:
                    value = int(input("Enter the new age: "))
                    if validate_employee_age(value):
                        employee["age"] = value
                        break
                    print("Please enter an age between 20 and 60.")
                    logging.warning("Invalid age entered during update for %s", employee_id)
                except ValueError:
                    print("Please enter a valid age.")
                    logging.warning("Non-numeric age entered during update for %s", employee_id)
        elif choice == 3:
            while True:
                value = input("Enter the new email: ").strip()
                if validate_employee_email(value):
                    employee["email"] = value
                    break
                print("Please enter a valid email address.")
                logging.warning("Invalid email entered during update for %s", employee_id)
        elif choice == 4:
            while True:
                value = input("Enter the new department: ").strip()
                if validate_employee_department(value):
                    employee["department"] = value
                    break
                print("Please enter a valid department, such as IT, Accounts, or HR.")
                logging.warning("Invalid department entered during update for %s", employee_id)
        else:  # choice == 5
            while True:
                try:
                    value = float(input("Enter the new salary: "))
                    if validate_employee_salary(value):
                        employee["salary"] = value
                        break
                    print("Salary must be greater than 0.")
                    logging.warning("Invalid salary entered during update for %s", employee_id)
                except ValueError:
                    print("Please enter a valid salary.")
                    logging.warning("Non-numeric salary entered during update for %s", employee_id)

        if save_employee(employees):
            logging.info("Employee %s updated successfully", employee_id)
            print("Employee updated successfully.")
        else:
            print("The change could not be saved.")
        return

def delete_employee() -> None:
    """Delete an employee after validating the ID and confirming the action."""

    employees = load_employee()
    if not employees:
        print("Employee list is empty. Please add employees.")
        return
    show_employee_summary()

    while True:
        employee_id = input("Enter the employee ID you want to delete: ").strip()
        if validate_employee_id(employee_id):
            break
        print("Invalid employee ID. Use a format like EMP001.")
        logging.warning("Invalid employee ID format entered during delete")

    employee = get_employee(employees, employee_id)

    if employee is None:
        print("Employee not found.")
        logging.warning("Delete failed: employee %s not found", employee_id)
        return

    print("\nEmployee selected:")
    print(f"ID: {employee.get('id', 'N/A')}")
    print(f"Name: {employee.get('name', 'N/A')}")
    print(f"Department: {employee.get('department', 'N/A')}")

    while True:
        confirmation = input(
            "Are you sure you want to delete this employee? (yes/no): "
        ).strip().lower()
        if confirmation in {"yes", "no"}:
            break
        print("Please enter yes or no.")

    if confirmation == "no":
        print("Delete operation cancelled.")
        logging.info("Delete cancelled for employee %s", employee_id)
        return
    employees.remove(employee)
    if save_employee(employees):
        logging.info("Employee %s deleted successfully", employee_id)
        print("Employee deleted successfully.")
    else:
        print("The employee could not be deleted from the saved file.")

def search_employee() -> None:

    """Search employees by ID, name, or email."""
    employees = load_employee()

    if not employees:
        print("Employee list is empty. Please add employees.")
        return

    print("\nSearch Employee By:")
    print("1. Employee ID")
    print("2. Employee Name")
    print("3. Employee Email")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        search_field = "id"
    elif choice == "2":
        search_field = "name"
    elif choice == "3":
        search_field = "email"
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    search_value = input("Enter the search value: ").strip()

    if not search_value:
        print("Search value cannot be empty.")
        return

    # Find all employees matching the search value.
    matches = []

    for employee in employees:
        employee_value = str(employee.get(search_field, ""))

        if search_field == "id":
            if employee_value.lower() == search_value.lower():
                matches.append(employee)
        else:
            if search_value.lower() in employee_value.lower():
                matches.append(employee)

    if not matches:
        print("Employee not found.")
        logging.warning(
            "No employee found using field %s and value %s",
            search_field,
            search_value,
        )
        return

    logging.info(
        "Employee search completed using field %s",
        search_field,
    )

    for employee in matches:
        print("\n--- Employee Details ---")
        print(f"ID: {employee.get('id', 'N/A')}")
        print(f"Name: {employee.get('name', 'N/A')}")
        print(f"Age: {employee.get('age', 'N/A')}")
        print(f"Email: {employee.get('email', 'Not provided')}")
        print(f"Department: {employee.get('department', 'N/A')}")
        print(f"Salary: {employee.get('salary', 'N/A')}")

def filter_employee() -> None:

    """Filter records using any combination of optional employee fields."""
    employees = load_employee()

    if not employees:
        print("Employee list is empty. Please add employees.")
        return

    while True:
        employee_id = input("Enter employee ID (press Enter to skip): ").strip()
        if not employee_id or validate_employee_id(employee_id):
            break
        print("Invalid employee ID. Use a format like EMP001.")

    while True:
        employee_name = input("Enter employee name (press Enter to skip): ").strip()
        if not employee_name or validate_employee_name(employee_name):
            break
        print("Please enter a valid name.")

    while True:
        employee_department = input("Enter department (press Enter to skip): ").strip()
        if not employee_department or validate_employee_department(employee_department):
            break
        print("Please enter a valid department.")

    while True:
        age_input = input("Enter age (press Enter to skip): ").strip()
        if not age_input:
            employee_age = None
            break
        try:
            employee_age = int(age_input)
            if validate_employee_age(employee_age):
                break
            print("Age must be between 20 and 60.")
        except ValueError:
            print("Please enter a valid age.")

    while True:
        employee_email = input("Enter employee email (press Enter to skip): ").strip()
        if not employee_email or validate_employee_email(employee_email):
            break
        print("Please enter a valid email address.")

    while True:
        salary_input = input("Enter salary (press Enter to skip): ").strip()
        if not salary_input:
            employee_salary = None
            break
        try:
            employee_salary = float(salary_input)
            if validate_employee_salary(employee_salary):
                break
            print("Salary must be greater than 0.")
        except ValueError:
            print("Please enter a valid salary.")

    if (
        not employee_id and not employee_name and not employee_department
        and employee_age is None and not employee_email and employee_salary is None
    ):
        print("Please enter at least one filter.")
        return

    matches: Employees = []
    for employee in employees:
        if employee_id and str(employee.get("id", "")).lower() != employee_id.lower():
            continue
        if employee_name and str(employee.get("name", "")).lower() != employee_name.lower():
            continue
        if employee_department and str(employee.get("department", "")).lower() != employee_department.lower():
            continue
        if employee_age is not None and employee.get("age") != employee_age:
            continue
        if employee_email and str(employee.get("email", "")).lower() != employee_email.lower():
            continue
        if employee_salary is not None and employee.get("salary") != employee_salary:
            continue
        matches.append(employee)

    if not matches:
        print("No employees matched the provided filters.")
        logging.info("Employee filter returned no matches")
        return
    for employee in matches:
        print(employee)
    logging.info("Employee filter returned %d match(es)", len(matches))


def export_json() -> None:
    """Export employee records to a separate JSON file."""

    employees = load_employee()

    try:
        with open(JSON_EXPORT_FILE, "w", encoding="utf-8") as file:
            json.dump(employees, file, indent=4)

    except (OSError, TypeError, ValueError) as error:
        logging.error("Unable to export employee data to JSON: %s", error)
        print("Unable to export employees to JSON.")
        return
    
    logging.info("Exported %d employee record(s) to JSON", len(employees))
    print("Employees exported to JSON successfully.")


def export_csv() -> None:

    """Export employee records to a CSV file."""
    employees = load_employee()
    fieldnames = ["id", "name", "age", "email", "department", "salary"]

    try:
        with open(CSV_EXPORT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(employees)

    except (OSError, csv.Error, ValueError) as error:
        logging.error("Unable to export employee data to CSV: %s", error)
        print("Unable to export employees to CSV.")
        return
    
    logging.info("Exported %d employee record(s) to CSV", len(employees))
    print("Employees exported to CSV successfully.")
