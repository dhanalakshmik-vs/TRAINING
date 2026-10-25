
WITH employee_monthly_spend AS (
    SELECT
        e.department_id,
        d.name AS department_name,
        e.employee_id,
        e.employee_code,
        e.full_name,
        DATE_TRUNC('month', ex.occurred_on)::date AS expense_month,
        SUM(ex.amount) AS monthly_spend
    FROM organization.employees AS e
    JOIN organization.departments AS d
        ON d.department_id = e.department_id
    JOIN organization.expenses AS ex
        ON ex.employee_id = e.employee_id
    GROUP BY
        e.department_id,
        d.name,
        e.employee_id,
        e.employee_code,
        e.full_name,
        DATE_TRUNC('month', ex.occurred_on)::date
)
SELECT
    department_name,
    employee_code,
    full_name,
    expense_month,
    monthly_spend,
    DENSE_RANK() OVER (
        PARTITION BY department_id, expense_month
        ORDER BY monthly_spend DESC
    ) AS spend_rank
FROM employee_monthly_spend
ORDER BY
    expense_month,
    department_name,
    spend_rank,
    employee_code;


WITH employee_monthly_spend AS (
    SELECT
        e.employee_id,
        e.employee_code,
        e.full_name,
        DATE_TRUNC('month', ex.occurred_on)::date AS expense_month,
        SUM(ex.amount) AS monthly_spend
    FROM organization.employees AS e
    JOIN organization.expenses AS ex
        ON ex.employee_id = e.employee_id
    GROUP BY
        e.employee_id,
        e.employee_code,
        e.full_name,
        DATE_TRUNC('month', ex.occurred_on)::date
)
SELECT
    employee_code,
    full_name,
    expense_month,
    monthly_spend,
    SUM(monthly_spend) OVER (
        PARTITION BY employee_id
        ORDER BY expense_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM employee_monthly_spend
ORDER BY
    employee_code,
    expense_month;
