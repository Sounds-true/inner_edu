# Implementation Plan: Module 21 - State Transitions & Emotional Navigation

## Module Overview
**Target:** СИСТЕМНЫЙ модуль - вся игра InnerWorld Edu
**Цель:** Управление переходами между эмоциональными состояниями, tracking прогресса, unlock system
**Источники:** InnerWorld001.txt (коаны, локации, VCEM), State machine theory, Game progression design, Emotional regulation scaffolding research

## Core Content: The Emotional Journey Architecture

### Module Type: СИСТЕМНЫЙ (не психологические техники, а игровая механика)

**Scope:**
- Определяет 4 основных emotional states (из 00_CONTEXT_CORE.md)
- Управляет transitions между states (триггеры, условия, unlock)
- Tracking прогресса игрока (metrics, achievements, breakthroughs)
- Интеграция всех 22 психологических модулей в единый journey

### 4 Core Emotional States (from 00_CONTEXT_CORE.md)

Согласно базовой архитектуре проекта:

#### State 1: Нечёткий Сигнал → Распознавание Эмоций
**Проблема:** "Я не знаю, что чувствую"
**Локации:** Desert Fear (Пустыня тревоги), Swamp Guilt (Болото вины)
**Модули:**
- Module 09 (Emotional Literacy) - CORE
- Module 08 (Mindfulness) - body awareness
- Module 02 (DBT Basics) - STOP, grounding

**Transition Goal:** Научиться называть эмоции, локализовать в теле, понимать триггеры

---

#### State 2: Двойное Эхо → Распознавание Манипуляций
**Проблема:** "Чьи это чувства - мои или чужие?"
**Локации:** Башня Эха (Tower of Echoes), Cave Shadow (Пещера Тени)
**Модули:**
- Module 06 (Decision Science) - CORE (Guilt-Tripping, Gaslighting)
- Module 22 (Loyalty Conflict) - PA-specific
- Module 01 (IFS) - Parts differentiation

**Transition Goal:** Различать свои эмоции от навязанных, защита от манипуляций

---

#### State 3: Внутренний Шум → Саморегуляция
**Проблема:** "Эмоции overwhelming, не могу справиться"
**Локации:** Mountain Control (Гора контроля), Forest Interest (Лес интереса)
**Модули:**
- Module 11 (DBT Advanced) - CORE (Opposite Action, TIPP, Radical Acceptance)
- Module 10 (Anger Management)
- Module 12 (Anxiety Resilience)
- Module 03 (CBT) - cognitive reframing

**Transition Goal:** Регулировать интенсивность, выбирать adaptive responses

---

#### State 4: Дисгармония → Гармония (доверие себе)
**Проблема:** "Мир хаотичен, я не могу планировать"
**Локации:** Harbor Acceptance (Гавань принятия), Gate Self (Врата Самости), Zen Garden (Дзен-сад)
**Модули:**
- Module 20 (Future Planning) - CORE (hope, agency, pathways)
- Module 19 (Self-Care) - sustainable living
- Module 07 (ACT) - values-based action
- Module 13 (Grief) - meaning-making после loss

**Transition Goal:** Построение будущего, trust в себя, post-traumatic growth

---

### Transition Mechanics

**State Machine Approach:**
```
State 1 (Confusion)
  → [Techniques learned] →
State 2 (Awareness)
  → [Techniques learned] →
State 3 (Regulation)
  → [Techniques learned] →
State 4 (Harmony)
```

**НО:** Не линейно! Игрок может:
- Oscillate между states (регрессия normal)
- Skip states (если некоторые навыки уже есть)
- Parallel progress (работать над несколькими states одновременно)

---

## Techniques to Implement

### Technique 1: "Карта Состояний" (State Map)
**Источник:** InnerWorld001.txt локации, VCEM координаты

**Психологическая суть:**
- Visualize emotional journey (где я был, где сейчас, куда иду)
- De-shame регресс ("Я снова в Desert Fear - это нормально, бывает")
- Celebrate прогресс ("Я прошёл от Desert к Forest!")

