
-- Q41: User-defined scalar function

-- Create the requested schema in the performance database
-- if it does not already exist.
-- CREATE SCHEMA IF NOT EXISTS organization;

CREATE OR REPLACE FUNCTION organization.expense_band(p_amount NUMERIC)
RETURNS TEXT
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_amount IS NULL THEN 'Unknown'
        WHEN p_amount <= 0 THEN 'Invalid amount'
        WHEN p_amount < 100 THEN 'Below 100'
        WHEN p_amount <= 500 THEN '100-500'
        ELSE 'Above 500'
    END;
$$;
