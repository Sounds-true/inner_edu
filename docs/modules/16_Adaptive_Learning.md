# Implementation Plan: Module 16 - Adaptive Learning System

## Module Overview
**Target:** Персонализация обучающего опыта для каждого ребёнка 7-14 лет
**Цель:** Создать адаптивную систему, которая подстраивает сложность, тайминг и контент под индивидуальный профиль ребёнка
**Источники:** Reinforcement Learning (Multi-Armed Bandit), Educational Data Mining, UCAM dynamic profiling, Zone of Proximal Development (Vygotsky)

## Core Concept: Why Adaptive Learning?

### Problem Statement:
- Дети имеют разные темпы обучения (один усваивает DBT за неделю, другому нужен месяц)
- Одинаковая сложность для всех → frustration (слишком сложно) или boredom (слишком легко)
- PA дети имеют разные триггеры, паттерны, needs
- Static curriculum не учитывает real-time progress

### Solution: Multi-Armed Bandit (MAB)
- **Метафора:** Игровой автомат с несколькими рычагами (arms)
- Каждый "рычаг" = обучающая стратегия/модуль/сложность
- Система выбирает рычаг → получает reward (успех ребёнка) → учится
- **Exploration vs Exploitation trade-off:**
  - Exploration: Попробовать новое (может быть лучше?)
  - Exploitation: Использовать лучшее из известного (maximize success)

### UCAM Integration:
```json
{
  "adaptive_learning_components": [
    "difficulty_adjustment",
    "content_personalization",
    "timing_optimization",
    "learning_style_detection",
    "real_time_profiling"
  ],
  "MAB_arms": {
    "content_type": ["visual", "narrative", "interactive", "reflective"],
    "difficulty": ["easy", "medium", "hard", "adaptive"],
    "pacing": ["slow", "moderate", "fast", "self_paced"],
    "focus_modules": ["M01_IFS", "M02_DBT", "M03_CBT", "..."]
  }
}
```

---

## Technical Architecture

### 1. Multi-Armed Bandit Algorithm
**Алгоритм:** Epsilon-Greedy with Thompson Sampling (hybrid)

**Псевдокод:**
```python
class AdaptiveLearningEngine:
    def __init__(self):
        self.arms = {
            "easy_visual": BanditArm(),
            "medium_narrative": BanditArm(),
            "hard_interactive": BanditArm(),
            # ... 20-30 комбинаций
        }
        self.epsilon = 0.1  # 10% exploration
        self.player_profile = {}

    def select_next_scene(self, player_state):
        """Выбор следующей сцены на основе MAB"""
        if random() < self.epsilon:
            # EXPLORATION: Try random arm
            return random.choice(self.arms)
        else:
            # EXPLOITATION: Best known arm
            return max(self.arms, key=lambda a: a.expected_reward(player_state))

    def update_reward(self, arm, success, engagement):
        """Обновление после попытки"""
        reward = calculate_reward(success, engagement, learning_gain)
        arm.update(reward)
        self.player_profile.update(arm, reward)
```

**Reward Function:**
```
Reward = w1 * Success(correct_answer)
       + w2 * Engagement(time_spent, click_rate)
       + w3 * Learning_Gain(skill_improvement)
       - w4 * Frustration(retries, skip_rate)
       - w5 * Boredom(idle_time, disengagement)

где w1=0.4, w2=0.2, w3=0.3, w4=0.05, w5=0.05
```

---

### 2. Difficulty Adjustment System (DAS)

**Принцип:** Zone of Proximal Development (ZPD)
- Слишком легко (< ZPD) → Boredom → снизить interest
- Слишком сложно (> ZPD) → Frustration → снизить self-efficacy
- В ZPD → Optimal challenge → максимальное обучение

**Алгоритм:**
```javascript
class DifficultyAdjuster {
  calculateDifficulty(player) {
    const skill_level = player.getCurrentSkillLevel(); // 0.0 - 1.0
    const recent_success_rate = player.getRecentSuccessRate(last_10_scenes);
    const emotional_state = player.getEmotionalState(); // anxiety, frustration

    let target_difficulty = skill_level + 0.15; // ZPD = текущий уровень + 15%

    // Корректировки:
    if (recent_success_rate < 0.5) {
      target_difficulty -= 0.1; // Снизить сложность
    } else if (recent_success_rate > 0.85) {
      target_difficulty += 0.1; // Повысить вызов
    }

    if (emotional_state.anxiety > 0.7) {
      target_difficulty -= 0.15; // Дать передышку
    }

    return clamp(target_difficulty, 0.0, 1.0);
  }

  selectScene(target_difficulty) {
    return vectorDB.query({
      difficulty: target_difficulty,
      similarity_threshold: 0.1 // ±10% от целевой
    });
  }
}
```