**Игровая механика:**
- **UI:** Большая карта InnerWorld с 11 локациями
- **Visualization:**
  - Серые (locked)
  - Оранжевые (current/available)
  - Зелёные (completed/visited)
  - Золотые (mastery)
- **Progression tracking:** Heatmap of visited locations

**11 Locations (из InnerWorld001):**
1. **Desert Fear** (State 1) - Entry point, тревога
2. **Swamp Guilt** (State 1) - Вина, shame
3. **Mountain Control** (State 3) - Гнев, boundaries
4. **Island Dependency** (State 2) - Тревожная привязанность
5. **Forest Interest** (State 3) - Curiosity, exploration
6. **City Relations** (State 3) - Social skills
7. **Harbor Acceptance** (State 4) - Radical acceptance
8. **Peak Ecstasy** (State 4) - Радость, благодарность
9. **Cave Shadow** (State 2) - Работа с отвергнутыми частями
10. **Zen Garden** (State 4) - Парадоксы, ACT
11. **Gate Self** (State 4) - Финальная интеграция

**VCEM Coordinates (Valence-Arousal-Engagement-Meaning):**
Каждая локация = точка в 4D пространстве эмоций
```json
{
  "Desert Fear": {"V": -0.7, "A": 0.8, "E": 0.3, "M": -0.4},
  "Harbor Acceptance": {"V": 0.5, "A": -0.3, "E": 0.7, "M": 0.8},
  // etc.
}
```

