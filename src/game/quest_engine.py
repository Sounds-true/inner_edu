"""
Quest Engine for InnerWorld Edu.

Loads YAML quest scenarios and processes them step-by-step.
Integrates psychological modules with game mechanics.
Manages Reality Bridge micro-actions.

Quest Structure (YAML):
- Metadata: id, title, location, module, difficulty, time
- Steps: input_text, choice, multiple_choice with validation
- Rewards: XP, learning profile changes, location progress
- Reality Bridge: micro-actions for real life
- Psychological Insights: explanations of techniques used
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

from src.core.logger import get_logger

logger = get_logger(__name__)


class StepType(str, Enum):
    """Quest step types."""
    INPUT_TEXT = "input_text"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    REFLECTION = "reflection"


class QuestDifficulty(str, Enum):
    """Quest difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class QuestStep:
    """A single step in a quest."""
    id: str
    type: StepType
    prompt: str
    validation: Dict[str, Any] = field(default_factory=dict)
    hint: Optional[str] = None
    options: List[Dict[str, Any]] = field(default_factory=list)  # For choice/multiple_choice
    feedback: Optional[str] = None


@dataclass
class QuestRewards:
    """Rewards for completing quest."""
    experience_points: int = 0
    learning_profile_changes: Dict[str, int] = field(default_factory=dict)
    location_progress: Dict[str, int] = field(default_factory=dict)


@dataclass
class RealityBridge:
    """Reality Bridge micro-action."""
    id: str
    title: str
    description: str
    deadline_hours: int = 48
    reminder_hours: int = 24
    verification_type: str = "self_report"
    verification_prompt: str = "Получилось выполнить?"
    verification_options: List[str] = field(default_factory=list)


@dataclass
class Quest:
    """A complete quest with all steps and metadata."""
    id: str
    title: str
    location: str
    psychological_module: str
    difficulty: QuestDifficulty
    estimated_time_minutes: int
    description: str
    steps: List[QuestStep] = field(default_factory=list)
    completion_message: str = ""
    rewards: Optional[QuestRewards] = None
    reality_bridge: Optional[RealityBridge] = None
    psychological_insights: List[Dict[str, Any]] = field(default_factory=list)
    target_learning_profile: Dict[str, str] = field(default_factory=dict)


@dataclass
class QuestProgress:
    """Progress through a quest."""
    quest_id: str
    user_id: str
    current_step_index: int = 0
    step_responses: Dict[str, Any] = field(default_factory=dict)  # step_id -> response
    step_scores: Dict[str, float] = field(default_factory=dict)  # step_id -> score
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    total_score: float = 0.0

    def is_completed(self) -> bool:
        """Check if quest is completed."""
        return self.completed_at is not None


