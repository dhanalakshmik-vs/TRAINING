
BEGIN;

-- 1. Departments
INSERT INTO organization.departments (name)
VALUES
    ('IT'),
    ('Finance'),
    ('HR'),
    ('Operations')
ON CONFLICT (name) DO NOTHING;


-- 2. Expense categories
INSERT INTO organization.categories (name)
VALUES
    ('Travel'),
    ('Equipment'),
    ('Meals'),
    ('Software'),
    ('Training')
ON CONFLICT (name) DO NOTHING;


-- 3. Projects
INSERT INTO organization.projects (name, department_id)
SELECT v.name, d.department_id
FROM (
    VALUES
        ('Portal', 'IT'),
        ('Budget', 'Finance'),
        ('People', 'HR'),
        ('Analytics', 'IT')
) AS v(name, department_name)
JOIN organization.departments AS d
    ON d.name = v.department_name
ON CONFLICT (name) DO NOTHING;


-- 4. Top-level employees (no manager)
INSERT INTO organization.employees
    (employee_code, email, full_name, department_id,
     manager_id, hired_on, is_active)
SELECT
    v.employee_code,
    v.email,
    v.full_name,
    d.department_id,
    NULL,
    v.hired_on,
    TRUE
FROM (
    VALUES
        ('E01', 'alice.morgan@example.com', 'Alice Morgan', 'IT',
         DATE '2022-01-10'),
        ('E05', 'emma.davis@example.com', 'Emma Davis', 'Finance',
         DATE '2021-04-12'),
        ('E09', 'isha.patel@example.com', 'Isha Patel', 'HR',
         DATE '2023-02-20')
) AS v(employee_code, email, full_name, department_name, hired_on)
JOIN organization.departments AS d
    ON d.name = v.department_name
ON CONFLICT (employee_code) DO NOTHING;


-- 5. Second-level employees
INSERT INTO organization.employees
    (employee_code, email, full_name, department_id,
     manager_id, hired_on, is_active)
SELECT
    v.employee_code,
    v.email,
    v.full_name,
    d.department_id,
    m.employee_id,
    v.hired_on,
    TRUE
FROM (
    VALUES
        ('E02', 'ben.carter@example.com', 'Ben Carter', 'IT',
         'E01', DATE '2022-06-15'),
        ('E06', 'farah.khan@example.com', 'Farah Khan', 'Finance',
         'E05', DATE '2022-08-01'),
        ('E10', 'jay.thomas@example.com', 'Jay Thomas', 'HR',
         'E09', DATE '2023-05-10')
) AS v(employee_code, email, full_name, department_name,
       manager_code, hired_on)
JOIN organization.departments AS d
    ON d.name = v.department_name
JOIN organization.employees AS m
    ON m.employee_code = v.manager_code
ON CONFLICT (employee_code) DO NOTHING;


-- 6. Third-level employees
INSERT INTO organization.employees
    (employee_code, email, full_name, department_id,
     manager_id, hired_on, is_active)
SELECT
    v.employee_code,
    v.email,
    v.full_name,
    d.department_id,
    m.employee_id,
    v.hired_on,
    TRUE
FROM (
    VALUES
        ('E03', 'cara.wilson@example.com', 'Cara Wilson', 'IT',
         'E02', DATE '2023-01-09'),
        ('E04', 'dev.kumar@example.com', 'Dev Kumar', 'IT',
         'E02', DATE '2023-03-13'),
        ('E07', 'gopal.rao@example.com', 'Gopal Rao', 'Finance',
         'E06', DATE '2023-07-17'),
        ('E08', 'hari.nair@example.com', 'Hari Nair', 'Finance',
         'E06', DATE '2024-02-05'),
        ('E11', 'kiran.joseph@example.com', 'Kiran Joseph', 'HR',
         'E10', DATE '2024-06-03'),
        ('E12', 'leena.paul@example.com', 'Leena Paul', 'HR',
         'E10', DATE '2024-09-16')
) AS v(employee_code, email, full_name, department_name,
       manager_code, hired_on)
JOIN organization.departments AS d
    ON d.name = v.department_name
JOIN organization.employees AS m
    ON m.employee_code = v.manager_code
ON CONFLICT (employee_code) DO NOTHING;


-- 7. Six optional employee profiles
INSERT INTO organization.employee_profiles
    (employee_id, phone, address)
