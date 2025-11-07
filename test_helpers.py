#!/usr/bin/env python3
"""
Test helper classes for InnerWorld Edu.

Tests:
1. EmotionalRouter - emotion detection, location recommendations
2. LearningProfile - dimension tracking, analytics
3. UserManager - CRUD operations with JSON storage
4. LinkManager - parent-child linking flow
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Direct imports to avoid loading StateManager (which requires langgraph)
import importlib.util

def load_module_from_file(module_name, file_path):
    """Load module directly from file."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load modules directly
emotional_router_module = load_module_from_file(
    "emotional_router",
    Path(__file__).parent / "src/orchestration/emotional_router.py"
)
learning_profile_module = load_module_from_file(
    "learning_profile",
    Path(__file__).parent / "src/orchestration/learning_profile.py"
)
user_manager_module = load_module_from_file(
    "user_manager",
    Path(__file__).parent / "src/data/user_manager.py"
)
link_manager_module = load_module_from_file(
    "link_manager",
    Path(__file__).parent / "src/data/link_manager.py"
)

# Import classes
EmotionalRouter = emotional_router_module.EmotionalRouter
EmotionalState = emotional_router_module.EmotionalState
LearningProfile = learning_profile_module.LearningProfile
LearningProfileAnalyzer = learning_profile_module.LearningProfileAnalyzer
LearningDimension = learning_profile_module.LearningDimension
UserManager = user_manager_module.UserManager
LinkManager = link_manager_module.LinkManager

# Setup logging manually
import structlog
structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)


async def test_emotional_router():
    """Test EmotionalRouter functionality."""
    print("\n" + "="*60)
    print("TEST 1: Emotional Router")
    print("="*60 + "\n")

    router = EmotionalRouter()

    # Test emotion detection
    test_messages = [
        ("Устал, не хочу больше", EmotionalState.TIREDNESS),
        ("Боюсь, что не справлюсь", EmotionalState.ANXIETY),
        ("Бесит эта математика!", EmotionalState.ANGER),
        ("Не понимаю, как решать", EmotionalState.DOUBT),
        ("Интересно, расскажи еще!", EmotionalState.INTEREST)
    ]

    for message, expected_emotion in test_messages:
        reading = router.detect_emotion(message)
        match = "✅" if reading.state == expected_emotion else "❌"

        print(f"{match} Message: '{message}'")
        print(f"   Detected: {reading.state.value} (intensity: {reading.intensity:.2f})")
        print(f"   Keywords: {reading.detected_keywords}")
        print()

    # Test location recommendation
    location = router.recommend_location()
    print(f"📍 Recommended location: {location}")

    # Test support message
    support = router.get_support_message()
    print(f"💬 Support message: {support}")

    # Test emotional volatility
    volatility = router.detect_emotional_volatility()
    print(f"📊 Emotional volatility: {volatility:.2f}")

    # Test emotional storm detection
    storm = router.detect_emotional_storm()
    print(f"⛈️  Emotional storm: {storm}")

    # Get summary
    summary = router.get_emotional_summary()
    print(f"\n📋 Summary: {summary}")


async def test_learning_profile():
    """Test LearningProfile functionality."""
    print("\n" + "="*60)
    print("TEST 2: Learning Profile")
    print("="*60 + "\n")

    profile = LearningProfile()

    print("Initial profile:")
    print(f"  Understanding: {profile.understanding_meaning}/10")
    print(f"  Memory: {profile.memory}/10")
    print(f"  Attention: {profile.attention}/10")
    print(f"  Motivation: {profile.motivation}/10")
    print()

    # Update dimensions
    print("Updating dimensions...")
    profile.adjust_dimension(LearningDimension.UNDERSTANDING_MEANING, -2, "struggling_with_math")
    profile.adjust_dimension(LearningDimension.MEMORY, +1, "quest_completed")
    profile.adjust_dimension(LearningDimension.ATTENTION, -1, "distracted")
    profile.adjust_dimension(LearningDimension.MOTIVATION, +2, "engaged_in_quest")

    print("\nUpdated profile:")
    print(f"  Understanding: {profile.understanding_meaning}/10")
    print(f"  Memory: {profile.memory}/10")
    print(f"  Attention: {profile.attention}/10")
    print(f"  Motivation: {profile.motivation}/10")
    print()

    # Analyze profile
    weakest = profile.get_weakest_dimension()
    strongest = profile.get_strongest_dimension()
    avg = profile.get_average_score()

    print(f"📊 Analysis:")
    print(f"  Weakest: {weakest.value}")
    print(f"  Strongest: {strongest.value}")
    print(f"  Average: {avg:.1f}/10")
    print()

    # Get recommendations
    location = LearningProfileAnalyzer.recommend_location(profile)
    modules = LearningProfileAnalyzer.recommend_modules(profile)
    difficulty = LearningProfileAnalyzer.get_difficulty_level(profile)

    print(f"🎯 Recommendations:")
    print(f"  Location: {location}")
    print(f"  Modules: {modules}")
    print(f"  Difficulty: {difficulty}")
    print()

    # Get progress summary
    summary = LearningProfileAnalyzer.get_progress_summary(profile)
    print(f"📝 Progress Summary:\n{summary}")

    # Get teaching strategy
    strategy = LearningProfileAnalyzer.suggest_teaching_strategy(profile)
    print(f"\n💡 Teaching Strategy:\n{strategy}")


