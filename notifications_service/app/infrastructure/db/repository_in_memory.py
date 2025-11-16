from typing import List, Dict
from app.domain.models import Notification
from app.domain.ports import NotificationRepository


class InMemoryNotificationRepository(NotificationRepository):
    """Implementación simple en memoria (lista) para pruebas y desarrollo."""

    def __init__(self) -> None:
        self._notifications: Dict[str, Notification] = {}

    def save(self, notification: Notification) -> Notification:
        self._notifications[notification.id] = notification
        return notification

    def list_by_user(self, user_id: str) -> List[Notification]:
        return [
            n for n in self._notifications.values()
            if n.user_id == user_id
        ]

    def mark_as_read(self, notification_id: str) -> Notification:
        notification = self._notifications.get(notification_id)
        if not notification:
            raise KeyError(f"Notification {notification_id} not found")

        if not notification.is_read:
            from datetime import datetime
            notification.is_read = True
            notification.read_at = datetime.utcnow()

        return notification
