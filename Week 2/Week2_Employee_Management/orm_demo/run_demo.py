
from getpass import getpass

from sqlalchemy import URL, create_engine, text

from models import Base


def main():
    password = getpass("Enter PostgreSQL password: ")

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="employee_orm_demo",
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
