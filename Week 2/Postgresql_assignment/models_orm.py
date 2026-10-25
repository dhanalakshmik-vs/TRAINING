from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="category"
    )


class Expense(Base):
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
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.category_id"),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        back_populates="expenses"
    )