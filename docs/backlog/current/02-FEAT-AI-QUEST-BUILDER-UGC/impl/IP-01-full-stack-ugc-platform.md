# Implementation Plan: AI Quest Builder UGC Platform

**Файл:** `docs/backlog/current/02-FEAT-AI-QUEST-BUILDER-UGC/impl/IP-01-full-stack-ugc-platform.md`

---

## Смысл и цель задачи

Трансформировать InnerWorld Edu из монолитного бота с фиксированными квестами в UGC-платформу, где родители создают и делятся образовательными квестами для своих детей. Основная ценность - упрощение создания качественных квестов через разговор с AI-агентом, который автоматически встраивает психологические методы и проверяет контент на безопасность. Результат: масштабируемая платформа с сообществом создателей квестов и библиотекой проверенных образовательных сценариев.

---

## Архитектура решения

### Компоненты системы

**Backend (FastAPI + PostgreSQL):**
- `backend/api/` - REST API endpoints
- `backend/quest_builder/` - AI Quest Builder Agent (GPT-4)
- `backend/moderation/` - двухслойная модерация контента
- `backend/database/` - SQLAlchemy модели и миграции
- `backend/storage/` - управление YAML квестами

**Frontend (React + TypeScript + React Flow):**
- `frontend/components/AIQuestBuilder/` - разговорный интерфейс + node-based визуализация
- `frontend/components/QuestFlowCanvas/` - React Flow канвас для графов квестов
- `frontend/components/NodeEditor/` - редактор отдельного узла графа
- `frontend/components/QuestFeed/` - лента квестов от сообщества
- `frontend/components/ParentDashboard/` - мониторинг прогресса ребенка
- `frontend/components/QuestPreview/` - линейный предпросмотр и редактирование

**Telegram Bot (обертка):**
- `bot/telegram_bot.py` - тонкий слой над StateManager
- Поддержка всех существующих функций (Phases 1-4)
- Интеграция с Reality Bridge напоминаниями

**Интеграция с существующим кодом:**
- Используем готовый `src/orchestration/state_manager.py`
- Используем `src/game/quest_engine.py` для выполнения квестов
- Используем `src/game/reality_bridge_manager.py` для напоминаний
- Добавляем новый слой для хранения и управления UGC

### Файловая структура

```
/home/user/inner_edu/
├── backend/                    # Новый FastAPI бэкенд
│   ├── api/
│   │   ├── quests.py          # CRUD для квестов
│   │   ├── users.py           # Управление пользователями
│   │   └── builder.py         # API для AI Quest Builder
│   ├── quest_builder/
│   │   ├── agent.py           # QuestBuilderAgent
│   │   └── templates.py       # Промпты и шаблоны
│   ├── moderation/
│   │   ├── content_filter.py  # OpenAI Moderation API
│   │   └── safety_checker.py  # GPT-4 проверки
│   ├── database/
│   │   ├── models.py          # SQLAlchemy модели
│   │   └── migrations/        # Alembic миграции
│   └── main.py                # FastAPI app
├── frontend/                   # Новый React фронтенд
│   ├── src/
│   │   ├── components/
│   │   │   ├── AIQuestBuilder/ # Разговорный интерфейс + граф
│   │   │   │   ├── index.tsx
│   │   │   │   ├── ChatPanel.tsx
│   │   │   │   └── GraphPanel.tsx
│   │   │   ├── QuestFlowCanvas/ # React Flow визуализация
│   │   │   │   ├── index.tsx
│   │   │   │   ├── nodes/       # Кастомные типы узлов
│   │   │   │   │   ├── StartNode.tsx
│   │   │   │   │   ├── QuestStepNode.tsx
│   │   │   │   │   ├── ChoiceNode.tsx
│   │   │   │   │   └── RealityBridgeNode.tsx
│   │   │   │   └── edges/       # Кастомные связи
│   │   │   ├── NodeEditor/      # Редактор узла
│   │   │   │   └── index.tsx
│   │   │   ├── QuestFeed/      # Лента квестов
│   │   │   ├── ParentDashboard/# Дашборд родителя
│   │   │   └── QuestPreview/   # Линейный предпросмотр
│   │   ├── api/               # Клиент для backend API
│   │   ├── types/             # TypeScript типы
│   │   │   ├── quest.ts
│   │   │   └── graph.ts
│   │   └── App.tsx
│   └── package.json
├── bot/                        # Telegram обертка
│   └── telegram_bot.py
└── src/                        # Существующий код (Phases 1-4)
    ├── orchestration/
    ├── game/
    └── ...
```

### Visual Node-Based Interface

**Концепция:**
Квесты визуализируются как граф узлов (майнд-карта), где каждый узел - это шаг истории, а связи показывают возможные пути развития сюжета. AI генерирует граф автоматически, родитель видит всю структуру сразу и может редактировать визуально.

**Типы узлов:**

1. **StartNode (Начало)** - зеленый круг
   - Стартовая точка квеста
   - Содержит: название квеста, описание
   - Одна исходящая связь