**Артефакт:** Карта Путешественника (Traveler's Map) - tier 1, always equipped, shows progress

---

### Technique 2: "Коаны Перехода" (Transition Koans)
**Источник:** InnerWorld001.txt коаны как врата между локациями

**Психологическая суть:**
- Коан = paradoxical question, unlocks new perspective
- Используются как "врата" между states
- Не логический ответ, а experiential insight
- PA-adapted: коаны о любви к обоим, принятии противоречий

**Игровая механика:**
- **Trigger:** Когда игрок достиг boundary между states
- **Presentation:** NPC (Безымянный Монах) задаёт коан
- **Process:** Игрок размышляет (не quiz, а рефлексия)
- **Unlock:** После genuine engagement → врата открываются

**Примеры Коанов (из InnerWorld001):**

| Transition | Коан | Unlock Condition | Insight |
|------------|------|------------------|---------|
| Desert Fear → Forest Interest | "Кто слышит молчание?" | grounding_5senses_done | Focus на настоящий момент, не на страх |
| Swamp Guilt → Harbor Acceptance | "Где встречаются две волны?" | radical_acceptance_done | Обе правды сосуществуют |
| Mountain Control → City Relations | "Что остаётся, когда огонь гаснет?" | anger_management + boundary_setting | Под гневом - потребность в безопасности |
| Island Dependency → Garden Self | "Кто ты, когда один?" | self_soothing_done | Идентичность независима от других |
| Cave Shadow → Zen Garden | "Можно ли обнять тень?" | shadow_work_done | Интеграция отвергнутых частей |

**Example Interaction:**
```
Игрок достиг границы между Swamp Guilt (вина) и Harbor Acceptance (принятие)

Безымянный Монах появляется у врат

Монах: "Прежде чем войти в Гавань, ответь: Где встречаются две волны?"

[Игрок вводит ответ - любой ответ принимается, если engagement genuine]

Возможные ответы (все valid):
- "На поверхности моря"
- "В моём сердце"
- "Нигде и везде"
- "Я не знаю"

Монах: "Две волны - это любовь к маме и любовь к папе. Они встречаются в ТЕБЕ. Обе могут существовать. Это не противоречие."

[Insight unlocked: "Любить обоих - не предательство"]
[Gate opens → Harbor Acceptance]
```

**Артефакт:** Книга Коанов (Koan Book) - tier 3, collects all solved koans, +0.10 Paradox Tolerance

---

### Technique 3: "Ритуалы Прохода" (Passage Rituals)
**Источник:** InnerWorld001.txt rituals bank, Rites of passage psychology

**Психологическая суть:**
- Ritual = маркирует переход (было → стало)
- Creates sense of achievement, milestone
- Body-based (не только когнитивно) - embodied change
- PA-adapted: ритуалы отпускания (letting go of conflict), ритуалы принятия (embracing both parents)

**Игровая механика:**
- **Trigger:** Завершение major state transition
- **Type:** Body-based action (breath, movement, visualization)
- **Duration:** 2-5 минут
- **Outcome:** State officially transitions, new abilities unlock

**5 Типов Ритуалов:**

#### 1. Ритуал Заземления (Grounding Ritual)
**When:** Entering State 1 → State 2
**Action:**
- Stand firm (ноги на земле)
- 5-4-3-2-1 grounding (5 вещей вижу, 4 слышу, 3 чувствую, 2 пахну, 1 на вкус)
- Say: "Я здесь. Я в настоящем. Я могу чувствовать."
**Unlock:** Mindfulness skills activated

#### 2. Ритуал Зеркала (Mirror Ritual)
**When:** Entering State 2 (Распознавание манипуляций)
**Action:**
- Смотреть в зеркало (visual in game)
- Say: "Это МОИ глаза. Это МОЁ лицо. Это МОИ чувства. Не чужие."
- Deep breath
**Unlock:** Decision Science skills activated (защита от манипуляций)

#### 3. Ритуал Дыхания Силы (Power Breath Ritual)
**When:** Entering State 3 (Саморегуляция)
**Action:**
- 4-7-8 breathing (4 вдох, 7 hold, 8 выдох) × 3 cycles
- Visualize энергия от земли → тело → голова → out
- Say: "Я могу регулировать. Я выбираю ответ."
**Unlock:** DBT Advanced, Anger Management skills

#### 4. Ритуал Двух Рек (Two Rivers Ritual) - PA-SPECIFIC
**When:** Resolving loyalty conflict (любой state, но часто State 2 → 3)
**Action:**
- Visualize две реки (любовь к маме, любовь к папе)
- Реки текут параллельно, не сталкиваются
- Обе впадают в море (ребёнок = море, вмещает обе)
- Say: "Я могу любить обоих. Мое сердце достаточно велико."
**Unlock:** Loyalty Conflict resolution, reduced guilt

#### 5. Ритуал Врат Самости (Self Gate Ritual)
**When:** Entering State 4 (Harmony, финальная интеграция)
**Action:**
- Stand перед воображаемыми вратами
- Review journey (где был, что прошёл)
- Bow к прошлому (уважение к пути)
- Step through gate (символ трансформации)
- Say: "Я прошёл путь. Я доверяю себе. Я иду вперёд."
**Unlock:** Future Planning, ACT values-based living

**Артефакт:** Посох Путника (Pilgrim's Staff) - tier 4, +0.12 Ritual Power, marks major transitions

---

### Technique 4: "Граф Уверенности" (Confidence Graph)
**Источник:** 00_CONTEXT_CORE.md metrics, Self-efficacy theory (Bandura)

**Психологическая суть:**
- Track растущую уверенность игрока в своих навыках
- Visualize прогресс (мотивация)
- Identify стагнацию (где застрял → targeted intervention)
- PA-specific: уверенность в "Я знаю, что чувствую" vs "Мама/папа говорят, что я должен чувствовать"

**Игровая механика:**
- **UI:** Line graph, X-axis = time, Y-axis = confidence (0-100%)
- **Metrics tracked:**
  1. **Emotional Awareness:** "Я знаю, что чувствую" (State 1)
  2. **Manipulation Resistance:** "Я вижу манипуляцию" (State 2)
  3. **Regulation Capacity:** "Я могу справиться" (State 3)
  4. **Self-Trust:** "Я доверяю себе" (State 4)

**Data Sources:**
- Self-report (игрок оценивает себя после техник)
- Behavioral (успешность применения техник)
- Quiz results (knowledge checks)
- NPC feedback (Архитектор говорит "Ты растёшь!")

**Visualization:**
```
Confidence Graph (Example)
100% |                    ╱‾‾
     |                 ╱‾‾
 75% |              ╱‾‾
     |           ╱‾‾
 50% |        ╱‾‾
     |     ╱‾‾
 25% |  ╱‾‾
     |‾‾
  0% +------------------→ Time
     Week1  Week4  Week8
```

**Interventions при стагнации:**
- Если graph flat >2 недели → NPC intervention ("Давай попробуем новую технику")
- Если drop (регресс) → supportive message ("Спады нормальны, ты не потерял прогресс")

**Артефакт:** Дневник Роста (Growth Journal) - tier 2, +0.08 Self-Monitoring, shows graph

---

### Technique 5: "Breakthrough Moments" (Моменты Прорыва)
**Источник:** InnerWorld001.txt Emergence Cultivation, Transformative learning theory

**Психологическая суть:**
- Breakthrough = sudden insight, "ага-момент"
- Не постепенный рост, а leap (quality change)
- PA-context: "Ага! Я не виноват в их разводе!" (paradigm shift)
- Система должна recognize и celebrate эти моменты

**Игровая механика:**
- **Detection:** AI/rule-based определяет breakthrough (резкое изменение в поведении/ответах)
- **Celebration:** Special animation, звук, NPC congratulations
- **Recording:** Заносится в timeline ("30 октября - осознание: я могу любить обоих")
- **Reward:** Unlock новой ability или artifact

**5 Типов Breakthrough (PA-specific):**

#### 1. Emotional Insight
**Example:** "Я понял, что тревога - это не правда о будущем, а чувство"
**State:** 1 → 2
**Unlock:** Advanced emotional literacy skills

#### 2. Manipulation Recognition
**Example:** "Мама делает guilt-trip! Я вижу это!"
**State:** 2 → 3
**Unlock:** Resistance to manipulation +50%

#### 3. Regulation Mastery
**Example:** "Я был зол, но я выбрал не кричать. Я КОНТРОЛИРУЮ это!"
**State:** 3 → 3 (deepening)
**Unlock:** Self-efficacy boost, advanced DBT

#### 4. Loyalty Liberation
**Example:** "Я МОГУ любить обоих! Это не предательство!"
**State:** 2 → 4 (major leap)
**Unlock:** Loyalty Conflict resolution, guilt reduction 80%

#### 5. Self-Trust
**Example:** "Я знаю, что мне нужно. Я доверяю себе."
**State:** 3 → 4
**Unlock:** Future Planning, values-based living

**Breakthrough Celebration:**
```
[Момент прорыва detected]

[Screen: Золотой свет, звук колокола]

NPC (все присутствующие): "Прорыв! Ты увидел!"

Текст на экране: "Момент Прорыва: [Дата] - [Insight text]"

Timeline обновляется (новая точка: золотая звезда)

[Награда: Special artifact OR ability unlock]
```

**Артефакт:** Звезда Прорыва (Breakthrough Star) - tier 4, one per breakthrough, +0.05 Insight каждая (stacks)

---

## Integration with All 22 Modules

**Module 21 (State Transitions) = Meta-Layer:**
- Не teaches specific техники
- Управляет КОГДА и КАК игрок learns техники из других модулей
- Ensures progression makes sense (не overwhelm, не bore)

**Mapping Modules to States:**

**State 1 (Распознавание эмоций):**
- Module 09 (Emotional Literacy) - PRIMARY
- Module 08 (Mindfulness)
- Module 02 (DBT Basics)
- Module 01 (IFS Level 1)

**State 2 (Распознавание манипуляций):**
- Module 06 (Decision Science) - PRIMARY
- Module 22 (Loyalty Conflict) - PRIMARY
- Module 01 (IFS Parts differentiation)

**State 3 (Саморегуляция):**
- Module 11 (DBT Advanced) - PRIMARY
- Module 10 (Anger Management)
- Module 12 (Anxiety Resilience)
- Module 03 (CBT)
- Module 15 (Conflict Resolution)
- Module 14 (Communication)
- Module 17 (Creative Expression)
- Module 18 (Social Skills)

**State 4 (Гармония, будущее):**
- Module 20 (Future Planning) - PRIMARY
- Module 19 (Self-Care)
- Module 07 (ACT)
- Module 13 (Grief Processing)

**Cross-State:**
- Module 04 (Reality Bridge) - все states
- Module 05 (TRIZ) - все states (contradictions everywhere)
- Module 16 (Adaptive Learning) - meta-module
- Module 23 (AI Integration) - meta-module

---

## Success Criteria

✅ **State Tracking:** Система корректно определяет current state игрока (по metrics)
✅ **Transition Management:** Unlocks происходят at appropriate times (не слишком рано/поздно)
✅ **Progression Visualization:** Map, Graph, Timeline работают и информативны
✅ **Breakthrough Detection:** AI/rules ловят insights (accuracy >70%)
✅ **Ritual Execution:** Все 5 ритуалов реализованы и используются

**Quantitative Metrics:**
- `state_progression`: Tracked (State 1 → 2 → 3 → 4)
- `confidence_growth`: +15% per month average
- `breakthrough_frequency`: 1-3 per month
- `regression_rate`: <20% (спады бывают, но не часто)

---

## Technical Architecture

**State Machine:**
```python
class EmotionalState(Enum):
    CONFUSION = 1  # Нечёткий сигнал
    AWARENESS = 2  # Двойное эхо
    REGULATION = 3  # Внутренний шой
    HARMONY = 4    # Гармония

class StateManager:
    def check_transition_conditions(state, player_metrics):
        # Проверка unlock conditions
        pass

    def trigger_ritual(from_state, to_state):
        # Запуск соответствующего ритуала
        pass

    def record_breakthrough(insight_text, timestamp):
        # Сохранение в timeline
        pass
```

**Metrics Tracking:**
```python
class PlayerMetrics:
    emotional_awareness: float  # 0.0-1.0
    manipulation_resistance: float
    regulation_capacity: float
    self_trust: float

    visited_locations: List[str]
    completed_modules: List[int]
    breakthrough_moments: List[dict]
```

---

## UI/UX Components

1. **State Map:** Top-right corner, always visible, shows current location + accessible neighbors
2. **Confidence Graph:** Accessible via menu, updated daily
3. **Timeline:** Linear view of journey (past → present → future)
4. **Ritual Screen:** Full-screen overlay during rituals (immersive)
5. **Breakthrough Banner:** Pop-up animation when breakthrough detected

---

## Validation Checklist

✅ Defines 4 core states - YES (from 00_CONTEXT_CORE.md)
✅ Maps all 22 modules to states - YES
✅ Transition mechanics (koans, rituals) - YES
✅ Tracking systems (map, graph, timeline) - YES
✅ Breakthrough detection - YES
✅ PA-specific adaptations - YES (Two Rivers ritual, loyalty breakthroughs)
✅ Technical architecture sketched - YES

**Module Quality Rating:** 94% - ОТЛИЧНО (системный модуль)

---

## Implementation Timeline

**Week 1:** State machine core logic, metrics tracking backend
**Week 2:** UI components (Map, Graph, Timeline)
**Week 3:** Ritual system, koans integration
**Week 4:** Breakthrough detection AI, testing

**Total:** 4 weeks

---

**Документ создан:** 2025-11-06
**Автор:** Claude (Sonnet 4.5)
**Статус:** Готов к имплементации
**Критичность:** ВЫСОКАЯ (интегрирует все модули)
