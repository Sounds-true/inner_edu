# 🚀 InnerWorld Edu - Инструкция по развертыванию

## 📦 Что запушено в GitHub

**Branch:** `claude/fork-repo-architecture-011CUtYG7BkBAjCcGNJrC3Ef`
**Repository:** https://github.com/Sounds-true/inner_edu

**Commits:**
- `6e77dc4` - Add AI Quest Builder with node-based visual interface
- `dd56f6a` - Add YAML to Graph converter and Quest Library UI
- `1809fd9` - Add QUICKSTART guide
- `c93dee4` - Fix import errors and add auto-database initialization

**Всего:** 29 новых файлов, 3000+ строк кода

---

## ✅ Что работает

1. **AI Quest Builder** - создание квестов через GPT-4
2. **YAML → Graph конвертер** - визуализация существующих квестов
3. **Quest Library** - библиотека квестов с фильтрами
4. **React Flow** - node-based редактор графов
5. **Автоматическое создание таблиц БД**
6. **Совместимость с Phases 1-4** - старый код не сломан

---

## 📥 Клонирование репозитория

```bash
# Если еще не клонирован
git clone https://github.com/Sounds-true/inner_edu.git
cd inner_edu

# Переключиться на ветку
git checkout claude/fork-repo-architecture-011CUtYG7BkBAjCcGNJrC3Ef

# Или если уже клонирован
cd /path/to/inner_edu
git fetch origin
git checkout claude/fork-repo-architecture-011CUtYG7BkBAjCcGNJrC3Ef
git pull
```

---

## 🛠️ Установка зависимостей

### 1. PostgreSQL

**Mac:**
```bash
# Установить PostgreSQL (если нет)
brew install postgresql@15
brew services start postgresql@15

# Создать базу
createdb innerworld_edu

# Проверить
psql -d innerworld_edu -c "SELECT 1"
```

**Linux:**
```bash
sudo apt-get install postgresql-15
sudo systemctl start postgresql
sudo -u postgres createdb innerworld_edu
```

### 2. Python зависимости

```bash
cd inner_edu

# Backend зависимости
pip install -r backend/requirements.txt

# Существующие зависимости (Phases 1-4)
pip install -r requirements.txt

# Проверить
python -c "import fastapi, openai, sqlalchemy; print('OK')"
```

### 3. Node.js зависимости

```bash
cd inner_edu/frontend

# Установить
npm install

# Проверить
npm list reactflow axios
```

---

## ⚙️ Конфигурация

### Backend .env

```bash
cd inner_edu/backend

cat > .env << EOF
# OpenAI API (для AI Quest Builder)
OPENAI_API_KEY=sk-your-actual-key-here

# PostgreSQL (локальная база)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/innerworld_edu

# Frontend URL (для CORS)
FRONTEND_URL=http://localhost:5173
EOF
```

**⚠️ Важно:**
- Замени `OPENAI_API_KEY` на свой ключ
- Замени `password` на пароль от PostgreSQL (если есть)
- На Mac обычно пароль не нужен: `DATABASE_URL=postgresql+asyncpg://postgres@localhost/innerworld_edu`

### Проверка конфигурации

```bash
# Проверить что .env читается
cd inner_edu/backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API KEY:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

---

## 🚀 Запуск приложения

### Terminal 1: Backend API

```bash
cd inner_edu/backend
python main.py
```

**Ожидаемый вывод:**
```
✅ Database tables created/verified
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Если ошибка:**
- `Database initialization failed` - проверь DATABASE_URL в .env
- `ModuleNotFoundError` - установи зависимости: `pip install -r backend/requirements.txt`

**Проверка:**
- http://localhost:8000 - должен вернуть `{"status": "ok"}`
- http://localhost:8000/docs - Swagger UI со всеми endpoints

### Terminal 2: Frontend (Vite)

```bash
cd inner_edu/frontend
npm run dev
```

**Ожидаемый вывод:**
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Проверка:**
- http://localhost:5173 - должен открыться AI Quest Builder

