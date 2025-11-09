"""
API endpoints для управления квестами
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.database.models import Quest, User, ModerationStatus
from backend.quest_builder.yaml_to_graph_converter import YAMLToGraphConverter

router = APIRouter()


class QuestResponse(BaseModel):
    """Ответ с информацией о квесте"""
    id: str
    title: str
    location: str
    difficulty: str
    psychological_module: str
    graph_structure: Dict
    is_public: bool
    moderation_status: str
    rating: float
    plays_count: int


class LoadExistingQuestsResponse(BaseModel):
    """Ответ при загрузке существующих квестов"""
    loaded_count: int
    quests: List[Dict]


@router.get("/existing", response_model=List[QuestResponse])
async def get_existing_quests(
    db: AsyncSession = Depends(get_db)
):
    """
    Получить все существующие квесты из БД

    Используется для:
    - Отображения библиотеки квестов
    - Выбора квеста для редактирования
    """
    try:
        result = await db.execute(
            select(Quest).where(Quest.moderation_status == ModerationStatus.APPROVED)
        )
        quests = result.scalars().all()

        return [
            QuestResponse(
                id=str(quest.id),
                title=quest.title,
                location=quest.location or "unknown",
                difficulty=quest.difficulty or "medium",
                psychological_module=quest.psychological_module or "",
                graph_structure=quest.graph_structure,
                is_public=quest.is_public,
                moderation_status=quest.moderation_status.value,
                rating=quest.rating,
                plays_count=quest.plays_count
            )
            for quest in quests
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{quest_id}", response_model=QuestResponse)
async def get_quest(
    quest_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить конкретный квест по ID"""
    try:
        quest_uuid = UUID(quest_id)
        result = await db.execute(
            select(Quest).where(Quest.id == quest_uuid)
        )
        quest = result.scalar_one_or_none()

        if not quest:
            raise HTTPException(status_code=404, detail="Quest not found")

        return QuestResponse(
            id=str(quest.id),
            title=quest.title,
            location=quest.location or "unknown",
            difficulty=quest.difficulty or "medium",
            psychological_module=quest.psychological_module or "",
            graph_structure=quest.graph_structure,
            is_public=quest.is_public,
            moderation_status=quest.moderation_status.value,
            rating=quest.rating,
            plays_count=quest.plays_count
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quest_id format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load_yaml_quests", response_model=LoadExistingQuestsResponse)
async def load_yaml_quests(
    db: AsyncSession = Depends(get_db)
):
    """
    Загрузить существующие YAML квесты в БД

    ВАЖНО: Это admin endpoint для первоначальной загрузки квестов.
    Конвертирует все YAML квесты из /src/data/quests/ в граф формат
    и сохраняет в БД.

    Используй ОДИН РАЗ при первом запуске.
    """
    try:
        # Инициализировать конвертер
        converter = YAMLToGraphConverter()

        # Конвертировать все квесты
        converted_quests = converter.convert_all_quests()

        if not converted_quests:
            raise HTTPException(status_code=404, detail="No YAML quests found")

        # Создать системного пользователя (если нет)
        result = await db.execute(
            select(User).where(User.telegram_id == None)
        )
        system_user = result.scalar_one_or_none()

        if not system_user:
            system_user = User(
                child_name="System",
                learning_profile={}
            )
            db.add(system_user)
            await db.flush()

        # Сохранить квесты в БД
        loaded_quests = []
        for quest_data in converted_quests:
            # Проверить, не существует ли уже
            result = await db.execute(
                select(Quest).where(Quest.title == quest_data["title"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                # Обновить граф
                existing.graph_structure = quest_data["graph"].model_dump()
                quest = existing
            else:
                # Создать новый квест
                quest = Quest(
                    author_id=system_user.id,
                    title=quest_data["title"],
                    graph_structure=quest_data["graph"].model_dump(),
                    yaml_content="",  # TODO: сохранить оригинальный YAML
                    psychological_module=quest_data["psychological_module"],
                    location=quest_data["location"],
                    difficulty=quest_data["difficulty"],
                    is_public=True,
                    moderation_status=ModerationStatus.APPROVED  # Системные квесты одобрены
                )
                db.add(quest)

            loaded_quests.append({
                "id": quest_data["quest_id"],
                "title": quest_data["title"],
                "nodes_count": len(quest_data["graph"].nodes),
                "edges_count": len(quest_data["graph"].edges)
            })

        await db.commit()

        return LoadExistingQuestsResponse(
            loaded_count=len(loaded_quests),
            quests=loaded_quests
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{quest_id}")
async def delete_quest(
    quest_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Удалить квест"""
    try:
        quest_uuid = UUID(quest_id)
        result = await db.execute(
            select(Quest).where(Quest.id == quest_uuid)
        )
        quest = result.scalar_one_or_none()

        if not quest:
            raise HTTPException(status_code=404, detail="Quest not found")

        await db.delete(quest)
        await db.commit()

        return {"success": True, "message": "Quest deleted"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quest_id")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
