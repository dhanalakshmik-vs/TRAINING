BEGIN;
INSERT INTO organization.employees
    (employee_code, full_name, email, department_id,
     manager_id, hired_on, is_active)
SELECT
    'E021',
    'Ramesh',
    email,
    department_id,
    NULL,
    DATE '2026-06-15',
    TRUE
FROM organization.employees
WHERE employee_code = 'E01'
 
 ROLLBACK;
 
    INSERT INTO organizatn.employees
        (employee_code, full_name, email, department_id,
        manager_id, hired_on, is_active)
    SELECT
        'E021',
        NULL,
        'ramesh@gmail.com',
        department_id,
        NULL,
        DATE '2026-06-15',
        TRUE
    FROM organization.departments
    WHERE name = 'IT'

INSERT INTO organizion.expenses
    (employee_id, category_id, amount, occurred_on, description, status)
VALUES
    (25, 1, 0, DATE '2026-06-15',
    'Q12 zero amount test', 'draft')

INSERT INTO organization.expenses
    (employee_id, category_id, amount, occurred_on, description, status)
VALUES
    (4, 1, 100, DATE '2026-06-15',
     'Q12 invalid status test', 'pending_review');


INSERT INTO organization.
    (employee_id, category_id, amount, occurred_on, description, status)
VALUES
    (999999, 1, 100, DATE '2026-06-15',
     'Q12 missing parent test', 'draft');

SELECT employee_id, project_id, assigned_on
FROM organization.employee_projects
LIMIT 1;

INSERT INTO organization.employee_projects
    (employee_id, project_id, assigned_on)
VALUES
    (16, 1, DATE '2026-06-15');

SELECT employee_code, full_name, email
FROM organization.employees
WHERE is_active = TRUE
  AND hired_on < DATE '2026-07-01'
ORDER BY full_name, employee_id
LIMIT 5;

SELECT employee_id, employee_code, full_name, manager_id
FROM organization.employees
WHERE manager_id IS NULL
ORDER BY employee_id;

SELECT expense_id, description, amount, occurred_on
FROM organization.expenses
WHERE description ILIKE '%taxi%'
ORDER BY expense_id;

SELECT expense_id, occurred_on, amount, description
FROM organization.expenses
WHERE occurred_on >= DATE '2026-07-01'
  AND occurred_on < DATE '2026-10-01'
  AND amount BETWEEN 100 AND 1000
ORDER BY occurred_on, expense_id;


