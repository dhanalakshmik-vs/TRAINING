
CREATE OR REPLACE FUNCTION organization.protect_expense_update()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Prevent changes to important fields after approval.
    IF OLD.status = 'approved' AND (
        NEW.amount IS DISTINCT FROM OLD.amount
        OR NEW.category_id IS DISTINCT FROM OLD.category_id
        OR NEW.employee_id IS DISTINCT FROM OLD.employee_id
        OR NEW.occurred_on IS DISTINCT FROM OLD.occurred_on
    ) THEN
        RAISE EXCEPTION
            'Approved expenses cannot change amount, category, employee, or date';
    END IF;

    -- Enforce the documented status-transition policy.
    IF OLD.status = 'draft' THEN
        IF NEW.status NOT IN ('draft', 'submitted') THEN
            RAISE EXCEPTION
                'Draft expenses can only remain draft or become submitted';
        END IF;

    ELSIF OLD.status = 'submitted' THEN
        IF NEW.status NOT IN ('submitted', 'approved', 'rejected') THEN
            RAISE EXCEPTION
                'Submitted expenses can remain submitted, be approved, or be rejected';
        END IF;

    ELSIF OLD.status = 'approved' THEN
        IF NEW.status IS DISTINCT FROM 'approved' THEN
            RAISE EXCEPTION
                'Approved expenses cannot change status';
        END IF;

    ELSIF OLD.status = 'rejected' THEN
        IF NEW.status IS DISTINCT FROM 'rejected' THEN
            RAISE EXCEPTION
                'Rejected expenses cannot change status';
        END IF;
    END IF;

    -- Update the timestamp for every accepted UPDATE.
    NEW.updated_at := clock_timestamp();

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_protect_expense_update
ON organization.expenses;

CREATE TRIGGER trg_protect_expense_update
BEFORE UPDATE ON organization.expenses
FOR EACH ROW
EXECUTE FUNCTION organization.protect_expense_update();