2. **QuestStepNode (Шаг квеста)** - синий прямоугольник
   - Обычный шаг с диалогом
   - Содержит: текст диалога, персонаж (NPC), психологический метод
   - Одна или несколько исходящих связей

3. **ChoiceNode (Выбор)** - желтый ромб
   - Точка ветвления сюжета
   - Содержит: вопрос, варианты ответов (2-3)
   - Несколько исходящих связей (по одной на вариант)

4. **RealityBridgeNode (Reality Bridge)** - фиолетовый шестиугольник
   - Задание в реальном мире
   - Содержит: описание задания, дедлайн (часы), напоминание
   - Одна исходящая связь (или конечный узел)

5. **EndNode (Завершение)** - красный круг
   - Финал квеста
   - Содержит: заключительное сообщение, награда (XP)
   - Нет исходящих связей

**Структура данных графа:**

```
{
  "nodes": [
    {
      "id": "start_1",
      "type": "start",
      "position": {"x": 250, "y": 50},
      "data": {
        "title": "Тайна фотосинтеза",
        "description": "Узнай, как растения получают энергию"
      }
    },
    {
      "id": "step_1",
      "type": "questStep",
      "position": {"x": 250, "y": 150},
      "data": {
        "character": "wise_owl",
        "location": "forest_memory",
        "psychological_method": "metaphor",
        "dialogue": "Привет! Видишь этот лист? Он как солнечная батарейка..."
      }
    },
    {
      "id": "choice_1",
      "type": "choice",
      "position": {"x": 250, "y": 300},
      "data": {
        "question": "Хочешь узнать, как это работает?",
        "options": [
          {"text": "Да, интересно!", "next": "step_2"},
          {"text": "Расскажи позже", "next": "step_3"}
        ]
      }
    }
  ],
  "edges": [
    {"id": "e1", "source": "start_1", "target": "step_1", "animated": true},
    {"id": "e2", "source": "step_1", "target": "choice_1"},
    {"id": "e3", "source": "choice_1", "target": "step_2", "label": "Да"},
    {"id": "e4", "source": "choice_1", "target": "step_3", "label": "Нет"}
  ]
}
```

**React Flow интеграция:**

Используем библиотеку `reactflow` (MIT license, opensource):
- Drag & drop узлов
- Автоматический layout (dagre.js)
- Zoom/Pan канваса
- Кастомные компоненты для каждого типа узла
- Валидация связей (нельзя создать цикл, нельзя подключить End к другим узлам)

**AI генерация графа:**

GPT-4 получает промпт:
```
Создай образовательный квест для ребенка 8 лет про фотосинтез.
Ребенок имеет сложности с памятью.

Требования:
- 5-7 узлов типа QuestStep
- 1-2 узла Choice для интерактивности
- 1 узел RealityBridge в конце
- Используй метафоры (фотосинтез = зарядка батарейки)
- Персонаж: wise_owl (мудрая сова)
- Локация: forest_memory

Верни JSON структуру с nodes и edges.
```

GPT-4 возвращает JSON → Frontend рендерит граф → Родитель редактирует визуально.

**Два режима работы:**

1. **AI-первый режим (рекомендуется):**
   - Родитель общается с AI в чате
   - AI задает вопросы, собирает контекст
   - AI генерирует полный граф
   - Родитель видит результат и редактирует

2. **Визуальный редактор (продвинутый):**
   - Родитель создает узлы вручную (drag & drop)
   - Клик на узел → AI заполняет текст диалога
   - Родитель соединяет узлы, создает ветвления
   - AI проверяет корректность структуры

---

## Полный flow работы функционала

### Flow 1: Создание квеста через AI Builder с визуальным графом

1. **Родитель открывает Quest Builder** (web интерфейс)
   - Левая панель: чат с AI
   - Центр: пустой канвас React Flow
   - Правая панель: редактор узла (пока скрыта)

2. **AI начинает разговор:** "Привет! Давай создадим квест для твоего ребенка. Расскажи, чему ты хочешь его научить?"

3. **Родитель отвечает:** "Хочу, чтобы он понял, что такое фотосинтез"

4. **AI задает уточняющие вопросы:**
   - Возраст ребенка? → "8 лет"
   - Какие у него сложности? → "Плохо запоминает"
   - Сколько шагов квеста? (3-7) → "5"
   - Линейный сюжет или с выборами? → "С выборами"

5. **AI генерирует граф квеста** через GPT-4 function calling:
   - Возвращает JSON структуру: {nodes: [...], edges: [...]}
   - Frontend получает данные и рендерит граф на канвасе
   - Родитель видит майнд-карту квеста:
     ```
     [Start] → [Шаг 1: Сова] → [Выбор] → [Шаг 2a] → [Reality Bridge]
                                     ↓
                               [Шаг 2b] ----↗
     ```

