# Implementation Plan: Module 20 - Future Planning

## Module Overview
**Target:** Дети 7-14 лет, готовые двигаться от обработки прошлого к построению будущего
**Цель:** Развить hope (надежду), научить goal-setting, построить pathways к целям, активировать agency
**Источники:** C.R. Snyder Hope Theory (pathways + agency), Goal-setting research (positive psychology), Solution-Focused Brief Therapy, Hope Therapy (Lopez), Future-focused therapeutic approaches

## Core Content: Hope as Cognitive-Motivational System

### Snyder's Hope Theory (1991-2002)

**Definition of Hope:**
> "Hope is the perceived capability to derive pathways to desired goals, and motivate oneself via agency thinking to use those pathways."

**Two Core Components:**

#### 1. Pathways Thinking (WayPower)
- **Ability to develop numerous and flexible pathways toward goals**
- Identify barriers and strategies to overcome them
- Link sequential actions from present to future goal
- "I can find a way"

#### 2. Agency Thinking (WillPower)
- **Goal-directed energy or determination to succeed**
- Mental energy to articulate goal, commit, persevere
- "I can do this"

**Interactive Process:**
- Pathways and Agency work together dynamically
- Goals provide targets of mental action sequences
- Higher hope → better outcomes (academics, athletics, health, adjustment, therapy)

**PA Context:**
- PA children often have LOW hope (future feels controlled by parents)
- "Nothing I do matters" (low agency)
- "There's no way to fix this" (low pathways)
- **Goal:** Restore hope by building both pathways and agency

### Goal-Setting Research (Positive Psychology)

**Benefits of Goal-Setting:**
- Linked with higher motivation, self-esteem, self-confidence, autonomy
- Strong connection between goal-setting and success
- Goals = first step towards planning for future
- Fundamental role in skill development across life facets

**Therapeutic Goal-Setting:**
- Collaborative goal setting, client participation, continuous feedback → better outcomes
- May have favourable effects on motivation and treatment outcomes
- Goals make therapy more structured and goal-oriented → more efficient/effective

**Key Principles:**
- Goals should be: Specific, Measurable, Achievable, Relevant, Time-bound (SMART)
- BUT for children: Focus on meaningful, intrinsic, value-based goals (not just SMART)

### Solution-Focused Brief Therapy (SFBT) - Future-Focused

**Core Principle:**
- Concentrate on desired future (not problem-focused past)
- Positive psychological impact, reduces helplessness
- Enhances overall well-being

**Miracle Question:**
> "If a miracle happened tonight while you were sleeping, and your problem was solved, what would be different tomorrow?"

**Scaling Questions:**
> "On a scale of 1-10, where are you now? Where do you want to be? What would one step forward look like?"

**PA Application:**
- Future where both parents are accessible (even if not together)
- Future where child has voice, agency, safety
- Steps toward that future (even small ones)

### Hope Therapy (Shane Lopez, C.R. Snyder)

**Definition:**
- Uses interventions to improve hopeful thinking
- Boosts psychological functioning
- Builds goal thoughts and mindset/skills to achieve them

**Components:**
1. **Goal-setting:** Identify meaningful, approach-oriented goals
2. **Pathways thinking:** Generate multiple routes to goal
3. **Agency thinking:** Build motivation and commitment
4. **Obstacle planning:** Anticipate barriers, create backup plans

### UCAM Integration:
```json
{
  "future_planning_skills": [
    "goal_articulation",
    "pathways_generation",
    "agency_activation",
    "obstacle_planning",
    "hope_building",
    "future_orientation"
  ],
  "ucam_hope_framework": {
    "goals": "Meaningful, value-based, approach-oriented",
    "pathways": "Multiple routes, flexible thinking, barrier awareness",
    "agency": "Self-efficacy, motivation, perseverance",
    "outcome": "Hope, future orientation, reduced helplessness"
  }
}
```

---

## Techniques to Implement

### Technique 1: "Карта Будущего" (Future Map)
**Источник:** Snyder Hope Theory - goals as targets, SFBT future-focused

**Психологическая суть:**
- Будущее кажется туманным → нужна карта
- Goals = destinations on map
- Pathways = routes to destinations
- Для PA: будущее, где есть контроль, выбор, голос (не victimhood)

