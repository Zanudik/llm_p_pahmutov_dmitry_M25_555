"""
Базовый класс для всех таблиц в базе данных.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Основа для ORM-моделей. От неё наследуются User и ChatMessage."""
    pass
