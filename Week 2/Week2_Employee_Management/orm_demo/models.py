from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal

class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department"
    )


class Employee(Base):
    __tablename__ = "employees"
    
    __table_args__ = (
        CheckConstraint(
            "salary > 0",
            name="ck_employees_salary_positive",
        ),
    )
    employee_id: Mapped[str] = mapped_column(
        String(20), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int]
    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )