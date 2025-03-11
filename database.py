# database.py - Конфігурація підключення до БД
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

DATABASE_URL = "postgresql://university:university@10.0.10.10/uni-hw6"  # PostgreSQL
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Створення базового класу для декларативних моделей
#class Base(DeclarativeBase):
#    pass