**Игровая визуализация:**
```
[DIFFICULTY METER]
├─────────┼─────────┼─────────┤
Easy   Optimal   Hard
   ↑
  You are here (adapting in real-time)
```

---

### 3. Learning Style Detection

**4 стиля обучения (адаптация VARK):**
1. **Visual Learner** - предпочитает картинки, схемы, visualizations
2. **Narrative Learner** - учится через истории, метафоры
3. **Interactive Learner** - учится через действие, mini-games
4. **Reflective Learner** - учится через анализ, вопросы, дневники

**Детекция стиля (MAB-based):**
```python
class LearningStyleDetector:
    def __init__(self):
        self.style_scores = {
            "visual": 0.25,
            "narrative": 0.25,
            "interactive": 0.25,
            "reflective": 0.25
        }  # Начинаем с равных вероятностей

    def detect_style(self, player_history):
        """Детекция через MAB - какие сцены давали лучший результат"""
        for scene in player_history:
            style = scene.content_type
            reward = scene.success * scene.engagement
            self.style_scores[style] = bayesian_update(
                prior=self.style_scores[style],
                likelihood=reward
            )

        return normalize(self.style_scores)

    def recommend_content(self, scene_pool):
        """Выбор контента на основе стиля"""
        dominant_style = max(self.style_scores, key=self.style_scores.get)

        # 70% dominant style, 30% exploration
        if random() < 0.7:
            return filter_by_style(scene_pool, dominant_style)
        else:
            return random.choice(scene_pool)
```

**Игровая имплементация:**
- Первые 15 сцен - balanced mix (детекция)
- После 15 → система знает предпочтения
- Адаптация: 70% preferred style, 30% variety (не застревать)

---

### 4. Personalized Learning Path

**Концепция:** Не линейный path (M01→M02→M03), а adaptive tree

**Dependency Graph:**
```
      M08 (Mindfulness)
      /              \
  M09 (Emotion)    M07 (ACT)
      \              /
      M11 (DBT Advanced)
           |
      M14 (Communication) ← M16 decides когда ready
           |
      M22 (Loyalty Conflict)
```

**Readiness Check (для каждого модуля):**
```javascript
class ModuleGatekeeper {
  isReady(player, next_module) {
    const prerequisites = next_module.prerequisites; // [M08, M09]
    const skill_requirements = next_module.min_skills; // {emotion_literacy: 0.6}

    // Check 1: Prerequisites completed?
    for (let prereq of prerequisites) {
      if (!player.hasCompleted(prereq)) {
        return {ready: false, reason: "Complete " + prereq.name + " first"};
      }
    }

    // Check 2: Skills sufficient?
    for (let [skill, min_level] of skill_requirements) {
      if (player.getSkill(skill) < min_level) {
        return {ready: false, reason: `${skill} needs ${min_level}, you have ${player.getSkill(skill)}`};
      }
    }

    // Check 3: Emotional state OK?
    if (player.currentAnxiety > 0.8) {
      return {ready: false, reason: "High anxiety - practice calming first"};
    }

    return {ready: true, unlock: next_module};
  }
}
```

**Игровой квест: "Карта Путей" (Map of Paths)**
- Визуализация: Дерево модулей
- Открытые (completed): зелёные
- Доступные (ready): жёлтые
- Заблокированные (not ready): серые с подсказкой
- Игрок ВЫБИРАЕТ следующий модуль из доступных (agency!)

---

### 5. Real-Time Profiling (UCAM Dynamic)

**Цель:** Постоянно обновлять профиль ребёнка на основе поведения в игре

