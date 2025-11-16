from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class NotificationType(str, Enum):
    REQUEST_CREATED = "REQUEST_CREATED"
    REQUEST_ACCEPTED = "REQUEST_ACCEPTED"
    REQUEST_REJECTED = "REQUEST_REJECTED"


@dataclass
class Notification:
    id: str
    user_id: str           # A quién va dirigida (cliente u ofertante)
    type: NotificationType
    title: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

    @staticmethod
    def new(
        user_id: str,
        type: NotificationType,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Notification":
        return Notification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            metadata=metadata or {},
        )
