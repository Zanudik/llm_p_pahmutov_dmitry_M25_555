"""
Создание асинхронного движка и фабрики сессий для SQLite.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

# Собираем ссылку на файл базы данных
DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"

# Движок — через него идут все запросы к базе
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика сессий — будет создавать отдельную сессию на каждый запрос
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)