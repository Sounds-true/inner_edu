"""
ChildBot - Main bot for children (7-14 years old)
Educational Mode - helps with learning and emotional literacy
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from ..config import CHILD_BOT_TOKEN, FEATURES
from ..game.scenario_engine import ScenarioEngine
from ..game.emotional_router import EmotionalRouter
from ..game.learning_profile import LearningProfile
from ..game.state_manager import StateManager
from ..data.user_manager import UserManager
from ..data.link_manager import LinkManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ChildBot:
    """Main bot class for children"""

    def __init__(self):
        self.app = Application.builder().token(CHILD_BOT_TOKEN).build()
        self.scenario_engine = ScenarioEngine()
        self.emotional_router = EmotionalRouter()
        self.learning_profile = LearningProfile()
        self.state_manager = StateManager()
        self.user_manager = UserManager()
        self.link_manager = LinkManager()

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(CommandHandler("profile", self.profile))

        # Callback queries (buttons)
        self.app.add_handler(CallbackQueryHandler(self.button_handler))

        # Text messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_handler))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - First entry point"""
        user_telegram_id = update.effective_user.id

        # Check if user already exists
        user = self.user_manager.get_user_by_telegram_id(user_telegram_id)

        if user:
            # Existing user
            await update.message.reply_text(
                f"С возвращением, {user['child_name']}! 😊\n\n"
                f"Продолжим наше путешествие?\n\n"
                f"Твой уровень: {user['progress']['level']}\n"
                f"XP: {user['progress']['experience_points']}/{user['progress']['next_level_xp']}"
            )

            # Continue from where they left off
            await self._show_main_menu(update, context, user)
        else:
            # New user - need parent linking
            await self._start_linking_flow(update, context, user_telegram_id)

    async def _start_linking_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_telegram_id: int):
        """Start the parent linking flow for new users"""
        await update.message.reply_text(
            "Привет! Я InnerWorld Edu 🌟\n\n"
            "Помогу тебе с учебой и научу понимать себя лучше.\n\n"
            "Но сначала нужно, чтобы твой родитель подключился.\n"
            "Это нужно для твоей безопасности.\n\n"
            "Как тебя зовут?"
        )

        # Set state: waiting for name
        self.state_manager.set_state(user_telegram_id, "waiting_for_name")

    async def text_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages based on current state"""
        user_telegram_id = update.effective_user.id
        text = update.message.text

        # Get current state
        current_state = self.state_manager.get_state(user_telegram_id)

        if current_state == "waiting_for_name":
            await self._handle_name_input(update, context, text)
        elif current_state == "onboarding":
            await self._handle_onboarding(update, context, text)
        elif current_state == "in_quest":
            await self._handle_quest_answer(update, context, text)
        else:
            # Default: echo or handle as regular message
            await update.message.reply_text(
                "Я не совсем понял. Попробуй использовать кнопки или команды.\n\n"
                "/help - помощь"
            )

    async def _handle_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, name: str):
        """Handle child's name input"""
        user_telegram_id = update.effective_user.id

        # Validate name
        if len(name) < 2 or len(name) > 50:
            await update.message.reply_text(
                "Имя должно быть от 2 до 50 символов. Попробуй еще раз:"
            )
            return

        # Create linking request
        link_id, parent_link = self.link_manager.create_link(user_telegram_id, name)

        await update.message.reply_text(
            f"Отлично, {name}! 😊\n\n"
            f"Теперь попроси маму или папу открыть эту ссылку:\n\n"
            f"👉 {parent_link}\n\n"
            f"Или можешь переслать это сообщение родителю.\n\n"
            f"Я подожду, когда родитель подключится.\n"
            f"Обычно это занимает 1-2 минуты.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Проверить статус ✅", callback_data="check_link_status")
            ]])
        )

        # Set state: waiting for parent
        self.state_manager.set_state(user_telegram_id, "waiting_for_parent")
        context.user_data['link_id'] = link_id
        context.user_data['child_name'] = name

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks (callback queries)"""
        query = update.callback_query
        await query.answer()

        user_telegram_id = update.effective_user.id
        data = query.data

        if data == "check_link_status":
            await self._check_link_status(query, context)
        elif data.startswith("emotion_"):
            emotion = data.split("_")[1]
            await self._handle_emotion_selection(query, context, emotion)
        elif data.startswith("location_"):
            location = data.split("_", 1)[1]
            await self._handle_location_selection(query, context, location)
        else:
            await query.edit_message_text("Функция в разработке 🚧")

    async def _check_link_status(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Check if parent has linked"""
        link_id = context.user_data.get('link_id')

        if not link_id:
            await query.edit_message_text("Ошибка: link_id не найден")
            return

        link = self.link_manager.get_link(link_id)

        if link and link['status'] == 'active':
            # Parent linked! Start onboarding
            child_name = context.user_data['child_name']
            user_telegram_id = query.from_user.id

            # Create user profile
            user = self.user_manager.create_user(
                telegram_id=user_telegram_id,
                child_name=child_name,
                link_id=link_id
            )

            await query.edit_message_text(
                f"🎉 Отлично! {link['relationship'].capitalize()} подключил{'а' if link['relationship'] == 'mother' else ''} ся.\n\n"
                f"Теперь мы можем начать твоё путешествие в Понималию!\n\n"
                f"Готов{'а' if child_name.endswith('а') or child_name.endswith('я') else ''}?"
            )

            # Start onboarding
            await self._start_onboarding(query, context, user)
        else:
            await query.edit_message_text(
                "Родитель еще не подключился.\n\n"
                "Попроси маму или папу открыть ссылку, которую я отправил выше.\n\n"
                "Проверим еще раз?",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Проверить снова ✅", callback_data="check_link_status")
                ]])
            )

    async def _start_onboarding(self, query_or_update, context: ContextTypes.DEFAULT_TYPE, user: dict):
        """Start the onboarding process"""
        # Load first onboarding scenario
        scenario = self.scenario_engine.load_scenario("onboarding/01_greeting.yaml")

        # Show first step
        await self.scenario_engine.show_step(query_or_update, context, scenario, step_index=0)

        # Set state
        user_telegram_id = user['telegram_id']
        self.state_manager.set_state(user_telegram_id, "onboarding")
        context.user_data['current_scenario'] = "onboarding/01_greeting"
        context.user_data['current_step'] = 0

    async def _handle_onboarding(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle onboarding flow"""
        # This will be implemented with ScenarioEngine
        pass

    async def _show_main_menu(self, update_or_query, context: ContextTypes.DEFAULT_TYPE, user: dict):
        """Show main menu with available options"""
        keyboard = [
            [InlineKeyboardButton("🗺️ Карта Понималии", callback_data="map")],
            [InlineKeyboardButton("📊 Мой профиль", callback_data="profile")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]

        text = (
            f"Главное меню\n\n"
            f"Уровень: {user['progress']['level']}\n"
            f"XP: {user['progress']['experience_points']}/{user['progress']['next_level_xp']}\n\n"
            f"Что будем делать?"
        )

        if isinstance(update_or_query, Update):
            await update_or_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update_or_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "🌟 InnerWorld Edu - Помощь\n\n"
            "Команды:\n"
            "/start - Начать или вернуться в главное меню\n"
            "/profile - Показать твой профиль\n"
            "/status - Текущий прогресс\n"
            "/help - Эта помощь\n\n"
            "Если застрял или не знаешь что делать - напиши 'Помогите!'"
        )
        await update.message.reply_text(help_text)

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current status"""
        user_telegram_id = update.effective_user.id
        user = self.user_manager.get_user_by_telegram_id(user_telegram_id)

        if not user:
            await update.message.reply_text("Сначала нужно пройти /start")
            return

        status_text = (
            f"📊 Твой статус\n\n"
            f"Имя: {user['child_name']}\n"
            f"Уровень: {user['progress']['level']}\n"
            f"XP: {user['progress']['experience_points']}/{user['progress']['next_level_xp']}\n"
            f"Квестов выполнено: {user['progress']['total_quests_completed']}\n"
            f"Серия дней: {user['progress']['streak_days']} 🔥\n\n"
            f"Текущая локация: {user['world']['current_location']}"
        )

        await update.message.reply_text(status_text)

    async def profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show learning profile"""
        user_telegram_id = update.effective_user.id
        user = self.user_manager.get_user_by_telegram_id(user_telegram_id)

        if not user:
            await update.message.reply_text("Сначала нужно пройти /start")
            return

        lp = user['learning_profile']
        profile_text = (
            f"📈 Learning Profile\n\n"
            f"Понимание смысла: {'⭐' * lp['understanding_meaning']}{'☆' * (10 - lp['understanding_meaning'])} ({lp['understanding_meaning']}/10)\n"
            f"Память: {'⭐' * lp['memory']}{'☆' * (10 - lp['memory'])} ({lp['memory']}/10)\n"
            f"Внимание: {'⭐' * lp['attention']}{'☆' * (10 - lp['attention'])} ({lp['attention']}/10)\n"
            f"Мотивация: {'⭐' * lp['motivation']}{'☆' * (10 - lp['motivation'])} ({lp['motivation']}/10)\n"
        )

        await update.message.reply_text(profile_text)

    def run(self):
        """Start the bot"""
        logger.info("Starting ChildBot...")
        self.app.run_polling()


if __name__ == "__main__":
    bot = ChildBot()
    bot.run()
