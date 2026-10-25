1.    SELECT
    d.name AS department_name,
    COUNT(ex.expense_id) AS total_expenses,
    COALESCE(SUM(ex.amount), 0) AS total_amount
FROM organization.departments d
LEFT JOIN organization.employees e  
    ON e.department_id = d.department_id
LEFT JOIN organization.expenses ex
    ON ex.employee_id = e.employee_id
GROUP BY d.department_id, d.name
ORDER BY total_amount DESC;

2. SELECT
    c.name AS category_name,
    COUNT(ex.expense_id) AS total_expenses,
    COALESCE(SUM(ex.amount), 0) AS total_amount
FROM organization.categories c
LEFT JOIN organization.expenses ex
    ON ex.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY total_amount DESC;

3. SELECT
    ex.status,
    COUNT(*) AS total_expenses,
    SUM(ex.amount) AS total_amount
FROM organization.expenses ex
GROUP BY ex.status
ORDER BY total_amount DESC;

4. SELECT
    e.employee_code,
    e.full_name,
    COUNT(ex.expense_id) AS total_expenses,
    COALESCE(SUM(ex.amount), 0) AS total_amount
FROM organization.employees e
LEFT JOIN organization.expenses ex
    ON ex.employee_id = e.employee_id
GROUP BY e.employee_id, e.employee_code, e.full_name
ORDER BY total_amount DESC;

5. SELECT
    DATE_TRUNC('month', occurred_on)::date AS expense_month,
    COUNT(*) AS total_expenses,
    SUM(amount) AS total_amount
FROM organization.expenses
GROUP BY DATE_TRUNC('month', occurred_on)
ORDER BY expense_month;

6. SELECT
    e.employee_code,
    e.full_name,
    ex.status,
    COUNT(ex.expense_id) AS total_expenses,
    SUM(ex.amount) AS total_amount
FROM organization.employees e
JOIN organization.expenses ex
    ON ex.employee_id = e.employee_id
GROUP BY
    e.employee_id,
    e.employee_code,
    e.full_name,
    ex.status
ORDER BY
    e.employee_code,
    ex.status;

7. SELECT
    e.employee_code AS employee_code,
    e.full_name AS employee_name,
    m.employee_code AS manager_code,
    m.full_name AS manager_name
FROM organization.employees e
LEFT JOIN organization.employees m
    ON e.manager_id = m.employee_id
ORDER BY e.employee_code;

8. SELECT
    e.employee_code,
    e.full_name
FROM organization.employees e
LEFT JOIN organization.expenses ex
    ON e.employee_id = ex.employee_id
WHERE ex.expense_id IS NULL
ORDER BY e.employee_code;

9. SELECT
    e.employee_code,
    e.full_name AS employee_name,
    p.name AS project_name
FROM organization.employees e
JOIN organization.employee_projects ep
    ON e.employee_id = ep.employee_id
JOIN organization.projects p
    ON ep.project_id = p.project_id
ORDER BY e.employee_code, p.name;

10. SELECT
    e.employee_code,
    e.full_name
FROM organization.employees e
LEFT JOIN organization.employee_projects ep
    ON e.employee_id = ep.employee_id
WHERE ep.employee_id IS NULL
ORDER BY e.employee_code;

-- Integrity Check 1 — Verify Foreign-Key Relationships
SELECT
    e.employee_code,
    e.full_name,
    e.department_id
FROM organization.employees e
LEFT JOIN organization.departments d
    ON e.department_id = d.department_id
WHERE d.department_id IS NULL;

-- Integrity Check 2 — Verify Expense Employee References
SELECT
    ex.expense_id,
    ex.employee_id
FROM organization.expenses ex
LEFT JOIN organization.employees e
    ON ex.employee_id = e.employee_id
WHERE e.employee_id IS NULL;

-- Integrity Check 3 — Verify All Foreign Keys Are Validated
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    convalidated AS is_validated
FROM pg_constraint
WHERE contype = 'f'
  AND connamespace = 'organization'::regnamespace
ORDER BY conrelid::regclass::text, conname;

-- Integrity Check 4 — Verify Check Constraints
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    pg_get_constraintdef(oid) AS constraint_definition,
    convalidated AS is_validated