**Игровая механика:**
- **Квест:** "Картограф Завтра" (Cartographer of Tomorrow)
- **Визуализация:**
  - Blank map of future (next year, 5 years, 10 years)
  - Игрок размещает "destinations" (goals) на карте
  - Destinations: school, relationships, hobbies, family, values
- **Интерактив:**
  - SFBT Miracle Question адаптирована для детей
  - Выбор целей из categories (или создать свою)
  - Размещение на timeline (short-term, mid-term, long-term)

**Игровая сцена:**
```
Картограф Завтра (NPC): "Будущее - белая карта. Ты можешь наполнить её."

[Miracle Question для детей:]
"Представь: ты просыпаешься через год. Волшебство случилось.
 Что ИЗМЕНИЛОСЬ в твоей жизни? Что стало лучше?"

Игрок (варианты):
  A. "Я увижусь с папой снова" (alienated parent - relationship goal) ✓
  B. "Я буду увереннее в себе" (personal growth goal) ✓
  C. "Я найду новых друзей" (social goal) ✓
  D. "Родители снова вместе" → Картограф: "Это не в твоём контроле. Что ТЫ можешь создать?"

[Если A, B, или C:]
Картограф: "Отличная цель. Поставим её на карту."

[Цель появляется на карте как "destination"]
Пример: "Встреча с папой" (relationship goal, 1 year)

Картограф: "Теперь у тебя есть место назначения. Дальше построим дороги к нему."

→ +0.10 Goal Articulation, +0.08 Future Orientation, -0.07 Hopelessness
```

**Goal Categories (PA-adapted):**
```javascript
{
  "goal_categories": {
    "Relationship": {
      "examples": ["See alienated parent", "Build trust with therapist", "Make new friend"],
      "PA_specific": "Reconnect with alienated parent safely"
    },
    "Personal_Growth": {
      "examples": ["Be more confident", "Manage anger better", "Express feelings clearly"],
      "PA_specific": "Find my own voice (not parent's script)"
    },
    "Academic": {
      "examples": ["Improve grades", "Learn new skill", "Join club"],
      "value": "Mastery, achievement"
    },
    "Family": {
      "examples": ["Peaceful home", "Honest communication with parent", "Both parents respect me"],
      "PA_specific": "Family where I don't have to choose"
    },
    "Self_Care": {
      "examples": ["Exercise regularly", "Sleep better", "Reduce stress"],
      "value": "Health, well-being"
    },
    "Values": {
      "examples": ["Live with honesty", "Be kind", "Stand up for myself"],
      "PA_specific": "Love both parents without guilt"
    }
  }
}
```

**Артефакт:**
- **Компас Надежды** (tier 3)
- Burden: 0.04
- Эффект: +0.12 Goal Articulation, +0.10 Future Orientation, -0.09 Hopelessness

**Школьные предметы:**
- **Обществознание (7-9 класс):** Целеполагание, планирование жизни
- **Литература (7-9 класс):** Цели героев, путь героя
- **География (5-7 класс):** Карты, маршруты
- **История (7-9 класс):** Планирование будущего обществ

**Локация:** **Башня Завтра** (Tower of Tomorrow) - новая
- VCEM: V=+0.8, C=+0.8, E=+0.6 (hope), M=+0.9

**Коан-переход:**
```
Вход: "Что, если будущее - это белая карта, и ты можешь нарисовать на ней места, куда хочешь попасть?"
→
Выход: "Что, если цель - это звезда на горизонте, и она направляет твои шаги, даже когда путь не ясен?"
```

**Reality Bridge:**
1. **Future Vision Journal** (раз/неделю): "Что я хочу через год? Через 5 лет?"
2. **3 Goals Exercise**: Написать 3 цели (short-term, mid-term, long-term)
3. **Miracle Question**: Ответить дома, обсудить с терапевтом

---

### Technique 2: "Дороги к Цели" (Pathways Builder)
**Источник:** Snyder Hope Theory - Pathways Thinking (WayPower)

**Психологическая суть:**
- Goal без pathways = мечта, не план
- Pathways = конкретные шаги к цели
- Множественные пути (если один заблокирован, есть другой)
- Для PA: "Я МОГУ влиять на будущее, даже если не контролирую всё"

