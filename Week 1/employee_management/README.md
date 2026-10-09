# Employee Management System

A simple command-line Employee Management System built with Python.

The application allows users to add, update, delete, search, and filter employee records. Employee data is stored in a JSON file and can be exported to JSON and CSV formats.

## Features

* Add employee records
* Update employee details
* Delete employee records
* Search employees by employee ID
* Filter employees using:

  * Employee ID
  * Employee name
  * Department
  * Age
  * Salary
  * Multiple fields
* Validate employee input
* Handle invalid input and missing employee records
* Store employee data in JSON
* Export employee data to JSON
* Export employee data to CSV
* Maintain application logs
* Automated tests for validation rules and important operations

## Project Structure

employee_management/
│
├── main.py
├── employee_functions.py
├── validators.py
├── employee.json
├── employee_data.json
├── employees_export.csv
├── logging_config.py
├── employee.log
├── test_employee.py
└── README.md


## Requirements

* Python 3.x
* No external Python packages are required for the basic application.

The project uses Python's built-in modules such as:

* `json`
* `csv`
* `logging`
* `unittest`

## Setup

### 1. Clone or download the project

Place the project in a local directory.

### 2. Open the project folder

Open a terminal or command prompt and navigate to the project directory.

Example:

```bash
cd employee_management
```

### 3. Run the application

```bash
python main.py
```

## Usage

After starting the application, the main menu can be used to perform employee management operations.

Typical operations include:

1. Add Employee
2. View Employees
3. Update Employee
4. Delete Employee
5. Search Employee
6. Filter Employee
7. Export JSON
8. Export CSV
9. Exit

The exact menu options may vary depending on the implementation in `main.py`.

## Sample Employee Record

Employee records use the following fields:

ID
Name
Age
Department
Salary

Example:

    ID: EMP001
    Name: Rahul
    Age: 25
    Department: IT
    Salary: 30000


Employee IDs are stored as strings using a format such as:

EMP001
EMP002
EMP003

## Validation Rules

The application validates employee information before storing it.

### Employee ID

Employee IDs should start with:

EMP

Example:

    EMP001

### Employee Name

The name should contain alphabetic characters and may contain spaces.

Example:

    Rahul Kumar

### Age

Employee age must be between:

    20 and 60

Both 20 and 60 are valid.

### Department

The department must contain a valid department value according to the validation rules implemented in `validators.py`.

Examples:

    IT
    HR
    Accounts

### Salary

Salary must be greater than zero.

For example:

    30000
    45000.50

are valid values.

## Filtering Employees

The application supports filtering employees using different fields.

Users can filter using information they already know instead of entering every employee field.

For example:

    Filter by Department
    Enter department: IT

Or multiple fields can be used together:

    Department: IT
    Age: 25

This returns employees matching the selected conditions.

## Data Storage

Employee records are stored in:

    employee.json

The JSON file contains the complete list of employee records.

Example:

[
    {
        "id": "EMP001",
        "name": "Rahul",
        "age": 25,
        "department": "IT",
        "salary": 30000.0
    }
]

## Export

### JSON Export

Employee records can be exported to a separate JSON file.

Example:

    employee_data.json

The exported file contains the employee records in JSON format.

### CSV Export

Employee records can also be exported to CSV.

Example:

    employees_export.csv

The CSV contains the following fields:

    id,name,age,department,salary

## Logging

The application uses Python's `logging` module to record important operations and failures.

Logs are stored in:

    employee.log

Examples of logged operations include:

Employee EMP001 added successfully
Employee EMP001 updated successfully
Employee EMP001 deleted successfully
Employee EMP001 searched successfully
Employee EMP999 not found during search
Error while saving employee data
Employee file not found

Logging helps reviewers understand important application activities and failures without relying only on console output.

## Testing

The project uses Python's built-in `unittest` framework.

Run the tests using:

```bash
python -m unittest test_employee.py
```

The tests cover important validation rules such as:

* Valid employee ID
* Invalid employee ID
* Valid employee name
* Invalid employee name
* Valid age
* Invalid age
* Valid department
* Invalid department
* Valid salary
* Invalid salary

Additional tests can be added for employee operations such as:

* Add employee
* Search employee
* Update employee
* Delete employee
* Filter employee

## Sample Commands

### Run the application

```bash
python main.py
```

### Run all tests

```bash
python -m unittest test_employee.py
```

### Run a specific test file

```bash
python -m unittest test_employee.py
```

## Error Handling

The application handles expected errors such as:

* Invalid numeric input
* Invalid employee information
* Employee not found
* Missing employee JSON file
* Invalid JSON data
* File saving errors

Clear messages are displayed to the user when an error occurs.

## Known Limitations

* Employee data is stored in a local JSON file rather than a database.
* The application is command-line based and does not have a graphical user interface.
* Employee IDs must follow the expected `EMP` format.
* The application is designed for a small set of synthetic employee records.
* Concurrent access by multiple users is not supported.
* The current filtering and search functionality is limited to the fields implemented in the application.
* Authentication and user access control are not implemented.

## Future Improvements

Possible future improvements include:

* Use a database such as PostgreSQL or SQLite
* Add a graphical or web interface
* Add employee ID uniqueness validation
* Add user authentication
* Add pagination for large employee datasets
* Add more advanced filtering and sorting
* Improve automated test coverage

## Author

Employee Management System developed as part of the Python trainee task.
