from abc import ABC, abstractmethod
from typing import List
from .models import Notification


class NotificationRepository(ABC):
    """Puerto de salida para guardar y leer notificaciones."""

    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> List[Notification]:
        ...

    @abstractmethod
    def mark_as_read(self, notification_id: str) -> Notification:
        ...


class EventConsumer(ABC):
    """Puerto de entrada para quien escucha la cola (simulado por ahora)."""

    @abstractmethod
    async def start(self) -> None:
        ...