**Игровая механика:**
- **Квест:** "Строитель Дорог" (Road Builder Quest)
- **Визуализация:**
  - Goal = destination (звезда на горизонте)
  - Pathways = roads leading there (3-5 разных дорог)
  - Obstacles = rocks on road (predictable barriers)
- **Интерактив:**
  - Игрок выбирает goal с Future Map
  - Создаёт 3+ pathways (разные способы достичь)
  - Предсказывает препятствия + планирует альтернативы

**Игровая сцена:**
```
Строитель Дорог (NPC): "У тебя есть цель: 'Встреча с папой'. Как туда добраться?"

[Pathway Generation:]
Строитель: "Нужно минимум 3 дороги. Если одна закрыта, есть другие."

Игрок создаёт pathways:
  Pathway 1: "Попросить маму разрешить встречу"
  Pathway 2: "Попросить терапевта помочь организовать"
  Pathway 3: "Написать письмо папе (через бабушку/суд)"

Строитель: "Хорошо. Три дороги. Теперь - препятствия."

[Obstacle Planning:]
Obstacle 1: "Мама скажет 'нет'" (к Pathway 1)
  Alternative: "Тогда пробую Pathway 2 (терапевт)"

Obstacle 2: "Терапевт не может" (к Pathway 2)
  Alternative: "Тогда Pathway 3 (письмо)"

Obstacle 3: "Папа не ответит на письмо"
  Alternative: "Продолжу писать. Или попробую через год снова."

Строитель: "Видишь? У тебя есть план A, B, C. Препятствия НЕ конец. Это просто 'попробуй другую дорогу'."

→ +0.15 Pathways Thinking, +0.12 Obstacle Planning, +0.10 Flexibility
```

**Pathways Framework:**
```javascript
{
  "pathways_thinking": {
    "step_1_brainstorm": "Generate 3-5 different ways to reach goal",
    "step_2_evaluate": "Which pathway is most realistic? Which is backup?",
    "step_3_obstacles": "What could block each pathway?",
    "step_4_alternatives": "If pathway A blocked, try B or C",
    "outcome": "Flexible, resilient planning (not rigid)"
  },
  "PA_example_goal": "Reconnect with alienated parent",
  "pathways": [
    {
      "pathway_A": "Request supervised visit through family court",
      "obstacles": ["Court delays", "Parent refusal"],
      "alternative": "Try pathway B"
    },
    {
      "pathway_B": "Therapist-mediated communication (letters, calls)",
      "obstacles": ["Therapist can't facilitate", "Parent doesn't respond"],
      "alternative": "Try pathway C"
    },
    {
      "pathway_C": "Internal relationship (write letters, keep hope alive until older)",
      "obstacles": ["Feels incomplete", "Sadness"],
      "alternative": "Continuing bonds (Module 13), revisit A/B later"
    }
  ]
}
```

**Артефакт:**
- **Карта Дорог** (tier 3)
- Burden: 0.05
- Эффект: +0.16 Pathways Thinking, +0.12 Flexibility, +0.10 Problem-Solving

**Школьные предметы:**
- **Математика (5-9 класс):** Задачи с несколькими решениями
- **Информатика (7-9 класс):** Алгоритмы, условия, ветвления (if-then-else)
- **География (6-9 класс):** Маршруты, альтернативные пути
- **Литература (7-9 класс):** План героя, препятствия, альтернативы

**Локация:** **Мастерская Дорог** (Road Workshop) - в Tower of Tomorrow
- VCEM: V=+0.7, C=+0.9 (clarity), E=+0.5, M=+0.8

**Коан-переход:**
```
Вход: "Что, если цель - это звезда, и она направляет твои шаги?"
→
Выход: "Что, если к каждой звезде ведёт не одна дорога, а три, и если одна закрыта, ты идёшь по другой?"
```

**Reality Bridge:**
1. **Pathways Exercise** (с терапевтом): Взять цель, создать 3 пути
2. **Obstacle Brainstorm**: "Что может помешать? Что тогда?"
3. **Plan A-B-C**: Записать основной план + 2 запасных

---

