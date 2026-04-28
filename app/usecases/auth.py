"""
Бизнес-логика регистрации, входа и профиля.
"""
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UsersRepository


class AuthUseCase:
    """Сценарии работы с пользователями."""

    def __init__(self, users_repo: UsersRepository):
        """Получаем репозиторий через конструктор."""
        self._users_repo = users_repo

    async def register(self, email: str, password: str) -> dict:
        """
        Регистрация нового пользователя.
        Если email занят — ошибка.
        Возвращает словарь с данными созданного пользователя.
        """
        # Проверяем, нет ли уже такого email
        existing = await self._users_repo.get_by_email(email)
        if existing is not None:
            raise ConflictError("Пользователь с таким email уже существует")

        # Хешируем пароль и сохраняем пользователя
        hashed = hash_password(password)
        user = await self._users_repo.create(email, hashed)

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }

    async def login(self, email: str, password: str) -> str:
        """
        Вход в систему.
        Если email или пароль неверный — ошибка.
        Возвращает JWT-токен.
        """
        # Ищем пользователя
        user = await self._users_repo.get_by_email(email)
        if user is None:
            raise UnauthorizedError("Неверный email или пароль")

        # Проверяем пароль
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверный email или пароль")

        # Создаём токен
        token = create_access_token(user.id, user.role)
        return token

    async def get_profile(self, user_id: int) -> dict:
        """
        Получить профиль пользователя по id.
        Если пользователь не найден — ошибка.
        """
        user = await self._users_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Пользователь не найден")

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }