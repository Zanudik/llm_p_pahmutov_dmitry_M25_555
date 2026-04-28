"""
Точка входа в приложение FastAPI.
Собирает всё вместе.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Срабатывает при запуске и остановке приложения.
    При запуске — создаём все таблицы в базе.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    # Разрешаем запросы с любого источника
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем роутеры
    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.get("/health")
    async def health():
        """Проверка, что сервер запущен."""
        return {
            "status": "ok",
            "env": settings.env,
        }

    return app


# Создаём приложение
app = create_app()