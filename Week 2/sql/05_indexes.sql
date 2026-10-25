-- 1. List existing indexes.
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'organization'
ORDER BY tablename, indexname;

-- 1. Support employee expense searches within a date range.
CREATE INDEX IF NOT EXISTS idx_expenses_employee_occurred
    ON organization.expenses (employee_id, occurred_on);

-- 2. Support queries that retrieve submitted expenses by date.
CREATE INDEX IF NOT EXISTS idx_expenses_submitted_date
    ON organization.expenses (occurred_on)
    WHERE status = 'submitted';

-- 3. Support case-insensitive employee-name lookups.
CREATE INDEX IF NOT EXISTS idx_employees_lower_full_name
    ON organization.employees (lower(full_name));

-- Verify the indexes after creation.
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'organization'
ORDER BY tablename, indexname;