6. **Родитель взаимодействует с графом:**
   - **Просмотр:** Клик на узел → правая панель показывает детали (текст диалога, персонаж, метод)
   - **Редактирование:** Изменяет текст в узле → AI помогает улучшить
   - **Добавление:** Drag & drop новый узел из палитры → AI заполняет содержимое
   - **Удаление:** Удаляет узел → AI перестраивает связи
   - **Запрос AI:** "Добавь еще одну ветку для любопытных детей" → AI обновляет граф

7. **Родитель доволен результатом:**
   - Нажимает "Сохранить квест"
   - Граф конвертируется в YAML формат для совместимости с существующим QuestEngine

8. **Квест отправляется на модерацию:**
   - OpenAI Moderation API проверяет все тексты диалогов
   - GPT-4 Safety Check анализирует весь граф на психологическую безопасность
   - Проверка возрастной адекватности

9. **Если одобрен:**
   - Сохраняется в БД (PostgreSQL) с полной структурой графа
   - YAML версия генерируется для выполнения ребенком
   - Становится доступен в библиотеке ребенка
   - Опционально публикуется в общую ленту (с согласия родителя)

10. **В Telegram Bot режиме:**
    - Родитель общается с AI через текст
    - AI генерирует граф на backend
    - Родитель получает линейное текстовое описание: "Квест создан: 5 шагов, 1 выбор, 1 Reality Bridge"
    - Может открыть web версию для визуального редактирования (отправляется ссылка)

### Flow 2: Использование квеста ребенком

1. **Ребенок заходит в приложение** (web или Telegram)
2. **StateManager загружает квест** из БД (YAML преобразуется в Quest object)
3. **QuestEngine выполняет квест** (существующая логика из Phase 3)
4. **EmotionalRouter отслеживает** эмоциональное состояние
5. **Reality Bridge создает напоминание** после квеста
6. **Прогресс сохраняется** в UserProfile

### Flow 3: Обнаружение и использование квестов сообщества

1. **Родитель открывает Quest Feed**
2. **Видит ленту квестов:**
   - Фильтры: возраст, психологический модуль, локация
   - Рейтинг (звезды от других родителей)
   - Количество прохождений
3. **Родитель добавляет квест** в библиотеку своего ребенка
4. **Квест становится доступен** ребенку

---

## API и интерфейсы

### Backend API (FastAPI)

**Quest Management:**
- `POST /api/quests/` - создать новый квест (после AI Builder)
- `GET /api/quests/{quest_id}` - получить квест по ID
- `GET /api/quests/user/{user_id}` - все квесты пользователя
- `GET /api/quests/feed` - публичная лента (пагинация, фильтры)
- `PUT /api/quests/{quest_id}` - обновить квест
- `DELETE /api/quests/{quest_id}` - удалить квест

**AI Quest Builder:**
- `POST /api/builder/chat` - отправить сообщение в диалог
  - Параметры: `{user_id, message, session_id}`
  - Возвращает: `{ai_response, stage, graph: {nodes, edges}}`
- `GET /api/builder/session/{session_id}` - получить историю диалога и текущий граф
- `POST /api/builder/generate_graph` - сгенерировать граф из текущего контекста
  - Параметры: `{session_id, force: boolean}`
  - Возвращает: `{nodes: [...], edges: [...]}`
- `POST /api/builder/refine_node` - улучшить текст конкретного узла через AI
  - Параметры: `{session_id, node_id, user_feedback}`
  - Возвращает: `{updated_node}`
- `POST /api/builder/add_node` - добавить узел в граф (AI заполнит содержимое)
  - Параметры: `{session_id, node_type, parent_node_id}`
  - Возвращает: `{new_node, updated_edges}`
- `DELETE /api/builder/node/{node_id}` - удалить узел (AI перестроит связи)
  - Параметры: `{session_id}`
  - Возвращает: `{updated_graph: {nodes, edges}}`
- `POST /api/builder/reset` - сбросить сессию

**Moderation:**
- `POST /api/moderation/check` - проверить контент (параметры: content, check_type)
- `GET /api/moderation/pending` - квесты на модерации (только для админов)
- `PUT /api/moderation/{quest_id}/approve` - одобрить квест
- `PUT /api/moderation/{quest_id}/reject` - отклонить квест (параметр: reason)

**User & Progress:**
- `GET /api/users/{user_id}/profile` - профиль пользователя
- `GET /api/users/{user_id}/progress` - прогресс по квестам
- `POST /api/users/{user_id}/library/add` - добавить квест в библиотеку

### QuestBuilderAgent (класс)

**Основные методы:**

- `chat(user_message, user_id, session_id)` - обработать сообщение пользователя
  - Управляет conversation flow
  - Определяет когда генерировать граф
  - Возвращает: `{ai_response: str, stage: str, graph: {nodes, edges} | null}`

- `generate_quest_graph(conversation_context)` - сгенерировать граф квеста через GPT-4
  - Использует GPT-4 function calling с JSON schema
  - Параметры: информация о ребенке, тема, сложности, количество шагов
  - Возвращает: `{nodes: QuestNode[], edges: QuestEdge[]}`
  - Автоматически выбирает психологические методы и персонажей

