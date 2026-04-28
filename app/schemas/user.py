"""
Публичная схема пользователя (без пароля).
"""
from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """То, что показываем о пользователе наружу."""
    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)