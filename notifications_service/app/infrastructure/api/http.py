from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel
from app.domain.models import Notification, NotificationType
from app.domain.ports import NotificationRepository
from app.application.use_cases import handle_raw_event


# --------- Esquemas Pydantic para respuestas --------- #

class NotificationOut(BaseModel):
    id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    metadata: Dict[str, Any]
    is_read: bool

    class Config:
        orm_mode = True


def notification_to_out(n: Notification) -> NotificationOut:
    return NotificationOut(
        id=n.id,
        user_id=n.user_id,
        type=n.type,
        title=n.title,
        message=n.message,
        metadata=n.metadata,
        is_read=n.is_read,
    )




def create_router(repo: NotificationRepository) -> APIRouter:
    router = APIRouter()


    def get_repo() -> NotificationRepository:
        return repo

    @router.get("/notifications", response_model=List[NotificationOut])
    def list_notifications(
        user_id: str = Query(..., description="ID del usuario (cliente u ofertante)"),
        repo: NotificationRepository = Depends(get_repo),
    ):
        user_id= user_id.strip()
        notifications = repo.list_by_user(user_id)
        return [notification_to_out(n) for n in notifications]

    @router.patch("/notifications/{notification_id}/read", response_model=NotificationOut)
    def mark_notification_as_read(
        notification_id: str,
        repo: NotificationRepository = Depends(get_repo),
    ):

        try:
            n = repo.mark_as_read(notification_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification_to_out(n)

    @router.post("/events/test", response_model=NotificationOut)
    def simulate_event(
        payload: Dict[str, Any] = Body(..., description="Evento simulado de la cola"),
        repo: NotificationRepository = Depends(get_repo),
    ):
        """
        Endpoint para simular un mensaje llegado desde la cola (sin Azure).
        En un futuro, esta lógica la usará el consumidor real de Azure.
        """
        notification = handle_raw_event(payload, repo)
        return notification_to_out(notification)

    return router
