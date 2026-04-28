"""
Свои исключения для приложения.
Они нужны, чтобы usecase не зависел от FastAPI.
"""


class AppError(Exception):
    """Базовая ошибка приложения."""
    pass


class ConflictError(AppError):
    """Возникает, когда данные уже есть (например, email занят)."""
    pass


class UnauthorizedError(AppError):
    """Неверный логин или пароль."""
    pass


class ForbiddenError(AppError):
    """Нет прав на действие."""
    pass


class NotFoundError(AppError):
    """Объект не найден в базе."""
    pass


class ExternalServiceError(AppError):
    """Ошибка при обращении к внешнему сервису (OpenRouter)."""
    pass