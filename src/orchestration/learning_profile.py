"""
Learning Profile tracker for InnerWorld Edu.

Tracks 4 learning dimensions:
1. Understanding Meaning (Понимание смысла) - comprehension, meaning-making
2. Memory (Память) - retention, recall
3. Attention (Внимание) - focus, concentration
4. Motivation (Мотивация) - engagement, persistence

Each dimension rated 1-10.
Used for:
- Personalized location recommendations
- Quest difficulty adaptation
- Progress tracking
- Parent reports
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class LearningDimension(str, Enum):
    """4 learning dimensions."""
    UNDERSTANDING_MEANING = "understanding_meaning"
    MEMORY = "memory"
    ATTENTION = "attention"
    MOTIVATION = "motivation"


@dataclass
class DimensionReading:
    """A single reading for a learning dimension."""
    dimension: LearningDimension
    value: int  # 1-10
    change: int  # +/- from previous
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""  # e.g., "quest_1_completed", "onboarding"


@dataclass
class LearningProfile:
    """
    Learning profile with 4 dimensions.

    Each dimension ranges from 1 (very low) to 10 (excellent).
    """
    understanding_meaning: int = 5
    memory: int = 5
    attention: int = 5
    motivation: int = 5

    # History of changes
    history: List[DimensionReading] = field(default_factory=list)

    def get_dimension(self, dimension: LearningDimension) -> int:
        """Get current value for a dimension."""
        return getattr(self, dimension.value)

    def set_dimension(self, dimension: LearningDimension, value: int, source: str = "") -> None:
        """
        Set dimension value and record change.

        Args:
            dimension: Which dimension to update
            value: New value (1-10)
            source: Source of change (e.g., "quest_completed")
        """
        # Clamp to 1-10 range
        value = max(1, min(10, value))

        # Calculate change
        old_value = getattr(self, dimension.value)
        change = value - old_value

        # Update value
        setattr(self, dimension.value, value)

        # Record change
        reading = DimensionReading(
            dimension=dimension,
            value=value,
            change=change,
            source=source
        )
        self.history.append(reading)

    def adjust_dimension(
        self,
        dimension: LearningDimension,
        delta: int,
        source: str = ""
    ) -> None:
        """
        Adjust dimension by delta amount.

        Args:
            dimension: Which dimension to adjust
            delta: Amount to add/subtract
            source: Source of change
        """
        current = getattr(self, dimension.value)
        new_value = current + delta
        self.set_dimension(dimension, new_value, source)

    def get_weakest_dimension(self) -> LearningDimension:
        """Get the dimension with lowest score."""
        dimensions = {
            LearningDimension.UNDERSTANDING_MEANING: self.understanding_meaning,
            LearningDimension.MEMORY: self.memory,
            LearningDimension.ATTENTION: self.attention,
            LearningDimension.MOTIVATION: self.motivation
        }
        return min(dimensions.items(), key=lambda x: x[1])[0]

    def get_strongest_dimension(self) -> LearningDimension:
        """Get the dimension with highest score."""
        dimensions = {
            LearningDimension.UNDERSTANDING_MEANING: self.understanding_meaning,
            LearningDimension.MEMORY: self.memory,
            LearningDimension.ATTENTION: self.attention,
            LearningDimension.MOTIVATION: self.motivation
        }
        return max(dimensions.items(), key=lambda x: x[1])[0]

    def get_average_score(self) -> float:
        """Get average score across all dimensions."""
        return (
            self.understanding_meaning +
            self.memory +
            self.attention +
            self.motivation
        ) / 4.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "understanding_meaning": self.understanding_meaning,
            "memory": self.memory,
            "attention": self.attention,
            "motivation": self.motivation,
            "average": self.get_average_score(),
            "weakest": self.get_weakest_dimension().value,
            "strongest": self.get_strongest_dimension().value
        }


class LearningProfileAnalyzer:
    """
    Analyzes learning profile and provides recommendations.

    Maps learning challenges to Ponimaliya locations.
    Recommends quest difficulty and teaching strategies.
    """

    # Location recommendations based on weakest dimension
    DIMENSION_TO_LOCATION = {
        LearningDimension.UNDERSTANDING_MEANING: "tower_confusion",  # Башня Непонимания
        LearningDimension.MEMORY: "valley_words",  # Долина Слов
        LearningDimension.ATTENTION: "forest_calm",  # Лес Спокойствия
        LearningDimension.MOTIVATION: "workshop_creator"  # Мастерская Создателя
    }

    # Module recommendations for each dimension
    DIMENSION_TO_MODULES = {
        LearningDimension.UNDERSTANDING_MEANING: [
            15,  # Metacognition - thinking about thinking
            6,   # Decision Science - analyzing reasoning
            5    # TRIZ - creative problem-solving
        ],
        LearningDimension.MEMORY: [
            16,  # Adaptive Learning - spaced repetition
            9,   # Emotional Literacy - emotional memory links
            15   # Metacognition - memory strategies
        ],
        LearningDimension.ATTENTION: [
            8,   # Mindfulness - attention training
            2,   # DBT - emotion regulation for focus
            19   # Self-Care - managing energy for attention
        ],
        LearningDimension.MOTIVATION: [
            17,  # Creative Expression - intrinsic motivation
            20,  # Future Planning - goals and meaning
            5    # TRIZ - engaging challenges
        ]
    }

    @staticmethod
    def recommend_location(profile: LearningProfile) -> str:
        """
        Recommend starting location based on learning profile.

        Targets weakest dimension first.

        Args:
            profile: Learning profile

        Returns:
            Location ID
        """
        weakest = profile.get_weakest_dimension()
        return LearningProfileAnalyzer.DIMENSION_TO_LOCATION[weakest]

    @staticmethod
    def recommend_modules(profile: LearningProfile, count: int = 3) -> List[int]:
        """
        Recommend modules to work on based on profile.

        Args:
            profile: Learning profile
            count: Number of modules to recommend

        Returns:
            List of module IDs
        """
        weakest = profile.get_weakest_dimension()
        modules = LearningProfileAnalyzer.DIMENSION_TO_MODULES[weakest]
        return modules[:count]

    @staticmethod
    def get_difficulty_level(profile: LearningProfile) -> str:
        """
        Get recommended quest difficulty level.

        Args:
            profile: Learning profile

        Returns:
            Difficulty level: "easy", "medium", "hard"
        """
        avg = profile.get_average_score()

        if avg < 4:
            return "easy"
        elif avg < 7:
            return "medium"
        else:
            return "hard"

    @staticmethod
    def detect_learning_pattern(profile: LearningProfile) -> Dict[str, Any]:
        """
        Detect learning patterns from profile history.

        Args:
            profile: Learning profile

        Returns:
            Dictionary with pattern analysis
        """
        if len(profile.history) < 5:
            return {
                "pattern": "insufficient_data",
                "trend": "neutral",
                "concern": False
            }

        # Analyze recent changes (last 10 readings)
        recent = profile.history[-10:]

        # Count positive vs negative changes
        positive = sum(1 for r in recent if r.change > 0)
        negative = sum(1 for r in recent if r.change < 0)

        # Determine trend
        if positive > negative * 1.5:
            trend = "improving"
        elif negative > positive * 1.5:
            trend = "declining"
        else:
            trend = "stable"

        # Check for concerning patterns
        concern = False
        concern_type = None

        # All dimensions below 4 = struggle
        if all(
            profile.get_dimension(d) < 4
            for d in LearningDimension
        ):
            concern = True
            concern_type = "general_struggle"

        # Motivation very low
        if profile.motivation < 3:
            concern = True
            concern_type = "low_motivation"

        # Declining trend over time
        if trend == "declining" and negative > 5:
            concern = True
            concern_type = "declining_performance"

        return {
            "pattern": "analyzed",
            "trend": trend,
            "concern": concern,
            "concern_type": concern_type,
            "positive_changes": positive,
            "negative_changes": negative,
            "average_score": profile.get_average_score(),
            "weakest_dimension": profile.get_weakest_dimension().value
        }

    @staticmethod
    def get_progress_summary(profile: LearningProfile) -> str:
        """
        Get human-readable progress summary.

        Args:
            profile: Learning profile

        Returns:
            Summary text
        """
        avg = profile.get_average_score()
        weakest = profile.get_weakest_dimension()
        strongest = profile.get_strongest_dimension()

        # Translate dimension names
        dimension_names = {
            LearningDimension.UNDERSTANDING_MEANING: "понимание смысла",
            LearningDimension.MEMORY: "память",
            LearningDimension.ATTENTION: "внимание",
            LearningDimension.MOTIVATION: "мотивация"
        }

        weakest_name = dimension_names[weakest]
        strongest_name = dimension_names[strongest]

        # Generate summary
        if avg >= 7:
            summary = f"Отличный прогресс! 🌟 Средний балл: {avg:.1f}/10"
        elif avg >= 5:
            summary = f"Хороший прогресс! 👍 Средний балл: {avg:.1f}/10"
        else:
            summary = f"Есть над чем поработать. Средний балл: {avg:.1f}/10"

        summary += f"\n\nСильная сторона: {strongest_name} ({profile.get_dimension(strongest)}/10)"
        summary += f"\nНад чем поработаем: {weakest_name} ({profile.get_dimension(weakest)}/10)"

        return summary

    @staticmethod
    def suggest_teaching_strategy(profile: LearningProfile) -> str:
        """
        Suggest teaching strategy based on profile.

        Args:
            profile: Learning profile

        Returns:
            Strategy description
        """
        weakest = profile.get_weakest_dimension()

        strategies = {
            LearningDimension.UNDERSTANDING_MEANING: (
                "Стратегия: Больше объяснений 'почему' и примеров из жизни. "
                "Связываем новое со знакомым."
            ),
            LearningDimension.MEMORY: (
                "Стратегия: Используем повторение с интервалами, "
                "эмоциональные якоря и визуализацию."
            ),
            LearningDimension.ATTENTION: (
                "Стратегия: Короткие сессии с перерывами, "
                "техники осознанности, убираем отвлекающие факторы."
            ),
            LearningDimension.MOTIVATION: (
                "Стратегия: Больше выбора и контроля, связь с личными целями, "
                "быстрые успехи для уверенности."
            )
        }

        return strategies[weakest]