**Профиль включает:**
```json
{
  "player_id": "P12345",
  "timestamp": "2025-11-06T10:30:00Z",

  "skills": {
    "emotion_literacy": 0.65,
    "mindfulness": 0.50,
    "opposite_action": 0.40,
    "I_statements": 0.55,
    "boundary_setting": 0.35
  },

  "learning_style": {
    "visual": 0.45,
    "narrative": 0.30,
    "interactive": 0.15,
    "reflective": 0.10
  },

  "emotional_profile": {
    "current_state": {
      "anxiety": 0.35,
      "sadness": 0.20,
      "anger": 0.10
    },
    "baseline": {
      "anxiety": 0.55,  // Улучшение!
      "sadness": 0.40
    },
    "triggers": ["parental_conflict", "peer_rejection"]
  },

  "engagement_metrics": {
    "avg_session_length": 25.5,  // минут
    "completion_rate": 0.82,
    "skip_rate": 0.05,
    "retry_rate": 0.12,
    "idle_time_pct": 0.08
  },

  "difficulty_sweet_spot": {
    "current_ZPD": 0.60,  // skill level
    "optimal_challenge": 0.70,  // +10% для роста
    "recent_success_rate": 0.75
  },

  "MAB_state": {
    "best_arms": [
      {"arm": "medium_narrative_M09", "reward": 0.85},
      {"arm": "easy_interactive_M08", "reward": 0.80}
    ],
    "exploration_count": 45,
    "exploitation_count": 130
  }
}
```

**Обновление профиля (после каждой сцены):**
```python
def update_profile(player, scene, outcome):
    # 1. Skill update (exponential moving average)
    skill = scene.primary_skill
    old_level = player.skills[skill]
    new_level = 0.8 * old_level + 0.2 * outcome.success  # EMA
    player.skills[skill] = new_level

    # 2. Learning style update (MAB)
    style = scene.content_type
    reward = outcome.success * outcome.engagement
    player.learning_style_MAB.update(style, reward)

    # 3. Emotional state update
    player.emotional_state = detect_emotion_from_gameplay(
        click_patterns, idle_time, skip_behavior
    )

    # 4. Difficulty adjustment
    player.optimal_challenge = calculate_ZPD(
        player.skills, player.recent_success_rate
    )

    # 5. Save to DB
    save_profile_to_ucam(player)
```

---

## Game Mechanics: Adaptive Features

### Feature 1: "Умный Помощник" (Smart Companion)
**Концепция:** NPC-помощник, который замечает struggle и предлагает помощь

**Игровая механика:**
```
[Игрок застрял на сцене 3 раза подряд]

Умный Помощник появляется:
"Эй, вижу, это сложно. Хочешь:
 A. Попробовать ещё раз (retry)
 B. Подсказку (hint - снижает сложность)
 C. Попрактиковаться на похожих, но проще (easier scenes)
 D. Вернуться позже (skip for now)"

[Выбор игрока → система учится:]
- Если часто B/C → снизить general difficulty
- Если часто A → игрок упорный, можно не снижать
- Если часто D → возможно, emotional fatigue → предложить mindfulness
```

**NPC:** Эхо-Гид (Echo-Guide) - adaptive companion
- Появляется при struggle
- Исчезает при flow state
- Тон адаптируется: encouraging (при frustration), challenging (при boredom)

---

### Feature 2: "Динамические Награды" (Dynamic Rewards)
**Концепция:** Награды адаптируются к сложности и усилиям

**Формула:**
```
XP_earned = base_XP
          * difficulty_multiplier
          * (1 + struggle_bonus)
          * (1 - retry_penalty * num_retries)

где:
- difficulty_multiplier: 1.0 (easy), 1.5 (medium), 2.0 (hard)
- struggle_bonus: 0.5 если сцена была близка к ZPD (optimal challenge)
- retry_penalty: 0.1 per retry (но макс -0.3, не демотивировать)
```

**Пример:**
```
Сцена: DBT Advanced, сложность 0.75 (hard для игрока с skill 0.65)
Success на 2-й попытке
XP = 100 * 2.0 * 1.5 * (1 - 0.1*1) = 270 XP

vs

Сцена: Easy (0.4 сложность, skill 0.65)
Success на 1-й попытке
XP = 100 * 1.0 * 1.0 * 1.0 = 100 XP

→ Игра поощряет вызов, не rote repetition
```

---

### Feature 3: "Прогноз Успеха" (Success Predictor)
**Концепция:** Показать игроку вероятность успеха перед сценой (self-efficacy)

**UI элемент:**
```
[SCENE PREVIEW]
"Opposite Action Challenge"
Difficulty: ████░░ (4/5)
Your skill: ███░░░ (3/5)
Success probability: ~65%

[This is challenging but doable - perfect for growth!]

[START] [Pick easier] [Learn more first]
```

**Психологическая цель:**
- Не overwhelm (если вероятность < 30% → предложить подготовку)
- Не bore (если > 90% → предложить harder)
- Sweet spot: 50-80% success probability

