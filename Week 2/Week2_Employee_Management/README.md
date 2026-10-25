# Employee Management System — SQLAlchemy ORM

## Project Overview

This project is a command-line Employee Management System built with Python, SQLAlchemy ORM, and PostgreSQL.

It demonstrates how a Python application can interact with a relational database using ORM models instead of writing every database operation as raw SQL.

The application manages employee records and their associated departments. It also demonstrates database migrations, input validation, transaction management, and error handling.

## Objectives

- Connect a Python application to PostgreSQL.
- Define database tables using SQLAlchemy ORM models.
- Create and manage employee and department records.
- Implement CRUD operations.
- Establish relationships between ORM models.
- Use SQLAlchemy sessions and transactions.
- Apply database migrations using Alembic.
- Validate input and handle database errors safely.

## Features

- Add a new employee
- List employees
- Search for an employee
- Edit employee details
- Delete an employee
- Associate employees with departments
- Validate employee data
- Handle database integrity errors
- Manage database schema changes with Alembic

## Technologies Used

- Python
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Psycopg 3
- Git and GitHub

## Database Design

### Departments

Stores department information.

- `department_id`: Primary key
- `name`: Department name with a uniqueness constraint

### Employees

Stores employee information.

- `employee_id`: String primary key, such as `EMP001`
- `name`: Employee name
- `age`: Employee age
- `salary`: Employee salary
- `department_id`: Foreign key referencing the department

### Relationship

One department can have multiple employees, while each employee belongs to a department.

```text
Department (1) ───────── (Many) Employee
```

The relationship is represented in SQLAlchemy using `relationship()` and `back_populates`.

## Project Structure

```text
orm_demo/
├── README.md
├── main.py
├── models.py
├── run_demo.py
├── alembic.ini
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        ├── d135748973f7_initial_employee_schema.py
        └── df9266980121_add_positive_salary_constraint.py
```

*This is an illustrative structure based on the project context. Keep the actual filenames and migration revisions that exist in your folder.*

## Prerequisites

- Python installed
- PostgreSQL installed and running
- A PostgreSQL database and user with suitable permissions

## Setup Instructions

### 1. Create and activate a virtual environment

From the `orm_demo` directory:

```bash
python -m venv .venv
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

If your virtual environment already exists in a parent folder, activate that environment instead of creating another one.

### 2. Install dependencies

```bash
pip install sqlalchemy "psycopg[binary]" alembic
```

### 3. Create the PostgreSQL database

Connect to PostgreSQL and create the database if needed:

```sql
CREATE DATABASE employee_orm_demo;
```

### 4. Configure the database connection

The application uses PostgreSQL through SQLAlchemy and Psycopg.

Configure the connection settings according to the existing `run_demo.py` or `main.py` implementation. The database URL follows this pattern:

```text
postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

Do not commit database passwords to GitHub. If the application prompts for the password, enter it when requested.

### 5. Apply database migrations

If the project uses Alembic migrations, activate the correct environment and run:

```bash
alembic upgrade head
```

Run this command from the directory containing `alembic.ini`, and verify that the configured database URL points to the intended database.

### 6. Run the application

Use the actual entry point in your project. For example:

```bash
python main.py
```

If `run_demo.py` is intended to test the connection and initialize the schema, run:

```bash
python run_demo.py
```

Use the appropriate entry point for the intended task; the demo script and interactive application may serve different purposes.

## Key Concepts Learned

- SQLAlchemy declarative models
- `mapped_column()` and `Mapped`
- Primary keys and foreign keys
- ORM relationships and `back_populates`
- CRUD operations
- `create_engine()` and connection pooling
- SQLAlchemy sessions and transactions
- Lazy loading and eager loading
- Database integrity constraints
- Exception handling
- Alembic migrations
- PostgreSQL integration with Python

## Expected Learning Outcomes

After completing this project, I can create ORM models, connect Python to PostgreSQL, perform employee CRUD operations, establish model relationships, manage transactions, and evolve the database schema with Alembic.

## Security and Maintenance

- Never commit passwords or secret credentials.
- Keep virtual environments and `__pycache__` out of Git.
- Apply migrations to the intended database.
- Test schema changes against a development database before using them elsewhere.

## Author

Created as part of my Python and database training.
