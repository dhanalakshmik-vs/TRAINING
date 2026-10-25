
-- 04_roles.sql
-- Create least-privilege group roles and grant business-table access.

-- Create roles only if they do not already exist.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'trainee_reader'
    ) THEN
        CREATE ROLE trainee_reader NOLOGIN;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'trainee_writer'
    ) THEN
        CREATE ROLE trainee_writer NOLOGIN;
    END IF;
END
$$;

-- Database and schema access.
GRANT CONNECT ON DATABASE org_expenses
TO trainee_reader, trainee_writer;

GRANT USAGE ON SCHEMA organization
TO trainee_reader, trainee_writer;

-- Reader: read-only access to business tables.
GRANT SELECT ON TABLE
    organization.categories,
    organization.departments,
    organization.employee_profiles,
    organization.employee_projects,
    organization.employees,
    organization.expenses,
    organization.projects
TO trainee_reader;

-- Writer: read and modify business tables.
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE
    organization.categories,
    organization.departments,
    organization.employee_profiles,
    organization.employee_projects,
    organization.employees,
    organization.expenses,
    organization.projects
TO trainee_writer;