### Technique 3: "Двигатель Воли" (Agency Activator)
**Источник:** Snyder Hope Theory - Agency Thinking (WillPower)

**Психологическая суть:**
- Pathways without Agency = знаю как, но не делаю
- Agency = "Я МОГУ. Я БУДУ. Я начну."
- Self-efficacy, motivation, perseverance
- Для PA: восстановление "Я влияю на мою жизнь" (против learned helplessness)

**Игровая механика:**
- **Квест:** "Зажигание Двигателя" (Engine Ignition)
- **Визуализация:**
  - Двигатель = Agency (топливо = motivation, искра = start action)
  - Low fuel = low motivation (need to refuel)
  - Высокое топливо = высокая agency
- **Интерактив:**
  - Измерить текущий уровень agency (1-10)
  - Identify motivation blockers (fear, learned helplessness, fatigue)
  - Activate agency через micro-actions

**Игровая сцена:**
```
Механик Воли (NPC): "Проверим твой двигатель. Сколько топлива?"

[Scaling Question - agency level:]
"По шкале 1-10, насколько ты веришь, что МОЖЕШЬ достичь своей цели?"

Игрок отвечает: 4/10 (low agency)

Механик: "4 из 10. Двигатель слабый. Что мешает?"

[Identify blockers:]
Варианты:
  A. "Я боюсь, что не получится" (fear of failure) ✓
  B. "Я пытался раньше, не вышло" (learned helplessness) ✓
  C. "Я слишком устал" (fatigue, depression)
  D. "Мама не разрешит" (external locus of control) ✓

[Игрок выбирает B: learned helplessness]

Механик: "Ты пытался, не вышло. И ты решил: 'Больше не буду'. Верно?"

Игрок: Да.

Механик: "Это called 'усталость надежды'. Но вот правда:
         Прошлые попытки ≠ будущий результат.
         Ты можешь попробовать ПО-ДРУГОМУ (новый pathway).
         Ты можешь начать МАЛЕНЬКО (micro-action)."

[Agency Activation:]
Механик: "Не говори: 'Я верну папу' (too big).
         Скажи: 'Я напишу одно письмо на этой неделе' (micro-action)."

Игрок: "Я напишу одно письмо."

Механик: "Да! Двигатель запустился. Маленькое действие = начало агентности."

[После выполнения micro-action:]
→ Agency level: 4 → 6/10
→ +0.14 Agency, +0.10 Self-Efficacy, -0.08 Learned Helplessness
```

**Agency Activation Strategies:**
```javascript
{
  "agency_activation": {
    "Micro_Actions": {
      "principle": "Start with smallest possible step (1% progress)",
      "examples": [
        "Write 1 sentence in journal (not 1 page)",
        "Send 1 text to friend (not have full conversation)",
        "Do 1 breathing exercise (not 10 min meditation)"
      ],
      "PA_example": "Write 1 line to alienated parent (not full letter)"
    },
    "Self_Talk": {
      "low_agency": "I can't. It's hopeless. Nothing I do matters.",
      "high_agency": "I can try. I'll start small. My actions matter.",
      "practice": "Replace 'I can't' with 'I can try one step'"
    },
    "Evidence_Gathering": {
      "question": "When have you succeeded before (even small)?",
      "goal": "Build evidence of past agency to activate future agency"
    },
    "Locus_of_Control_Shift": {
      "external": "Мама/суд/судьба решает (no control)",
      "internal": "Я могу влиять на МОИ действия (some control)",
      "acceptance": "Я не контролирую ВСЁ, но контролирую СВОИ шаги"
    }
  }
}
```

**Артефакт:**
- **Искра Начала** (tier 3)
- Burden: 0.04
- Эффект: +0.15 Agency, +0.12 Self-Efficacy, -0.10 Learned Helplessness

**Школьные предметы:**
- **Обществознание (7-9 класс):** Активная гражданская позиция, влияние
- **Литература (7-9 класс):** Агентность героев, выбор
- **История (7-9 класс):** Исторические личности, влияние на события
- **Физика (7-9 класс):** Энергия, движение, инерция (метафоры)

**Локация:** **Мастерская Двигателя** (Engine Workshop) - в Tower of Tomorrow
- VCEM: V=+0.8, C=+0.7, E=+0.7 (motivation), M=+0.9

