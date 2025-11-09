"""
SQLAlchemy модели для InnerWorld Edu
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, Enum, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()


class ModerationStatus(str, enum.Enum):
    """Статусы модерации квестов"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(Base):
    """Пользователь системы (родитель)"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=True, index=True)
    child_name = Column(String(255), nullable=True)
    learning_profile = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    quests = relationship("Quest", back_populates="author")
    builder_sessions = relationship("QuestBuilderSession", back_populates="user")
    quest_library = relationship("UserQuestLibrary", back_populates="user")


class Quest(Base):
    """Квест (UGC контент от родителей)"""
    __tablename__ = "quests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)

    # Граф квеста (основное хранилище)
    graph_structure = Column(JSONB, nullable=False)

    # YAML (генерируется из graph_structure для совместимости)
    yaml_content = Column(Text, nullable=True)

    # Метаданные
    psychological_module = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)
    age_range = Column(String(20), nullable=True)  # "7-9"

    # Публичность и модерация
    is_public = Column(Boolean, default=False)
    moderation_status = Column(Enum(ModerationStatus), default=ModerationStatus.PENDING, index=True)
    moderation_reason = Column(Text, nullable=True)

    # Статистика
    rating = Column(Float, default=0.0)
    plays_count = Column(Integer, default=0)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)

    # Relationships
    author = relationship("User", back_populates="quests")
    ratings = relationship("QuestRating", back_populates="quest")
    progress_records = relationship("QuestProgress", back_populates="quest")


class QuestBuilderSession(Base):
    """Сессия создания квеста через AI Builder"""
    __tablename__ = "quest_builder_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # История диалога с AI
    conversation_history = Column(JSONB, default=list)

    # Стадия диалога
    current_stage = Column(String(50), default="greeting")

    # Текущий граф квеста
    current_graph = Column(JSONB, nullable=True)

    # Контекст квеста
    quest_context = Column(JSONB, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="builder_sessions")


class UserQuestLibrary(Base):
    """Библиотека квестов пользователя"""
    __tablename__ = "user_quest_library"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"), nullable=False, index=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="quest_library")
    quest = relationship("Quest")


class QuestProgress(Base):
    """Прогресс прохождения квеста ребенком"""
    __tablename__ = "quest_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"), nullable=False, index=True)

    current_step = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    quest = relationship("Quest", back_populates="progress_records")


class QuestRating(Base):
    """Рейтинг квеста от родителей"""
    __tablename__ = "quest_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 звезд
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    quest = relationship("Quest", back_populates="ratings")
