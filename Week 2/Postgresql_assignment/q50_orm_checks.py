
from getpass import getpass
from decimal import Decimal

from sqlalchemy import func, text, event
from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from models_orm import Category, Expense


def test_negative_amount(engine):

    try:
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
                print("FAIL: negative amount was accepted")
            except IntegrityError as error:
                session.rollback()
                print("PASS: PostgreSQL rejected negative amount")
                print("Constraint:", error.orig)

    except Exception:
        raise


def test_missing_category(engine):
    from sqlalchemy.exc import IntegrityError

    with Session(engine) as session:
        try:
            expense = Expense(
                title="Missing Category Test",
                amount=Decimal("50.00"),
                category_id=999999,
            )
            session.add(expense)
            session.flush()

            print("FAIL: nonexistent category was accepted")

        except IntegrityError as error:
            session.rollback()
            print("PASS: PostgreSQL rejected nonexistent category")
            print("Constraint error:", error.orig)


def test_persistence(engine):
    category_id = None
    expense_id = None

    # Session 1: create and commit records
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

    # Session 2: verify committed data is still present
    with Session(engine) as session:
        saved_expense = session.get(Expense, expense_id)

        if (
            saved_expense is not None
            and saved_expense.title == "Q50 Persistence Expense"
        ):
            print("PASS: expense persisted across sessions")
        else:
            raise AssertionError("Persistence test failed")

    # Cleanup: delete the expense before its category
    with Session(engine) as session:
        session.delete(session.get(Expense, expense_id))
        session.flush()
        session.delete(session.get(Category, category_id))
        session.commit()

    print("PASS: persistence test records cleaned up")


def test_aggregate_parity(engine):
    # Temporary test data
    with Session(engine) as session:
        category = Category(name="Q50 Aggregate Test")
        session.add(category)
        session.flush()

        session.add_all([
            Expense(
                title="Aggregate Expense 1",
                amount=Decimal("100.00"),
                category_id=category.category_id,
            ),
            Expense(
                title="Aggregate Expense 2",
                amount=Decimal("50.00"),
                category_id=category.category_id,
            ),
        ])
        session.commit()
        category_id = category.category_id

    try:
        # ORM aggregate
        with Session(engine) as session:
            orm_result = session.execute(
                select(
                    Category.name,
                    func.count(Expense.expense_id),
                    func.coalesce(func.sum(Expense.amount), 0),
                )
                .join(Expense, Category.category_id == Expense.category_id)
                .where(Category.category_id == category_id)
                .group_by(Category.name)
            ).one()

        # Equivalent SQL aggregate
        with engine.connect() as connection:
            sql_result = connection.execute(
                text("""
                    SELECT
                        c.name,
                        COUNT(e.expense_id),
                        COALESCE(SUM(e.amount), 0)
                    FROM categories AS c
                    JOIN expenses AS e
                        ON e.category_id = c.category_id
                    WHERE c.category_id = :category_id
                    GROUP BY c.name
                """),
                {"category_id": category_id},
            ).one()

        print("ORM aggregate:", orm_result)
        print("SQL aggregate:", sql_result)

        assert orm_result == sql_result
        print("PASS: ORM and SQL aggregates match")

    finally:
        # Clean up only this test's records
        with Session(engine) as session:
            session.execute(
                text("DELETE FROM expenses WHERE category_id = :id"),
                {"id": category_id},
            )
            session.execute(
                text("DELETE FROM categories WHERE category_id = :id"),
                {"id": category_id},
            )
            session.commit()

def test_loading_strategies(engine):
    statements = []

    def count_queries(
        conn, cursor, statement, parameters, context, executemany
    ):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    # Create temporary data for three categories and expenses
    with Session(engine) as session:
        categories = [
            Category(name=f"Q50 Loading Test {i}")
            for i in range(1, 4)
        ]
        session.add_all(categories)
        session.flush()

        session.add_all([
            Expense(
                title=f"Q50 Loading Expense {i}",
                amount=Decimal("10.00"),
                category_id=category.category_id,
            )
            for i, category in enumerate(categories, start=1)
        ])
        session.commit()
        category_ids = [category.category_id for category in categories]

    try:
        event.listen(engine, "before_cursor_execute", count_queries)

        # Lazy loading: one query for categories, then one per category
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

        # Eager loading: fetch categories and expenses together
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

        print("PASS: loading strategies compared")

    finally:
        event.remove(engine, "before_cursor_execute", count_queries)

        with Session(engine) as session:
            session.execute(
                text("DELETE FROM expenses WHERE category_id = ANY(:ids)"),
                {"ids": category_ids},
            )
            session.execute(
                text("DELETE FROM categories WHERE category_id = ANY(:ids)"),
                {"ids": category_ids},
            )
            session.commit()


def test_injection_like_input(engine):
    suspicious_title = "'; DROP TABLE expenses; --"
    category_id = None
    expense_id = None

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

        # Read the title back from PostgreSQL
        with Session(engine) as session:
            saved = session.get(Expense, expense_id)

            assert saved is not None
            assert saved.title == suspicious_title

            print("PASS: injection-like input stored as ordinary data")
            print("Stored title:", saved.title)

    finally:
        # Clean up only the records created by this test
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

def main():
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

    test_negative_amount(engine)
    test_missing_category(engine)
    test_persistence(engine)
    test_aggregate_parity(engine)
    test_loading_strategies(engine)
    test_injection_like_input(engine)

    try:
        with Session(engine) as session:
            try:
                # CREATE: add a category
                category = Category(name="Q50 Test Category")
                session.add(category)
                session.flush()

                # CREATE: add an expense
                expense = Expense(
                    title="Q50 Test Expense",
                    amount=Decimal("125.50"),
                    category_id=category.category_id,
                )
                session.add(expense)
                session.flush()

                print(
                    "CREATE:",
                    expense.expense_id,
                    expense.title,
                    expense.amount,
                )

                # READ: retrieve the expense
                saved_expense = session.scalar(
                    select(Expense).where(
                        Expense.expense_id == expense.expense_id
                    )
                )
                print("READ:", saved_expense.title)

                # UPDATE: change the title
                saved_expense.title = "Q50 Updated Expense"
                session.flush()
                print("UPDATE:", saved_expense.title)

                # DELETE: remove the expense
                session.delete(saved_expense)
                session.flush()
                print("DELETE: expense deleted")

                # Roll back the category and all other test changes
                session.rollback()
                print("ROLLBACK: test changes discarded")

            except Exception:
                session.rollback()
                raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