- `refine_node(node_id, user_feedback, graph_context)` - улучшить узел
  - AI получает текущий узел и весь граф для контекста
  - Параметры: `{node_id, feedback: str, current_graph}`
  - Возвращает: `{updated_node: QuestNode}`

- `add_node_with_ai(parent_node_id, node_type, graph_context)` - добавить узел
  - AI генерирует содержимое нового узла на основе родительского
  - Автоматически создает связь с родителем
  - Возвращает: `{new_node, new_edge}`

- `rebuild_graph_after_deletion(deleted_node_id, graph)` - перестроить граф
  - AI анализирует граф после удаления узла
  - Восстанавливает связи, чтобы не было изолированных узлов
  - Возвращает: `{updated_graph}`

- `graph_to_yaml(graph)` - конвертировать граф в YAML
  - Преобразует node-based структуру в формат для QuestEngine
  - Обрабатывает ветвления (ChoiceNode → несколько next)
  - Возвращает: YAML строку

**Conversation Stages:**
- `greeting` - приветствие
- `collecting_info` - сбор информации о ребенке и целях
- `clarifying` - уточнение деталей (возраст, сложности, количество шагов)
- `generating` - генерация графа квеста
- `reviewing` - просмотр графа, редактирование узлов
- `quest_ready` - квест готов к сохранению

**GPT-4 Function Calling Schema:**

Функция `generate_quest_graph`:
```json
{
  "name": "generate_quest_graph",
  "description": "Генерирует граф образовательного квеста",
  "parameters": {
    "type": "object",
    "properties": {
      "nodes": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "type": {"enum": ["start", "questStep", "choice", "realityBridge", "end"]},
            "data": {"type": "object"}
          }
        }
      },
      "edges": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "source": {"type": "string"},
            "target": {"type": "string"},
            "label": {"type": "string"}
          }
        }
      }
    }
  }
}
```

### Moderation Pipeline

**ContentFilter:**
- `check_with_openai(text)` - проверка через OpenAI Moderation API
  - Возвращает: безопасно/небезопасно, категории нарушений
- `check_with_gpt4(quest_yaml)` - проверка через GPT-4
  - Проверяет: возрастная адекватность, психологическая безопасность, корректность психологических методов
  - Возвращает: одобрено/отклонено, рекомендации

---

## Взаимодействие компонентов

### Создание квеста (упрощенная схема)

```
Frontend (AIQuestBuilder)
  -> POST /api/builder/chat
  -> QuestBuilderAgent.chat()
  -> GPT-4 (function calling)
  -> Quest YAML draft
  -> Frontend (QuestPreview)
  -> POST /api/quests/
  -> ContentFilter.check_with_openai()
  -> SafetyChecker.check_with_gpt4()
  -> Database (quest с status=pending/approved)
```

### Выполнение квеста ребенком

```
Telegram Bot / Web Frontend
  -> GET /api/quests/{quest_id}
  -> YAML преобразуется в Quest object
  -> StateManager.process_message()
  -> QuestEngine.get_step_dialogue()
  -> Response возвращается ребенку
  -> RealityBridgeManager создает напоминание
```

### Лента квестов

```
Frontend (QuestFeed)
  -> GET /api/quests/feed?age=7-9&module=memory
  -> Database query (фильтры + пагинация)
  -> Возврат списка квестов с рейтингом
  -> Родитель выбирает квест
  -> POST /api/users/{user_id}/library/add
  -> Квест доступен ребенку
```

---

## Порядок реализации

### Шаг 1: Backend Foundation (неделя 1)
1. Поднять FastAPI приложение (`backend/main.py`)
2. Создать PostgreSQL схему (см. раздел "Параметры стека")
3. Настроить SQLAlchemy модели и Alembic миграции
4. Реализовать базовые CRUD endpoints для квестов
5. Интеграция с существующим `src/` через импорты

### Шаг 2: AI Quest Builder Agent (неделя 1-2)
1. Создать класс `QuestBuilderAgent` с GPT-4 integration
2. Определить system prompt для AI агента
3. Реализовать conversation stages (greeting -> collecting_info -> generating)
4. Добавить GPT-4 function calling для генерации YAML квестов
5. Реализовать API endpoints `/api/builder/*`

### Шаг 3: Content Moderation (неделя 2)
1. Интегрировать OpenAI Moderation API
2. Создать GPT-4 Safety Checker с промптами для возрастной проверки
3. Реализовать двухслойную проверку (Moderation API + GPT-4)
4. Добавить статусы модерации в БД (pending/approved/rejected)

### Шаг 4: Telegram Bot (неделя 2)
1. Создать `bot/telegram_bot.py` с python-telegram-bot
2. Реализовать handlers для существующих команд
3. Подключить StateManager из `src/orchestration/`
4. Добавить команду `/create_quest` для запуска Quest Builder через Telegram
5. Интеграция с RealityBridgeManager для напоминаний

