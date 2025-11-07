# Semantic Blocks Map: InnerWorld002.txt → Modules

## Overview
Этот документ картирует содержимое InnerWorld002.txt (база знаний игровых механик) к 23 модулям проекта InnerWorld Edu.

## Source File Analysis: InnerWorld002.txt (275KB, 32236 tokens)

### Block 1: CBT Game Mechanics (Lines 0-806)
**Темы:**
- Поведенческая активация (Behavioral Activation) - квесты с XP
- Журнал автоматических мыслей - мини-игра "Перепрошивка"
- Трёхминутная осознанность - breathing UI с таймером
- Лист оценки активности (Value × Pleasure) - 2D heatmap
- Мини-эксперимент - Random Challenge механика
- Система Love-Navigator для анализа паттернов в отношениях

**Соотносится с модулями:**
- **Module 03 (CBT)** ✓ - основная механика когнитивных искажений
- **Module 07 (ACT)** - Values clarification, defusion
- **Module 08 (Mindfulness)** - осознанность, дыхание
- **Module 22 (Loyalty Conflict)** - применение к отношениям родитель-ребенок

**Ключевые игровые элементы:**
```javascript
{
  "XP-система": "за выполненные действия",
  "Дневные миссии": "BA + мысль + дыхание",
  "Карта устойчивости": "mood chart на 7 дней",
  "Мини-игры": "Brick brainstorming"
}
```

### Block 2: DBT Skills for Distress Tolerance (Lines 807-899)
**Темы:**
- **ACCEPTS** навыки отвлечения (Activities, Contribute, Comparisons, Emotions, Push away, Thoughts, Sensations)
- **TIPP** техника (Temperature, Intense exercise, Paced breathing, Paired muscle relaxation)
- **Self-Soothing** через 5 органов чувств

**Соотносится с модулями:**
- **Module 02 (DBT Level 1)** ✓ - дистресс-толерантность
- **Module 11 (DBT Advanced)** - продвинутые навыки
- **Module 04 (Reality Bridge)** ✓ - микро-действия в реальности

**Random Challenge примеры:**
```json
{
  "ACCEPTS": "Сделай 1 действие из категории Contribute — помоги кому-то онлайн",
  "TIPP": "Устрой 30-секундную ледяную паузу: умыться / дотронуться до холодного",
  "Self-Soothing": "Послушай 2 мин звуки природы / Нюхни эфирное масло"
}
```

### Block 3: UCAM - Unified Cognitive-Affective Map (Lines 810-896)
**Концепция:** Общая система координат для всех психологических состояний и паттернов

**5 слоёв UCAM:**
1. **Эмо-ось** (8 базовых эмоций): Радость, Интерес, Спокойствие, Тревога, Грусть, Гнев, Стыд, Вина
2. **Когнитивная ошибка** (10+ типов): Catastrophizing, Mind-Reading, All-or-Nothing, Should-statements, etc.
3. **DBT/ACT-навык**: Check the Facts, Opposite Action, Wise Mind, Defusion, Values
4. **Love Style** (для сценариев отношений): Eros, Ludus, Storge, Pragma, Mania, Agape
5. **Attachment**: Secure, Anxious, Avoidant, Fearful-Avoidant

**Соотносится с модулями:**
- **ВСЕ модули** - это глобальная система тегирования
- **Module 06 (Decision Science)** ✓ - когнитивные искажения
- **Module 09 (Emotional Literacy)** - эмоциональная ось
- **Module 22 (Loyalty Conflict)** - attachment patterns
- **Module 14 (Communication Skills)** - love styles для отношений

**Ключевая структура:**
```json
{
  "emotion": "anxiety",
  "cbt": "mind_reading",
  "dbt": "check_the_facts",
  "love": "mania",
  "attachment": "anxious"
}
```

### Block 4: Relationship Scenarios with Cognitive Distortions (Lines 837-896)
**20+ готовых сценариев:**
- Сцена 11: "Не поставил лайк" (Mind-Reading + Mania)
- Сцена 12: "Опоздание на 30 мин" (Catastrophizing)
- Сцена 13: "Сюрприз-подарок" (Discount Positive)
- Сцена 14: "Предложение переехать" (Dependency)
- И др.

