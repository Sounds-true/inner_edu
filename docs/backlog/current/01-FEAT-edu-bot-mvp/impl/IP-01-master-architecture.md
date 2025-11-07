# Implementation Plan: InnerWorld Edu Bot - MVP Architecture

**Ticket:** `01-FEAT-edu-bot-mvp`
**Plan ID:** `IP-01-master-architecture`
**Date:** 2025-11-07
**Status:** Draft

---

## Смысл и цель задачи

Создать MVP Telegram-бота InnerWorld Edu, который превращает школьные уроки в игровые квесты с психологическими проработками для детей 7-14 лет. Бот должен интегрировать 23 психологических модуля через механику "урок → игровой квест → эмоциональная рефлексия → микро-действие в жизни". Основная цель - восстановление доверия к себе, особенно для детей с опытом родительского отчуждения.

---

## Архитектура решения

### Основные компоненты MVP

**1. Core Bot Layer** (`src/core/`)
- `bot.py` - основной Telegram bot handler (python-telegram-bot)
- `config.py` - конфигурация (env variables, константы)
- `state_manager.py` - управление состоянием пользователя
- `logger.py` - структурированное логирование

**2. Educational Layer** (`src/edu/`)
- `curriculum/` - интеграция со школьной программой (ФГОС)
  - `fgos_mapper.py` - маппинг предметов → модули
  - `homework_detector.py` - распознавание домашних заданий
- `quest_engine.py` - генерация и управление квестами
- `module_loader.py` - загрузка психологических модулей

**3. Game Mechanics** (`src/game/`)
- `npc_system.py` - NPC-проводники (Архитектор, Музыкант, Лис, Эхо)
- `location_manager.py` - управление эмоциональной картой мира
- `progress_tracker.py` - отслеживание прогресса (Ноты Доверия, артефакты)
- `artifact_system.py` - система наград и артефактов

**4. Psychological Integration** (`src/psychology/`)
- `module_registry.py` - реестр 23 модулей с метаданными
- `intervention_engine.py` - выбор и применение психо-техник
- `emotional_check.py` - эмоциональные чек-ины
- `reality_bridge.py` - генерация микро-действий

**5. Content & Data** (`src/data/`)
- `quest_library/` - библиотека готовых квестов (JSON/YAML)
- `npc_dialogues/` - диалоги NPC по модулям
- `module_metadata.json` - метаданные 23 модулей
- `scenarios/` - сценарии для разных триггеров

**6. Storage** (`src/storage/`)
- `user_profile.py` - профили детей (возраст, прогресс)
- `session_store.py` - хранение сессий и состояния
- `simple_db.py` - простая JSON-based БД для MVP (позже Postgres)

### Структура файлов

```
inner_edu/
├── main.py                      # Entry point
├── requirements.txt
├── .env.example
├── src/
│   ├── core/
│   │   ├── bot.py
│   │   ├── config.py
│   │   ├── state_manager.py
│   │   └── logger.py
│   ├── edu/
│   │   ├── curriculum/
│   │   │   ├── fgos_mapper.py
│   │   │   └── homework_detector.py
│   │   ├── quest_engine.py
│   │   └── module_loader.py
│   ├── game/
│   │   ├── npc_system.py
│   │   ├── location_manager.py
│   │   ├── progress_tracker.py
│   │   └── artifact_system.py
│   ├── psychology/
│   │   ├── module_registry.py
│   │   ├── intervention_engine.py
│   │   ├── emotional_check.py
│   │   └── reality_bridge.py
│   ├── storage/
│   │   ├── user_profile.py
│   │   ├── session_store.py
│   │   └── simple_db.py
│   └── data/
│       ├── quest_library/
│       ├── npc_dialogues/
│       ├── module_metadata.json
│       └── scenarios/
└── docs/
    ├── modules/              # 23 модуля (уже есть)
    └── backlog/
```

---

## Полный flow работы функционала

### 1. Онбординг (первый запуск)
1. Ребенок запускает `/start`
2. Бот приветствует от имени NPC "Ребёнок-Эхо"
3. Собирает базовую информацию: возраст (7-10 или 11-14), класс
4. Показывает эмоциональную карту мира (текстовое описание + эмодзи)
5. Предлагает первый квест "Знакомство с Городом Доверия"
6. Создает профиль пользователя