### Шаг 5: Frontend - Quest Builder UI (неделя 3)
1. Поднять React приложение с Vite
2. Создать компонент `AIQuestBuilder` - чат интерфейс
3. Реализовать WebSocket или polling для realtime обновлений
4. Создать компонент `QuestPreview` с предпросмотром и редактированием
5. Интеграция с backend API (`/api/builder/chat`)

### Шаг 6: Frontend - Quest Feed & Dashboard (неделя 3-4)
1. Создать компонент `QuestFeed` с фильтрами и пагинацией
2. Реализовать поиск и рейтинг квестов
3. Создать `ParentDashboard` для отслеживания прогресса ребенка
4. Добавить возможность публикации квеста в общую ленту

### Шаг 7: Integration & Testing (неделя 4)
1. End-to-end тестирование всех flows
2. Тестирование модерации на проблемном контенте
3. Проверка интеграции Telegram Bot с StateManager
4. Нагрузочное тестирование API

### Шаг 8: Deployment (неделя 4-5)
1. Настроить Docker Compose для всего стека
2. Развернуть PostgreSQL (self-hosted или managed)
3. Развернуть backend (Railway, DigitalOcean, или VPS)
4. Развернуть frontend (Vercel для простоты или self-hosted Nginx)
5. Настроить Telegram webhook

---

## Критичные граничные случаи

### Модерация
- **GPT-4 недоступен:** Fallback на базовые правила (запрет мата, насилия, дискриминации)
- **Родитель пытается обойти модерацию:** Логировать все попытки, банить при повторных нарушениях
- **Неоднозначный контент:** Статус "на ручной проверке", уведомление админа

### AI Quest Builder
- **AI генерирует некорректный YAML:** Валидация через Pydantic перед сохранением
- **Родитель застрял в диалоге:** Кнопка "Начать заново", ограничение на 20 сообщений в сессии
- **AI не может понять запрос:** Fallback ответ: "Попробуй описать по-другому" + примеры

### Производительность
- **Много одновременных запросов к GPT-4:** Очередь с rate limiting (10 req/min на пользователя)
- **Большая лента квестов:** Пагинация (20 квестов на страницу), кэширование популярных квестов

### Безопасность
- **Утечка API ключей:** Все ключи только в переменных окружения, никогда в коде
- **PII в квестах:** GPT-4 промпт явно запрещает запрашивать личные данные
- **SQL injection:** SQLAlchemy ORM защищает автоматически

---

## Объем работ

### Что входит в реализацию:

**Backend:**
- FastAPI REST API с 15+ endpoints
- PostgreSQL база данных (users, quests, quest_sessions, ratings)
- QuestBuilderAgent с GPT-4 function calling
- Двухслойная модерация контента
- Интеграция с существующим `src/` кодом
- Alembic миграции для версионирования БД

**Frontend:**
- React приложение с 4 основными компонентами
- Разговорный интерфейс создания квестов
- Лента квестов с фильтрами и поиском
- Дашборд родителя с прогрессом ребенка
- Предпросмотр и редактирование квестов

**Telegram Bot:**
- Обертка над StateManager
- Поддержка всех существующих функций (Phases 1-4)
- Команда `/create_quest` для AI Builder
- Reality Bridge напоминания через APScheduler

**DevOps:**
- Docker Compose для локального развертывания
- Production развертывание (backend + frontend + DB)
- CI/CD не требуется на MVP стадии

### Что НЕ входит:

- **Платежи и монетизация** - отложено на следующую фазу
- **Мобильное приложение** - только web и Telegram
- **Расширенная аналитика** - только базовый прогресс ребенка
- **Социальные функции** (комментарии, лайки) - только рейтинг звездами
- **Автоматические тесты** - на MVP стадии ручное тестирование
- **Мультиязычность** - только русский язык
- **Админ панель** - модерация через API endpoints (позже можно добавить UI)

---

## Допущения

1. **OpenAI API доступен и стабилен** - используем GPT-4 для Quest Builder и модерации
2. **Средний родитель создает 1-2 квеста в месяц** - нагрузка низкая на MVP
3. **PostgreSQL достаточно для хранения** - не нужны распределенные БД на старте
4. **Родители готовы создавать квесты через разговор** - UX предпочтительнее форм
5. **Существующий код из `src/` работает корректно** - Phases 1-4 прошли тестирование (9/9 тестов)
6. **Telegram Bot API стабилен** - используем для основного канала доступа
7. **Модерация GPT-4 достаточна** - не требуется ML модели для контент-фильтрации

## Открытые вопросы

1. **Нужна ли регистрация/аутентификация?**
   - Вариант 1: Telegram ID как primary key (проще)
   - Вариант 2: Email + password для web версии (сложнее, но универсальнее)

2. **Как часто проверять квесты на повторную модерацию?**
   - Родитель может отредактировать одобренный квест - нужна ли повторная проверка?

3. **Лимиты на количество квестов?**
   - Ограничить создание до 10 квестов на пользователя или без лимитов?

4. **Публичная лента - модерация перед публикацией?**
   - Все квесты публикуются автоматически или только после ручной проверки?

---

## Acceptance Criteria

### Минимальные критерии приемки:

