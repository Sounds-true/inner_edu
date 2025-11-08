"""
State management for InnerWorld Edu using LangGraph.

Manages educational flow through Ponimaliya:
1. Onboarding → Learn about child
2. Location Selection → Based on learning profile
3. Quest Active → Interactive YAML scenarios
4. Reflection → Process learning
5. Casual Chat → Natural conversation with LLM

Integrates OpenAI for natural language understanding.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import asyncio

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from src.core.logger import get_logger
from src.config import (
    EDUCATIONAL_MODULES,
    EDUCATIONAL_LOCATIONS,
    SCREENING_THRESHOLDS
)

# Import helper classes
from src.orchestration.emotional_router import EmotionalRouter, EmotionalState
from src.orchestration.learning_profile import LearningProfile, LearningProfileAnalyzer, LearningDimension
from src.data.user_manager import UserManager, ScreeningMetrics as UserScreeningMetrics
from src.data.link_manager import LinkManager
from src.game.quest_engine import QuestEngine
from src.game.reality_bridge_manager import RealityBridgeManager

logger = get_logger(__name__)


class ConversationState(str, Enum):
    """Conversation states for educational bot."""
    START = "start"
    PARENT_LINKING = "parent_linking"
    ONBOARDING = "onboarding"
    EMOTION_CHECK = "emotion_check"
    LOCATION_SELECTION = "location_selection"
    QUEST_ACTIVE = "quest_active"
    QUEST_REFLECTION = "quest_reflection"
    CASUAL_CHAT = "casual_chat"
    LEARNING_SUPPORT = "learning_support"
    SCREENING_CHECK = "screening_check"
    END_SESSION = "end_session"


# Use ScreeningMetrics from user_manager
ScreeningMetrics = UserScreeningMetrics


@dataclass
class UserState:
    """User state for educational bot."""
    user_id: str
    child_name: Optional[str] = None
    age: Optional[int] = None

    # State tracking
    current_state: ConversationState = ConversationState.START
    emotional_state: EmotionalState = EmotionalState.INTEREST

    # Learning and progress
    learning_profile: LearningProfile = field(default_factory=LearningProfile)
    current_location: Optional[str] = None
    current_quest: Optional[str] = None
    quest_step: int = 0

    # Screening for therapeutic transition
    screening: ScreeningMetrics = field(default_factory=ScreeningMetrics)

    # Session management
    messages_count: int = 0
    session_start: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

    # Conversation memory
    message_history: List[BaseMessage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

    # Parent linking
    parent_linked: bool = False
    link_id: Optional[str] = None


class StateManager:
    """Manages educational conversation states using LangGraph."""

    def __init__(self):
        """Initialize state manager."""
        self.user_states: Dict[str, UserState] = {}
        self.graph: Optional[StateGraph] = None
        self.llm: Optional[ChatOpenAI] = None

        # Helper classes (initialized lazily in initialize())
        self.emotional_router: Optional[EmotionalRouter] = None
        self.user_manager: Optional[UserManager] = None
        self.link_manager: Optional[LinkManager] = None
        self.quest_engine: Optional[QuestEngine] = None
        self.reality_bridge_manager: Optional[RealityBridgeManager] = None

        # Emotional router per user (tracks emotional history)
        self.user_emotional_routers: Dict[str, EmotionalRouter] = {}

        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the state graph, LLM, and helper classes."""
        try:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                max_tokens=500
            )
            logger.info("llm_initialized", model="gpt-4")

            # Initialize helper classes
            self.user_manager = UserManager()
            self.link_manager = LinkManager()
            self.quest_engine = QuestEngine()
            self.reality_bridge_manager = RealityBridgeManager()

            # Load all quests
            quest_count = await self.quest_engine.load_all_quests()
            logger.info("quests_loaded", count=quest_count)

            # Initialize Reality Bridge Manager
            await self.reality_bridge_manager.initialize()

            # Set reminder callback to send messages to users
            self.reality_bridge_manager.set_reminder_callback(self._send_reality_bridge_reminder)
            logger.info("reality_bridge_manager_ready")

            # Build state graph
            self.graph = self._build_state_graph()
            logger.info("state_graph_built")

            self.initialized = True
            logger.info("state_manager_initialized")

        except Exception as e:
            logger.error("state_manager_init_failed", error=str(e))
            raise

    def _build_state_graph(self) -> StateGraph:
        """Build the LangGraph state machine for educational flow."""
        workflow = StateGraph(Dict[str, Any])

        # Add nodes
        workflow.add_node("start", self._handle_start)
        workflow.add_node("parent_linking", self._handle_parent_linking)
        workflow.add_node("onboarding", self._handle_onboarding)
        workflow.add_node("emotion_check", self._handle_emotion_check)
        workflow.add_node("location_selection", self._handle_location_selection)
        workflow.add_node("quest_active", self._handle_quest_active)
        workflow.add_node("quest_reflection", self._handle_quest_reflection)
        workflow.add_node("casual_chat", self._handle_casual_chat)
        workflow.add_node("learning_support", self._handle_learning_support)
        workflow.add_node("screening_check", self._handle_screening_check)
        workflow.add_node("end_session", self._handle_end_session)

        # Set entry point
        workflow.set_entry_point("start")

        # Add transitions
        workflow.add_conditional_edges(
            "start",
            self._route_after_start,
            {
                "parent_linking": "parent_linking",
                "onboarding": "onboarding",
                "emotion_check": "emotion_check"
            }
        )

        workflow.add_edge("parent_linking", END)

        workflow.add_conditional_edges(
            "onboarding",
            self._route_after_onboarding,
            {
                "continue": "onboarding",
                "complete": "location_selection"
            }
        )

        workflow.add_edge("emotion_check", "screening_check")

        workflow.add_conditional_edges(
            "screening_check",
            self._route_after_screening,
            {
                "normal": "location_selection",
                "support_needed": "learning_support",
                "crisis": "learning_support"  # Gentle support, escalate to parent
            }
        )

        workflow.add_edge("location_selection", END)

        workflow.add_conditional_edges(
            "quest_active",
            self._route_after_quest,
            {
                "continue": "quest_active",
                "complete": "quest_reflection",
                "stuck": "learning_support"
            }
        )

        workflow.add_edge("quest_reflection", END)

        workflow.add_conditional_edges(
            "casual_chat",
            self._route_after_casual_chat,
            {
                "continue": END,
                "quest": "quest_active",
                "support": "learning_support",
                "end": "end_session"
            }
        )

        workflow.add_edge("learning_support", END)
        workflow.add_edge("end_session", END)

        return workflow.compile()

    async def initialize_user(self, user_id: str, child_name: Optional[str] = None) -> None:
        """Initialize a new user state, loading from UserManager if exists."""
        # Try to load from UserManager
        if self.user_manager:
            profile = await self.user_manager.get_user(user_id)
            if profile:
                # Convert UserProfile to UserState
                user_state = self._profile_to_state(profile)
                self.user_states[user_id] = user_state
                logger.info("user_loaded_from_storage", user_id=user_id)
                return

        # Create new user state
        self.user_states[user_id] = UserState(
            user_id=user_id,
            child_name=child_name
        )
        logger.info("user_initialized_new", user_id=user_id, child_name=child_name)

    def _profile_to_state(self, profile) -> UserState:
        """Convert UserProfile to UserState."""
        from src.data.user_manager import UserProfile

        # Reconstruct LearningProfile
        learning_profile = LearningProfile()
        if profile.learning_profile:
            learning_profile.understanding_meaning = profile.learning_profile.get("understanding_meaning", 5)
            learning_profile.memory = profile.learning_profile.get("memory", 5)
            learning_profile.attention = profile.learning_profile.get("attention", 5)
            learning_profile.motivation = profile.learning_profile.get("motivation", 5)

        # Reconstruct ScreeningMetrics
        screening = ScreeningMetrics()
        if profile.screening:
            screening.self_worth = profile.screening.get("self_worth", 0.5)
            screening.self_criticism = profile.screening.get("self_criticism", 0.5)
            screening.emotional_volatility = profile.screening.get("emotional_volatility", 0.5)
            screening.manipulation_score = profile.screening.get("manipulation_score", 0)
            screening.self_harm_detected = profile.screening.get("self_harm_detected", False)
            screening.emotional_storm_count = profile.screening.get("emotional_storm_count", 0)

        # Create UserState
        user_state = UserState(
            user_id=profile.user_id,
            child_name=profile.child_name,
            age=profile.age,
            learning_profile=learning_profile,
            current_location=profile.current_location,
            current_quest=profile.current_quest,
            quest_step=profile.quest_step,
            screening=screening,
            parent_linked=profile.parent_linked,
            link_id=profile.link_id
        )

        return user_state

    def _state_to_profile(self, user_state: UserState):
        """Convert UserState to UserProfile."""
        from src.data.user_manager import UserProfile

        profile = UserProfile(
            user_id=user_state.user_id,
            child_name=user_state.child_name,
            age=user_state.age,
            parent_linked=user_state.parent_linked,
            link_id=user_state.link_id,
            learning_profile={
                "understanding_meaning": user_state.learning_profile.understanding_meaning,
                "memory": user_state.learning_profile.memory,
                "attention": user_state.learning_profile.attention,
                "motivation": user_state.learning_profile.motivation
            },
            current_location=user_state.current_location,
            current_quest=user_state.current_quest,
            quest_step=user_state.quest_step,
            screening={
                "self_worth": user_state.screening.self_worth,
                "self_criticism": user_state.screening.self_criticism,
                "emotional_volatility": user_state.screening.emotional_volatility,
                "manipulation_score": user_state.screening.manipulation_score,
                "self_harm_detected": user_state.screening.self_harm_detected,
                "emotional_storm_count": user_state.screening.emotional_storm_count
            }
        )

        return profile

    async def save_user_state(self, user_state: UserState) -> None:
        """Save user state to UserManager."""
        if not self.user_manager:
            return

        try:
            profile = self._state_to_profile(user_state)
            await self.user_manager.update_user(profile)
            logger.debug("user_state_saved", user_id=user_state.user_id)
        except Exception as e:
            logger.error("user_state_save_failed", user_id=user_state.user_id, error=str(e))

    async def process_message(self, user_id: str, message: str) -> str:
        """
        Process user message through state machine with LLM.

        Uses OpenAI for natural language understanding while maintaining
        structured state transitions.
        """
        if not self.initialized:
            await self.initialize()

        # Get or create user state
        user_state = self.user_states.get(user_id)
        if not user_state:
            await self.initialize_user(user_id)
            user_state = self.user_states[user_id]

        # Update state
        user_state.last_activity = datetime.now()
        user_state.messages_count += 1
        user_state.message_history.append(HumanMessage(content=message))

        # Detect emotional state from message
        await self._detect_emotional_state(user_state, message)

        # Update screening metrics
        await self._update_screening_metrics(user_state, message)

        # Process through state graph
        try:
            graph_state = {
                "user_id": user_id,
                "message": message,
                "user_state": user_state,
                "timestamp": datetime.now().isoformat()
            }

            result = await self.graph.ainvoke(graph_state)
            response = result.get("response", "Я здесь, чтобы помочь! 🌟")

            # Add to message history
            user_state.message_history.append(AIMessage(content=response))

            # Save user state to persistent storage
            await self.save_user_state(user_state)

            return response

        except Exception as e:
            logger.error("message_processing_failed", user_id=user_id, error=str(e))
            return "Извини, что-то пошло не так. Давай попробуем еще раз? 😊"

    async def _detect_emotional_state(self, user_state: UserState, message: str) -> None:
        """Detect emotional state using EmotionalRouter."""
        # Get or create emotional router for user
        if user_state.user_id not in self.user_emotional_routers:
            self.user_emotional_routers[user_state.user_id] = EmotionalRouter()

        router = self.user_emotional_routers[user_state.user_id]

        # Detect emotion
        reading = router.detect_emotion(message)
        user_state.emotional_state = reading.state

        logger.info("emotional_state_detected",
                   user_id=user_state.user_id,
                   state=reading.state.value,
                   intensity=reading.intensity,
                   keywords=reading.detected_keywords)

    async def _update_screening_metrics(self, user_state: UserState, message: str) -> None:
        """Update screening metrics for therapeutic transition detection."""
        message_lower = message.lower()

        # Check for self-harm keywords
        self_harm_keywords = SCREENING_THRESHOLDS["critical"]["self_harm_keywords"]
        if any(keyword in message_lower for keyword in self_harm_keywords):
            user_state.screening.self_harm_detected = True
            logger.warning("self_harm_keyword_detected", user_id=user_state.user_id)

        # Check for self-worth indicators
        if any(word in message_lower for word in ["тупой", "идиот", "ничего не умею", "не получается"]):
            user_state.screening.self_worth = max(0, user_state.screening.self_worth - 0.05)
            user_state.screening.self_criticism = min(1, user_state.screening.self_criticism + 0.05)

        # Check for emotional storm
        if user_state.emotional_state in [EmotionalState.ANGER, EmotionalState.ANXIETY]:
            if user_state.screening.last_emotional_storm:
                time_since_last = datetime.now() - user_state.screening.last_emotional_storm
                if time_since_last.total_seconds() < 3600:  # Within 1 hour
                    user_state.screening.emotional_storm_count += 1
            user_state.screening.last_emotional_storm = datetime.now()

    # State handlers
    async def _handle_start(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start state."""
        user_state = state["user_state"]

        if not user_state.parent_linked:
            state["response"] = (
                "Привет! Я InnerWorld Edu 🌟\n\n"
                "Помогу тебе с учебой и научу понимать себя лучше.\n\n"
                "Но сначала нужно, чтобы твой родитель подключился.\n"
                "Это нужно для твоей безопасности.\n\n"
                "Как тебя зовут?"
            )
        elif not user_state.child_name:
            state["response"] = "Привет! Как тебя зовут?"
        else:
            state["response"] = f"С возвращением, {user_state.child_name}! 😊"

        return state

    async def _handle_parent_linking(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle parent linking flow."""
        state["response"] = (
            "Отправлю ссылку для родителя...\n"
            "(В MVP это будет реализовано через LinkManager)"
        )
        return state

    async def _handle_onboarding(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle onboarding with LLM for natural conversation."""
        user_state = state["user_state"]
        message = state["message"]

        # Build conversation context
        system_prompt = f"""Ты — добрый помощник в мире Понималия, помогающий детям 7-14 лет.

Твоя задача на этапе знакомства:
1. Узнать имя ребенка (если еще не знаешь)
2. Узнать, с какими предметами есть сложности (математика, чтение и т.д.)
3. Понять, что именно сложно (не понимаю, забываю, скучно)
4. Определить эмоциональное состояние

Говори дружелюбно, просто, с эмодзи. Задавай по одному вопросу за раз.

Имя ребенка: {user_state.child_name or 'неизвестно'}
Количество сообщений: {user_state.messages_count}
"""

        # Get LLM response with conversation history
        messages = [SystemMessage(content=system_prompt)]

        # Add recent conversation history (last 10 messages)
        if user_state.message_history:
            messages.extend(user_state.message_history[-10:])

        try:
            response = await self.llm.ainvoke(messages)
            state["response"] = response.content

            # Extract child name if mentioned
            if not user_state.child_name and user_state.messages_count == 1:
                # First message likely contains name
                user_state.child_name = message.strip()

        except Exception as e:
            logger.error("llm_call_failed", error=str(e))
            state["response"] = "Расскажи мне о себе! Какой предмет в школе кажется самым сложным?"

        return state

    async def _handle_emotion_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emotion check state."""
        user_state = state["user_state"]

        state["response"] = f"Вижу, что ты чувствуешь {self._translate_emotion(user_state.emotional_state)}."

        return state

    async def _handle_location_selection(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle location selection based on learning profile."""
        user_state = state["user_state"]

        # Use LearningProfileAnalyzer to recommend location based on weakest dimension
        recommended = LearningProfileAnalyzer.recommend_location(user_state.learning_profile)

        # Location names mapping
        location_names = {
            "tower_confusion": "Башню Непонимания",
            "valley_words": "Долину Слов",
            "mountain_emptiness": "Гору Пустоты",
            "forest_calm": "Лес Спокойствия",
            "city_mind": "Город Разума",
            "workshop_creator": "Мастерскую Творца",
            "bridge_actions": "Мост Действий"
        }

        location_name = location_names.get(recommended, "Башню Непонимания")
        user_state.current_location = recommended

        # Get first quest for location from QuestEngine
        first_quest = None
        if self.quest_engine:
            first_quest = self.quest_engine.get_first_quest_for_location(recommended)
            if first_quest:
                user_state.current_quest = first_quest.id

        state["response"] = (
            f"Отлично! Думаю, тебе стоит посетить {location_name} 🏰\n\n"
            f"Там мы научимся справляться с твоими сложностями.\n\n"
            f"Готов начать первый квест?"
        )

        return state

    async def _handle_quest_active(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle active quest state with QuestEngine."""
        user_state = state["user_state"]
        message = state["message"]

        if not self.quest_engine:
            state["response"] = "Квесты временно недоступны. Попробуй позже! 😊"
            return state

        # Check if quest is already started
        progress = self.quest_engine.get_current_quest_progress(user_state.user_id)

        if not progress:
            # Start new quest
            if not user_state.current_quest:
                state["response"] = "Сначала выбери локацию и квест!"
                return state

            success, first_step = await self.quest_engine.start_quest(
                user_state.user_id,
                user_state.current_quest
            )

            if not success or not first_step:
                state["response"] = "Не могу начать квест. Попробуй позже! 😅"
                return state

            # Show first step
            state["response"] = f"🎯 **{first_step.id}**\n\n{first_step.prompt}"

            if first_step.hint:
                state["response"] += f"\n\n💡 *Подсказка:* {first_step.hint}"

            user_state.quest_step = 1
            return state

        # Process response to current step
        success, next_step, feedback = await self.quest_engine.process_step_response(
            user_state.user_id,
            message
        )

        if not success:
            # Invalid response
            state["response"] = f"❌ {feedback}\n\nПопробуй еще раз!"
            return state

        # Valid response
        response_parts = []

        if feedback:
            response_parts.append(f"✅ {feedback}")

        if next_step:
            # Continue to next step
            response_parts.append(
                f"\n\n🎯 **Шаг {user_state.quest_step + 1}**\n\n{next_step.prompt}"
            )

            if next_step.hint:
                response_parts.append(f"\n\n💡 *Подсказка:* {next_step.hint}")

            user_state.quest_step += 1
        else:
            # Quest completed!
            response_parts.append("\n\n🎉 **Квест завершен!**")

            # Get rewards
            rewards = await self.quest_engine.get_quest_rewards(user_state.user_id)
            if rewards:
                response_parts.append(f"\n\n🎁 **Награды:**")
                response_parts.append(f"• XP: +{rewards.experience_points}")

                # Apply learning profile changes
                for dimension, change in rewards.learning_profile_changes.items():
                    if dimension == "understanding_meaning":
                        user_state.learning_profile.understanding_meaning += change
                    elif dimension == "memory":
                        user_state.learning_profile.memory += change
                    elif dimension == "attention":
                        user_state.learning_profile.attention += change
                    elif dimension == "motivation":
                        user_state.learning_profile.motivation += change

            # Get Reality Bridge micro-action
            reality_bridge = await self.quest_engine.get_reality_bridge(user_state.user_id)
            if reality_bridge and self.reality_bridge_manager:
                # Create Reality Bridge reminder
                await self.reality_bridge_manager.create_bridge(
                    user_id=user_state.user_id,
                    quest_id=user_state.current_quest or "unknown",
                    bridge_id=reality_bridge.id,
                    title=reality_bridge.title,
                    description=reality_bridge.description,
                    deadline_hours=reality_bridge.deadline_hours,
                    reminder_hours=reality_bridge.reminder_hours
                )

                response_parts.append(f"\n\n🌉 **Reality Bridge:**")
                response_parts.append(f"\n{reality_bridge.title}")
                response_parts.append(f"\n{reality_bridge.description}")
                response_parts.append(f"\n\nУ тебя есть {reality_bridge.deadline_hours} часов!")
                response_parts.append(f"\nЯ напомню через {reality_bridge.reminder_hours} часов. ⏰")

            # Mark quest as completed
            user_state.current_quest = None
            user_state.quest_step = 0

        state["response"] = "".join(response_parts)
        return state

    async def _handle_quest_reflection(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle quest reflection state."""
        state["response"] = (
            "Отлично справился! 🎉\n\n"
            "Что нового ты узнал? Что было самым интересным?"
        )
        return state

    async def _handle_casual_chat(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle casual chat with LLM for natural conversation."""
        user_state = state["user_state"]
        message = state["message"]

        system_prompt = f"""Ты — добрый помощник в мире Понималия для детей 7-14 лет.

Ребенок сейчас просто общается с тобой (не в квесте).

Твои правила:
1. Отвечай дружелюбно, с эмодзи
2. Если ребенок шутит — пошути в ответ
3. Если пишет не по теме — нормально отреагируй, потом мягко верни к обучению
4. Если говорит о сложностях — предложи помощь или квест
5. Говори на языке ребенка, просто и понятно

Имя: {user_state.child_name}
Эмоция: {user_state.emotional_state.value}
Локация: {user_state.current_location or 'не выбрана'}
"""

        messages = [SystemMessage(content=system_prompt)]

        # Add conversation history (last 10 messages) - THIS IS CRITICAL
        if user_state.message_history:
            messages.extend(user_state.message_history[-10:])

        try:
            response = await self.llm.ainvoke(messages)
            state["response"] = response.content
        except Exception as e:
            logger.error("llm_call_failed", error=str(e))
            state["response"] = "Ха-ха, интересно! 😄 Расскажи еще что-нибудь!"

        return state

    async def _handle_learning_support(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle learning support state."""
        user_state = state["user_state"]

        # Gentle support based on emotional state
        if user_state.emotional_state == EmotionalState.TIREDNESS:
            state["response"] = (
                "Вижу, ты устал 😴\n\n"
                "Может, сделаем перерыв? Или попробуем что-то более легкое и интересное?"
            )
        elif user_state.emotional_state == EmotionalState.ANXIETY:
            state["response"] = (
                "Все нормально, не волнуйся 🤗\n\n"
                "Давай разберемся вместе, шаг за шагом. Ты справишься!"
            )
        elif user_state.emotional_state == EmotionalState.ANGER:
            state["response"] = (
                "Понимаю, что ты злишься 😤\n\n"
                "Иногда так бывает, когда что-то не получается. Хочешь попробовать по-другому?"
            )
        else:
            state["response"] = "Я здесь, чтобы помочь! Что тебя беспокоит?"

        return state

    async def _handle_screening_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle screening check for therapeutic transition."""
        user_state = state["user_state"]

        # Check screening metrics
        metrics = user_state.screening

        if metrics.self_harm_detected:
            logger.warning("screening_critical", user_id=user_state.user_id)
            # TODO: Notify parent, escalate
        elif (metrics.self_worth < SCREENING_THRESHOLDS["high_concern"]["self_worth"] or
              metrics.self_criticism > SCREENING_THRESHOLDS["high_concern"]["self_criticism"]):
            logger.warning("screening_high_concern", user_id=user_state.user_id)
            # TODO: Suggest therapeutic mode transition

        return state

    async def _handle_end_session(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle end session."""
        user_state = state["user_state"]

        state["response"] = (
            f"Спасибо за сегодня, {user_state.child_name}! 🌟\n\n"
            f"Ты молодец! Возвращайся, когда захочешь.\n\n"
            f"Пока! 👋"
        )

        return state

    # Routing functions
    def _route_after_start(self, state: Dict[str, Any]) -> str:
        """Route after start state."""
        user_state = state["user_state"]

        if not user_state.parent_linked:
            return "parent_linking"
        elif not user_state.child_name or user_state.messages_count < 5:
            return "onboarding"
        else:
            return "emotion_check"

    def _route_after_onboarding(self, state: Dict[str, Any]) -> str:
        """Route after onboarding."""
        user_state = state["user_state"]

        # Complete onboarding after 5+ messages and have name
        if user_state.messages_count >= 5 and user_state.child_name:
            return "complete"
        return "continue"

    def _route_after_screening(self, state: Dict[str, Any]) -> str:
        """Route after screening check."""
        user_state = state["user_state"]
        metrics = user_state.screening

        if metrics.self_harm_detected:
            return "crisis"
        elif (metrics.self_worth < SCREENING_THRESHOLDS["moderate_concern"]["self_worth"] or
              metrics.emotional_storm_count > 5):
            return "support_needed"
        return "normal"

    def _route_after_quest(self, state: Dict[str, Any]) -> str:
        """Route after quest step."""
        # TODO: Implement quest step tracking
        return "complete"

    def _route_after_casual_chat(self, state: Dict[str, Any]) -> str:
        """Route after casual chat."""
        message = state["message"].lower()

        if any(word in message for word in ["пока", "до свидания", "уйду"]):
            return "end"
        elif any(word in message for word in ["квест", "задание", "учиться"]):
            return "quest"
        elif any(word in message for word in ["помоги", "не понимаю", "сложно"]):
            return "support"
        return "continue"

    # Helper functions
    def _translate_emotion(self, emotion: EmotionalState) -> str:
        """Translate emotional state to Russian."""
        translations = {
            EmotionalState.TIREDNESS: "усталость",
            EmotionalState.ANXIETY: "тревогу",
            EmotionalState.ANGER: "злость",
            EmotionalState.INTEREST: "интерес",
            EmotionalState.DOUBT: "сомнение"
        }
        return translations.get(emotion, "что-то интересное")

    async def _send_reality_bridge_reminder(self, user_id: str, bridge) -> None:
        """
        Send Reality Bridge reminder to user.

        This is called by RealityBridgeManager when it's time to remind user.
        In production, this would send a Telegram message.
        For now, we log it.

        Args:
            user_id: User ID
            bridge: ActiveBridge object
        """
        # TODO: In production, send via Telegram bot
        # For now, just log
        logger.info("reality_bridge_reminder_triggered",
                   user_id=user_id,
                   bridge_id=bridge.bridge_id,
                   title=bridge.title)

        # Store reminder for next user interaction
        user_state = self.user_states.get(user_id)
        if user_state:
            user_state.context["pending_reality_bridge_reminder"] = {
                "bridge_id": bridge.bridge_id,
                "title": bridge.title,
                "description": bridge.description,
                "deadline_at": bridge.deadline_at
            }
            logger.debug("reminder_stored_in_context", user_id=user_id)
