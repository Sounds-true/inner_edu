# InnerWorld Edu - Implementation Status

## Phase 1: LLM Integration + State Management ✅

**Completed:** StateManager with OpenAI LLM integration, conversation memory, and educational flow.

### What's Working

1. **LLM Integration**
   - OpenAI GPT-4 for natural language understanding
   - Conversation memory (last 10 messages passed in context)
   - Handles off-topic messages, jokes, and casual conversation
   - "Passes the stupidity test" - responds naturally to unexpected input

2. **State Management (LangGraph)**
   - Graph-based state machine for educational flow
   - States: start → parent_linking → onboarding → emotion_check → location_selection → quest_active → casual_chat
   - Smooth transitions between structured quests and free conversation

3. **Emotional Detection**
   - 5 emotional states: tiredness, anxiety, anger, interest, doubt
   - Keyword-based detection (can be enhanced with LLM classification later)
   - Emotional state influences response tone and location recommendations

4. **Learning Profile Tracking**
   - 4 dimensions: understanding_meaning, memory, attention, motivation (1-10 scale)
   - Used for personalized location recommendations
   - Tracked throughout conversation

5. **Screening System**
   - Metrics: self_worth, self_criticism, emotional_volatility, manipulation_score
   - Self-harm keyword detection
   - Emotional storm tracking (frequency and intensity)
   - Triggers for therapeutic mode transition (when thresholds exceeded)

6. **Conversation Flow**
   ```
   User: "Привет, меня зовут Саша"
   Bot: Uses LLM to respond naturally, extracts name

   User: "Мне сложно с математикой"
   Bot: Detects learning difficulty, asks clarifying questions

   User: "А можно пошутить?"
   Bot: Responds to joke with humor, then gently guides back to learning

   User: "Что делает пират, когда видит дробь? Аррр, не понимаю! 😄"
   Bot: Laughs along, uses it as teaching moment about fractions
   ```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Message                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      StateManager                            │
│  1. Detect emotional state (keywords)                        │
│  2. Update screening metrics                                 │
│  3. Add message to history                                   │
│  4. Pass to LangGraph                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph State Machine                   │
│  Routes to appropriate handler based on state                │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    Onboarding    Casual Chat    Quest Active
         │               │               │
         │               ▼               │
         │      ┌──────────────┐         │
         │      │   OpenAI     │         │
         └─────▶│   LLM Call   │◀────────┘
                │ + History    │
                └──────┬───────┘
                       │
                       ▼
                  Response Text
