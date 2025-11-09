"""
InnerWorld Edu - FastAPI Backend
UGC платформа для создания образовательных квестов через AI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Создание FastAPI приложения
app = FastAPI(
    title="InnerWorld Edu API",
    description="API для UGC платформы образовательных квестов с AI Quest Builder",
    version="1.0.0"
)

# CORS настройка (для фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # альтернативный порт
        os.getenv("FRONTEND_URL", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "InnerWorld Edu API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "not_connected",  # TODO: добавить проверку БД
        "openai_api": "not_checked"   # TODO: добавить проверку OpenAI
    }


# Импорт роутеров
from backend.api import builder, quests

# Подключение роутеров
app.include_router(builder.router, prefix="/api/builder", tags=["AI Quest Builder"])
app.include_router(quests.router, prefix="/api/quests", tags=["Quests"])

# TODO: Добавить остальные роутеры
# from backend.api import users, moderation
# app.include_router(users.router, prefix="/api/users", tags=["users"])
# app.include_router(moderation.router, prefix="/api/moderation", tags=["moderation"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # для разработки
    )
