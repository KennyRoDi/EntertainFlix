from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api.http import create_router
from app.infrastructure.db.repository_azure_sql import AzureSqlNotificationRepository
from dotenv import load_dotenv
load_dotenv()

notification_repo = AzureSqlNotificationRepository()


app = FastAPI(
    title="Notifications Service",
    description="Microservicio de notificaciones para solicitudes y cambios de estado.",
    version="0.1.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = create_router(notification_repo)
app.include_router(router)

