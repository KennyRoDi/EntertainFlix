from typing import List
import os
import json
from datetime import datetime

import pyodbc  # asegura que el driver esté cargado
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Boolean,
    DateTime,
    Text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from app.domain.models import Notification, NotificationType
from app.domain.ports import NotificationRepository


# Cargar variables de entorno desde .env
load_dotenv()

# Leer cadena de conexión
DATABASE_URL = os.getenv("AZURE_SQL_CONNECTION_STRING")

print(">>> DATABASE_URL CARGADA:", DATABASE_URL)
if not DATABASE_URL:
    raise RuntimeError("AZURE_SQL_CONNECTION_STRING no está definida")


# Crear engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"autocommit": False},
    echo=False,
)

# Crear fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()


class NotificationORM(Base):
    __tablename__ = "Notifications"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    metadata_json = Column("metadata", Text, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)



class AzureSqlNotificationRepository(NotificationRepository):
    def __init__(self) -> None:
        self._Session = SessionLocal

    def _to_domain(self, orm: NotificationORM) -> Notification:
        return Notification(
            id=orm.id,
            user_id=orm.user_id,
            type=NotificationType(orm.type),
            title=orm.title,
            message=orm.message,
            metadata=json.loads(orm.metadata_json) if orm.metadata_json else {},
            is_read=orm.is_read,
            created_at=orm.created_at,
            read_at=orm.read_at,
        )

    def save(self, notification: Notification) -> Notification:
        db = self._Session()
        try:
            # Si el use case no envía user_id, usamos uno de prueba para no romper la BD
            user_id = notification.user_id or "test-user"

            orm = NotificationORM(
                id=notification.id,
                user_id=user_id,
                type=notification.type.value,
                title=notification.title,
                message=notification.message,
                metadata_json=json.dumps(notification.metadata or {}),
                is_read=notification.is_read,
                created_at=notification.created_at,
                read_at=notification.read_at,
            )
            db.merge(orm)  # inserta o actualiza según el id
            db.commit()
            notification.user_id = user_id
            return notification
        finally:
            db.close()

    def list_by_user(self, user_id: str) -> List[Notification]:
        db = self._Session()
        try:
            rows = (
                db.query(NotificationORM)
                .filter(NotificationORM.user_id == user_id)
                .order_by(NotificationORM.created_at.desc())
                .all()
            )
            return [self._to_domain(r) for r in rows]
        finally:
            db.close()

    def mark_as_read(self, notification_id: str) -> Notification:
        db = self._Session()
        try:
            orm = (
                db.query(NotificationORM)
                .filter(NotificationORM.id == notification_id)
                .first()
            )
            if not orm:
                raise KeyError(f"Notification {notification_id} not found")

            if not orm.is_read:
                orm.is_read = True
                orm.read_at = datetime.utcnow()
                db.commit()

            return self._to_domain(orm)
        finally:
            db.close()