FROM pg_constraint
WHERE contype = 'c'
  AND connamespace = 'organization'::regnamespace
ORDER BY conrelid::regclass::text, conname;

-- Integrity Check 5 — Verify Primary Keys and Unique Constraints
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE contype IN ('p', 'u')
  AND connamespace = 'organization'::regnamespace
ORDER BY conrelid::regclass::text, contype, conname;

-- Integrity Check 6 — Check for Duplicate Employee Emails
SELECT
    email,
    COUNT(*) AS occurrences
FROM organization.employees
GROUP BY email
HAVING COUNT(*) > 1;

CREATE OR REPLACE FUNCTION organization.capture_expense_audit()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, organization
AS $$
DECLARE
    invoking_role TEXT;
BEGIN
    invoking_role := NULLIF(
        current_setting('role', true),
        'none'
    );

    IF invoking_role IS NULL THEN
        invoking_role := session_user;
    END IF;

    IF TG_OP = 'INSERT' THEN
        INSERT INTO organization.expense_audit (
            expense_id,
            operation,
            old_data,
            new_data,
            changed_by,
            function_owner
        )
        VALUES (
            NEW.expense_id,
            TG_OP,
            NULL,
            pg_catalog.to_jsonb(NEW),
            invoking_role,
            current_user
        );

        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO organization.expense_audit (
            expense_id,
            operation,
            old_data,
            new_data,
            changed_by,
            function_owner
        )
        VALUES (
            NEW.expense_id,
            TG_OP,
            pg_catalog.to_jsonb(OLD),
            pg_catalog.to_jsonb(NEW),
            invoking_role,
            current_user
        );

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO organization.expense_audit (
            expense_id,
            operation,
            old_data,
            new_data,
            changed_by,
            function_owner
        )
        VALUES (
            OLD.expense_id,
            TG_OP,
            pg_catalog.to_jsonb(OLD),
            NULL,
            invoking_role,
            current_user
        );

        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_expenses_audit
AFTER INSERT OR UPDATE OR DELETE
ON organization.expenses
FOR EACH ROW
EXECUTE FUNCTION organization.capture_expense_audit();

REVOKE ALL ON TABLE organization.expense_audit
FROM PUBLIC, trainee_writer;

REVOKE CREATE ON SCHEMA organization
FROM PUBLIC, trainee_writer;

SELECT
    to_regclass('organization.expense_audit') AS audit_table;

SELECT
    trigger_name,
    event_manipulation,
    action_timing
FROM information_schema.triggers
WHERE trigger_schema = 'organization'
  AND event_object_table = 'expenses'
ORDER BY trigger_name, event_manipulation;

SELECT *
FROM organization.expense_audit
ORDER BY audit_id DESC
LIMIT 5;

SELECT MAX(expense_id) AS highest_expense_id
FROM organization.expenses;

BEGIN;
SET LOCAL ROLE trainee_writer;

INSERT INTO organization.expenses
    (employee_id, category_id, amount, occurred_on, description, status)
VALUES
    (1, 1, 12.50, DATE '2026-10-19',
     'Q42 audit INSERT test', 'draft')
RETURNING expense_id, amount, description;

SELECT
    audit_id,
    expense_id,
    operation,
    changed_by,
    function_owner,
    new_data
FROM organization.expense_audit
ORDER BY audit_id DESC
LIMIT 1;


CREATE OR REPLACE FUNCTION organization.protect_approved_expense()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.status = 'approved' THEN
        IF NEW.amount IS DISTINCT FROM OLD.amount
           OR NEW.category_id IS DISTINCT FROM OLD.category_id
           OR NEW.employee_id IS DISTINCT FROM OLD.employee_id
           OR NEW.occurred_on IS DISTINCT FROM OLD.occurred_on
        THEN
            RAISE EXCEPTION
                'Cannot change amount, category, employee, or date of an approved expense (expense_id=%)',
                OLD.expense_id;
        END IF;
    END IF;

    NEW.updated_at := CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_protect_approved_expense
BEFORE UPDATE
ON organization.expenses
FOR EACH ROW
EXECUTE FUNCTION organization.protect_approved_expense();