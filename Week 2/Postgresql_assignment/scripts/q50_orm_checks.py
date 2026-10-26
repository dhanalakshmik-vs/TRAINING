
"""Run Q50 ORM checks against PostgreSQL."""

from decimal import Decimal
from getpass import getpass
from typing import Any

from sqlalchemy import URL, create_engine, event, func, select, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from models_orm import Category, Expense


def test_negative_amount(engine: Engine) -> None:
    """Verify that PostgreSQL rejects expenses with negative amounts."""
    with Session(engine) as session:
        category = Category(name="Q50 Negative Test")
        session.add(category)
        session.flush()

        expense = Expense(
            title="Negative Amount Test",
            amount=Decimal("-10.00"),
            category_id=category.category_id,
        )
        session.add(expense)

        try:
            session.flush()
            session.rollback()
            print("FAIL: negative amount was accepted")
        except IntegrityError as error:
            session.rollback()
            print("PASS: PostgreSQL rejected negative amount")
            print("Constraint:", error.orig)


def test_missing_category(engine: Engine) -> None:
    """Verify that an expense cannot reference a nonexistent category."""
    with Session(engine) as session:
        try:
            expense = Expense(
                title="Missing Category Test",
                amount=Decimal("50.00"),
                category_id=999999,
            )
            session.add(expense)
            session.flush()

            session.rollback()
            print("FAIL: nonexistent category was accepted")

        except IntegrityError as error:
            session.rollback()
            print("PASS: PostgreSQL rejected nonexistent category")
            print("Constraint error:", error.orig)


def test_persistence(engine: Engine) -> None:
    """Verify that committed records remain available in a new session."""
    category_id: int
    expense_id: int

    # Session 1: create and commit records.
    with Session(engine) as session:
        category = Category(name="Q50 Persistence Test")
        session.add(category)
        session.flush()

        expense = Expense(
            title="Q50 Persistence Expense",
            amount=Decimal("75.25"),
            category_id=category.category_id,
        )
        session.add(expense)
        session.flush()

        category_id = category.category_id
        expense_id = expense.expense_id

        session.commit()
        print("PASS: test records committed")

    # Session 2: verify the committed expense is still present.
    with Session(engine) as session:
        saved_expense = session.get(Expense, expense_id)

        if (
            saved_expense is not None
            and saved_expense.title == "Q50 Persistence Expense"
        ):
            print("PASS: expense persisted across sessions")
        else:
            raise AssertionError("Persistence test failed")

    # Delete the expense before deleting its category.
    with Session(engine) as session:
        saved_expense = session.get(Expense, expense_id)
        saved_category = session.get(Category, category_id)

        if saved_expense is not None:
            session.delete(saved_expense)

        if saved_category is not None:
            session.delete(saved_category)

        session.commit()

    print("PASS: persistence test records cleaned up")


def test_aggregate_parity(engine: Engine) -> None:
    """Compare equivalent aggregate results from ORM and SQL."""
    with Session(engine) as session:
        category = Category(name="Q50 Aggregate Test")
        session.add(category)
        session.flush()

        category_id = category.category_id

        session.add_all(
            [
                Expense(
                    title="Aggregate Expense 1",
                    amount=Decimal("100.00"),
                    category_id=category_id,
                ),
                Expense(
                    title="Aggregate Expense 2",
                    amount=Decimal("50.00"),
                    category_id=category_id,
                ),
            ]
        )
        session.commit()

    try:
        # Calculate the aggregate using SQLAlchemy ORM.
        with Session(engine) as session:
            orm_result = session.execute(
                select(
                    Category.name,
                    func.count(Expense.expense_id),
                    func.coalesce(func.sum(Expense.amount), 0),
                )
                .join(
                    Expense,
                    Category.category_id == Expense.category_id,
                )
                .where(Category.category_id == category_id)
                .group_by(Category.name)
            ).one()

        # Calculate the equivalent aggregate using SQL.
        with engine.connect() as connection:
            sql_result = connection.execute(
                text(
                    """
                    SELECT
                        c.name,
                        COUNT(e.expense_id),
                        COALESCE(SUM(e.amount), 0)
                    FROM categories AS c
                    JOIN expenses AS e
                        ON e.category_id = c.category_id
                    WHERE c.category_id = :category_id
                    GROUP BY c.name
                    """
                ),
                {"category_id": category_id},
            ).one()

        print("ORM aggregate:", orm_result)
        print("SQL aggregate:", sql_result)

        assert orm_result == sql_result
        print("PASS: ORM and SQL aggregates match")

    finally:
        # Remove only records created by this test.
        with Session(engine) as session:
            session.execute(
                text(
                    "DELETE FROM expenses "
                    "WHERE category_id = :category_id"
                ),
                {"category_id": category_id},
            )
            session.execute(
                text(
                    "DELETE FROM categories "
                    "WHERE category_id = :category_id"
                ),
                {"category_id": category_id},
            )
            session.commit()


