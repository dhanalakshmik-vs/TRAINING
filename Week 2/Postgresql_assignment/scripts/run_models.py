"""Connect to PostgreSQL and create the ORM tables."""

from getpass import getpass
from sqlalchemy import URL, create_engine, text
from models_orm import Base


def main()-> None:
    """Connect to the database and create missing ORM tables."""
    password = getpass("Enter PostgreSQL password: ")

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_migration_test",
    )

    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("PostgreSQL connection successful!")

        Base.metadata.create_all(engine)
        print("Employee and Department tables created successfully!")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
