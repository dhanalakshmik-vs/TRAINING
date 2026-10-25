CREATE TABLE IF NOT EXISTS organization.expense_audit (
    audit_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    action_type TEXT NOT NULL
        CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE')),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    invoking_role TEXT NOT NULL,
    definer_role TEXT NOT NULL,
    old_data JSONB,
    new_data JSONB
);

CREATE OR REPLACE FUNCTION organization.audit_expense_change()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, pg_temp
AS $$
BEGIN
    INSERT INTO organization.expense_audit (
        expense_id,
        action_type,
        changed_at,
        invoking_role,
        definer_role,
        old_data,
        new_data
    )
    VALUES (
        CASE
            WHEN TG_OP = 'DELETE' THEN OLD.expense_id
            ELSE NEW.expense_id
        END,
        TG_OP,
        clock_timestamp(),
        CASE
            WHEN current_setting('role') = 'none'
                THEN session_user::text
            ELSE current_setting('role')
        END,
        current_user::text,
        CASE
            WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD)
            ELSE NULL
        END,
        CASE
            WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW)
            ELSE NULL
        END
    );

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_expense_audit
ON organization.expenses;

CREATE TRIGGER trg_expense_audit
AFTER INSERT OR UPDATE OR DELETE
ON organization.expenses
FOR EACH ROW
EXECUTE FUNCTION organization.audit_expense_change();

REVOKE ALL ON TABLE organization.expense_audit FROM PUBLIC;
REVOKE ALL ON TABLE organization.expense_audit FROM trainee_writer;

REVOKE ALL ON SEQUENCE organization.expense_audit_audit_id_seq
FROM PUBLIC, trainee_writer;

REVOKE CREATE ON SCHEMA organization FROM trainee_writer;

SELECT
    n.nspname AS schema_name,
    c.relname AS object_name,
    pg_get_userbyid(c.relowner) AS owner
FROM pg_class AS c
JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
WHERE n.nspname = 'organization'
  AND c.relname IN ('expenses', 'expense_audit')
ORDER BY c.relname;

SELECT
    p.proname AS function_name,
    pg_get_userbyid(p.proowner) AS function_owner,
    p.prosecdef AS security_definer,
    p.proconfig AS function_settings
FROM pg_proc AS p
JOIN pg_namespace AS n
    ON n.oid = p.pronamespace
WHERE n.nspname = 'organization'
  AND p.proname = 'audit_expense_change';

SELECT
    has_table_privilege(
        'trainee_writer',
        'organization.expenses',
        'INSERT'
    ) AS can_insert_expense,
    has_table_privilege(
        'trainee_writer',
        'organization.expenses',
        'UPDATE'
    ) AS can_update_expense,
    has_table_privilege(
        'trainee_writer',
        'organization.expenses',
        'DELETE'
    ) AS can_delete_expense,
    has_table_privilege(
        'trainee_writer',
        'organization.expense_audit',
        'INSERT'
    ) AS can_insert_audit,
    has_table_privilege(
        'trainee_writer',
        'organization.expense_audit',
        'UPDATE'
    ) AS can_update_audit,
    has_table_privilege(
        'trainee_writer',
        'organization.expense_audit',
        'DELETE'
    ) AS can_delete_audit;

BEGIN;

SET LOCAL ROLE trainee_writer;

-- 1. Insert a temporary expense
INSERT INTO organization.expenses
    (employee_id, category_id, amount, occurred_on, description, status)
VALUES
    (7, 1, 125.00, DATE '2026-10-18',
     'Q42 audit trigger test', 'submitted')
RETURNING expense_id, amount, status;

UPDATE organization.expenses
SET amount = 150.00,
    description = 'Q42 audit update test'
WHERE expense_id = 55
RETURNING expense_id, amount, description, status;

DELETE FROM organization.expenses
WHERE expense_id = 55
RETURNING expense_id, amount, description;

RESET ROLE;

SELECT
    audit_id,
    expense_id,
    action_type,
    invoking_role,
    definer_role,
    old_data,
    new_data
FROM organization.expense_audit
WHERE expense_id = 55
ORDER BY audit_id;

ROLLBACK;