### 2. Триггерный сценарий: "Домашнее задание"
1. Ребенок пишет: "У меня домашка по русскому, не знаю как делать"
2. `homework_detector.py` распознает: предмет=русский язык, эмоция=растерянность
3. `fgos_mapper.py` находит связь: Русский язык → Модуль 06 (Decision Science)
4. `quest_engine.py` генерирует квест "Детектив Фактов" (факты vs мнения)
5. NPC "Зеркальный Лис" появляется в чате
6. Квест: найти в тексте учебника 3 факта и 3 мнения
7. Ребенок выполняет квест (пишет ответы)
8. `intervention_engine.py` применяет технику из Модуля 06
9. Эмоциональный чек-ин: "Как ты себя чувствуешь после квеста?"
10. `reality_bridge.py` предлагает микро-действие: "Сегодня найди 1 факт в новостях"
11. `progress_tracker.py` начисляет +1 Нота Доверия, выдает артефакт "Лупа Правды"
12. Обновление эмоциональной карты

### 3. Триггерный сценарий: "Эмоциональный кризис"
1. Ребенок пишет: "Мне грустно, не хочу ни с кем говорить"
2. `emotional_check.py` детектирует: эмоция=грусть, интенсивность=высокая
3. `intervention_engine.py` выбирает Модуль 08 (Mindfulness) или Модуль 02 (DBT)
4. NPC "Музыкант Сердца" появляется
5. Предлагает мини-упражнение: "Дыхание 4-6" (TIPP из DBT)
6. Визуализация через текст + эмодзи: "Вдох...1...2...3...4..."
7. После упражнения: "Стало легче? Выбери эмодзи своего состояния"
8. Если состояние улучшилось → закрыть сессию с поддержкой
9. Если не помогло → предложить написать "письмо Грусти" (IFS)
10. Reality Bridge: "Когда снова станет грустно - вспомни это дыхание"

### 4. Триггерный сценарий: "Игровое исследование"
1. Ребенок пишет: `/map` (хочет исследовать мир)
2. `location_manager.py` показывает доступные локации
3. Выбирает "Башня Эха" (Модуль 06 - манипуляции)
4. Встречает NPC "Зеркальный Лис"
5. Лис предлагает квест: "Игра в детектива обмана"
6. Серия мини-сценариев с когнитивными искажениями
7. За каждый правильный ответ - очки опыта
8. Разблокировка новых этажей Башни
9. Получение артефакта "Зеркало Правды"

### 5. Прогрессия и персонализация
1. Каждые 3 дня - эмоциональный чек-ин от NPC
2. Адаптация сложности квестов по возрасту (7-10 проще, 11-14 сложнее)
3. Отслеживание триггеров: какие темы/модули актуальны
4. Рекомендация следующих модулей на основе истории
5. Еженедельный отчет: "Твой прогресс за неделю" с графом навыков

---

## API и интерфейсы

### Core Bot API

**`EduBot.start(update, context)`**
- Обработка команды `/start`
- Параметры: telegram update, context
- Возвращает: приветственное сообщение + inline keyboard
- Создает профиль пользователя если не существует

**`EduBot.handle_message(update, context)`**
- Обработка всех текстовых сообщений
- Параметры: telegram update, context
- Определяет тип сообщения (homework, emotional, question)
- Маршрутизирует в соответствующий handler

**`EduBot.handle_callback(update, context)`**
- Обработка inline button нажатий
- Параметры: callback_query, context
- Парсит callback_data (формат: `action:entity_id`)
- Возвращает: обновленное сообщение или новый квест

### Quest Engine API

**`QuestEngine.generate_quest(user_id, trigger_type, context_data)`**
- Генерация квеста на основе триггера
- Параметры: ID пользователя, тип триггера (homework/emotion/explore), контекст
- Возвращает: объект Quest с steps, npc, module_id
- Ошибки: InvalidTriggerError если триггер неизвестен

**`QuestEngine.validate_answer(quest_id, step_id, user_answer)`**
- Проверка ответа пользователя
- Параметры: ID квеста, ID шага, ответ
- Возвращает: feedback (текст обратной связи), is_correct (bool), next_step
- Применяет психологическую технику из модуля

**`QuestEngine.complete_quest(quest_id)`**
- Завершение квеста
- Параметры: ID квеста
- Возвращает: rewards (Ноты Доверия, артефакты), emotional_check
- Обновляет прогресс пользователя

### Module Registry API

**`ModuleRegistry.get_module(module_id)`**
- Получение метаданных модуля
- Параметры: ID модуля (01-23)
- Возвращает: Module объект (name, techniques, npc, school_subjects)
- Ошибки: ModuleNotFoundError

**`ModuleRegistry.find_by_subject(subject_name)`**
- Поиск модулей по школьному предмету
- Параметры: название предмета ("Русский язык", "Математика")
- Возвращает: список Module объектов
- Используется для маппинга homework → модули

**`ModuleRegistry.find_by_emotion(emotion, intensity)`**
- Поиск модулей по эмоции
- Параметры: эмоция (грусть, страх, злость), интенсивность (1-10)
- Возвращает: приоритизированный список Module объектов
- Логика: высокая интенсивность → DBT, средняя → CBT/IFS

### NPC System API

**`NPCSystem.get_npc(npc_id)`**
- Получение NPC по ID
- Параметры: npc_id ("architect", "musician", "fox", "echo")
- Возвращает: NPC объект (name, greeting, personality, modules)

**`NPCSystem.generate_dialogue(npc_id, context, user_state)`**
- Генерация диалога NPC
- Параметры: ID NPC, контекст квеста, состояние пользователя
- Возвращает: текст диалога персонализированный под возраст
- Использует шаблоны из `data/npc_dialogues/`

### Emotional Check API

**`EmotionalCheck.detect_emotion(message_text)`**
- Простое распознавание эмоции из текста
- Параметры: текст сообщения
- Возвращает: emotion (название), intensity (1-10), keywords (триггерные слова)
- Метод: keyword matching (MVP), позже NLP

**`EmotionalCheck.run_check_in(user_id)`**
- Запуск эмоционального чек-ина
- Параметры: ID пользователя
- Возвращает: check-in вопросы, inline keyboard с эмодзи
- Сохраняет результаты в профиль

### Reality Bridge API

**`RealityBridge.generate_micro_action(module_id, user_age, context)`**
- Генерация микро-действия
- Параметры: ID модуля, возраст, контекст квеста
- Возвращает: текст действия, expected_time (в минутах), difficulty
- Выбирает из 130 микро-действий Модуля 04

**`RealityBridge.check_completion(user_id, action_id)`**
- Запрос о выполнении действия (через день)
- Параметры: ID пользователя, ID действия
- Возвращает: reminder сообщение с вопросом "Ты попробовал?"
- Не требует доказательств (система честности)

---

## Взаимодействие компонентов

### Основной flow: Homework → Quest

```
User (Telegram)
  → EduBot.handle_message()
  → HomeworkDetector.parse(text)
  → FGOSMapper.map_to_modules(subject)
  → QuestEngine.generate_quest(trigger="homework")
  → ModuleRegistry.get_module(id)
  → NPCSystem.get_npc(module.npc_id)
  → QuestEngine.create_steps(module.techniques)
  → Bot sends quest to User

User answers
  → EduBot.handle_message()
  → QuestEngine.validate_answer()
  → InterventionEngine.apply_technique(module, answer)
  → EmotionalCheck.run_check_in()
  → RealityBridge.generate_micro_action()
  → ProgressTracker.update(user_id, rewards)
  → Bot sends feedback + rewards
```

### Эмоциональный кризис flow

```
User writes emotional message
  → EmotionalCheck.detect_emotion(text)
  → if intensity > 7:
      → InterventionEngine.select_module(emotion, intensity)
      → ModuleRegistry.get_module() [DBT или Mindfulness]
      → NPCSystem.get_npc("musician")
      → QuestEngine.generate_quest(trigger="emotional_crisis")
      → Mini-exercise (breathing, grounding)
  → EmotionalCheck.run_check_in() [after exercise]
  → if improved: close with support
  → if not: escalate to IFS technique or safety protocol
```

### Периодический чек-ин flow

```
CronJob (every 3 days)
  → EmotionalCheck.run_check_in(user_id)
  → Bot sends: "Привет! Как ты себя чувствуешь?"
  → User selects emoji
  → ProgressTracker.record_emotion(user_id, emotion, timestamp)
  → if negative emotion → suggest quest
  → if positive → celebrate + optional new quest
```

---

## Порядок реализации

