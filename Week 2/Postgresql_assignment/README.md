# PostgreSQL Organization Expenses Management

## Project Overview

This project focuses on relational database design and PostgreSQL concepts through an organization expense management system. It demonstrates how to design a normalized database, maintain data integrity, write SQL queries, and implement database programmability and performance checks.

The database uses the `org_expenses` database and the `organization` schema.

## Objectives

- Design relational tables with appropriate primary keys, foreign keys, and alternate keys.
- Implement relationships between employees, departments, projects, categories, and expenses.
- Apply normalization principles and database constraints.
- Write SQL queries for retrieving, filtering, and summarizing business data.
- Use transactions and understand ACID properties.
- Create indexes to support query performance.
- Implement database functions, procedures, and triggers.
- Apply database roles and permissions.
- Test database integrity, rebuilds, and performance.

## Database Design

The project includes seven main tables:

| Table | Purpose |
|---|---|
| `departments` | Stores department information. |
| `employees` | Stores employee details and reporting relationships. |
| `employee_profiles` | Stores optional one-to-one employee profile information. |
| `categories` | Stores expense categories. |
| `projects` | Stores project information. |
| `employee_projects` | Connects employees and projects through a many-to-many relationship. |
| `expenses` | Stores employee expense records and their approval status. |

## Technologies Used

- PostgreSQL
- SQL
- Python
- SQLAlchemy ORM
- Git and GitHub

## Key Concepts Covered

- Relational database design and ER diagrams
- Primary keys, foreign keys, alternate keys, and constraints
- One-to-one, one-to-many, and many-to-many relationships
- Normalization
- Joins, aggregate functions, subqueries, and window functions
- Transactions, `COMMIT`, and `ROLLBACK`
- Indexes and query performance
- Functions, procedures, and triggers
- Audit logging and protected database operations
- Roles and privileges
- SQLAlchemy ORM and parameterized queries

## Project Structure

```text
Postgresql_assignment/
├── README.md
├── models_orm.py
├── q50_orm_checks.py
├── run_models.py
└── sql/
    ├── 00_database.sql
    ├── 01_schema.sql
    ├── 02_parent_tables.sql
    ├── 02_seed.sql
    ├── 02_verify_seed.sql
    ├── 03_employee_tables.sql
    ├── 04_expenses_and_projects.sql
    ├── 04_roles.sql
    ├── 05_indexes.sql
    ├── 06_programmability.sql
    ├── 07_audit_trigger.sql
    ├── 08_protected_expenses.sql
    ├── 09_submit_expense.sql
    └── 10_business_reports.sql
```

*The structure above shows the main files and examples of SQL scripts; retain any additional scripts present in your actual project.*

## Prerequisites

- PostgreSQL installed
- Python installed
- `pip` available
- A PostgreSQL role with the required database permissions

## Setup

### 1. Create and activate a virtual environment

From the project directory:

```bash
python -m venv .venv
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 2. Install Python dependencies

Install the packages required by the project, such as SQLAlchemy and the PostgreSQL driver used by your scripts:

```bash
pip install sqlalchemy "psycopg[binary]"
```

### 3. Create the database

Connect to PostgreSQL and create the database if it does not already exist:

```sql
CREATE DATABASE org_expenses;
```

### 4. Run the SQL scripts

Run the SQL scripts in the order required by their dependencies. Database creation may need to be performed separately while connected to a maintenance database.

For example, using `psql`:

```bash
psql -U postgres -d org_expenses -f sql/01_schema.sql
```

Adjust the database, schema, and script names to match the setup instructions in the actual files. Some scripts may require prerequisite tables or permissions.

### 5. Run the Python checks

Use the commands appropriate to the scripts included in the project:

```bash
python run_models.py
python q50_orm_checks.py
```

## Expected Learning Outcomes

After completing this project, I can explain relational database design, write SQL for business requirements, enforce data integrity, use transactions, manage permissions, and implement database programmability in PostgreSQL.

## Notes

- Keep database passwords and other credentials out of source control.
- Use `.env` or environment variables for sensitive configuration where applicable.
- Run destructive rebuild scripts only against a test database.
- Check the individual SQL scripts before executing them against an existing database.

## Author

Created as part of my database and Python training.