def test_loading_strategies(engine: Engine) -> None:
    """Compare SELECT counts for lazy and joined eager loading."""
    statements: list[str] = []

    def count_queries(
        connection: Connection,
        cursor: Any,
        statement: str,
        parameters: Any,
        context: Any,
        executemany: bool,
    ) -> None:
        """Record SELECT statements executed by SQLAlchemy."""
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    # Create temporary data for three categories and their expenses.
    with Session(engine) as session:
        categories = [
            Category(name=f"Q50 Loading Test {index}")
            for index in range(1, 4)
        ]
        session.add_all(categories)
        session.flush()

        category_ids = [
            category.category_id for category in categories
        ]

        session.add_all(
            [
                Expense(
                    title=f"Q50 Loading Expense {index}",
                    amount=Decimal("10.00"),
                    category_id=category.category_id,
                )
                for index, category in enumerate(categories, start=1)
            ]
        )
        session.commit()

    event.listen(engine, "before_cursor_execute", count_queries)

    try:
        # Lazy loading: load expenses separately for each category.
        statements.clear()

        with Session(engine) as session:
            categories = session.scalars(
                select(Category).where(
                    Category.category_id.in_(category_ids)
                )
            ).all()

            for category in categories:
                _ = category.expenses

        lazy_count = len(statements)
        print("Lazy loading SELECT count:", lazy_count)

        # Joined eager loading: load categories and expenses together.
        statements.clear()

        with Session(engine) as session:
            categories = session.scalars(
                select(Category)
                .options(joinedload(Category.expenses))
                .where(Category.category_id.in_(category_ids))
            ).unique().all()

            for category in categories:
                _ = category.expenses

        eager_count = len(statements)
        print("Eager loading SELECT count:", eager_count)

        assert eager_count < lazy_count, (
            "Expected joined eager loading to use fewer SELECT statements"
        )
        print("PASS: loading strategies compared")

    finally:
        event.remove(engine, "before_cursor_execute", count_queries)

        # Clean up the test records.
        with Session(engine) as session:
            session.execute(
                text(
                    "DELETE FROM expenses "
                    "WHERE category_id = ANY(:category_ids)"
                ),
                {"category_ids": category_ids},
            )
            session.execute(
                text(
                    "DELETE FROM categories "
                    "WHERE category_id = ANY(:category_ids)"
                ),
                {"category_ids": category_ids},
            )
            session.commit()


def test_injection_like_input(engine: Engine) -> None:
    """Verify that suspicious-looking input is stored as ordinary data."""
    suspicious_title = "'; DROP TABLE expenses; --"
    category_id: int | None = None
    expense_id: int | None = None

    try:
        with Session(engine) as session:
            category = Category(name="Q50 Injection Test")
            session.add(category)
            session.flush()

            category_id = category.category_id

            expense = Expense(
                title=suspicious_title,
                amount=Decimal("25.00"),
                category_id=category_id,
            )
            session.add(expense)
            session.commit()

            expense_id = expense.expense_id

        # Read the title back from PostgreSQL.
        with Session(engine) as session:
            saved_expense = session.get(Expense, expense_id)

            assert saved_expense is not None
            assert saved_expense.title == suspicious_title

            print("PASS: injection-like input stored as ordinary data")
            print("Stored title:", saved_expense.title)

    finally:
        # Delete only records created by this test.
        with Session(engine) as session:
            if expense_id is not None:
                expense = session.get(Expense, expense_id)
                if expense is not None:
                    session.delete(expense)

            if category_id is not None:
                category = session.get(Category, category_id)
                if category is not None:
                    session.delete(category)

            session.commit()


def main() -> None:
    """Run Q50 ORM checks and demonstrate CRUD and rollback."""
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
        # Run the database constraint and ORM behaviour checks.
        test_negative_amount(engine)
        test_missing_category(engine)
        test_persistence(engine)
        test_aggregate_parity(engine)
        test_loading_strategies(engine)
        test_injection_like_input(engine)

        # Demonstrate CREATE, READ, UPDATE, DELETE and ROLLBACK.
        with Session(engine) as session:
            try:
                category = Category(name="Q50 Test Category")
                session.add(category)
                session.flush()

                expense = Expense(
                    title="Q50 Test Expense",
                    amount=Decimal("125.50"),
                    category_id=category.category_id,
                )
                session.add(expense)
                session.flush()

                expense_id = expense.expense_id

                print(
                    "CREATE:",
                    expense.expense_id,
                    expense.title,
                    expense.amount,
                )

                saved_expense = session.scalar(
                    select(Expense).where(
                        Expense.expense_id == expense_id
                    )
                )

                if saved_expense is None:
                    raise AssertionError("Created expense was not found")

                print("READ:", saved_expense.title)

                saved_expense.title = "Q50 Updated Expense"
                session.flush()
                print("UPDATE:", saved_expense.title)

                session.delete(saved_expense)
                session.flush()
                print("DELETE: expense deleted")

                session.rollback()
                print("ROLLBACK: test changes discarded")

            except Exception:
                session.rollback()
                raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