### Phase 1: Core Foundation (Week 1)
1. Настроить Telegram bot skeleton (`core/bot.py`, `core/config.py`)
2. Реализовать `storage/simple_db.py` (JSON file storage)
3. Реализовать `storage/user_profile.py` (create, read, update user)
4. Создать базовые команды: `/start`, `/help`, `/map`
5. Реализовать `core/state_manager.py` (ConversationHandler states)

### Phase 2: Module Integration (Week 2)
1. Создать `data/module_metadata.json` на основе 23 модулей
2. Реализовать `psychology/module_registry.py` (load, get, find modules)
3. Реализовать `edu/curriculum/fgos_mapper.py` (subject → modules mapping)
4. Создать 3-5 простых квестов в `data/quest_library/` (JSON format)
5. Реализовать `edu/quest_engine.py` (load, generate simple quest)

### Phase 3: NPC System (Week 2-3)
1. Создать диалоги для 4 NPC в `data/npc_dialogues/` (по 5-10 фраз каждого)
2. Реализовать `game/npc_system.py` (load NPC, generate dialogue)
3. Интегрировать NPC в квесты
4. Реализовать `game/location_manager.py` (5 основных локаций)
5. Добавить команду `/map` с визуализацией через эмодзи

### Phase 4: Quest Mechanics (Week 3)
1. Реализовать `edu/quest_engine.py` полностью (validate_answer, complete)
2. Реализовать `psychology/intervention_engine.py` (apply technique based on module)
3. Создать 10-15 квестов покрывающих Модули 01-06
4. Реализовать `game/progress_tracker.py` (Ноты Доверия, уровни)
5. Реализовать `game/artifact_system.py` (награды, инвентарь)

### Phase 5: Emotional & Reality Bridge (Week 4)
1. Реализовать `psychology/emotional_check.py` (detect, check-in)
2. Реализовать `psychology/reality_bridge.py` (generate micro-action)
3. Добавить автоматические чек-ины (через 3 дня после квеста)
4. Интегрировать Reality Bridge в конец каждого квеста
5. Реализовать систему напоминаний о микро-действиях

### Phase 6: Homework Integration (Week 4-5)
1. Реализовать `edu/curriculum/homework_detector.py` (keyword matching)
2. Создать квесты для 5 школьных предметов
3. Интегрировать homework trigger в основной flow
4. Добавить адаптацию по возрасту (7-10 vs 11-14)
5. Создать команду `/homework` для явного запроса помощи

### Phase 7: Polish & Testing (Week 5)
1. Добавить error handling и fallback сценарии
2. Улучшить тексты и форматирование сообщений
3. Добавить inline keyboards для всех квестов
4. Ручное тестирование всех 3 основных flow
5. Создать документацию для пользователей

### Phase 8: Deployment (Week 6)
1. Настроить production конфиг (.env)
2. Задеплоить на сервер (Render/Railway/VPS)
3. Настроить логирование и мониторинг
4. Запустить alpha-тест с 5-10 детьми
5. Собрать обратную связь и итерировать

---

## Критичные граничные случаи

### 1. Эмоциональный кризис высокой интенсивности
**Ситуация:** Ребенок пишет о суицидальных мыслях или самоповреждении
**Решение:**
- `emotional_check.py` детектирует красные флаги (ключевые слова)
- Немедленно показать сообщение: "Мне кажется, тебе сейчас очень тяжело. Вот номер телефона доверия: 8-800-2000-122"
- Логировать событие с высоким приоритетом
- НЕ продолжать квест, НЕ применять психологические техники
- Рекомендовать обратиться к взрослому (родитель, учитель, психолог)

### 2. Ребенок застрял в квесте
**Ситуация:** Не может ответить на вопрос квеста, пишет "не знаю" 3+ раза
**Решение:**
- После 2 попытки: дать подсказку от NPC
- После 3 попытки: предложить пропустить шаг
- После 4 попытки: завершить квест с частичными наградами
- НЕ наказывать, НЕ снижать прогресс
- Предложить альтернативный квест на ту же тему

### 3. Некорректный ввод (мат, спам, бессмыслица)
**Ситуация:** Ребенок шлет неадекватные сообщения
**Решение:**
- Игнорировать мат (не реагировать, не ругать)
- На спам (10+ сообщений за минуту): мягкое сообщение "Кажется, ты торопишься. Давай замедлимся?"
- На бессмыслицу: переспросить 1 раз, затем предложить команду `/help`
- НЕ блокировать пользователя (MVP)

