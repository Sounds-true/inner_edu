#!/usr/bin/env python3
"""
Test StateManager for InnerWorld Edu.

This script tests the basic flow:
1. Initialize StateManager
2. Simulate child starting conversation
3. Test onboarding flow
4. Test casual conversation with LLM
5. Test emotional state detection
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.orchestration.state_manager import StateManager
from src.core.logger import setup_logging

setup_logging("INFO")


async def main():
    """Test state manager with sample dialogue."""
    print("=== InnerWorld Edu StateManager Test ===\n")

    # Initialize state manager
    print("Initializing StateManager...")
    state_manager = StateManager()

    try:
        await state_manager.initialize()
        print("✅ StateManager initialized\n")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("\nℹ️  Make sure you have:")
        print("   1. Created .env file with OPENAI_API_KEY")
        print("   2. Installed dependencies: pip install -r requirements.txt")
        return

    user_id = "test_child_123"

    # Initialize user
    await state_manager.initialize_user(user_id)
    print(f"✅ User {user_id} initialized\n")

    # Test conversation flow
    test_messages = [
        "Привет, меня зовут Саша",
        "Мне сложно с математикой",
        "Я не понимаю дроби",
        "Да, давай попробуем!",
        "А можно пошутить?",
        "Что делает пират, когда видит дробь? Аррр, не понимаю! 😄"
    ]

    print("=== Starting conversation ===\n")

    for i, message in enumerate(test_messages, 1):
        print(f"👦 Ребенок (сообщение {i}): {message}")

        try:
            response = await state_manager.process_message(user_id, message)
            print(f"🤖 Бот: {response}\n")

            # Show current state
            user_state = state_manager.user_states[user_id]
            print(f"   📊 Состояние: {user_state.current_state.value}")
            print(f"   💭 Эмоция: {user_state.emotional_state.value}")
            print(f"   📍 Локация: {user_state.current_location or 'не выбрана'}")
            print(f"   💬 Сообщений: {user_state.messages_count}\n")
            print("-" * 60 + "\n")

            # Small delay to avoid rate limiting
            await asyncio.sleep(1)

        except Exception as e:
            print(f"❌ Error processing message: {e}\n")

    print("=== Test completed ===\n")

    # Show final user state
    user_state = state_manager.user_states[user_id]
    print(f"Final state:")
    print(f"  - Name: {user_state.child_name}")
    print(f"  - State: {user_state.current_state.value}")
    print(f"  - Emotion: {user_state.emotional_state.value}")
    print(f"  - Location: {user_state.current_location}")
    print(f"  - Messages: {user_state.messages_count}")
    print(f"  - Learning Profile:")
    print(f"      Understanding: {user_state.learning_profile.understanding_meaning}/10")
    print(f"      Memory: {user_state.learning_profile.memory}/10")
    print(f"      Attention: {user_state.learning_profile.attention}/10")
    print(f"      Motivation: {user_state.learning_profile.motivation}/10")
    print(f"  - Screening:")
    print(f"      Self-worth: {user_state.screening.self_worth:.2f}")
    print(f"      Self-criticism: {user_state.screening.self_criticism:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