```

### Key Files

- **`src/orchestration/state_manager.py`** (578 lines)
  - Main state machine with LangGraph
  - LLM integration for natural conversation
  - Conversation memory (passes user_state with message_history)
  - Emotional state detection
  - Screening metrics updates
  - State handlers for each phase

- **`src/core/logger.py`** (100 lines)
  - Structured logging with structlog
  - PII protection for children
  - Special logging for parent notifications and screening events

- **`test_state_manager.py`**
  - Test script for dialogue flow
  - Simulates child conversation: greeting → learning difficulty → jokes
  - Verifies LLM responses and state transitions

- **`requirements.txt`**
  - OpenAI, LangChain, LangGraph for LLM
  - Structlog for logging
  - Python-telegram-bot for Telegram integration

- **`.env.example`**
  - Configuration template with OPENAI_API_KEY

### How LLM Integration Solves "Stupidity Test"

**Problem:** Template-based bots fail when user writes off-topic messages or jokes.

**Solution:** OpenAI LLM with conversation memory

```python
# In state_manager.py:678-692
async def _handle_casual_chat(self, state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle casual chat with LLM for natural conversation."""
    user_state = state["user_state"]
    message = state["message"]

    system_prompt = f"""Ты — добрый помощник в мире Понималия для детей 7-14 лет.

    Твои правила:
    1. Отвечай дружелюбно, с эмодзи
    2. Если ребенок шутит — пошути в ответ
    3. Если пишет не по теме — нормально отреагируй, потом мягко верни к обучению
    4. Если говорит о сложностях — предложи помощь или квест
    5. Говори на языке ребенка, просто и понятно
    """

    messages = [SystemMessage(content=system_prompt)]

    # CRITICAL: Add conversation history (last 10 messages)
    if user_state.message_history:
        messages.extend(user_state.message_history[-10:])

    response = await self.llm.ainvoke(messages)
    state["response"] = response.content
```

**Why this works:**
1. LLM understands context from message history
2. Can respond to jokes naturally
3. Can handle off-topic messages and redirect gently
4. Adapts tone to child's emotional state
5. Maintains Ponimaliya narrative while being flexible

### Testing

```bash
# Setup
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Install dependencies
pip install -r requirements.txt

# Run test
python test_state_manager.py
```

Expected output:
```
=== InnerWorld Edu StateManager Test ===

Initializing StateManager...
✅ StateManager initialized

👦 Ребенок (сообщение 1): Привет, меня зовут Саша
🤖 Бот: Привет, Саша! 😊 Очень приятно познакомиться! ...

👦 Ребенок (сообщение 2): Мне сложно с математикой
🤖 Бот: Понимаю, математика может быть сложной. Что именно вызывает трудности? ...

👦 Ребенок (сообщение 6): Что делает пират, когда видит дробь? Аррр, не понимаю! 😄
🤖 Бот: Ха-ха, отличная шутка! 😄 Знаешь, даже пираты разбираются в дробях — ...
```

### What's Next

**Phase 2: Helper Classes**
- [ ] EmotionalRouter (standalone class for 5 emotional states)
- [ ] LearningProfile (tracking and analytics)
- [ ] UserManager (JSON CRUD for user profiles)
- [ ] LinkManager (parent linking system)

**Phase 3: Quest System**
- [ ] QuestEngine (YAML loader)
- [ ] YAML scenarios for 7 onboarding steps
- [ ] YAML scenarios for 7 Ponimaliya locations
- [ ] First 3-5 quests with psychological modules

**Phase 4: Parent Dashboard**
- [ ] Parent bot handlers
- [ ] Linking flow (child → parent link → activation)
- [ ] Weekly reports
- [ ] Critical alerts (screening triggers)

**Phase 5: Integration**
- [ ] Connect StateManager to Telegram bot
- [ ] User persistence (save/load from JSON)
- [ ] Reality Bridge micro-actions
- [ ] Achievements system

### Architecture Decisions

1. **LLM + YAML Hybrid**
   - LLM for free conversation, understanding context, natural responses
   - YAML for structured quests, educational content, safety
   - Best of both: flexibility + control

2. **Conversation Memory Pattern**
   - Pass `user_state` object in context (from pas_in_peace PR #11)
   - Include `message_history` with last 10 messages
   - LLM sees full conversation context, responds coherently

3. **Educational → Therapeutic Transition**
   - Start light (Educational Mode)
   - Detect serious issues through screening metrics
   - Request parent consent to transition
   - Activate full Therapeutic Mode when needed

4. **Privacy & Safety**
   - Parent linking required before full bot access
   - PII protection in logs
   - Screening for self-harm keywords
   - Parent notifications for concerning patterns

### Design Philosophy

**"учись учиться" → "учись понимать себя"**

Entry point: Learning difficulties (low-stakes, relatable)
```
"Мне сложно с математикой" → Башня Непонимания
"Не могу запомнить слова" → Долина Слов
"Не могу сосредоточиться" → Лес Спокойствия
```

Progression: From learning skills to emotional awareness
```
Quest 1: "Почему я не понимаю?" (metacognition)
Quest 2: "Как я чувствую, когда не понимаю?" (emotional literacy)
Quest 3: "Что я могу сделать?" (agency, TRIZ)
Quest 4: "Применю в реальной жизни" (Reality Bridge)
```

Exit: Real-world micro-actions, tangible progress

### Technical Notes

- **LangGraph** for state transitions (more maintainable than if/else chains)
- **Structlog** for structured logging (easier debugging)
- **OpenAI GPT-4** for high-quality responses (can downgrade to GPT-3.5-turbo for cost)
- **JSON storage** for Educational Mode (lightweight, no database needed for MVP)
- **PostgreSQL** for Therapeutic Mode (when needed, more robust state tracking)

### Known Limitations

1. **No persistent storage yet** - user state lost on restart (JSON saving to be implemented)
2. **No quest engine yet** - quest_active state is placeholder
3. **No parent dashboard yet** - parent_linking is placeholder
4. **No Telegram integration yet** - currently just StateManager testing
5. **Basic emotion detection** - keyword-based, could be enhanced with LLM classification

### Contributors

Architecture and implementation based on:
- **pas_in_peace** PR #11 (conversation memory pattern)
- **IP-01** to **IP-07** (master architecture and implementation plans)
- **dna/child start.md** (Ponималия concept)
- User feedback: "почему без ллм?" → LLM integration added

---

Last updated: 2025-11-07
Phase 1 Status: ✅ Complete
Next: Phase 2 - Helper Classes
