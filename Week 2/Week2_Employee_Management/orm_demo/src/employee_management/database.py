
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from employee_management.config import get_database_url

DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