SELECT e.employee_id, v.phone, v.address
FROM (
    VALUES
        ('E01', '9000000001', '12 Lake Road'),
        ('E02', '9000000002', '24 Hill Street'),
        ('E03', '9000000003', '8 Garden Avenue'),
        ('E05', '9000000005', '19 Park Lane'),
        ('E06', '9000000006', '31 River Road'),
        ('E09', '9000000009', '5 Market Street')
) AS v(employee_code, phone, address)
JOIN organization.employees AS e
    ON e.employee_code = v.employee_code
ON CONFLICT (employee_id) DO NOTHING;


-- 8. Twelve employee-project assignments
INSERT INTO organization.employee_projects
    (employee_id, project_id, assigned_on)
SELECT e.employee_id, p.project_id, v.assigned_on
FROM (
    VALUES
        ('E01', 'Portal',    DATE '2026-01-05'),
        ('E01', 'Analytics',DATE '2026-01-06'),
        ('E02', 'Portal',    DATE '2026-01-10'),
        ('E03', 'Portal',    DATE '2026-01-12'),
        ('E04', 'Analytics',DATE '2026-01-15'),
        ('E05', 'Budget',    DATE '2026-02-01'),
        ('E06', 'Budget',    DATE '2026-02-05'),
        ('E07', 'Budget',    DATE '2026-02-08'),
        ('E08', 'Analytics',DATE '2026-02-12'),
        ('E09', 'People',    DATE '2026-03-01'),
        ('E10', 'People',    DATE '2026-03-05'),
        ('E11', 'People',    DATE '2026-03-10')
) AS v(employee_code, project_name, assigned_on)
JOIN organization.employees AS e
    ON e.employee_code = v.employee_code
JOIN organization.projects AS p
    ON p.name = v.project_name
ON CONFLICT (employee_id, project_id) DO NOTHING;


-- 9. Forty expenses: 10 in each of four categories.
-- Training intentionally has no expenses.
-- Employees E11 and E12 intentionally have no expenses.
-- Two July monthly totals tie at 849.99 for E01 and E02.

WITH seed_expenses
    (employee_code, category_name, amount, occurred_on,
     description, status) AS (
    VALUES
        -- Travel: 10 expenses; no rejected status
        ('E01', 'Travel',    200.00::NUMERIC(12,2), DATE '2026-07-05', 'Client visit',       'approved'),
        ('E02', 'Travel',    250.00::NUMERIC(12,2), DATE '2026-07-05', 'Site visit',         'submitted'),
        ('E03', 'Travel',    180.00::NUMERIC(12,2), DATE '2026-07-18', 'Team meeting',      'approved'),
        ('E04', 'Travel',    220.00::NUMERIC(12,2), DATE '2026-08-03', 'Business trip',     'submitted'),
        ('E05', 'Travel',    350.00::NUMERIC(12,2), DATE '2026-08-11', 'Vendor meeting',    'approved'),
        ('E06', 'Travel',    125.00::NUMERIC(12,2), DATE '2026-08-19', 'Office visit',      'submitted'),
        ('E07', 'Travel',    410.00::NUMERIC(12,2), DATE '2026-09-02', 'Conference travel', 'approved'),
        ('E08', 'Travel',    160.00::NUMERIC(12,2), DATE '2026-09-09', 'Project visit',     'submitted'),
        ('E09', 'Travel',    275.00::NUMERIC(12,2), DATE '2026-09-15', 'Training travel',   'approved'),
        ('E10', 'Travel',    190.00::NUMERIC(12,2), DATE '2026-09-22', 'Client meeting',    'submitted'),

        -- Equipment: 10 expenses; no rejected status
        ('E01', 'Equipment', 500.00::NUMERIC(12,2), DATE '2026-07-08', 'Laptop purchase',   'approved'),
        ('E02', 'Equipment', 450.00::NUMERIC(12,2), DATE '2026-07-08', 'Monitor purchase',  'submitted'),
        ('E03', 'Equipment', 125.00::NUMERIC(12,2), DATE '2026-07-21', 'Keyboard and mouse','approved'),
        ('E04', 'Equipment', 275.00::NUMERIC(12,2), DATE '2026-08-04', 'Office equipment',  'submitted'),
        ('E05', 'Equipment', 620.00::NUMERIC(12,2), DATE '2026-08-12', 'Workstation',       'approved'),
        ('E06', 'Equipment', 180.00::NUMERIC(12,2), DATE '2026-08-20', 'Headset',           'submitted'),
        ('E07', 'Equipment', 330.00::NUMERIC(12,2), DATE '2026-09-03', 'Storage device',    'approved'),
        ('E08', 'Equipment', 215.00::NUMERIC(12,2), DATE '2026-09-10', 'Office supplies',   'submitted'),
        ('E09', 'Equipment', 540.00::NUMERIC(12,2), DATE '2026-09-16', 'Computer parts',    'approved'),
        ('E10', 'Equipment', 145.00::NUMERIC(12,2), DATE '2026-09-23', 'Adapter purchase',  'submitted'),

        -- Meals: 10 expenses; no approved status
        ('E01', 'Meals',      50.00::NUMERIC(12,2), DATE '2026-07-12', 'Team lunch',        'rejected'),
        ('E02', 'Meals',      80.00::NUMERIC(12,2), DATE '2026-07-12', 'Client lunch',      'rejected'),
        ('E03', 'Meals',      35.00::NUMERIC(12,2), DATE '2026-07-25', 'Working lunch',     'rejected'),
        ('E04', 'Meals',      65.00::NUMERIC(12,2), DATE '2026-08-06', 'Project lunch',     'rejected'),
        ('E05', 'Meals',      95.00::NUMERIC(12,2), DATE '2026-08-14', 'Client dinner',     'rejected'),
        ('E06', 'Meals',      42.00::NUMERIC(12,2), DATE '2026-08-22', 'Team meal',         'rejected'),
        ('E07', 'Meals',      55.00::NUMERIC(12,2), DATE '2026-09-05', 'Meeting meal',      'rejected'),
        ('E08', 'Meals',      72.00::NUMERIC(12,2), DATE '2026-09-12', 'Project meal',      'rejected'),
        ('E09', 'Meals',      38.00::NUMERIC(12,2), DATE '2026-09-18', 'Working meal',      'rejected'),
        ('E10', 'Meals',      60.00::NUMERIC(12,2), DATE '2026-09-25', 'Team dinner',       'rejected'),

        -- Software: 10 expenses; mixed statuses and NULL descriptions
        ('E01', 'Software',   99.99::NUMERIC(12,2), DATE '2026-07-15', 'Software licence',  'approved'),
        ('E02', 'Software',   69.99::NUMERIC(12,2), DATE '2026-07-15', 'Monthly licence',  'submitted'),
        ('E03', 'Software',   25.00::NUMERIC(12,2), DATE '2026-07-28', NULL,                'draft'),
        ('E04', 'Software',  100.00::NUMERIC(12,2), DATE '2026-08-08', 'Cloud service',     'approved'),
        ('E05', 'Software',  500.00::NUMERIC(12,2), DATE '2026-08-16', 'Annual subscription','submitted'),
        ('E06', 'Software',   49.99::NUMERIC(12,2), DATE '2026-08-24', NULL,                'rejected'),
        ('E07', 'Software',  120.00::NUMERIC(12,2), DATE '2026-09-07', 'Developer tool',    'approved'),
        ('E08', 'Software',   85.50::NUMERIC(12,2), DATE '2026-09-14', 'Security software', 'submitted'),
        ('E09', 'Software',  650.00::NUMERIC(12,2), DATE '2026-09-20', 'Platform renewal', 'draft'),
        ('E10', 'Software',   15.00::NUMERIC(12,2), DATE '2026-09-27', 'Utility tool',      'rejected')
)
INSERT INTO organization.expenses
    (employee_id, category_id, amount, occurred_on,
     description, status, updated_at)
SELECT
    e.employee_id,
    c.category_id,
    s.amount,
    s.occurred_on,
    s.description,
    s.status,
    s.occurred_on::TIMESTAMP AT TIME ZONE 'Asia/Kolkata'
FROM seed_expenses AS s
JOIN organization.employees AS e
    ON e.employee_code = s.employee_code
JOIN organization.categories AS c
    ON c.name = s.category_name
WHERE NOT EXISTS (
    SELECT 1
    FROM organization.expenses AS existing
    WHERE existing.employee_id = e.employee_id
      AND existing.category_id = c.category_id
      AND existing.amount = s.amount
      AND existing.occurred_on = s.occurred_on
      AND existing.description IS NOT DISTINCT FROM s.description
      AND existing.status = s.status
);

COMMIT;