**Коан-переход:**
```
Вход: "Что, если к каждой звезде ведёт не одна дорога, а три?"
→
Выход: "Что, если первый шаг - самый важный, и даже самый маленький шаг - это уже движение?"
```

**Reality Bridge:**
1. **Daily Micro-Action** (каждый день): Одно маленькое действие к цели
2. **Agency Affirmation**: "Я могу. Я буду. Я начну."
3. **Evidence Journal**: "Когда я раньше влиял на ситуацию? (Доказательства агентности)"

---

### Technique 4: "Барьеры и Мосты" (Obstacles & Bridges)
**Источник:** Hope Therapy - obstacle planning, SFBT - scaling and progress

**Психологическая суть:**
- Obstacles are inevitable (не "если", а "когда")
- Планирование препятствий ≠ пессимизм, это реализм
- Bridges = coping strategies для преодоления
- Для PA: "Даже если мама блокирует, я найду обходной путь"

**Игровая механика:**
- **Квест:** "Мосты Через Бездны" (Bridges Across Chasms)
- **Визуализация:**
  - Pathway = road, Obstacles = chasms (пропасти)
  - Bridges = solutions to cross chasms
- **Интерактив:**
  - Игрок идёт по pathway, встречает obstacle
  - Выбирает или создаёт bridge (coping strategy)
  - Overcomes obstacle, продолжает путь

**Игровая сцена:**
```
[Игрок идёт по Pathway 1: "Попросить маму о встрече с папой"]

[Obstacle появляется: Пропасть перед дорогой]
Страж Барьеров (NPC): "Препятствие: Мама сказала 'нет'. Что теперь?"

Варианты:
  A. "Сдаюсь. Не получилось." (give up, low hope)
  B. "Попробую pathway 2 (терапевт)" (alternative pathway) ✓
  C. "Подожду, попробую снова через месяц" (persistence + timing) ✓
  D. "Построю мост через пропасть" (coping strategy - e.g., compromise) ✓

[Игрок выбирает D: построить мост]

Страж: "Какой мост построишь?"

Игрок (варианты):
  - "Предложу маме: сначала короткая встреча (30 мин)" (compromise)
  - "Попрошу бабушку поговорить с мамой" (seek support)
  - "Напишу маме письмо, объясню, почему важно" (communication)

[Игрок выбирает compromise]

Страж: "Мост компромисса. Мудро. Мама может согласиться на меньшее."

[Сцена: Игрок предлагает компромисс]
Мама (NPC): "30 минут... Ладно. Попробуем."

Страж: "Мост сработал. Препятствие преодолено. Ты продолжаешь путь."

→ +0.13 Obstacle Navigation, +0.11 Coping Strategies, +0.09 Persistence
```

**Obstacle Types & Bridges (PA-specific):**
```javascript
{
  "obstacles_and_bridges": {
    "Obstacle_1_Parental_Refusal": {
      "obstacle": "Alienating parent says 'no' to contact",
      "bridges": [
        "Seek therapist mediation (external support)",
        "Propose compromise (short visit, supervised)",
        "Wait and try again later (timing + persistence)",
        "Write letter to parent explaining importance (communication)",
        "Seek court intervention (if age-appropriate, with therapist)"
      ]
    },
    "Obstacle_2_Fear": {
      "obstacle": "Child fears alienated parent (due to programming)",
      "bridges": [
        "Process fear with therapist (CBT, exposure)",
        "Start with letters/photos before in-person (gradual)",
        "Supervised visit for safety (scaffolding)",
        "Remind self: 'Fear is from stories, not experience' (cognitive)"
      ]
    },
    "Obstacle_3_Guilt": {
      "obstacle": "Child feels guilty for wanting contact (loyalty conflict)",
      "bridges": [
        "Affirmation: 'Loving both is OK' (Module 22)",
        "Process with therapist (Continuing Bonds, Module 13)",
        "Separate love from obedience (I can love both + see both)"
      ]
    },
    "Obstacle_4_External_Barriers": {
      "obstacle": "Court order, distance, parent disappeared",
      "bridges": [
        "If court: work with lawyer/therapist to modify order",
        "If distance: letters, video calls (when possible)",
        "If disappeared: continuing bonds internally, hope for future"
      ]
    }
  }
}
```