**Формат каждой сцены:**
- Вопрос + 3 варианта ответа (A = дисторсия 1, B = адаптивный, C = дисторсия 2)
- UCAM-теги
- Источник (цитата из Ильин Е.П.)

**Соотносится с модулями:**
- **Module 22 (Loyalty Conflict)** - адаптация сценариев для родитель-ребенок
- **Module 14 (Communication)** - здоровая коммуникация
- **Module 19 (Self-Care)** - boundaries

### Block 5: Vector Database Architecture (Lines 897-983)
**Концепция: VECTOR-MIND DB**

**Пайплайн:**
1. Ingestion-Crawler (PDF → text)
2. SCENE-Extractor (LLM + промпт)
3. Validator (JSON schema)
4. Vectorizer (embedding_text → 1536-D)
5. Tag-Encoder (UCAM → multi-hot)
6. Upsert в Qdrant/Pinecone
7. Online-Learner (RL-bandit)
8. Re-weigh Index (scene scoring)
9. Retrieval API

**Алгоритм подбора:**
```python
user_vec = weighted_avg(last_k_embeddings, weights=response_error)
bonus = one_hot['weak_skill'] * λ
res = qdrant.search(
    vector=user_vec + bonus,
    filter={"must_not": recent_seen_ids},
    top=5
)
```

**Соотносится с модулями:**
- **Module 23 (AI Integration)** - адаптивная система подбора контента
- **Module 16 (Adaptive Learning)** - персонализация пути
- **Все модули** - источник контента для векторной базы

**KPI метрики:**
- Therapy Gain: Δ% адаптивных ответов / 7 дней → ↑10%/нед
- Retrieval Precision: relevant_top-3/3 → >0.8
- Scene Fatigue: повторы/N → <15%
- Engagement: avg daily scenes → ≥4

### Block 6: SUPER-PROMPT for o3-pro (Lines 1095-1396)
**Финальный усиленный промпт для автоматической генерации сценариев из любых источников**

**Ключевые компоненты промпта:**
1. Роль эксперта (CBT + гейм-дизайн + векторная семантика)
2. Структура генерации (10 шагов)
3. UCAM-инструктаж (5 измерений)
4. Версионирование таксономии
5. Карта переходов (prereq_tags, followup_tags)
6. Контекст-триггеры
7. Мультиязычность
8. Валидация
9. Расширяемые поля

**JSON-схема выхода:**
```json
{
  "scene_id": "SRC-v1.0-page-hash",
  "ucam_schema": "v1.0",
  "lang": "ru",
  "question": "...",
  "answers": [...],
  "correct_index": 1,
  "display_order": [2,0,1],
  "embedding_text": "...",
  "embedding_strategy": "distortion_focus",
  "tags": {...},
  "context_trigger": {...},
  "prereq_tags": [...],
  "followup_tags": [...],
  "difficulty": 1-3,
  "expected_reward": 0.0-1.0,
  "citation": "...",
  "ext_tags": {...},
  "validation_checklist": {...},
  "new_tags": [],
  "tag_definitions": {}
}
```

**Соотносится с модулями:**
- **Module 23 (AI Integration)** - агент для генерации контента
- **Все исследовательские модули** - автоматизация создания контента

---

## Mapping to 23 Modules

### Уже созданные модули (используют InnerWorld002.txt):
1. ✅ **Module 01 (IFS)** - частично, нужно добавить UCAM-теги
2. ✅ **Module 02 (DBT)** - частично, добавить ACCEPTS, TIPP, Self-Soothing
3. ✅ **Module 03 (CBT)** - частично, добавить Love-Navigator, игровые механики
4. ✅ **Module 04 (Reality Bridge)** - добавить Random Challenge механику
5. ✅ **Module 05 (TRIZ)** - ok, но можно связать с UCAM
6. ✅ **Module 06 (Decision Science)** - обогатить UCAM-тегами когнитивных искажений

