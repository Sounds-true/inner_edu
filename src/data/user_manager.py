"""
User Manager for InnerWorld Edu - Educational Mode.

Manages user profiles stored as JSON files.

Storage structure:
    src/data/user_profiles/{user_id}.json

Each file contains:
- User metadata (id, name, age)
- Parent linking status
- Learning profile
- Progress tracking (level, XP, streak)
- Current state (location, quest)
- Screening metrics
- Timestamps

Educational Mode uses JSON (lightweight, no database).
Therapeutic Mode will use PostgreSQL (not implemented yet).
"""

import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict

from src.core.logger import get_logger
from src.orchestration.learning_profile import LearningProfile

logger = get_logger(__name__)


@dataclass
class UserProgress:
    """Progress tracking for gamification."""
    level: int = 1
    xp: int = 0
    streak_days: int = 0
    last_activity_date: str = ""  # YYYY-MM-DD
    total_quests_completed: int = 0
    total_time_minutes: int = 0


@dataclass
class ScreeningMetrics:
    """Screening metrics for therapeutic transition."""
    self_worth: float = 0.5  # 0-1
    self_criticism: float = 0.5  # 0-1
    emotional_volatility: float = 0.5  # 0-1
    manipulation_score: int = 0  # 0-10
    self_harm_detected: bool = False
    emotional_storm_count: int = 0
    last_check: str = ""  # ISO timestamp


@dataclass
class UserProfile:
    """Complete user profile for Educational Mode."""
    # Identity
    user_id: str
    child_name: Optional[str] = None
    age: Optional[int] = None

    # Parent linking
    parent_linked: bool = False
    link_id: Optional[str] = None
    parent_id: Optional[str] = None

    # Learning
    learning_profile: Dict[str, Any] = None  # LearningProfile.to_dict()
    progress: Dict[str, Any] = None  # UserProgress as dict

    # Current state
    current_location: Optional[str] = None
    current_quest: Optional[str] = None
    quest_step: int = 0

    # Screening
    screening: Dict[str, Any] = None  # ScreeningMetrics as dict

    # Timestamps
    created_at: str = ""  # ISO timestamp
    last_activity: str = ""  # ISO timestamp

    def __post_init__(self):
        """Initialize nested objects if None."""
        if self.learning_profile is None:
            self.learning_profile = LearningProfile().to_dict()

        if self.progress is None:
            self.progress = asdict(UserProgress())

        if self.screening is None:
            self.screening = asdict(ScreeningMetrics())

        if not self.created_at:
            self.created_at = datetime.now().isoformat()

        if not self.last_activity:
            self.last_activity = datetime.now().isoformat()


