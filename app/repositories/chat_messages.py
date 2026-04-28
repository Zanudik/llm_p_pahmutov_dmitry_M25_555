"""
Репозиторий для работы с историей чата.
"""
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessagesRepository:
    """Доступ к сообщениям чата."""

    def __init__(self, session: AsyncSession):
        """Сохраняем сессию для запросов к таблице сообщений."""
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Сохраняет одно сообщение."""
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_history(self, user_id: int, limit: int = 20) -> list[ChatMessage]:
        """Возвращает последние limit сообщений пользователя."""
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def clear_history(self, user_id: int) -> None:
        """Удаляет все сообщения пользователя."""
        await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()