---

### Feature 4: "Микро-Адаптация внутри Сцены"
**Концепция:** Даже внутри одной сцены можно адаптировать

**Пример:**
```
Сцена: Emotion Identification (M09)
Вопрос: "Мама кричит на тебя. Что ты чувствуешь?"

[Версия EASY:]
Answers:
  A. Радость
  B. Страх ✓
  C. Голод
(Абсурдные дистракторы, очевидный правильный)

[Версия MEDIUM:]
Answers:
  A. Грусть
  B. Страх ✓
  C. Гнев
(Все правдоподобные, нужно различать)

[Версия HARD:]
Answers:
  A. Страх + Грусть ✓
  B. Только страх
  C. Страх + Гнев ✓
(Смешанные эмоции, несколько правильных)

Система выбирает версию на основе player.skills["emotion_literacy"]
```

---

### Feature 5: "Время Отдыха" (Rest & Reflection)
**Концепция:** Система детектирует усталость и предлагает паузу

**Триггеры:**
```python
def should_suggest_break(player, session):
    if session.duration > 40:  # 40+ минут непрерывно
        return True

    if player.recent_errors > 5 in last_10_scenes:
        return True  # Frustration

    if player.emotional_state.anxiety > 0.8:
        return True  # High distress

    if player.idle_time_pct > 0.3:
        return True  # Disengagement

    return False
```

**Игровая сцена:**
```
[После 45 минут игры]

Эхо-Гид: "Ты много работал сегодня. Мозгу нужен отдых, чтобы закрепить знания.

Хочешь:
 A. Сделать 5-минутную паузу (mindfulness) → bonus XP
 B. Закончить на сегодня (save progress)
 C. Продолжить (но я буду следить за тобой 👀)"

[Если выбрано A → 5 мин дыхательная практика → +50 bonus XP]
```

---

## Integration with UCAM

### Data Flow:
```
Player Action (in-game)
    ↓
Scene Outcome (success, emotion, time, engagement)
    ↓
UCAM Profile Update (skills, emotional state, learning style)
    ↓
MAB Reward Calculation
    ↓
Adaptive Decision (next scene difficulty, content type, module)
    ↓
Vector DB Query (fetch matching scenes)
    ↓
Present to Player
    ↓
[Loop]
```

### UCAM Schema Updates:
```json
{
  "ucam_adaptive_extensions": {
    "difficulty_level": "float 0.0-1.0",
    "content_type": "enum [visual, narrative, interactive, reflective]",
    "success_probability": "float 0.0-1.0",
    "ZPD_match": "bool (is this in Zone of Proximal Development?)",
    "MAB_arm_id": "string (для tracking)",
    "reward_earned": "float (для MAB update)"
  }
}
```

---

## Technical Specifications

### Implementation Stack:
- **MAB Engine:** Python (scikit-learn, scipy для Thompson Sampling)
- **Real-time profiling:** Redis (fast read/write для session state)
- **Long-term storage:** PostgreSQL (player profiles, history)
- **Scene selection:** Vector DB (Pinecone/Qdrant) с difficulty filters
- **Game client:** JavaScript (получает adaptive recommendations via API)

### API Endpoints:
```
POST /api/adaptive/next-scene
  Input: {player_id, current_module, emotional_state}
  Output: {scene_id, difficulty, content_type, success_prob}

POST /api/adaptive/update-profile
  Input: {player_id, scene_id, outcome: {success, engagement, time}}
  Output: {updated_profile, new_skill_levels}

GET /api/adaptive/learning-path
  Input: {player_id}
  Output: {available_modules, recommended_next, blocked_modules}
```

### Performance:
- Scene selection: < 200ms (real-time)
- Profile update: < 100ms (не блокирует UI)
- MAB model update: async (каждые 10 сцен)

---

## Success Metrics

### Learning Outcomes:
- **Персонализация:** 80%+ сцен в ZPD (не слишком легко/сложно)
- **Engagement:** Среднее время сессии рост на 30%
- **Success rate:** Стабильный 65-75% (optimal challenge)
- **Skill growth:** Все дети прогрессируют, но своим темпом

### Technical Metrics:
- **MAB convergence:** После 50 сцен система знает предпочтения (90% уверенность)
- **Difficulty accuracy:** ±0.1 от ZPD в 85% случаев
- **Exploration rate:** 10-15% (не застревать в локальном оптимуме)
- **API latency:** < 200ms (99 percentile)

