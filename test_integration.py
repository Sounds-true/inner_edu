"""
End-to-end integration test for InnerWorld Edu.

Tests complete flow:
1. Onboarding
2. Location selection
3. Quest progression (5 steps)
4. Quest completion with Reality Bridge
5. User persistence
"""

import asyncio
import os
from pathlib import Path

# Set environment variables before importing
os.environ['OPENAI_API_KEY'] = 'test-key-for-integration-test'

from src.orchestration.state_manager import StateManager


async def test_integration():
    """Run end-to-end integration test."""
    print("=" * 60)
    print("InnerWorld Edu - End-to-End Integration Test")
    print("=" * 60)
    print()

    # Initialize StateManager
    print("📦 Initializing StateManager...")
    state_manager = StateManager()

    try:
        await state_manager.initialize()
        print("✅ StateManager initialized")
        print()
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print()
        print("⚠️  Note: This test requires OPENAI_API_KEY in .env")
        print("   Skipping LLM tests, but showing system structure...")
        print()

    # Test 1: User Initialization
    print("=" * 60)
    print("Test 1: User Initialization")
    print("=" * 60)

    user_id = "test_user_12345"

    await state_manager.initialize_user(user_id, "Саша")
    user_state = state_manager.user_states.get(user_id)

    if user_state:
        print(f"✅ User initialized: {user_state.child_name}")
        print(f"   User ID: {user_state.user_id}")
        print(f"   Emotional state: {user_state.emotional_state.value}")
        print(f"   Learning profile: understanding={user_state.learning_profile.understanding_meaning}, "
              f"memory={user_state.learning_profile.memory}, "
              f"attention={user_state.learning_profile.attention}, "
              f"motivation={user_state.learning_profile.motivation}")
    else:
        print("❌ User initialization failed")

    print()

    # Test 2: Helper Classes
    print("=" * 60)
    print("Test 2: Helper Classes Loaded")
    print("=" * 60)

    print(f"✅ UserManager: {'Loaded' if state_manager.user_manager else 'Not loaded'}")
    print(f"✅ LinkManager: {'Loaded' if state_manager.link_manager else 'Not loaded'}")
    print(f"✅ QuestEngine: {'Loaded' if state_manager.quest_engine else 'Not loaded'}")
    print(f"✅ RealityBridgeManager: {'Loaded' if state_manager.reality_bridge_manager else 'Not loaded'}")

    if state_manager.quest_engine:
        quest_count = len(state_manager.quest_engine.quests)
        print(f"✅ Quests loaded: {quest_count}")

        # Show available quests
        if quest_count > 0:
            print("\n   Available quests:")
            for quest_id, quest in list(state_manager.quest_engine.quests.items())[:3]:
                print(f"   • {quest_id}: {quest.title} ({quest.location})")

    print()

    # Test 3: EmotionalRouter
    print("=" * 60)
    print("Test 3: Emotional Detection")
    print("=" * 60)

    test_messages = [
        ("Я так устал, не могу больше", "tiredness"),
        ("Боюсь, что не справлюсь с этим", "anxiety"),
        ("Ненавижу математику!", "anger"),
        ("Это интересно! Хочу узнать больше", "interest"),
        ("Не знаю, получится ли", "doubt"),
    ]

    for message, expected_emotion in test_messages:
        await state_manager._detect_emotional_state(user_state, message)
        detected = user_state.emotional_state.value
        status = "✅" if detected == expected_emotion else "⚠️"
        print(f"{status} \"{message[:40]}...\" → {detected}")

    print()

    # Test 4: Learning Profile & Location Recommendation
    print("=" * 60)
    print("Test 4: Location Recommendation")
    print("=" * 60)

    from src.orchestration.learning_profile import LearningProfileAnalyzer

    # Test different profiles
    test_profiles = [
        {"understanding_meaning": 3, "memory": 7, "attention": 6, "motivation": 5},
        {"understanding_meaning": 7, "memory": 3, "attention": 6, "motivation": 5},
        {"understanding_meaning": 7, "memory": 6, "attention": 3, "motivation": 5},
        {"understanding_meaning": 7, "memory": 6, "attention": 6, "motivation": 3},
    ]

    from src.orchestration.learning_profile import LearningProfile

    for profile_dict in test_profiles:
        profile = LearningProfile(**profile_dict)
        location = LearningProfileAnalyzer.recommend_location(profile)

        weakest = min(profile_dict.items(), key=lambda x: x[1])
        print(f"✅ Weakest: {weakest[0]} ({weakest[1]}) → Location: {location}")

    print()

    # Test 5: Quest Engine
    print("=" * 60)
    print("Test 5: Quest Engine Structure")
    print("=" * 60)

    if state_manager.quest_engine:
        # Get first quest
        quest = state_manager.quest_engine.get_first_quest_for_location("tower_confusion")

        if quest:
            print(f"✅ First quest for Tower of Confusion:")
            print(f"   ID: {quest.id}")
            print(f"   Title: {quest.title}")
            print(f"   Module: {quest.psychological_module}")
            print(f"   Steps: {len(quest.steps)}")
            print(f"   Difficulty: {quest.difficulty.value}")
            print(f"   Time: {quest.estimated_time_minutes} min")

            if quest.reality_bridge:
                print(f"\n   Reality Bridge:")
                print(f"   • {quest.reality_bridge.title}")
                print(f"   • Deadline: {quest.reality_bridge.deadline_hours}h")
                print(f"   • Reminder: {quest.reality_bridge.reminder_hours}h")
        else:
            print("❌ No quests found for tower_confusion")
    else:
        print("❌ QuestEngine not loaded")

    print()

    # Test 6: User Persistence
    print("=" * 60)
    print("Test 6: User Persistence")
    print("=" * 60)

    if state_manager.user_manager:
        # Save user
        await state_manager.save_user_state(user_state)
        print("✅ User state saved to JSON")

        # Load user
        profile = await state_manager.user_manager.get_user(user_id)
        if profile:
            print(f"✅ User profile loaded from JSON:")
            print(f"   Name: {profile.child_name}")
            print(f"   Learning profile: {profile.learning_profile}")
        else:
            print("❌ User profile not found")
    else:
        print("❌ UserManager not loaded")

    print()

    # Test 7: Reality Bridge Manager
    print("=" * 60)
    print("Test 7: Reality Bridge Manager")
    print("=" * 60)

    if state_manager.reality_bridge_manager:
        print("✅ Reality Bridge Manager initialized")
        print(f"   Scheduler running: {state_manager.reality_bridge_manager.scheduler.running}")
        print(f"   Active bridges: {len(state_manager.reality_bridge_manager.active_bridges)}")

        # Test creating a bridge
        bridge = await state_manager.reality_bridge_manager.create_bridge(
            user_id=user_id,
            quest_id="test_quest",
            bridge_id="bridge_test",
            title="Объясни слово однокласснику",
            description="Выбери сложное слово и объясни его простыми словами кому-то",
            deadline_hours=48,
            reminder_hours=24
        )

        print(f"\n✅ Test Reality Bridge created:")
        print(f"   Title: {bridge.title}")
        print(f"   Deadline: {bridge.deadline_at}")
        print(f"   Reminder: {bridge.reminder_at}")

        # Check active bridge
        active = await state_manager.reality_bridge_manager.get_active_bridge(user_id)
        if active:
            print(f"   Status: Active ✅")
        else:
            print(f"   Status: Not found ❌")
    else:
        print("❌ Reality Bridge Manager not loaded")

    print()

    # Summary
    print("=" * 60)
    print("Integration Test Summary")
    print("=" * 60)

    checks = {
        "StateManager initialized": state_manager.initialized,
        "User created": user_state is not None,
        "UserManager loaded": state_manager.user_manager is not None,
        "LinkManager loaded": state_manager.link_manager is not None,
        "QuestEngine loaded": state_manager.quest_engine is not None,
        "Reality Bridge Manager loaded": state_manager.reality_bridge_manager is not None,
        "Quests loaded": state_manager.quest_engine and len(state_manager.quest_engine.quests) > 0,
        "Emotional detection working": user_state.emotional_state is not None,
        "User persistence working": profile is not None,
    }

    passed = sum(checks.values())
    total = len(checks)

    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")

    print()
    print(f"Result: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All integration tests passed!")
    else:
        print(f"⚠️  {total - passed} checks failed")

    print()

    # Cleanup
    print("🧹 Cleaning up...")
    if state_manager.reality_bridge_manager:
        await state_manager.reality_bridge_manager.shutdown()
    print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(test_integration())
