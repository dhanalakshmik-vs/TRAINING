SELECT 'departments' AS table_name, COUNT(*) AS row_count
FROM organization.departments

UNION ALL

SELECT 'employees', COUNT(*)
FROM organization.employees

UNION ALL

SELECT 'employee_profiles', COUNT(*)
FROM organization.employee_profiles

UNION ALL

SELECT 'categories', COUNT(*)
FROM organization.categories

UNION ALL

SELECT 'projects', COUNT(*)
FROM organization.projects

UNION ALL

SELECT 'employee_projects', COUNT(*)
FROM organization.employee_projects

UNION ALL

SELECT 'expenses', COUNT(*)
FROM organization.expenses

ORDER BY table_name;

SELECT
    COUNT(*) AS total_expenses,
    COALESCE(SUM(amount), 0) AS total_expense_amount
FROM organization.expenses;

-- 3. Per-category expense counts and totals (includes categories with no expenses)
SELECT
    c.name AS category_name,
    COUNT(e.expense_id) AS expense_count,
    COALESCE(SUM(e.amount), 0) AS total_amount
FROM organization.categories AS c
LEFT JOIN organization.expenses AS e
    ON e.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY c.name;
