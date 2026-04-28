"""
Зависимости для FastAPI (Dependency Injection).
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session() -> AsyncSession:
    """Создаёт сессию базы данных и закрывает её после запроса."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_users_repo(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    """Возвращает репозиторий пользователей."""
    return UsersRepository(session)


async def get_chat_repo(session: AsyncSession = Depends(get_session)) -> ChatMessagesRepository:
    """Возвращает репозиторий сообщений."""
    return ChatMessagesRepository(session)


def get_llm_client() -> OpenRouterClient:
    """Возвращает клиент для OpenRouter."""
    return OpenRouterClient()


async def get_auth_usecase(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCase:
    """Возвращает usecase для авторизации."""
    return AuthUseCase(users_repo)


async def get_chat_usecase(
    chat_repo: ChatMessagesRepository = Depends(get_chat_repo),
    llm_client: OpenRouterClient = Depends(get_llm_client),
) -> ChatUseCase:
    """Возвращает usecase для чата."""
    return ChatUseCase(chat_repo, llm_client)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Достаёт user_id из JWT-токена.
    Если токен невалидный или истёк — возвращает 401.
    """
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )