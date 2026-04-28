"""
Бизнес-логика общения с языковой моделью.
"""
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Сценарии работы с чатом и LLM."""

    def __init__(
        self,
        chat_repo: ChatMessagesRepository,
        llm_client: OpenRouterClient,
    ):
        """Получаем репозиторий и клиент LLM через конструктор."""
        self._chat_repo = chat_repo
        self._llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 20,
        temperature: float = 0.7,
    ) -> str:
        """
        Отправить запрос модели и получить ответ.
        Попутно сохраняет запрос и ответ в историю.
        """
        # Собираем список сообщений для модели
        messages: list[dict] = []

        # Если есть системная инструкция — добавляем её первой
        if system:
            messages.append({"role": "system", "content": system})

        # Берём историю из базы
        history = await self._chat_repo.get_history(user_id, limit=max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Добавляем текущий запрос пользователя
        messages.append({"role": "user", "content": prompt})

        # Сохраняем запрос пользователя в базу
        await self._chat_repo.add_message(user_id, "user", prompt)

        # Отправляем всё в OpenRouter
        answer = await self._llm_client.ask(messages, temperature)

        # Сохраняем ответ модели в базу
        await self._chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[dict]:
        """
        Получить историю сообщений пользователя.
        Возвращает список словарей с role и content.
        """
        messages = await self._chat_repo.get_history(user_id, limit=limit)
        return [
            {"role": msg.role, "content": msg.content, "created_at": msg.created_at}
            for msg in messages
        ]

    async def clear_history(self, user_id: int) -> None:
        """Удалить всю историю сообщений пользователя."""
        await self._chat_repo.clear_history(user_id)