### 4. Родитель пытается использовать бота
**Ситуация:** Взрослый человек начинает общаться (по языку/содержанию видно)
**Решение:**
- На онбординге спросить: "Тебе сколько лет?" (валидация 7-14)
- Если > 14 или < 7: "Этот бот создан для детей 7-14 лет. Для родителей есть другой бот: @pas_in_peace_bot"
- Разрешить продолжить если хотят "попробовать за ребенка"
- Логировать для аналитики

### 5. Данные пользователя повреждены/утеряны
**Ситуация:** JSON файл профиля поврежден или удален
**Решение:**
- При загрузке профиля: try/except с fallback на создание нового
- Показать сообщение: "К сожалению, твой прогресс потерялся. Но мы можем начать заново!"
- НЕ крешить бота
- Логировать ошибку для исправления

---

## Объем работ

### Что входит в MVP:

✅ **Telegram bot с 4 NPC и 5 локациями**
✅ **3 триггерных сценария:** homework, emotional, explore
✅ **15-20 квестов** покрывающих Модули 01-06, 08, 09
✅ **Интеграция с 23 модулями** через метаданные
✅ **Система прогресса:** Ноты Доверия, артефакты, уровни
✅ **Эмоциональные чек-ины** (автоматические каждые 3 дня)
✅ **Reality Bridge:** генерация микро-действий
✅ **ФГОС маппинг:** 5 предметов (русский, литература, математика, история, музыка)
✅ **Адаптация по возрасту:** 7-10 vs 11-14 лет
✅ **Safety protocol:** детекция кризисов, телефон доверия

### Что НЕ входит в MVP:

❌ Векторная БД (Qdrant) - будет в v2
❌ ML/NLP для продвинутого распознавания эмоций
❌ Адаптивное обучение через RL (Модуль 16)
❌ Голосовые сообщения и аудио-упражнения
❌ Групповые квесты и социальные функции
❌ Web-приложение с визуальной картой
❌ Интеграция с реальными школами
❌ Родительская панель управления
❌ Автоматическая генерация контента через LLM
❌ Покрытие всех 23 модулей квестами (только 8-10 модулей)

---

## Допущения

1. **Telegram как платформа достаточна для MVP** - не требуется web/mobile app
2. **JSON-based storage достаточна** для 50-100 пользователей в alpha-тесте
3. **Keyword matching достаточен** для детекции эмоций и homework (не нужен NLP)
4. **Готовые диалоги NPC** (не генеративные) достаточны для MVP
5. **Квесты создаются вручную** (не автогенерация через LLM)
6. **Дети 7-14 лет умеют печатать** на телефоне/компьютере
7. **Родители дали разрешение** ребенку пользоваться ботом
8. **Интернет доступен** у пользователей (нет offline режима)
9. **Русский язык** как основной (без локализации)
10. **Один ребенок = один Telegram аккаунт** (нет multi-user profiles)

---

## Открытые вопросы

1. **Parental Consent:** Как получать согласие родителей на обработку данных детей? (COPPA/GDPR)
2. **Safety Monitoring:** Нужен ли автоматический алерт психологу при красных флагах?
3. **Age Verification:** Как валидировать возраст (самоотчет достаточен или нужна проверка)?
4. **Content Moderation:** Нужно ли хранить все сообщения для аудита или только метрики?
5. **Crisis Protocol:** Какой именно телефон доверия использовать (регион-специфичен)?
6. **Gamification Balance:** Сколько Нот Доверия давать за квест (не слишком много/мало)?
7. **Quest Difficulty:** Как точно определить сложность для 7-10 vs 11-14 лет?
8. **Privacy:** Можно ли хранить переписку или только анонимизированные метрики?

---

## Acceptance Criteria

### Критерии приемки MVP:

**Онбординг:**
- [ ] Ребенок может запустить `/start` и пройти приветствие
- [ ] Бот собирает возраст и класс
- [ ] Создается профиль пользователя с начальным состоянием

**Homework Scenario:**
- [ ] Ребенок пишет "У меня домашка по математике"
- [ ] Бот предлагает квест связанный с Модулем 03 (CBT) или 12 (Math-specific)
- [ ] NPC появляется и ведет квест
- [ ] Ребенок отвечает на вопросы квеста
- [ ] Бот дает feedback и начисляет Ноты Доверия
- [ ] Предлагается микро-действие из Reality Bridge

