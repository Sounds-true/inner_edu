#!/usr/bin/env python3
"""
Test QuestEngine for InnerWorld Edu.

Tests:
1. Loading quest from YAML
2. Starting quest
3. Processing step responses
4. Quest completion
5. Rewards and Reality Bridge

Run: python test_quest_engine.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.game.quest_engine import QuestEngine, StepType


async def test_quest_engine():
    """Test QuestEngine with tower quest."""
    print("\n" + "="*60)
    print("InnerWorld Edu - QuestEngine Test")
    print("="*60 + "\n")

    # Initialize engine
    print("Initializing QuestEngine...")
    engine = QuestEngine()
    print("✅ QuestEngine initialized\n")

    # Load quest
    print("Loading quest from YAML...")
    quest_file = Path("src/data/quests/tower_confusion/quest_01_simple_words.yaml")

    if not quest_file.exists():
        print(f"❌ Quest file not found: {quest_file}")
        return

    quest = await engine.load_quest(quest_file)

    if quest:
        print(f"✅ Quest loaded: {quest.title}")
        print(f"   ID: {quest.id}")
        print(f"   Location: {quest.location}")
        print(f"   Module: {quest.psychological_module}")
        print(f"   Difficulty: {quest.difficulty.value}")
        print(f"   Steps: {len(quest.steps)}")
        print(f"   XP Reward: {quest.rewards.experience_points}")
        print()
    else:
        print("❌ Failed to load quest")
        return

    # Start quest
    print("Starting quest for user_123...")
    success, first_step = await engine.start_quest("user_123", quest.id)

    if success:
        print(f"✅ Quest started!")
        print(f"   First step: {first_step.id}")
        print(f"   Type: {first_step.type.value}")
        print(f"   Prompt: {first_step.prompt[:50]}...")
        print()
    else:
        print("❌ Failed to start quest")
        return

    # Simulate step responses
    print("="*60)
    print("SIMULATING QUEST PROGRESSION")
    print("="*60 + "\n")

    test_responses = [
        ("дробь", "Step 1: Choose word"),
        (0, "Step 2: Choose explanation method"),
        ("Это когда целое число делится на части", "Step 3: Explain in own words"),
        ("Пицца, разделённая на кусочки", "Step 4: Real example"),
        (0, "Step 5: Reflection")
    ]

    for i, (response, description) in enumerate(test_responses, 1):
        print(f"\n📝 {description}")
        print(f"   Response: {response}")

        success, next_step, feedback = await engine.process_step_response("user_123", response)

        if success:
            print(f"   ✅ Valid response")

            if feedback:
                print(f"   💬 Feedback: {feedback[:80]}...")

            if next_step:
                print(f"   ➡️  Next step: {next_step.id}")
            else:
                print(f"   🎉 Quest completed!")
                print()
                break
        else:
            print(f"   ❌ Invalid response: {feedback}")
            break

    # Check completion
    progress = engine.get_current_quest_progress("user_123")

    if progress and progress.is_completed():
        print("\n" + "="*60)
        print("QUEST COMPLETED!")
        print("="*60 + "\n")

        print(f"📊 Progress:")
        print(f"   Total score: {progress.total_score}")
        print(f"   Steps completed: {len(progress.step_responses)}")
        print(f"   Duration: {(progress.completed_at - progress.started_at).total_seconds():.1f}s")
        print()

        # Get rewards
        rewards = await engine.get_quest_rewards("user_123")

        if rewards:
            print(f"🎁 Rewards:")
            print(f"   XP: +{rewards.experience_points}")
            print(f"   Learning Profile Changes:")

            for dimension, change in rewards.learning_profile_changes.items():
                print(f"      {dimension}: {change:+d}")

            print(f"   Location Progress:")
            for location, progress in rewards.location_progress.items():
                print(f"      {location}: {progress:+d}")
            print()

        # Get Reality Bridge
        rb = await engine.get_reality_bridge("user_123")

        if rb:
            print(f"🌉 Reality Bridge:")
            print(f"   Title: {rb.title}")
            print(f"   Description: {rb.description[:80]}...")
            print(f"   Deadline: {rb.deadline_hours} hours")
            print(f"   Reminder: {rb.reminder_hours} hours")
            print(f"   Verification: {rb.verification_type}")
            print()

        # Get psychological insights
        print(f"🧠 Psychological Insights:")
        for insight in quest.psychological_insights:
            print(f"   Module: {insight['module']}")
            print(f"   Technique: {insight['technique']}")
            print(f"   Explanation: {insight['explanation'][:80]}...")
            print()

    else:
        print("\n❌ Quest not completed")

    print("="*60)
    print("Test finished!")
    print("="*60)


async def test_load_all_quests():
    """Test loading all quests from directory."""
    print("\n" + "="*60)
    print("Loading all quests...")
    print("="*60 + "\n")

    engine = QuestEngine()
    count = await engine.load_all_quests()

    print(f"✅ Loaded {count} quests\n")

    if count > 0:
        print("Available quests:")
        for quest_id, quest in engine.quests.items():
            print(f"  - {quest_id}: {quest.title} ({quest.location})")


async def main():
    """Run all tests."""
    try:
        await test_quest_engine()
        print("\n")
        await test_load_all_quests()

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
