
CREATE TABLE organization.departments (
    department_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE organization.categories (
    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE organization.projects (
    project_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,

    CONSTRAINT fk_projects_department
        FOREIGN KEY (department_id)
        REFERENCES organization.departments(department_id)
        ON DELETE RESTRICT
);