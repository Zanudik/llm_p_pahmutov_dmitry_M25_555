"""
Эндпоинты для общения с языковой моделью.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправить запрос языковой модели и получить ответ."""
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=body.prompt,
            system=body.system,
            max_history=body.max_history,
            temperature=body.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )


@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Получить историю сообщений текущего пользователя."""
    history = await chat_usecase.get_history(user_id)
    return history


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Удалить всю историю сообщений текущего пользователя."""
    await chat_usecase.clear_history(user_id)