---

## 🎮 Тестирование (3 сценария)

### Сценарий 1: Загрузить квест из YAML ⭐ ГЛАВНЫЙ

**Цель:** Визуализировать существующий квест "Три простых объяснения" как граф

1. Открой **http://localhost:5173**
2. Нажми **📚** (иконка книги справа от заголовка)
3. Появится модальное окно "Библиотека квестов"
4. Если пусто → нажми **"Загрузить квесты из YAML"**
   - Backend конвертирует `/src/data/quests/**/*.yaml` → графы
   - Загрузит в PostgreSQL
   - Должно появиться: "loaded_count: 1"
5. Закрой модалку и открой снова (📚)
6. Увидишь квест **"Три простых объяснения"**
7. **Кликни на него**
8. **Увидишь граф квеста! 🎉**

**Что должно быть:**
```
[Start: Три простых объяснения]
         ↓
[Шаг 1: Напиши одно сложное слово...]
         ↓
[Choice: Как бы ты объяснил это слово...]
         ↓
[Шаг 3: Теперь объясни это слово своими словами...]
         ↓
[Шаг 4: Придумай пример из жизни...]
         ↓
[Choice: Стало ли тебе понятнее...]
         ↓
[Reality Bridge: Объясни одно слово учителю...]
         ↓
[End]
```

**8 узлов, 7 связей**

- 🟢 Зеленый круг (Start)
- 🔵 Синие блоки (QuestStep x3)
- 🟡 Желтые ромбы (Choice x2)
- 🟣 Фиолетовый шестиугольник (Reality Bridge)
- 🔴 Красный круг (End)

**Можно:**
- Зумить (Ctrl+Scroll)
- Двигать канвас (Drag)
- Перетаскивать узлы
- Видеть MiniMap (справа внизу)

**Нельзя (пока):**
- Кликнуть на узел и редактировать (TODO)
- Сохранить изменения (TODO)

---

### Сценарий 2: Создать квест через AI

**Цель:** Попросить GPT-4 сгенерировать новый квест

1. В чате (левая панель) напиши: **"Хочу квест про фотосинтез"**
2. AI спросит: **"Отлично! Сколько лет твоему ребенку?"**
3. Ответь: **"8 лет"**
4. AI спросит: **"Какие у него сложности?"**
5. Ответь: **"Плохо запоминает"**
6. AI спросит: **"Сколько шагов квеста? (рекомендую 5-7)"**
7. Ответь: **"5"**
8. AI скажет: **"Генерирую квест..."**
9. **Появится граф!** (если OPENAI_API_KEY настроен)

**Если ошибка:**
- `401 Unauthorized` - проверь OPENAI_API_KEY
- `Извини, произошла ошибка` - проверь логи backend (Terminal 1)
- Долго думает - это нормально, GPT-4 может думать 10-20 секунд

---

### Сценарий 3: Swagger API

**Цель:** Протестировать API напрямую

1. Открой **http://localhost:8000/docs**
2. Попробуй endpoints:

**GET /api/quests/existing** - список квестов
- Нажми "Try it out" → "Execute"
- Должен вернуть `[]` (пока пусто)

**POST /api/quests/load_yaml_quests** - загрузить YAML квесты
- Нажми "Try it out" → "Execute"
- Должен вернуть `{"loaded_count": 1, "quests": [...]}`

**GET /api/quests/existing** (повторно)
- Теперь должен вернуть 1 квест

**POST /api/builder/chat** - чат с AI
- Body:
```json
{
  "user_id": "test-user-123",
  "message": "Привет"
}
```
- Должен вернуть `{"ai_response": "...", "stage": "greeting", ...}`

---

## 🐛 Troubleshooting

### Backend ошибки

**"Database initialization failed"**
```bash
# Проверь что PostgreSQL запущен
pg_isready

# Проверь DATABASE_URL
cat backend/.env | grep DATABASE_URL

# Попробуй создать базу вручную
createdb innerworld_edu
```

