"""
Схемы для запросов и ответов чата.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Запрос к языковой модели."""
    prompt: str = Field(..., description="Текст запроса пользователя")
    system: str | None = Field(
        default=None,
        description="Системная инструкция (необязательно)"
    )
    max_history: int = Field(
        default=20,
        ge=0,
        description="Сколько последних сообщений брать из истории"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Насколько креативной будет модель (0 — строго, 2 — свободно)"
    )


class ChatResponse(BaseModel):
    """Ответ от языковой модели."""
    answer: str = Field(..., description="Текст ответа модели")