**Emotional Scenario:**
- [ ] Ребенок пишет "Мне грустно"
- [ ] Бот детектирует эмоцию (грусть)
- [ ] Предлагает мини-упражнение (дыхание или grounding)
- [ ] Запускает эмоциональный чек-ин после упражнения
- [ ] Если улучшение - поддержка, если нет - предложение квеста

**Explore Scenario:**
- [ ] Ребенок пишет `/map`
- [ ] Бот показывает 5 локаций с описаниями
- [ ] Ребенок выбирает локацию
- [ ] Появляется соответствующий NPC
- [ ] Предлагается квест из этой локации

**Progress Tracking:**
- [ ] Прогресс сохраняется после каждого квеста
- [ ] Команда `/progress` показывает: Ноты Доверия, артефакты, completed quests
- [ ] Уровень пользователя растет с прогрессом

**Safety:**
- [ ] При красных флагах (суицид, самоповреждение) показывается телефон доверия
- [ ] Квест НЕ продолжается в кризисной ситуации

### Ручной сценарий проверки:

1. Запустить бота: `/start` → проверить онбординг
2. Написать: "Не хочу делать математику" → проверить homework flow
3. Пройти квест до конца → проверить rewards
4. Написать: "Мне страшно" → проверить emotional flow
5. Написать: `/map` → проверить explore flow
6. Написать: `/progress` → проверить отображение прогресса
7. Написать красный флаг → проверить safety protocol
8. Подождать 3 дня → проверить автоматический чек-ин

---

## Definition of Done

- [ ] Код всех компонентов из Architecture добавлен в `src/`
- [ ] Конфиг `.env.example` с описанием переменных
- [ ] `requirements.txt` с зависимостями
- [ ] `README.md` в корне с инструкцией запуска
- [ ] Логирование всех критичных событий (quest start/complete, errors, red flags)
- [ ] Метрики: счетчик started quests, completed quests, emotional check-ins
- [ ] Feature flag `EDU_BOT_ENABLED=true/false` для включения/выключения
- [ ] 15-20 квестов в `data/quest_library/`
- [ ] Диалоги для 4 NPC в `data/npc_dialogues/`
- [ ] `data/module_metadata.json` заполнен для всех 23 модулей
- [ ] Ручное тестирование всех acceptance criteria пройдено
- [ ] Документация для пользователей: `/help` команда с инструкциями

---

## Минимальные NFR для MVP

### Производительность:
- Ответ бота на сообщение: < 3 секунды
- Генерация квеста: < 5 секунд
- Поддержка: до 100 одновременных пользователей
- Размер JSON профиля: < 100KB на пользователя

### Надежность:
- Uptime: 95% (допустимы кратковременные падения в alpha)
- Ошибки при запуске: < 1% (graceful degradation)
- Потеря данных: 0% (обязательно сохранение всех профилей)

### Ограничения по ресурсам:
- RAM: до 512MB (для 100 пользователей)
- CPU: 1 vCPU достаточно
- Disk: 1GB для логов + профилей
- Telegram API: 30 сообщений/секунду (лимит Telegram)

---

## Требования безопасности

### Секреты:
- [ ] `TELEGRAM_BOT_TOKEN` только из `.env` (НЕ хардкодить)
- [ ] `.env` в `.gitignore`
- [ ] `.env.example` без реальных значений

### Приватность:
- [ ] НЕ логировать полные сообщения детей (только метаданные)
- [ ] НЕ логировать PII (имена, фамилии, телефоны)
- [ ] Хешировать `user_id` в логах

### Внешние запросы:
- [ ] Только к Telegram API (api.telegram.org)
- [ ] Никаких других внешних API в MVP

---

## Наблюдаемость

### Логи:
- `INFO`: quest started, quest completed, emotional check-in, module loaded
- `WARNING`: unknown message type, invalid user input, module not found
- `ERROR`: failed to save profile, telegram API error, exception in handler
- `CRITICAL`: red flag detected (суицид, самоповреждение)

Формат: structured JSON logs

### Метрики:
- `quests_started_total` (counter)
- `quests_completed_total` (counter)
- `emotional_checkins_total` (counter)
- `red_flags_detected_total` (counter)
- `modules_used` (histogram by module_id)
- `user_age_distribution` (histogram)