**Артефакт:**
- **Набор Мостов** (tier 4)
- Burden: 0.05
- Эффект: +0.14 Obstacle Navigation, +0.12 Coping Strategies, +0.10 Persistence

**Школьные предметы:**
- **Математика (5-9 класс):** Задачи с препятствиями, поиск решений
- **Физика (7-9 класс):** Преодоление барьеров, мосты (конструкция)
- **Литература (7-9 класс):** Препятствия героя, как преодолевает
- **История (7-9 класс):** Исторические препятствия, как решали

**Локация:** **Долина Препятствий** (Valley of Obstacles) - на пути к Tower of Tomorrow
- VCEM: V=+0.4 (challenge), C=+0.8, E=+0.4, M=+0.7

**Коан-переход:**
```
Вход: "Что, если первый шаг - самый важный?"
→
Выход: "Что, если каждое препятствие - это пропасть, и ты можешь построить мост, если знаешь как?"
```

**Reality Bridge:**
1. **Obstacle List** (для каждой цели): "Что может помешать? Как преодолею?"
2. **Bridge Brainstorm**: 2-3 способа преодолеть каждое препятствие
3. **When-Then Planning**: "КОГДА встречу [препятствие], ТОГДА сделаю [bridge]"

---

### Technique 5: "Компас Надежды" (Hope Compass - Integration)
**Источник:** Hope Therapy integration, Snyder synthesis of goals + pathways + agency

**Психологическая суть:**
- Hope = Goals + Pathways + Agency (all three together)
- Компас = tool для навигации в будущее
- Регулярная проверка: "Где я? Куда иду? Как? Могу ли?"
- Для PA: "Надежда - это не мечта, это план + вера в себя"

**Игровая механика:**
- **Квест:** "Калибровка Компаса" (Compass Calibration) - финальный
- **Визуализация:**
  - Компас с 4 направлениями:
    - North: Goal (куда иду?)
    - East: Pathways (как иду?)
    - South: Agency (могу ли?)
    - West: Progress (где сейчас?)
- **Интерактив:**
  - Регулярная проверка (раз/неделю в игре)
  - Adjustments (цель изменилась? pathway заблокирован? agency упало?)

**Игровая сцена (финал модуля):**
```
Хранитель Компаса (NPC): "Твой компас надежды готов. Проверим каждое направление."

[North: Goal]
"Куда ты идёшь?"
Игрок: "Я хочу восстановить отношения с папой."
Хранитель: "Чёткая цель. Север определён." ✓

[East: Pathways]
"Как ты туда доберёшься?"
Игрок: "Pathway A: Попросить маму. Pathway B: Терапевт. Pathway C: Письма."
Хранитель: "Три дороги. Восток ясен." ✓

[South: Agency]
"Веришь ли, что можешь?"
Игрок: "Да. Я начну с одного письма на этой неделе."
Хранитель: "Действие запланировано. Юг активен." ✓

[West: Progress]
"Где ты сейчас?"
Игрок: "Я на 3/10 к цели. Написал одно письмо. Мама пока сказала 'подожди'."
Хранитель: "Прогресс есть. Ты движешься. Запад отмечен." ✓

[Компас активирован]
Хранитель: "Компас работает. Надежда жива.
            Помни: Надежда - это не 'всё сразу получится'.
            Надежда - это 'У меня есть цель, план, и я начал'.
            Ты идёшь."

→ +0.18 Hope, +0.15 Future Orientation, +0.12 Self-Direction
→ Unlocked: Permanent Hope Compass (check anytime)
```

**Hope Compass Framework:**
```javascript
{
  "hope_compass_4_directions": {
    "North_Goal": {
      "question": "Where am I going?",
      "check": "Is goal still meaningful? Clear? Approach-oriented?",
      "adjust": "Refine goal if needed"
    },
    "East_Pathways": {
      "question": "How will I get there?",
      "check": "Are pathways realistic? Multiple? Flexible?",
      "adjust": "Generate new pathways if blocked"
    },
    "South_Agency": {
      "question": "Can I do this?",
      "check": "Motivation level? Self-efficacy? Taking action?",
      "adjust": "Activate agency (micro-actions, self-talk)"
    },
    "West_Progress": {
      "question": "Where am I now?",
      "check": "How far have I come? What's next step?",
      "adjust": "Celebrate progress, plan next action"
    }
  },
  "weekly_check_in": "Review compass every week, adjust as needed",
  "hope_equation": "Hope = (Goal + Pathways + Agency) - Obstacles + Progress"
}
```

