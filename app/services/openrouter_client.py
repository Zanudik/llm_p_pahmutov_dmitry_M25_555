"""
Клиент для общения с OpenRouter API.
Отправляет запрос к языковой модели и возвращает ответ.
"""
import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """Клиент для внешнего сервиса OpenRouter."""

    def __init__(self):
        """Берём настройки из конфига."""
        self._base_url = settings.openrouter_base_url
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._site_url = settings.openrouter_site_url
        self._app_name = settings.openrouter_app_name

    async def ask(self, messages: list[dict], temperature: float = 0.7) -> str:
        """
        Отправляет сообщения модели и возвращает текст ответа.
        
        messages — список словарей с ключами role и content.
        temperature — насколько креативной будет модель.
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._site_url,
            "X-Title": self._app_name,
            "Content-Type": "application/json",
        }

        body = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=body,
            )

        # Если статус не 200 — это ошибка
        if response.status_code != 200:
            raise ExternalServiceError(
                f"OpenRouter вернул ошибку {response.status_code}: {response.text}"
            )

        # Достаём ответ модели из JSON
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return answer