class QuestEngine:
    """
    Quest Engine for loading and processing YAML quests.

    Manages:
    - YAML quest loading and validation
    - Step-by-step quest progression
    - Answer validation
    - Scoring and rewards
    - Reality Bridge actions
    """

    def __init__(self, quests_dir: Path = Path("src/data/quests")):
        """
        Initialize quest engine.

        Args:
            quests_dir: Directory containing quest YAML files
        """
        self.quests_dir = quests_dir
        self.quests: Dict[str, Quest] = {}
        self.quest_progress: Dict[str, QuestProgress] = {}  # user_id -> current quest progress

        logger.info("quest_engine_initialized", quests_dir=str(quests_dir))

    async def load_quest(self, quest_file: Path) -> Optional[Quest]:
        """
        Load quest from YAML file.

        Args:
            quest_file: Path to YAML file

        Returns:
            Quest object or None if loading fails
        """
        try:
            with open(quest_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Parse steps
            steps = []
            for step_data in data.get('steps', []):
                step = QuestStep(
                    id=step_data['id'],
                    type=StepType(step_data['type']),
                    prompt=step_data['prompt'],
                    validation=step_data.get('validation', {}),
                    hint=step_data.get('hint'),
                    options=step_data.get('options', []),
                    feedback=step_data.get('feedback')
                )
                steps.append(step)

            # Parse rewards
            rewards_data = data.get('rewards', {})
            rewards = QuestRewards(
                experience_points=rewards_data.get('experience_points', 0),
                learning_profile_changes=rewards_data.get('learning_profile', {}),
                location_progress=rewards_data.get('location_progress', {})
            )

            # Parse Reality Bridge
            reality_bridge = None
            rb_data = data.get('reality_bridge')
            if rb_data:
                reality_bridge = RealityBridge(
                    id=rb_data['id'],
                    title=rb_data['title'],
                    description=rb_data['description'],
                    deadline_hours=rb_data.get('deadline_hours', 48),
                    reminder_hours=rb_data.get('reminder_hours', 24),
                    verification_type=rb_data.get('verification', {}).get('type', 'self_report'),
                    verification_prompt=rb_data.get('verification', {}).get('prompt', ''),
                    verification_options=rb_data.get('verification', {}).get('options', [])
                )

            # Create quest
            quest = Quest(
                id=data['id'],
                title=data['title'],
                location=data['location'],
                psychological_module=data['psychological_module'],
                difficulty=QuestDifficulty(data['difficulty']),
                estimated_time_minutes=data['estimated_time_minutes'],
                description=data['description'],
                steps=steps,
                completion_message=data.get('completion_message', ''),
                rewards=rewards,
                reality_bridge=reality_bridge,
                psychological_insights=data.get('psychological_insights', []),
                target_learning_profile=data.get('target_learning_profile', {})
            )

            # Cache quest
            self.quests[quest.id] = quest

            logger.info("quest_loaded",
                       quest_id=quest.id,
                       location=quest.location,
                       steps=len(quest.steps))

            return quest

        except Exception as e:
            logger.error("quest_load_failed",
                        quest_file=str(quest_file),
                        error=str(e))
            return None

    async def load_all_quests(self) -> int:
        """
        Load all quests from quests directory.

        Returns:
            Number of quests loaded
        """
        if not self.quests_dir.exists():
            logger.warning("quests_dir_not_found", path=str(self.quests_dir))
            return 0

        count = 0

        # Search all subdirectories for YAML files
        for yaml_file in self.quests_dir.rglob("*.yaml"):
            quest = await self.load_quest(yaml_file)
            if quest:
                count += 1

        logger.info("all_quests_loaded", count=count)
        return count

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get quest by ID."""
        return self.quests.get(quest_id)

    def get_quests_by_location(self, location: str) -> List[Quest]:
        """
        Get all quests for a location.

        Args:
            location: Location ID

        Returns:
            List of quests
        """
        return [
            quest for quest in self.quests.values()
            if quest.location == location
        ]

    def get_quests_by_difficulty(self, difficulty: QuestDifficulty) -> List[Quest]:
        """Get quests by difficulty level."""
        return [
            quest for quest in self.quests.values()
            if quest.difficulty == difficulty
        ]

    async def start_quest(self, user_id: str, quest_id: str) -> Tuple[bool, Optional[QuestStep]]:
        """
        Start a quest for user.

        Args:
            user_id: User ID
            quest_id: Quest ID

        Returns:
            (success, first_step)
        """
        quest = self.get_quest(quest_id)

        if not quest:
            logger.error("quest_not_found", quest_id=quest_id)
            return False, None

        if not quest.steps:
            logger.error("quest_has_no_steps", quest_id=quest_id)
            return False, None

        # Create progress tracker
        progress = QuestProgress(
            quest_id=quest_id,
            user_id=user_id,
            current_step_index=0
        )

        self.quest_progress[user_id] = progress

        logger.info("quest_started",
                   user_id=user_id,
                   quest_id=quest_id)

        return True, quest.steps[0]

    async def process_step_response(
        self,
        user_id: str,
        response: Any
    ) -> Tuple[bool, Optional[QuestStep], Optional[str]]:
        """
        Process user response to current quest step.

        Args:
            user_id: User ID
            response: User's response (text, choice index, etc.)

        Returns:
            (success, next_step, feedback)
        """
        progress = self.quest_progress.get(user_id)

        if not progress:
            return False, None, "Нет активного квеста"

        quest = self.get_quest(progress.quest_id)

        if not quest:
            return False, None, "Квест не найден"

        # Get current step
        if progress.current_step_index >= len(quest.steps):
            return False, None, "Квест уже завершён"

        current_step = quest.steps[progress.current_step_index]

        # Validate response
        is_valid, validation_message = self._validate_response(current_step, response)

        if not is_valid:
            return False, current_step, validation_message

        # Calculate score (for choice/multiple_choice steps)
        score = self._calculate_step_score(current_step, response)

        # Save response and score
        progress.step_responses[current_step.id] = response
        progress.step_scores[current_step.id] = score
        progress.total_score += score

        # Move to next step
        progress.current_step_index += 1

        # Check if quest is complete
        if progress.current_step_index >= len(quest.steps):
            progress.completed_at = datetime.now()

            logger.info("quest_completed",
                       user_id=user_id,
                       quest_id=quest.id,
                       total_score=progress.total_score)

            return True, None, quest.completion_message

        # Return next step
        next_step = quest.steps[progress.current_step_index]

        # Get feedback for current step (if choice was made)
        feedback = self._get_step_feedback(current_step, response)

        return True, next_step, feedback

    def _validate_response(self, step: QuestStep, response: Any) -> Tuple[bool, str]:
        """
        Validate user response against step validation rules.

        Args:
            step: Quest step
            response: User response

        Returns:
            (is_valid, message)
        """
        if step.type == StepType.INPUT_TEXT:
            if not isinstance(response, str):
                return False, "Ответ должен быть текстом"

            # Check min_length
            min_length = step.validation.get('min_length', 0)
            if len(response) < min_length:
                return False, f"Ответ слишком короткий (минимум {min_length} символов)"

            # Check max_length
            max_length = step.validation.get('max_length', 1000)
            if len(response) > max_length:
                return False, f"Ответ слишком длинный (максимум {max_length} символов)"

            return True, ""

        elif step.type in [StepType.CHOICE, StepType.MULTIPLE_CHOICE]:
            if not isinstance(response, int):
                return False, "Выбери один из вариантов"

            if response < 0 or response >= len(step.options):
                return False, "Неверный номер варианта"

            return True, ""

        return True, ""

    def _calculate_step_score(self, step: QuestStep, response: Any) -> float:
        """
        Calculate score for step response.

        Args:
            step: Quest step
            response: User response

        Returns:
            Score (0.0 - 1.0)
        """
        if step.type in [StepType.CHOICE, StepType.MULTIPLE_CHOICE]:
            if isinstance(response, int) and 0 <= response < len(step.options):
                return step.options[response].get('score', 0.0)

        # Input text steps don't have automatic scoring
        return 0.0

    def _get_step_feedback(self, step: QuestStep, response: Any) -> Optional[str]:
        """
        Get feedback for step response.

        Args:
            step: Quest step
            response: User response

        Returns:
            Feedback text or None
        """
        if step.type in [StepType.CHOICE, StepType.MULTIPLE_CHOICE]:
            if isinstance(response, int) and 0 <= response < len(step.options):
                return step.options[response].get('feedback')

        return step.feedback

    async def get_quest_rewards(self, user_id: str) -> Optional[QuestRewards]:
        """
        Get rewards for completed quest.

        Args:
            user_id: User ID

        Returns:
            QuestRewards or None
        """
        progress = self.quest_progress.get(user_id)

        if not progress or not progress.is_completed():
            return None

        quest = self.get_quest(progress.quest_id)

        if not quest:
            return None

        return quest.rewards

    async def get_reality_bridge(self, user_id: str) -> Optional[RealityBridge]:
        """
        Get Reality Bridge action for completed quest.

        Args:
            user_id: User ID

        Returns:
            RealityBridge or None
        """
        progress = self.quest_progress.get(user_id)

        if not progress or not progress.is_completed():
            return None

        quest = self.get_quest(progress.quest_id)

        if not quest:
            return None

        return quest.reality_bridge

    def get_current_quest_progress(self, user_id: str) -> Optional[QuestProgress]:
        """Get current quest progress for user."""
        return self.quest_progress.get(user_id)

    def clear_quest_progress(self, user_id: str) -> None:
        """Clear quest progress for user (after completion/abandonment)."""
        if user_id in self.quest_progress:
            del self.quest_progress[user_id]
            logger.info("quest_progress_cleared", user_id=user_id)