**Артефакт:**
- **Вечный Компас Надежды** (tier 5, permanent tool)
- Burden: 0.03
- Эффект: +0.20 Hope, +0.16 Future Orientation, +0.14 Self-Direction

**Школьные предметы:**
- **Обществознание (7-9 класс):** Жизненные цели, планирование
- **Литература (7-9 класс):** Путь героя, надежда в литературе
- **География (5-9 класс):** Компасы, навигация
- **Философия (9 класс):** Смысл, цель, надежда

**Локация:** **Вершина Башни Завтра** (Top of Tower of Tomorrow) - финал модуля
- VCEM: V=+0.9, C=+0.9, E=+0.8 (hope, determination), M=+0.95

**Коан-переход:**
```
Вход: "Что, если каждое препятствие - это пропасть, и ты можешь построить мост?"
→
Выход: "Что, если надежда - это компас, и он показывает: куда идти, как идти, и что ты МОЖЕШЬ идти?"
```

**Reality Bridge:**
1. **Weekly Compass Check** (каждое воскресенье): Проверить 4 направления
2. **Hope Journal**: "Моя цель, мои пути, мои действия на этой неделе"
3. **Progress Celebration**: Отмечать даже маленький прогресс (1% лучше 0%)

---

## Integration Points

### With Other Modules:
- **Module 13 (Grief Processing):** После интеграции горя → готов планировать будущее
- **Module 09 (Emotional Literacy):** Понимание эмоций → принятие эмоциональных целей
- **Module 10 (Anger Management):** Контроль гнева → конструктивное движение к целям
- **Module 17 (Creative Expression):** Визуализация будущего через творчество
- **Module 22 (Loyalty Conflict):** Цель "любить обоих" как future goal

### Game Progression:
- **Prerequisites:** Module 13 (Grief Processing - readiness to look forward), Module 09 (Emotional Literacy)
- **Unlocks:** Module 22 (Loyalty Conflict - applying hope to PA-specific relational goals), End-game content, Life Skills modules

### UCAM Tags:
```json
{
  "future_planning_dimensions": {
    "hope_components": ["goals", "pathways", "agency"],
    "skills": ["goal_setting", "obstacle_planning", "motivation", "progress_tracking"],
    "outcomes": ["hope", "future_orientation", "self_direction", "reduced_helplessness"]
  },
  "clinical_targets": ["hopelessness", "learned_helplessness", "passive_victimhood", "external_locus_control"],
  "developmental_stage": ["7-14 years", "future_thinking_development"]
}
```

---

## Technical Specifications

### Vector DB Scenes:
25-30 future planning scenes:
- 6 scenes: Goal Articulation (Future Map)
- 7 scenes: Pathways Thinking (multiple routes)
- 6 scenes: Agency Activation (motivation, action)
- 6 scenes: Obstacle Navigation (barriers + bridges)
- 3 scenes: Hope Compass (integration check-ins)

**Scene example:**
```json
{
  "scene_id": "FUT20-v1.0-agency-T7M3",
  "ucam_schema": "v1.0",
  "module_id": "20_Future_Planning",
  "question": "У тебя есть цель: 'Встретиться с папой'. Но попытка 1 не вышла (мама сказала нет). Что ты чувствуешь и делаешь?",
  "answers": [
    {"id": 0, "text": "Сдаюсь. Бесполезно пытаться.", "tag": ["hopelessness", "learned_helplessness"]},
    {"id": 1, "text": "Попробую по-другому (другой pathway)", "tag": ["adaptive", "pathways_thinking", "best"]},
    {"id": 2, "text": "Подожду и попробую снова через месяц", "tag": ["adaptive", "persistence"]},
    {"id": 3, "text": "Злюсь и ничего не делаю", "tag": ["stuck_in_emotion", "low_agency"]}
  ],
  "correct_index": 1,
  "tags": {
    "hope_component": "pathways + agency",
    "difficulty": 3,
    "PA_specific": true
  }
}
```