**"ModuleNotFoundError: No module named 'backend'"**
```bash
# Запускай из правильной директории
cd inner_edu/backend
python main.py

# НЕ из корня проекта!
```

**"sqlalchemy.exc.OperationalError"**
```bash
# Неправильный DATABASE_URL
# Для Mac без пароля:
DATABASE_URL=postgresql+asyncpg://postgres@localhost/innerworld_edu

# Для Linux с паролем:
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/innerworld_edu
```

### Frontend ошибки

**"Failed to fetch" в консоли браузера**
```bash
# Проверь что backend запущен
curl http://localhost:8000/health

# Проверь CORS
# В backend/main.py должно быть allow_origins с localhost:5173
```

**"Cannot find module 'reactflow'"**
```bash
cd inner_edu/frontend
rm -rf node_modules package-lock.json
npm install
```

### AI не генерирует квест

**"401 Unauthorized"**
- Проверь OPENAI_API_KEY в backend/.env
- Убедись что ключ начинается с `sk-`
- Проверь баланс на OpenAI аккаунте

**"Квест не появляется после генерации"**
- Проверь логи backend (Terminal 1)
- Открой консоль браузера (F12) → вкладка Console
- Ищи ошибки JavaScript

---

## 📊 Проверка что всё работает

### Checklist ✅

- [ ] PostgreSQL запущен (`pg_isready`)
- [ ] База `innerworld_edu` создана (`psql -l | grep innerworld`)
- [ ] Backend .env настроен (OPENAI_API_KEY, DATABASE_URL)
- [ ] Backend запущен (http://localhost:8000/health → `{"status": "healthy"}`)
- [ ] Frontend запущен (http://localhost:5173 → AI Quest Builder UI)
- [ ] Библиотека квестов открывается (📚 кнопка)
- [ ] YAML квесты загружаются ("Загрузить квесты из YAML")
- [ ] Квест визуализируется (клик на квест → граф появляется)
- [ ] AI чат работает (можно написать "Привет")

### Если всё ✅

**Поздравляю! 🎉 Всё работает!**

Ты можешь:
- 📚 Визуализировать квесты Понималии как майнд-карты
- 🤖 Создавать новые квесты через AI
- 🎨 Редактировать графы визуально
- 👀 Видеть структуру квестов наглядно

---

## 📝 Следующие шаги (опционально)

### Если хочешь допилить:

1. **NodeEditor** - редактирование текста узлов кликом
   - Создать `frontend/src/components/NodeEditor/index.tsx`
   - Добавить панель справа при клике на узел

2. **Save Quest** - сохранение отредактированного квеста
   - Endpoint `POST /api/quests/save`
   - Кнопка "Сохранить" в UI

3. **Graph → YAML** - конвертация обратно
   - Реализовать `graph_to_yaml()` в `yaml_to_graph_converter.py`
   - Преобразовать nodes/edges → YAML структуру

4. **Child Execution** - прохождение квестов детьми
   - Интеграция graph-based квестов с StateManager
   - Web UI для детей (не только Telegram)

### Если хочешь смержить в main:

```bash
cd inner_edu
git checkout main
git merge claude/fork-repo-architecture-011CUtYG7BkBAjCcGNJrC3Ef
git push origin main
```

---

## 🔗 Полезные ссылки

- **Repository:** https://github.com/Sounds-true/inner_edu
- **Branch:** claude/fork-repo-architecture-011CUtYG7BkBAjCcGNJrC3Ef
- **Swagger API:** http://localhost:8000/docs (после запуска backend)
- **Frontend:** http://localhost:5173 (после запуска frontend)

---

## 📞 Помощь

Если что-то не работает:
1. Проверь POTENTIAL_ISSUES.md
2. Проверь логи backend (Terminal 1)
3. Проверь консоль браузера (F12)
4. Проверь что все зависимости установлены

---

**Удачи! 🚀✨**

Теперь твои квесты Понималии можно визуализировать как красивые майнд-карты и редактировать с помощью AI!
