"""Define SQLAlchemy ORM models for categories and expenses."""

from decimal import Decimal
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Provide the base class for all ORM models."""
    pass


class Category(Base):
    """Represent an expense category."""

    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="category"
    )
    """Expenses associated with this category."""

class Expense(Base):
    """Represent an expense record."""

    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("amount > 0", name="ck_expenses_positive_amount"),
        nullable=False
    )
    """Positive expense amount, stored with two decimal places."""

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.category_id"),
        nullable=False,
    )
    """Foreign key identifying the expense category."""

    category: Mapped["Category"] = relationship(
        back_populates="expenses"
    )
    """Category associated with this expense."""