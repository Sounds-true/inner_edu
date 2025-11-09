"""
Database module initialization
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Database URL из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/innerworld_edu")

# Async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # логирование SQL запросов (отключить в production)
    future=True
)

# Async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """Dependency для FastAPI endpoints"""
    async with async_session_maker() as session:
        yield session