### UI/UX Features:
1. **Future Map** (timeline visualization, goal placement)
2. **Pathways Builder** (3-5 routes, obstacles marked)
3. **Agency Meter** (1-10 scale, fuel visualization)
4. **Obstacle-Bridge Interface** (chasms + bridge options)
5. **Hope Compass** (4-direction check-in tool)

### MVP Scope:
- **Content:** ~50-55KB
- **Scenes:** 28 vector scenes
- **Artifacts:** 5 (Компас Надежды [goal], Карта Дорог [pathways], Искра Начала [agency], Набор Мостов [obstacles], Вечный Компас Надежды [integration])
- **Locations:** 4 (Tower of Tomorrow, Road Workshop, Engine Workshop, Valley of Obstacles)
- **NPCs:** 5 (Картограф, Строитель, Механик, Страж Барьеров, Хранитель Компаса)
- **School subjects:** 10 integrations

---

## Success Metrics

### Learning Outcomes:
- Ребёнок формулирует 3+ meaningful goals
- Создаёт 3+ pathways для каждой цели
- Демонстрирует agency (начинает micro-actions)
- Планирует препятствия + bridges
- Проверяет Hope Compass регулярно (weekly)

### Game Metrics:
- Hope ≥ 0.75
- Goal Articulation ≥ 0.70
- Pathways Thinking ≥ 0.70
- Agency ≥ 0.65
- Future Orientation ≥ 0.75
- Hopelessness снижение на 60%

### Clinical Markers:
- Hopelessness Scale снижение на 50%
- Future Orientation рост на 55%
- Locus of Control shift (external → internal) 40%
- Goal-directed behavior рост на 45%

---

## References

### Clinical:
- Snyder, C. R. (2002). Hope theory: Rainbows in the mind. *Psychological Inquiry*, 13(4), 249-275.
- Snyder, C. R., et al. (1991). The will and the ways: Development and validation of an individual-differences measure of hope. *Journal of Personality and Social Psychology*, 60(4), 570-585.
- Lopez, S. J., et al. (2000). Hope therapy: Helping clients build a house of hope. In C. R. Snyder (Ed.), *Handbook of Hope* (pp. 123-150). Academic Press.

### Research:
- Cheavens, J. S., et al. (2006). Hope therapy in a community sample: A pilot investigation. *Social Indicators Research*, 77(1), 61-78.
- Feldman, D. B., & Dreher, D. E. (2012). Can hope be changed in 90 minutes? Testing the efficacy of a single-session goal-pursuit intervention. *Journal of Happiness Studies*, 13(4), 745-759.
- Valle, M. F., et al. (2006). Hope, viability, and posttraumatic stress disorder: A prospective study of soldiers deployed to Iraq. *Journal of Traumatic Stress*, 19(6), 935-939.

### Solution-Focused & Positive Psychology:
- de Shazer, S., & Berg, I. K. (1997). 'What works?' Remarks on research aspects of solution-focused brief therapy. *Journal of Family Therapy*, 19(2), 121-124.
- Seligman, M. E. P. (2011). *Flourish: A Visionary New Understanding of Happiness and Well-being*. Free Press.
- Research on goal-setting in therapy (multiple studies cited in search results)

---

## Implementation Priority: VERY HIGH

**Rationale:**
- **Critical transition** - from processing past/present (grief, anger) to building future
- **Strong research base** - Snyder's Hope Theory extensively validated
- **Counteracts PA effects** - restores agency, hope, internal locus of control
- **Builds resilience** - goal-oriented thinking predicts positive outcomes
- **Prerequisite for adulthood** - future planning = life skill
- **Completes therapeutic arc** - past processing → present coping → future building

**Dependencies:**
- Requires: Module 13 (Grief Processing - readiness to move forward), Module 09 (Emotional Literacy)
- Enables: Life skills modules, end-game content

**Next Module:** Integration modules, advanced life skills, or Module 22 (Loyalty Conflict - applying hope to PA-specific relational goals)