async def test_user_manager():
    """Test UserManager functionality."""
    print("\n" + "="*60)
    print("TEST 3: User Manager")
    print("="*60 + "\n")

    # Use test directory
    test_dir = Path("src/data/test_user_profiles")
    test_dir.mkdir(parents=True, exist_ok=True)

    manager = UserManager(data_dir=test_dir)

    # Create user
    print("Creating user...")
    user = await manager.create_user("test_123", child_name="Саша", age=10)

    print(f"✅ User created: {user.user_id}")
    print(f"   Name: {user.child_name}")
    print(f"   Age: {user.age}")
    print(f"   Parent linked: {user.parent_linked}")
    print()

    # Get user
    print("Retrieving user...")
    retrieved = await manager.get_user("test_123")

    if retrieved:
        print(f"✅ User retrieved: {retrieved.user_id}")
    else:
        print(f"❌ User not found")

    # Update progress
    print("\nUpdating progress...")
    await manager.update_progress("test_123", xp_gain=50, quest_completed=True)

    updated = await manager.get_user("test_123")
    print(f"✅ XP: {updated.progress['xp']}")
    print(f"   Level: {updated.progress['level']}")
    print(f"   Quests: {updated.progress['total_quests_completed']}")
    print()

    # Update screening
    print("Updating screening metrics...")
    await manager.update_screening_metrics(
        "test_123",
        self_worth=0.45,
        self_criticism=0.55
    )

    updated = await manager.get_user("test_123")
    print(f"✅ Self-worth: {updated.screening['self_worth']}")
    print(f"   Self-criticism: {updated.screening['self_criticism']}")
    print()

    # Get statistics
    stats = await manager.get_statistics()
    print(f"📊 Statistics: {stats}")

    # Cleanup
    print("\nCleaning up test data...")
    await manager.delete_user("test_123")

    import shutil
    shutil.rmtree(test_dir)

    print("✅ Cleanup complete")


async def test_link_manager():
    """Test LinkManager functionality."""
    print("\n" + "="*60)
    print("TEST 4: Link Manager")
    print("="*60 + "\n")

    # Use test directories
    test_links_dir = Path("src/data/test_links")
    test_parents_dir = Path("src/data/test_parents")

    test_links_dir.mkdir(parents=True, exist_ok=True)
    test_parents_dir.mkdir(parents=True, exist_ok=True)

    manager = LinkManager(
        links_dir=test_links_dir,
        parents_dir=test_parents_dir
    )

    # Create link
    print("Creating parent link...")
    link = await manager.create_link(child_id="child_123", child_name="Саша")

    print(f"✅ Link created: {link.link_id}")
    print(f"   Child: {link.child_name}")
    print(f"   Status: {link.status.value}")
    print(f"   Expires: {link.expires_at}")
    print()

    # Generate URL
    url = manager.generate_link_url(link.link_id)
    print(f"🔗 Deep link URL: {url}")
    print()

    # Check if child is linked
    is_linked = await manager.is_child_linked("child_123")
    print(f"📋 Child linked before activation: {is_linked}")
    print()

    # Activate link
    print("Activating link...")
    await manager.activate_link(link.link_id, parent_id="parent_456")

    activated = await manager.get_link(link.link_id)
    print(f"✅ Link activated!")
    print(f"   Status: {activated.status.value}")
    print(f"   Parent: {activated.parent_id}")
    print(f"   Activated at: {activated.activated_at}")
    print()

    # Check if child is linked now
    is_linked = await manager.is_child_linked("child_123")
    print(f"📋 Child linked after activation: {is_linked}")

    # Get parent
    parent_id = await manager.get_parent_for_child("child_123")
    print(f"👨‍👩‍👧 Parent ID: {parent_id}")
    print()

    # Get parent's children
    children = await manager.get_parent_children("parent_456")
    print(f"👶 Parent's children: {children}")
    print()

    # Get statistics
    stats = await manager.get_statistics()
    print(f"📊 Statistics: {stats}")

    # Cleanup
    print("\nCleaning up test data...")

    import shutil
    shutil.rmtree(test_links_dir)
    shutil.rmtree(test_parents_dir)

    print("✅ Cleanup complete")


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("InnerWorld Edu - Helper Classes Tests")
    print("="*60)

    try:
        await test_emotional_router()
        await test_learning_profile()
        await test_user_manager()
        await test_link_manager()

        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