### Модули для создания (приоритет по содержимому InnerWorld002.txt):
7. 🔴 **Module 07 (ACT)** - есть контент: Values, Defusion, техники принятия
8. 🔴 **Module 08 (Mindfulness)** - есть контент: 3-минутная осознанность, STOPP
9. 🔴 **Module 09 (Emotional Literacy)** - UCAM эмо-ось, 8 базовых эмоций
10. ⚪ **Module 10 (Anger Management)** - нет прямого контента
11. 🔴 **Module 11 (DBT Advanced)** - продолжение DBT навыков
12. ⚪ **Module 12 (Anxiety Resilience)** - частично TIPP
13. ⚪ **Module 13 (Grief Processing)** - нет контента
14. 🔴 **Module 14 (Communication)** - сценарии отношений адаптировать
15. 🔴 **Module 15 (Conflict Resolution)** - связать с TRIZ
16. 🔴 **Module 16 (Adaptive Learning)** - RL-bandit алгоритм из векторной БД
17. ⚪ **Module 17 (Creative Expression)** - нет контента
18. ⚪ **Module 18 (Social Skills)** - частично сценарии
19. 🔴 **Module 19 (Self-Care & Boundaries)** - Behavioral Activation
20. ⚪ **Module 20 (Future Planning)** - нет контента
21. ⚪ **Module 21 (Resilience Building)** - частично
22. 🔴 **Module 22 (Loyalty Conflict)** - адаптация сценариев отношений для PA
23. 🔴 **Module 23 (AI Integration)** - SUPER-PROMPT, векторная БД архитектура

**Легенда:**
- ✅ Модуль создан
- 🔴 Богатый контент в InnerWorld002.txt (высокий приоритет)
- ⚪ Мало/нет контента (низкий приоритет, нужны другие источники)

---

## Next Steps

### Immediate Implementation Plans Needed:
1. **Module 07 (ACT)** - много контента про Values, Defusion
2. **Module 08 (Mindfulness)** - готовые техники дыхания, осознанности
3. **Module 09 (Emotional Literacy)** - UCAM эмо-ось
4. **Module 22 (Loyalty Conflict)** - адаптация relationship scenarios
5. **Module 23 (AI Integration)** - SUPER-PROMPT + векторная БД

### Content Enrichment for Existing Modules:
- **Module 02 (DBT)** ← добавить Block 2 (ACCEPTS, TIPP, Self-Soothing)
- **Module 03 (CBT)** ← добавить Block 1 (игровые механики)
- **Module 04 (Reality Bridge)** ← добавить Random Challenge из DBT
- **Module 06 (Decision Science)** ← интегрировать UCAM-теги

### Research Sources Still Needed:
- Module 10: Anger Management techniques
- Module 13: Grief processing for children
- Module 17: Creative/Art therapy
- Module 20: Future planning skills

---

## Technical Architecture Notes

### UCAM Integration Points:
Каждый модуль должен:
1. Тегировать техники по UCAM (emotion, cbt, dbt, love, attachment)
2. Указывать prereq_tags и followup_tags для навигации
3. Присваивать difficulty (1-3)
4. Определять context_trigger (когда применять)

### Vector DB Schema:
```typescript
interface Scene {
  scene_id: string;          // "MODULE##-v1.0-tech#-HASH"
  ucam_schema: string;       // "v1.0"
  module_id: string;         // "03_CBT", "22_LoyaltyConflict"
  technique_name: string;    // русское название техники
  embedding_text: string;    // для векторного поиска
  tags: UCAMTags;           // 5-мерная разметка
  prereq_tags: string[];    // условия показа
  followup_tags: string[];  // что тренировать дальше
  difficulty: 1|2|3;
  game_mechanics: GameMech; // квест, NPC, артефакт, локация
  reality_bridge: Action[]; // микро-действия в реальности
  school_subjects: SubjectLink[]; // связь с предметами
}
```

---

## Summary Stats

- **Total blocks identified:** 6
- **Lines analyzed:** 1396
- **Modules with rich content:** 9
- **Modules need other sources:** 6
- **Modules already complete:** 6
- **Implementation priority:** Modules 7, 8, 9, 22, 23