class UserManager:
    """
    Manages user profiles with JSON file storage.

    Thread-safe operations with file locking.
    Automatic directory creation.
    Error recovery and logging.
    """

    def __init__(self, data_dir: Path = Path("src/data/user_profiles")):
        """
        Initialize user manager.

        Args:
            data_dir: Directory for user profile JSON files
        """
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info("user_manager_initialized", data_dir=str(data_dir))

    def _get_user_path(self, user_id: str) -> Path:
        """Get file path for user profile."""
        return self.data_dir / f"{user_id}.json"

    async def create_user(
        self,
        user_id: str,
        child_name: Optional[str] = None,
        age: Optional[int] = None
    ) -> UserProfile:
        """
        Create new user profile.

        Args:
            user_id: Unique user ID (Telegram ID)
            child_name: Child's name
            age: Child's age

        Returns:
            UserProfile

        Raises:
            ValueError: If user already exists
        """
        user_path = self._get_user_path(user_id)

        if user_path.exists():
            raise ValueError(f"User {user_id} already exists")

        # Create profile
        profile = UserProfile(
            user_id=user_id,
            child_name=child_name,
            age=age
        )

        # Save to disk
        await self._save_profile(profile)

        logger.info("user_created", user_id=user_id, child_name=child_name)
        return profile

    async def get_user(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by ID.

        Args:
            user_id: User ID

        Returns:
            UserProfile or None if not found
        """
        user_path = self._get_user_path(user_id)

        if not user_path.exists():
            return None

        try:
            # Read from disk
            async with asyncio.Lock():
                with open(user_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            # Convert to UserProfile
            profile = UserProfile(**data)

            logger.debug("user_loaded", user_id=user_id)
            return profile

        except Exception as e:
            logger.error("user_load_failed", user_id=user_id, error=str(e))
            return None

    async def update_user(self, profile: UserProfile) -> bool:
        """
        Update user profile.

        Args:
            profile: UserProfile to save

        Returns:
            True if successful
        """
        # Update last activity
        profile.last_activity = datetime.now().isoformat()

        try:
            await self._save_profile(profile)
            logger.debug("user_updated", user_id=profile.user_id)
            return True

        except Exception as e:
            logger.error("user_update_failed", user_id=profile.user_id, error=str(e))
            return False

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user profile.

        Args:
            user_id: User ID

        Returns:
            True if successful
        """
        user_path = self._get_user_path(user_id)

        if not user_path.exists():
            return False

        try:
            user_path.unlink()
            logger.info("user_deleted", user_id=user_id)
            return True

        except Exception as e:
            logger.error("user_delete_failed", user_id=user_id, error=str(e))
            return False

    async def user_exists(self, user_id: str) -> bool:
        """
        Check if user exists.

        Args:
            user_id: User ID

        Returns:
            True if user exists
        """
        return self._get_user_path(user_id).exists()

    async def get_or_create_user(
        self,
        user_id: str,
        child_name: Optional[str] = None,
        age: Optional[int] = None
    ) -> UserProfile:
        """
        Get existing user or create new one.

        Args:
            user_id: User ID
            child_name: Child's name (for new users)
            age: Child's age (for new users)

        Returns:
            UserProfile
        """
        profile = await self.get_user(user_id)

        if profile is None:
            profile = await self.create_user(user_id, child_name, age)

        return profile

    async def list_users(self) -> List[str]:
        """
        List all user IDs.

        Returns:
            List of user IDs
        """
        user_ids = []

        for path in self.data_dir.glob("*.json"):
            user_ids.append(path.stem)

        return sorted(user_ids)

    async def get_users_by_parent(self, parent_id: str) -> List[UserProfile]:
        """
        Get all children linked to a parent.

        Args:
            parent_id: Parent Telegram ID

        Returns:
            List of UserProfile
        """
        profiles = []

        for user_id in await self.list_users():
            profile = await self.get_user(user_id)
            if profile and profile.parent_id == parent_id:
                profiles.append(profile)

        return profiles

    async def update_learning_profile(
        self,
        user_id: str,
        learning_profile: LearningProfile
    ) -> bool:
        """
        Update user's learning profile.

        Args:
            user_id: User ID
            learning_profile: LearningProfile object

        Returns:
            True if successful
        """
        profile = await self.get_user(user_id)

        if not profile:
            return False

        profile.learning_profile = learning_profile.to_dict()
        return await self.update_user(profile)

    async def update_progress(
        self,
        user_id: str,
        xp_gain: int = 0,
        quest_completed: bool = False
    ) -> bool:
        """
        Update user progress (XP, quests, etc.).

        Args:
            user_id: User ID
            xp_gain: XP to add
            quest_completed: Whether quest was completed

        Returns:
            True if successful
        """
        profile = await self.get_user(user_id)

        if not profile:
            return False

        # Update progress
        progress = UserProgress(**profile.progress)
        progress.xp += xp_gain

        # Level up check (every 100 XP)
        while progress.xp >= progress.level * 100:
            progress.xp -= progress.level * 100
            progress.level += 1
            logger.info("user_level_up", user_id=user_id, new_level=progress.level)

        if quest_completed:
            progress.total_quests_completed += 1

        # Update streak
        today = datetime.now().strftime("%Y-%m-%d")
        if progress.last_activity_date != today:
            # Check if streak continues (yesterday = today - 1 day)
            from datetime import timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            if progress.last_activity_date == yesterday:
                progress.streak_days += 1
            else:
                progress.streak_days = 1  # Reset streak

            progress.last_activity_date = today

        profile.progress = asdict(progress)
        return await self.update_user(profile)

    async def update_screening_metrics(
        self,
        user_id: str,
        self_worth: Optional[float] = None,
        self_criticism: Optional[float] = None,
        emotional_volatility: Optional[float] = None,
        self_harm_detected: Optional[bool] = None,
        emotional_storm_count: Optional[int] = None
    ) -> bool:
        """
        Update screening metrics.

        Args:
            user_id: User ID
            self_worth: Self-worth score (0-1)
            self_criticism: Self-criticism score (0-1)
            emotional_volatility: Volatility score (0-1)
            self_harm_detected: Whether self-harm keywords detected
            emotional_storm_count: Count of emotional storms

        Returns:
            True if successful
        """
        profile = await self.get_user(user_id)

        if not profile:
            return False

        screening = ScreeningMetrics(**profile.screening)

        if self_worth is not None:
            screening.self_worth = self_worth

        if self_criticism is not None:
            screening.self_criticism = self_criticism

        if emotional_volatility is not None:
            screening.emotional_volatility = emotional_volatility

        if self_harm_detected is not None:
            screening.self_harm_detected = self_harm_detected

        if emotional_storm_count is not None:
            screening.emotional_storm_count = emotional_storm_count

        screening.last_check = datetime.now().isoformat()

        profile.screening = asdict(screening)
        return await self.update_user(profile)

    async def _save_profile(self, profile: UserProfile) -> None:
        """
        Save profile to disk with error handling.

        Args:
            profile: UserProfile to save
        """
        user_path = self._get_user_path(profile.user_id)

        # Convert to dict
        data = asdict(profile)

        # Write to disk with atomic operation
        async with asyncio.Lock():
            # Write to temp file first
            temp_path = user_path.with_suffix('.tmp')

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(user_path)

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics.

        Returns:
            Dictionary with statistics
        """
        user_ids = await self.list_users()
        total_users = len(user_ids)

        linked_users = 0
        total_xp = 0
        total_quests = 0

        for user_id in user_ids:
            profile = await self.get_user(user_id)
            if profile:
                if profile.parent_linked:
                    linked_users += 1

                progress = UserProgress(**profile.progress)
                total_xp += progress.xp
                total_quests += progress.total_quests_completed

        return {
            "total_users": total_users,
            "linked_users": linked_users,
            "unlinked_users": total_users - linked_users,
            "total_xp": total_xp,
            "total_quests_completed": total_quests,
            "avg_xp_per_user": total_xp / total_users if total_users > 0 else 0
        }
