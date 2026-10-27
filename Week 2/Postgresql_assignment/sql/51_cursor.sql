DO $$
DECLARE
    employee_cursor CURSOR FOR
        SELECT employee_id, full_name
        FROM organization.employees;

    employee_record RECORD;
BEGIN
    OPEN employee_cursor;

    LOOP
        FETCH employee_cursor INTO employee_record;

        EXIT WHEN NOT FOUND;

        RAISE NOTICE 'Employee ID: %, Name: %',
            employee_record.employee_id,
            employee_record.full_name;
    END LOOP;

    CLOSE employee_cursor;
END;
$$;


### OUTPUT:
    org_expenses=# \i 51_cursor.sql
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 4, Name: Test Employee
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 7, Name: Alice Morgan
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 8, Name: Emma Davis
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 9, Name: Isha Patel
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 10, Name: Ben Carter
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 11, Name: Farah Khan
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 12, Name: Jay Thomas
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 13, Name: Cara Wilson
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 14, Name: Dev Kumar
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 15, Name: Gopal Rao
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 16, Name: Hari Nair
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 17, Name: Kiran Joseph
    psql:51_cursor.sql:23: NOTICE:  Employee ID: 18, Name: Leena Paul
    DO