1. **Родитель может создать квест через разговор с AI:**
   - Начинает диалог в web или Telegram
   - Отвечает на 3-5 вопросов о ребенке и целях обучения
   - Получает готовый квест в формате YAML
   - Может отредактировать или попросить AI доработать

2. **Квест проходит модерацию:**
   - OpenAI Moderation API блокирует мат и насилие
   - GPT-4 проверяет возрастную адекватность
   - Небезопасные квесты отклоняются с объяснением причины

3. **Ребенок может пройти созданный квест:**
   - Квест загружается через StateManager
   - Все 5 шагов выполняются корректно
   - Reality Bridge создает напоминание после завершения
   - Прогресс сохраняется в UserProfile

4. **Родитель видит лену квестов:**
   - Может фильтровать по возрасту, модулю, локации
   - Видит рейтинг и количество прохождений
   - Может добавить квест в библиотеку своего ребенка

5. **Telegram Bot работает:**
   - Все команды из Phases 1-4 функционируют
   - Команда `/create_quest` запускает AI Builder
   - Reality Bridge напоминания приходят вовремя

### Сценарий ручной проверки:

1. Открыть web приложение или Telegram
2. Запустить `/create_quest` или нажать "Создать квест"
3. Пройти диалог с AI (3-5 сообщений)
4. Получить черновик квеста
5. Принять квест или попросить доработать
6. Убедиться, что квест сохранен в БД
7. Зайти под ребенком и начать квест
8. Пройти все 5 шагов
9. Получить Reality Bridge напоминание через 24 часа
10. Проверить лену квестов - созданный квест виден (если публичный)

---

## Definition of Done

- ✅ Все API endpoints реализованы и тестированы (Postman или curl)
- ✅ QuestBuilderAgent генерирует корректные YAML квесты
- ✅ Модерация блокирует небезопасный контент (проверено на 10+ тестовых случаях)
- ✅ Frontend компоненты отрисовываются без ошибок
- ✅ Telegram Bot интегрирован с StateManager
- ✅ Reality Bridge напоминания работают (проверено вручную с коротким интервалом)
- ✅ Прогресс ребенка сохраняется в БД и отображается в дашборде
- ✅ Docker Compose файл для локального развертывания
- ✅ README с инструкциями по развертыванию
- ✅ Логи всех критичных операций (создание квеста, модерация, ошибки)
- ✅ .env.example с примерами переменных окружения

---

## Минимальные NFR для MVP

### Производительность:
- **Время генерации квеста AI Builder:** до 10 секунд (зависит от GPT-4 API)
- **Время модерации:** до 5 секунд (2 sec OpenAI Moderation + 3 sec GPT-4)
- **Загрузка ленты квестов:** до 1 секунды для 20 квестов
- **Одновременные пользователи:** до 100 (MVP не рассчитан на массовую нагрузку)

### Надежность:
- **Uptime backend API:** 95% (допустимы кратковременные сбои на MVP)
- **Telegram Bot:** 99% (критичнее, так как основной канал доступа)
- **OpenAI API недоступен:** Graceful degradation - уведомление пользователя "Сервис временно недоступен"

### Ограничения по ресурсам:
- **RAM backend:** до 512MB (FastAPI + SQLAlchemy легковесны)
- **PostgreSQL:** до 1GB данных на первые 100 пользователей
- **OpenAI API квота:** 10000 tokens/min (достаточно для 50-100 пользователей)

---

## Требования безопасности

### Секреты:
- Все API ключи (OPENAI_API_KEY, TELEGRAM_BOT_TOKEN, DATABASE_URL) только в `.env` файле
- `.env` в `.gitignore` - никогда не коммитится
- Production секреты в переменных окружения хостинга (Railway/DigitalOcean)

### Логирование:
- **НЕ логировать:** API ключи, токены, Telegram user_id (PII)
- **Логировать:** факт запроса, статус модерации, ошибки (без чувствительных данных)

### Внешние запросы:
- **Белый список:**
  - `api.openai.com` - GPT-4 и Moderation API
  - `api.telegram.org` - Telegram Bot API
- **Все остальные домены блокировать** - не требуется на MVP

### Дополнительно:
- **SQL Injection:** защита через SQLAlchemy ORM (не используем raw SQL)
- **XSS:** React автоматически экранирует вывод
- **CSRF:** FastAPI CORS настроить только для своего фронтенда

---

## Наблюдаемость

### Логи:

**Ключевые события:**
- `quest_builder_session_started` - старт диалога (параметры: user_id, session_id)
- `quest_generated` - квест сгенерирован (параметры: quest_id, user_id, модуль, локация)
- `moderation_passed` - модерация пройдена (параметры: quest_id, duration_ms)
- `moderation_failed` - модерация не пройдена (параметры: quest_id, reason)
- `quest_started_by_child` - ребенок начал квест (параметры: user_id, quest_id)
- `quest_completed` - квест завершен (параметры: user_id, quest_id, duration_minutes)
- `reality_bridge_created` - Reality Bridge создан (параметры: user_id, reminder_at)