### Clinical Markers:
- **Reduced frustration:** Quit rate снижение на 40%
- **Increased self-efficacy:** "Я могу!" feelings рост на 35%
- **Better learning retention:** Skill decay rate снижение на 25%
- **Personalized paths:** 60%+ детей проходят модули в нелинейном порядке

---

## Visualizations in Game

### 1. "Моя Карта Роста" (My Growth Map)
```
[SKILLS RADAR CHART]
      Emotion Literacy (0.65)
          /  |  \
    Mindfulness  DBT Skills
       /          \
 Boundaries    Communication
      \          /
     Self-Care

[Each skill grows visually as player progresses]
```

### 2. "Умный График" (Smart Dashboard)
```
[LINE CHART: Skill over time]
Emotion Literacy
  1.0 ┤
  0.8 ┤        ╱──
  0.6 ┤    ╱──
  0.4 ┤ ╱──
  0.2 ┤──
    Week 1  2  3  4

[Shows progress + projected growth]
```

### 3. "Зона Роста" (Growth Zone)
```
[ZPD VISUALIZATION]
       │ Too Hard (Frustration)
  ─────┼─────────────────────
   ✓   │ ← Your Zone (Perfect!)
  ─────┼─────────────────────
       │ Too Easy (Boredom)

[Real-time indicator where player is]
```

---

## Research Foundation

### References:
- **Reinforcement Learning:**
  - Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction
  - Thompson, W. R. (1933). On the likelihood that one unknown probability exceeds another

- **Adaptive Learning:**
  - Vygotsky, L. S. (1978). Mind in Society: Zone of Proximal Development
  - Koedinger, K. R., et al. (2013). The Knowledge-Learning-Instruction Framework

- **Educational Data Mining:**
  - Baker, R. S., & Inventado, P. S. (2014). Educational Data Mining and Learning Analytics
  - Pardos, Z. A., & Heffernan, N. T. (2010). Modeling Individualization in a Bayesian Networks Implementation of Knowledge Tracing

- **Game-Based Learning:**
  - Shute, V. J., et al. (2015). Stealth Assessment in Game-Based Learning
  - Dörner, R., et al. (2016). Serious Games: Foundations, Concepts and Practice

---

## Implementation Priority: HIGH

**Rationale:**
- **Enhances all modules** - не standalone, а meta-система
- **Addresses heterogeneity** - дети в PA очень разные
- **Increases engagement** - frustration/boredom = главные причины drop-off
- **Clinical benefit** - персонализация = лучшие outcomes
- **Technical feasibility** - MAB = proven, не экспериментально

**Dependencies:**
- Requires: Базовые модули (M01-M14) для data collection
- Enables: Optimal learning paths для всех детей
- Infrastructure: Vector DB, Redis, Python ML backend

**Phased Rollout:**
1. **Phase 1 (MVP):** Simple difficulty adjustment (без MAB, rule-based)
2. **Phase 2:** MAB для content selection (2-3 arms)
3. **Phase 3:** Full adaptive learning (10+ arms, learning style detection)
4. **Phase 4:** Predictive analytics (success forecasting)

**Next Steps:**
1. Implement basic profiling system
2. Collect baseline data (100+ kids, 2 weeks)
3. Train MAB models
4. A/B test: adaptive vs static curriculum

---

## Special Considerations

### Ethical & Privacy:
- **Data collection transparency:** Родители + дети должны знать, что собирается
- **Opt-out option:** Возможность отключить adaptive features
- **No discriminatory outcomes:** Мониторить, что все группы получают качественное обучение
- **Explainability:** "Почему мне показали эту сцену?" (transparency)

### Safety:
- **Clinical oversight:** Adaptive система НЕ заменяет терапевта
- **Red flags:** Если детектируется высокий риск → уведомление клинициста
- **Bias mitigation:** Регулярный аудит, что система не создаёт unfair advantages

---

## Summary

Module 16 - это **мета-система**, которая делает все остальные модули эффективнее через:
1. **Адаптивную сложность** (ZPD)
2. **Персонализированный контент** (learning style)
3. **Оптимальный тайминг** (когда показать что)
4. **Real-time profiling** (кто ты сейчас vs 5 минут назад)
5. **MAB оптимизацию** (learn from every child, improve for all)

Это НЕ отдельный игровой модуль, а **invisible engine**, который работает behind the scenes, делая игру умнее с каждым сыгранным сценарием.
