# Testing Guide for InnerWorld Edu

## Installation

Before running tests, install all dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- LangChain, LangGraph, OpenAI (for LLM integration)
- Structlog (for logging)
- Python-Telegram-Bot (for bot integration)
- And other required packages

## Environment Setup

Create `.env` file from template:

```bash
cp .env.example .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running Tests

### Test 1: StateManager (LLM Integration)

Tests conversation flow with OpenAI LLM:

```bash
python test_state_manager.py
```

**What it tests:**
- StateManager initialization
- Conversation memory (last 10 messages)
- Natural language responses
- Emotional state detection
- Onboarding flow

**Expected output:**
```
=== InnerWorld Edu StateManager Test ===

Initializing StateManager...
✅ StateManager initialized

=== Starting conversation ===

👦 Ребенок (сообщение 1): Привет, меня зовут Саша
🤖 Бот: Привет, Саша! 😊 ...

   📊 Состояние: onboarding
   💭 Эмоция: interest
   📍 Локация: не выбрана
   💬 Сообщений: 1
```

### Test 2: Helper Classes

Tests all helper classes independently:

```bash
python test_helpers.py
```

**What it tests:**

1. **EmotionalRouter**
   - Emotion detection from keywords
   - Location recommendations
   - Support message generation
   - Emotional volatility tracking
   - Emotional storm detection

2. **LearningProfile**
   - Dimension tracking (understanding, memory, attention, motivation)
   - Profile analysis (weakest/strongest dimensions)
   - Recommendations (locations, modules, difficulty)
   - Progress summaries
   - Teaching strategy suggestions

3. **UserManager**
   - User creation and retrieval (JSON storage)
   - Progress updates (XP, level, quests)
   - Screening metrics updates
   - Statistics generation

4. **LinkManager**
   - Parent link creation
   - Deep link URL generation
   - Link activation by parent
   - Parent profile management
   - Statistics tracking

**Expected output:**
```
=== InnerWorld Edu - Helper Classes Tests ===

TEST 1: Emotional Router
✅ Message: 'Устал, не хочу больше'
   Detected: tiredness (intensity: 0.60)
   Keywords: ['устал', 'не хочу']
...

TEST 2: Learning Profile
Initial profile:
  Understanding: 5/10
  Memory: 5/10
...

TEST 3: User Manager
✅ User created: test_123
   Name: Саша
   Age: 10
...

TEST 4: Link Manager
✅ Link created: {link_id}
   Child: Саша
   Status: pending
...

✅ All tests completed successfully!
```

## Manual Testing

### Test EmotionalRouter manually:

```python
from src.orchestration.emotional_router import EmotionalRouter

router = EmotionalRouter()
reading = router.detect_emotion("Боюсь, что не справлюсь")
print(f"Emotion: {reading.state.value}")  # anxiety
print(f"Location: {router.recommend_location()}")  # forest_calm
```

### Test LearningProfile manually:

```python
from src.orchestration.learning_profile import (
    LearningProfile,
    LearningProfileAnalyzer,
    LearningDimension
)

profile = LearningProfile()
profile.adjust_dimension(LearningDimension.UNDERSTANDING_MEANING, -2, "struggling")

location = LearningProfileAnalyzer.recommend_location(profile)
print(f"Location: {location}")  # tower_confusion
```

### Test UserManager manually:

```python
import asyncio
from src.data.user_manager import UserManager

async def test():
    manager = UserManager()
    user = await manager.create_user("123", child_name="Саша", age=10)
    print(f"Created: {user.user_id}")

    await manager.update_progress("123", xp_gain=50, quest_completed=True)
    updated = await manager.get_user("123")
    print(f"XP: {updated.progress['xp']}")

asyncio.run(test())
```

### Test LinkManager manually:

```python
import asyncio
from src.data.link_manager import LinkManager

async def test():
    manager = LinkManager()

    # Create link
    link = await manager.create_link("child_123", "Саша")
    url = manager.generate_link_url(link.link_id)
    print(f"Link URL: {url}")

    # Activate link
    await manager.activate_link(link.link_id, "parent_456")

    # Check if linked
    is_linked = await manager.is_child_linked("child_123")
    print(f"Linked: {is_linked}")  # True

asyncio.run(test())
```

## Troubleshooting

### ModuleNotFoundError: No module named 'langgraph'

Install dependencies:
```bash
pip install -r requirements.txt
```

### OpenAI API key error

Make sure `.env` file has valid OPENAI_API_KEY:
```bash
cat .env | grep OPENAI_API_KEY
```

### Permission errors on data directories

Create data directories:
```bash
mkdir -p src/data/{user_profiles,parents,links}
touch src/data/{user_profiles,parents,links}/.gitkeep
```

## CI/CD Testing

To run tests in automated pipeline:

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
python test_helpers.py

# Run integration tests (requires OPENAI_API_KEY)
python test_state_manager.py
```

## Next Steps

- [ ] Add pytest for proper test framework
- [ ] Add test coverage reporting
- [ ] Add mock for OpenAI API (avoid costs in CI)
- [ ] Add integration tests for Telegram bot
- [ ] Add performance tests for large user bases
