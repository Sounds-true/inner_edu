"""
Emotional Router for InnerWorld Edu.

Manages 5 emotional states for children:
1. Tiredness (Усталость) - needs rest or lighter activities
2. Anxiety (Тревога) - needs calming, reassurance
3. Anger (Злость) - needs validation, reframing
4. Interest (Интерес) - ready to learn, explore
5. Doubt (Сомнение) - needs encouragement, clarity

Routes child to appropriate location and adjusts bot responses.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class EmotionalState(str, Enum):
    """5 emotional states for children."""
    TIREDNESS = "tiredness"  # Усталость
    ANXIETY = "anxiety"  # Тревога
    ANGER = "anger"  # Злость
    INTEREST = "interest"  # Интерес
    DOUBT = "doubt"  # Сомнение


@dataclass
class EmotionalReading:
    """A single emotional reading from a message."""
    state: EmotionalState
    intensity: float  # 0-1
    timestamp: datetime = field(default_factory=datetime.now)
    message_snippet: str = ""  # First 50 chars for context
    detected_keywords: List[str] = field(default_factory=list)


class EmotionalRouter:
    """
    Routes children to appropriate support based on emotional state.

    Uses keyword-based detection (can be extended with LLM classification).
    Tracks emotional history for pattern detection.
    Recommends locations in Ponimaliya based on emotional state.
    """

    # Keywords for each emotional state (Russian)
    EMOTION_KEYWORDS = {
        EmotionalState.TIREDNESS: [
            "устал", "устала", "не хочу", "скучно", "надоело", "хватит",
            "не могу больше", "сил нет", "замучил", "замучила"
        ],
        EmotionalState.ANXIETY: [
            "боюсь", "страшно", "волнуюсь", "тревожно", "беспокоюсь",
            "переживаю", "нервничаю", "паникую", "испугался", "испугалась"
        ],
        EmotionalState.ANGER: [
            "злюсь", "бесит", "раздражает", "ненавижу", "достало",
            "разозлился", "разозлилась", "противно", "фу", "глупо"
        ],
        EmotionalState.DOUBT: [
            "не понимаю", "не знаю", "не уверен", "не уверена", "сомневаюсь",
            "непонятно", "сложно", "трудно", "запутался", "запуталась"
        ],
        EmotionalState.INTEREST: [
            "интересно", "хочу", "расскажи", "покажи", "здорово", "круто",
            "давай", "попробую", "можно", "а что", "а как"
        ]
    }

    # Location recommendations based on emotional state
    EMOTION_TO_LOCATION = {
        EmotionalState.TIREDNESS: "forest_calm",  # Лес Спокойствия
        EmotionalState.ANXIETY: "forest_calm",  # Лес Спокойствия
        EmotionalState.ANGER: "mountain_emptiness",  # Гора Пустоты
        EmotionalState.DOUBT: "tower_confusion",  # Башня Непонимания
        EmotionalState.INTEREST: "city_mind"  # Город Разума
    }

    # Support messages for each emotional state
    SUPPORT_MESSAGES = {
        EmotionalState.TIREDNESS: [
            "Вижу, ты устал/устала 😴 Может, сделаем перерыв?",
            "Все нормально, отдыхать важно! Хочешь что-то попроще?",
            "Давай попробуем что-то более легкое и интересное?"
        ],
        EmotionalState.ANXIETY: [
            "Все нормально, не волнуйся 🤗 Я рядом!",
            "Давай разберемся вместе, шаг за шагом. Ты справишься!",
            "Понимаю, что тревожно. Но ты не один/одна, я помогу!"
        ],
        EmotionalState.ANGER: [
            "Понимаю, что ты злишься 😤",
            "Иногда так бывает, когда что-то не получается.",
            "Хочешь попробовать по-другому? Или сначала успокоимся?"
        ],
        EmotionalState.DOUBT: [
            "Сомнения — это нормально! Значит, ты думаешь 🤔",
            "Давай разберемся вместе, что непонятно.",
            "Все когда-то чего-то не понимали. Зато теперь научимся!"
        ],
        EmotionalState.INTEREST: [
            "Вижу, тебе интересно! 🌟 Отлично!",
            "Супер, когда есть интерес! Давай погружаться глубже!",
            "Круто, что хочешь узнать больше! Начинаем!"
        ]
    }

    def __init__(self, max_history: int = 50):
        """
        Initialize emotional router.

        Args:
            max_history: Maximum number of emotional readings to keep
        """
        self.max_history = max_history
        self.emotional_history: List[EmotionalReading] = []

    def detect_emotion(self, message: str) -> EmotionalReading:
        """
        Detect emotional state from message using keyword matching.

        Args:
            message: User message

        Returns:
            EmotionalReading with detected state and intensity
        """
        message_lower = message.lower()

        # Count keyword matches for each emotion
        emotion_scores: Dict[EmotionalState, List[str]] = {
            emotion: [] for emotion in EmotionalState
        }

        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    emotion_scores[emotion].append(keyword)

        # Find emotion with most keyword matches
        detected_keywords = []
        detected_emotion = EmotionalState.INTEREST  # Default
        max_matches = 0

        for emotion, matches in emotion_scores.items():
            if len(matches) > max_matches:
                max_matches = len(matches)
                detected_emotion = emotion
                detected_keywords = matches

        # Calculate intensity based on number of keywords
        # 1 keyword = 0.3, 2 keywords = 0.6, 3+ keywords = 1.0
        intensity = min(1.0, max_matches * 0.3) if max_matches > 0 else 0.5

        reading = EmotionalReading(
            state=detected_emotion,
            intensity=intensity,
            message_snippet=message[:50],
            detected_keywords=detected_keywords
        )

        # Add to history
        self.emotional_history.append(reading)
        if len(self.emotional_history) > self.max_history:
            self.emotional_history.pop(0)

        return reading

    def recommend_location(self, emotion: Optional[EmotionalState] = None) -> str:
        """
        Recommend Ponimaliya location based on emotional state.

        Args:
            emotion: Emotional state (uses latest if None)

        Returns:
            Location ID (e.g., "forest_calm")
        """
        if emotion is None:
            if not self.emotional_history:
                return "tower_confusion"  # Default starting location
            emotion = self.emotional_history[-1].state

        return self.EMOTION_TO_LOCATION.get(emotion, "tower_confusion")

    def get_support_message(self, emotion: Optional[EmotionalState] = None) -> str:
        """
        Get supportive message for emotional state.

        Args:
            emotion: Emotional state (uses latest if None)

        Returns:
            Support message
        """
        if emotion is None:
            if not self.emotional_history:
                emotion = EmotionalState.INTEREST
            else:
                emotion = self.emotional_history[-1].state

        messages = self.SUPPORT_MESSAGES.get(emotion, ["Я здесь, чтобы помочь!"])

        # Rotate through messages based on history length
        index = len(self.emotional_history) % len(messages)
        return messages[index]

    def detect_emotional_volatility(self, window_minutes: int = 60) -> float:
        """
        Detect emotional volatility (rapid state changes).

        High volatility may indicate emotional dysregulation.

        Args:
            window_minutes: Time window to check

        Returns:
            Volatility score (0-1), higher = more volatile
        """
        if len(self.emotional_history) < 2:
            return 0.0

        # Get recent readings within time window
        now = datetime.now()
        cutoff = now.timestamp() - (window_minutes * 60)

        recent_readings = [
            r for r in self.emotional_history
            if r.timestamp.timestamp() > cutoff
        ]

        if len(recent_readings) < 2:
            return 0.0

        # Count state changes
        changes = 0
        for i in range(1, len(recent_readings)):
            if recent_readings[i].state != recent_readings[i-1].state:
                changes += 1

        # Normalize by number of readings
        volatility = changes / (len(recent_readings) - 1)

        return volatility

    def detect_emotional_storm(self, threshold_count: int = 3) -> bool:
        """
        Detect "emotional storm" - repeated negative emotions.

        Args:
            threshold_count: Number of negative readings to trigger storm

        Returns:
            True if storm detected
        """
        if len(self.emotional_history) < threshold_count:
            return False

        # Get last N readings
        recent = self.emotional_history[-threshold_count:]

        # Check if all are negative emotions (not interest)
        negative_emotions = {
            EmotionalState.TIREDNESS,
            EmotionalState.ANXIETY,
            EmotionalState.ANGER
        }

        storm = all(r.state in negative_emotions for r in recent)

        return storm

    def get_dominant_emotion(self, count: int = 10) -> EmotionalState:
        """
        Get dominant emotion from recent history.

        Args:
            count: Number of recent readings to consider

        Returns:
            Most common emotional state
        """
        if not self.emotional_history:
            return EmotionalState.INTEREST

        recent = self.emotional_history[-count:]

        # Count occurrences
        emotion_counts: Dict[EmotionalState, int] = {}
        for reading in recent:
            emotion_counts[reading.state] = emotion_counts.get(reading.state, 0) + 1

        # Find most common
        dominant = max(emotion_counts.items(), key=lambda x: x[1])
        return dominant[0]

    def get_emotional_summary(self) -> Dict[str, Any]:
        """
        Get summary of emotional state for analytics.

        Returns:
            Dictionary with emotional metrics
        """
        if not self.emotional_history:
            return {
                "current_emotion": "interest",
                "dominant_emotion": "interest",
                "volatility": 0.0,
                "emotional_storm": False,
                "total_readings": 0
            }

        return {
            "current_emotion": self.emotional_history[-1].state.value,
            "current_intensity": self.emotional_history[-1].intensity,
            "dominant_emotion": self.get_dominant_emotion().value,
            "volatility": self.detect_emotional_volatility(),
            "emotional_storm": self.detect_emotional_storm(),
            "total_readings": len(self.emotional_history),
            "recommended_location": self.recommend_location()
        }

    def clear_history(self) -> None:
        """Clear emotional history (e.g., at session end)."""
        self.emotional_history.clear()
