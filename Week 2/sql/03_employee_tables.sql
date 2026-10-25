
CREATE TABLE organization.employees (
    employee_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_code VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    department_id INTEGER NOT NULL,
    manager_id INTEGER,
    hired_on DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_employee_email_lowercase
        CHECK (email = LOWER(email)),

    CONSTRAINT fk_employees_department
        FOREIGN KEY (department_id)
        REFERENCES organization.departments(department_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employees_manager
        FOREIGN KEY (manager_id)
        REFERENCES organization.employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_not_own_manager
        CHECK (
            manager_id IS NULL
            OR manager_id <> employee_id
        )
);

CREATE TABLE organization.employee_profiles (
    employee_id INTEGER PRIMARY KEY,
    phone VARCHAR(30),
    address TEXT,

    CONSTRAINT fk_employee_profiles_employee
        FOREIGN KEY (employee_id)
        REFERENCES organization.employees(employee_id)
        ON DELETE CASCADE
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'organization'
  AND table_name IN ('employees', 'employee_profiles')
ORDER BY table_name;

INSERT INTO organization.employees
    (employee_code, email, full_name, department_id, hired_on)
SELECT
    'Q9TEST001',
    'q9test001@example.com',
    'Test Employee',
    department_id,
    DATE '2026-10-14'
FROM organization.departments
WHERE name = 'test_department'
ON CONFLICT (employee_code) DO NOTHING;

INSERT INTO organization.employee_profiles
    (employee_id, phone, address)
SELECT
    employee_id,
    '6727672628',
    'Another Address'
FROM organization.employees
WHERE employee_code = 'Q9TEST001';

INSERT INTO organization.employees
    (employee_code, email, full_name, department_id, hired_on)
SELECT
    'Q9TEST001',
    'different@example.com',
    'Another Employee',
    department_id,
    DATE '2026-10-14'
FROM organization.departments
WHERE name = 'test_department';