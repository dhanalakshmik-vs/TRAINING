
-- Q10: Expenses and employee-project assignments

CREATE TABLE organization.expenses (
    expense_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    occurred_on DATE NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_expenses_positive_amount
        CHECK (amount > 0),

    CONSTRAINT chk_expenses_valid_status
        CHECK (status IN ('draft', 'submitted', 'approved', 'rejected')),

    CONSTRAINT fk_expenses_employee
        FOREIGN KEY (employee_id)
        REFERENCES organization.employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_expenses_category
        FOREIGN KEY (category_id)
        REFERENCES organization.categories(category_id)
        ON DELETE RESTRICT
);


CREATE TABLE organization.employee_projects (
    employee_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    assigned_on DATE NOT NULL,

    CONSTRAINT pk_employee_projects
        PRIMARY KEY (employee_id, project_id),

    CONSTRAINT fk_employee_projects_employee
        FOREIGN KEY (employee_id)
        REFERENCES organization.employees(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_employee_projects_project
        FOREIGN KEY (project_id)
        REFERENCES organization.projects(project_id)
        ON DELETE CASCADE
);

