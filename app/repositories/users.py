"""
Репозиторий для работы с таблицей пользователей.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User


class UsersRepository:
    """Доступ к данным пользователей."""

    def __init__(self, session: AsyncSession):
        """Сохраняем сессию, через неё идут все запросы."""
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Найти пользователя по email. Вернёт None, если такого нет."""
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Найти пользователя по id."""
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """Создать нового пользователя и сохранить в базу."""
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user