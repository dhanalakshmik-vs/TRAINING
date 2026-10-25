
CREATE OR REPLACE PROCEDURE organization.submit_expense(
    p_expense_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_status VARCHAR;
BEGIN
    -- Find the expense and lock its row against concurrent updates.
    SELECT status
    INTO v_current_status
    FROM organization.expenses
    WHERE expense_id = p_expense_id
    FOR UPDATE;

    -- Raise a clear error if the expense does not exist.
    IF NOT FOUND THEN
        RAISE EXCEPTION
            'Expense ID % does not exist', p_expense_id;
    END IF;

    -- Only draft expenses can be submitted.
    IF v_current_status IS DISTINCT FROM 'draft' THEN
        RAISE EXCEPTION
            'Cannot submit expense ID %: current status is "%"; only draft expenses can be submitted',
            p_expense_id, v_current_status;
    END IF;

    -- Change the status. The Q42 audit trigger records this update.
    UPDATE organization.expenses
    SET status = 'submitted'
    WHERE expense_id = p_expense_id;
END;
$$;