**Ошибки:**
- `openai_api_error` - ошибка GPT-4 API (параметры: error_type, status_code)
- `database_error` - ошибка БД (параметры: operation, error_message)
- `telegram_send_error` - ошибка отправки в Telegram (параметры: user_id, error)

### Метрики:

**Счетчики:**
- `quests_created_total` - всего создано квестов
- `quests_approved_total` - одобрено модерацией
- `quests_rejected_total` - отклонено модерацией
- `quest_sessions_started_total` - детей начали квесты
- `quest_sessions_completed_total` - детей завершили квесты

**Гистограммы (опционально, если добавим Prometheus):**
- `quest_generation_duration_seconds` - время генерации квеста
- `moderation_duration_seconds` - время модерации

### Трассировка:

**На MVP стадии - упрощенная трассировка через логи:**
- Каждый запрос имеет `request_id` (UUID)
- Логи операций содержат `request_id` для связывания

**Пример span:**
```
[INFO] quest_builder_session_started request_id=abc123 user_id=456
[INFO] openai_request_sent request_id=abc123 model=gpt-4
[INFO] quest_generated request_id=abc123 quest_id=789
[INFO] moderation_started request_id=abc123 quest_id=789
[INFO] moderation_passed request_id=abc123 duration_ms=3200
```

---

## Релиз и откат

### Релиз:

**Feature Flags (упрощенная версия для MVP):**
- Переменная окружения `ENABLE_UGC_PLATFORM=true/false`
- Если `false` - только базовые функции Phases 1-4
- Если `true` - доступен AI Quest Builder и лента

**План развертывания:**
1. **Локальное тестирование:**
   - Docker Compose с полным стеком
   - Проверка всех flows вручную
2. **Staging (опционально):**
   - Развертывание на тестовом сервере
   - Приглашение 3-5 родителей для альфа-тестирования
3. **Production:**
   - Развертывание backend на Railway/DigitalOcean
   - Развертывание frontend на Vercel
   - PostgreSQL на managed хостинге (DigitalOcean Managed DB)
   - Миграция БД через Alembic
   - Запуск с `ENABLE_UGC_PLATFORM=false`
   - Постепенное включение для выбранных пользователей
   - Полное включение после 1 недели стабильной работы

### Откат:

**Условия отката:**
- Критичные ошибки в модерации (пропускает небезопасный контент)
- OpenAI API выходит за бюджет (неожиданно высокие расходы)
- Database миграция сломала данные
- >50% пользователей жалуются на баги

**Шаги отката:**
1. Установить `ENABLE_UGC_PLATFORM=false` - отключить новые функции
2. Если проблема в БД - откатить миграцию Alembic (`alembic downgrade -1`)
3. Если проблема в коде - откатить Git commit и передеплоить
4. Уведомить пользователей через Telegram broadcast (если было много активных сессий)

**Восстановление данных:**
- Ежедневные бэкапы PostgreSQL (managed DB делает автоматически)
- Критичные данные (UserProfile, активные квесты) можно восстановить из бэкапа
- User-generated квесты не критичны - потеря допустима на MVP

---

## Риски и митигации

### Риск 1: OpenAI API становится дорогим
**Вероятность:** высокая (зависит от количества пользователей)
**Митигация:**
- Лимит на количество генераций квестов (5 в день на пользователя)
- Кэширование популярных промптов
- Мониторинг расходов через OpenAI Dashboard

### Риск 2: Модерация GPT-4 пропускает небезопасный контент
**Вероятность:** средняя (AI не идеален)
**Митигация:**
- Двухслойная проверка (OpenAI Moderation + GPT-4)
- Кнопка "Пожаловаться" для родителей
- Ручная проверка первых 100 квестов
- Бан пользователей при повторных нарушениях

### Риск 3: Родители не понимают, как создавать квесты через AI
**Вероятность:** средняя (новый UX паттерн)
**Митигация:**
- Онбординг с примером диалога
- Подсказки AI ("Например: Хочу, чтобы ребенок понял, что такое фотосинтез")
- Видео-инструкция (1-2 минуты)

### Риск 4: PostgreSQL не справится с нагрузкой
**Вероятность:** низкая (MVP - малая нагрузка)
**Митигация:**
- Индексы на частые запросы (user_id, quest_id, created_at)
- Connection pooling в SQLAlchemy
- Мониторинг slow queries
- Вертикальное масштабирование БД (upgrade тарифа)

### Риск 5: Telegram Bot API изменит формат или станет платным
**Вероятность:** низкая (стабильный API)
**Митигация:**
- Тонкий слой абстракции (`bot/telegram_bot.py`)
- Легко переключиться на web-версию как основной канал
- Дублирование всех функций в web UI

### Риск 6: Дети находят способы обмануть систему
**Вероятность:** средняя (дети изобретательны)
**Митигация:**
- Валидация ответов на каждом шаге квеста
- EmotionalRouter детектирует скуку и отвлечение
- Родитель видит детальный прогресс в дашборде