### Трассировка:
- Span начало: user sends message
- Span конец: bot sends response
- Включить trace_id в логи для корреляции

---

## Релиз

### Feature Flag:
- Переменная `EDU_BOT_ENABLED=true` в `.env`
- При `false` - бот отвечает: "Бот временно недоступен. Попробуй позже."

### План развертывания:
1. **Local testing:** разработчик тестирует локально
2. **Staging deploy:** на test Telegram bot (отдельный токен)
3. **Alpha test:** 5-10 детей (знакомые разработчика)
4. **Beta test:** 50-100 детей (через сообщества родителей)
5. **Production:** публичный запуск

### Окружения:
- **Development:** локальная машина
- **Staging:** Render/Railway (бесплатный tier)
- **Production:** Render/Railway (платный tier с гарантиями)

---

## Откат

### Условия отката:
- Критичная ошибка блокирующая работу > 50% пользователей
- Детекция красных флагов не работает (safety-critical)
- Потеря данных пользователей

### Шаги отката:
1. Установить `EDU_BOT_ENABLED=false` через `.env`
2. Перезапустить бот
3. Бот показывает сообщение: "Технические работы. Вернемся скоро!"
4. Исправить проблему в dev
5. Повторный deploy через staging
6. Установить `EDU_BOT_ENABLED=true`

### Откат данных:
- JSON профили хранятся в `data/profiles/` с timestamp backup
- При критичной ошибке: восстановить из последнего backup (daily)
- Потеря данных максимум за 24 часа

---

## Риски и митигации

### Риск 1: Дети не понимают квесты (слишком сложно)
**Митигация:**
- A/B тест формулировок в alpha
- Адаптация по возрасту 7-10 (проще) vs 11-14
- Feedback от детей: "Квест был понятен?" после каждого

### Риск 2: Низкая вовлеченность (дети бросают после 1-2 квестов)
**Митигация:**
- Gamification: Ноты Доверия, артефакты, уровни
- Персонализация: NPC запоминают прогресс
- Напоминания: чек-ины каждые 3 дня

### Риск 3: Safety protocol не сработает (пропущен красный флаг)
**Митигация:**
- Extensive keyword list для детекции
- Manual review логов каждую неделю
- Консультация с психологом для улучшения детекции

### Риск 4: Telegram заблокирует бота (нарушение ToS)
**Митигация:**
- Следовать Telegram Bot API Guidelines
- Не спамить пользователей (max 1 сообщение в день)
- Parental consent disclaimer в `/start`

### Риск 5: Родители недовольны (privacy concerns)
**Митигация:**
- Прозрачная privacy policy в `/help`
- Минимальный сбор данных (только необходимое)
- Возможность удалить все данные: `/delete_my_data`

### Риск 6: JSON storage не масштабируется (>100 пользователей)
**Митигация:**
- Мониторинг производительности
- План миграции на SQLite при 50 пользователей
- План миграции на PostgreSQL при 500 пользователей

---

## Параметры стека

### Язык и версии:
- Python 3.11+
- python-telegram-bot 20.x

### Фреймворк:
- python-telegram-bot (async)
- pydantic для валидации данных

### База данных:
- JSON files (MVP)
- Драйвер: стандартная библиотека `json`
- Миграция на SQLite в v2

### Целевая платформа:
- Render.com (рекомендовано) - бесплатный tier для alpha
- Альтернатива: Railway.app, PythonAnywhere, VPS

### Зависимости:
```
python-telegram-bot==20.7
pydantic==2.5.0
python-dotenv==1.0.0
```

---

## Самопроверка плана

- [x] Нет кода и псевдокода - выполнено
- [x] Заполнены scope, acceptance, risk, release - выполнено
- [x] Формат `01-FEAT-edu-bot-mvp` следует naming conventions - выполнено
- [x] Нет секретов и приватных URL - выполнено
- [x] Все пути в POSIX-формате - выполнено
- [x] Язык: русский - выполнено

---

## Проверки перед "ломкой" API

- [x] Новый проект - нет внешних потребителей API
- [x] Нет зависимых задач в спринте

---

## Профиль языка

- **primary_language:** python
- **stdlib_preferred:** true
- **note:** Используем минимум зависимостей, предпочитаем стандартную библиотеку где возможно