---

## Параметры стека

### Язык и версии:
- **Python:** 3.11+ (для backend и AI Agent)
- **Node.js:** 18+ (для frontend)
- **TypeScript:** 5+ (для React компонентов)

### Фреймворки:
- **Backend:** FastAPI 0.104+
- **Frontend:** React 18+ с Vite
- **Telegram Bot:** python-telegram-bot 20+
- **AI:** OpenAI Python SDK 1.0+

### База данных:
- **PostgreSQL:** 15+
- **ORM:** SQLAlchemy 2.0+
- **Миграции:** Alembic

### Основные библиотеки:

**Backend (Python):**
- **OpenAI:** GPT-4, Moderation API
- **APScheduler:** Reality Bridge напоминания (уже используется)
- **Pydantic:** Валидация YAML квестов и graph структур
- **python-dotenv:** Управление переменными окружения
- **asyncpg:** Асинхронный PostgreSQL драйвер

**Frontend (JavaScript/TypeScript):**
- **React Flow:** 11.10+ (MIT license) - node-based визуализация графов
- **dagre:** 0.8+ - автоматический layout графов (иерархический)
- **axios:** HTTP клиент для API запросов
- **zustand:** Легковесный state management
- **tailwindcss:** Стилизация UI компонентов

### Целевая платформа деплоя:
- **Backend:** Railway.app (простой деплой) или DigitalOcean Droplet (больше контроля)
- **Frontend:** Vercel (бесплатный тариф для MVP) или self-hosted Nginx
- **База данных:** DigitalOcean Managed PostgreSQL или self-hosted в Docker
- **Telegram Bot:** Webhook на том же сервере, что и backend

### PostgreSQL Schema (основные таблицы):

**users:**
- `id` (UUID, PK)
- `telegram_id` (BigInt, unique, nullable)
- `child_name` (String)
- `learning_profile` (JSONB)
- `created_at` (Timestamp)

**quests:**
- `id` (UUID, PK)
- `author_id` (UUID, FK users.id)
- `title` (String)
- `graph_structure` (JSONB) - полная структура графа {nodes: [], edges: []}
- `yaml_content` (Text) - YAML квеста (генерируется из graph_structure)
- `psychological_module` (String)
- `location` (String)
- `difficulty` (String)
- `age_range` (String) - например "7-9"
- `is_public` (Boolean) - доступен в общей ленте?
- `moderation_status` (Enum: pending, approved, rejected)
- `moderation_reason` (Text, nullable) - причина отклонения
- `rating` (Float) - средний рейтинг
- `plays_count` (Int) - количество прохождений
- `created_at` (Timestamp)

**quest_builder_sessions:**
- `id` (UUID, PK)
- `user_id` (UUID, FK users.id)
- `conversation_history` (JSONB) - история диалога
- `current_stage` (String) - greeting/collecting_info/generating/etc
- `current_graph` (JSONB, nullable) - текущий граф квеста {nodes: [], edges: []}
- `quest_context` (JSONB, nullable) - контекст: {age, topic, difficulties, num_steps}
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

**user_quest_library:**
- `id` (UUID, PK)
- `user_id` (UUID, FK users.id)
- `quest_id` (UUID, FK quests.id)
- `added_at` (Timestamp)

**quest_progress:**
- `id` (UUID, PK)
- `user_id` (UUID, FK users.id) - ребенок
- `quest_id` (UUID, FK quests.id)
- `current_step` (Int)
- `completed` (Boolean)
- `started_at` (Timestamp)
- `completed_at` (Timestamp, nullable)

**quest_ratings:**
- `id` (UUID, PK)
- `user_id` (UUID, FK users.id) - родитель, который оценил
- `quest_id` (UUID, FK quests.id)
- `rating` (Int) - 1-5 звезд
- `created_at` (Timestamp)

---

## Самопроверка плана перед выдачей

- ✅ Нет кода и псевдокода - только описание логики и архитектуры
- ✅ Заполнены все разделы: scope, acceptance, risk, release
- ✅ Регэксп именования: `02-FEAT-AI-QUEST-BUILDER-UGC` и `IP-01-full-stack-ugc-platform.md`
- ✅ Нет упоминаний секретов - только переменные окружения
- ✅ Только открытый код и self-hosted решения (PostgreSQL, FastAPI, React)
- ✅ Язык: русский
- ✅ Используются только символы "-" и обычный пробел " "
- ✅ Все пути в POSIX формате

---

## Проверки перед "ломкой" API

- ✅ Подтверждено отсутствие внешних потребителей - проект внутренний, MVP стадия
- ✅ Нет зависимых задач в текущем спринте - это первая задача после завершения Phases 1-4
- ✅ Можно менять структуру БД и API без учета обратной совместимости

---

## Профиль языка

- **primary_language:** python
- **stdlib_preferred:** true
- **note:** Используем стандартную библиотеку Python где возможно (asyncio, json, pathlib), добавляем внешние зависимости только когда необходимо (FastAPI, SQLAlchemy, OpenAI SDK)
