# Implementation Plan: Module 11 - DBT Advanced Skills

## Module Overview
**Target:** Дети 7-14 лет с высокой эмоциональной дизрегуляцией, impulsivity, self-harm risk
**Цель:** Продвинутые навыки DBT - Opposite Action, TIPP, Radical Acceptance, Problem-Solving
**Источники:** InnerWorld002.txt (DBT blocks), Linehan's DBT Skills Training Manual adapted for adolescents

## Core Content: Advanced DBT Skills

### Module Prerequisites:
- Module 02 (DBT Basics): Wise Mind, STOP, Distress Tolerance basics
- Module 08 (Mindfulness): Present moment, body awareness
- Module 09 (Emotional Literacy): Emotion identification & intensity

### 4 Продвинутых навыка:
1. **Opposite Action** - действие против неадаптивной эмоции
2. **TIPP** (Temperature, Intense exercise, Paced breathing, Paired muscle relaxation) - кризисное вмешательство
3. **Radical Acceptance** - принятие того, что нельзя изменить
4. **Problem-Solving Effectiveness** - решение проблем vs эмоциональная реакция

### UCAM Integration:
```json
{
  "dbt_advanced_skills": [
    "opposite_action",
    "crisis_survival",
    "radical_acceptance",
    "problem_solving",
    "emotion_regulation_mastery"
  ],
  "clinical_targets": {
    "high_priority": ["self_harm_urges", "impulsivity", "emotional_storms"],
    "medium_priority": ["helplessness", "rumination", "avoidance"]
  }
}
```

---

## Techniques to Implement

### Technique 1: "Обратное Действие" (Opposite Action)
**Источник:** Linehan's DBT, Block 2 InnerWorld002.txt

**Психологическая суть:**
- Эмоции побуждают к действию (страх → убежать, гнев → атаковать)
- Если эмоция неоправданна или непропорциональна → действуй ПРОТИВ неё
- Страх непропорционален → Подойди БЛИЖЕ (exposure)
- Незаслуженный стыд → Подними ГОЛОВУ, скажи о чувстве
- Работает, когда эмоция = FALSE ALARM или мешает ценностям

**Ключевая проверка:**
```
1. Какая эмоция? (из 8 базовых)
2. Какова интенсивность? (0-10)
3. Соответствует ли эмоция фактам? (justified?)
4. Если НЕТ → Opposite Action
5. Если ДА → Problem Solving или Acceptance
```

**Игровая механика:**
- **Квест:** "Перекрёсток Выбора" (Crossroads of Choice)
- **NPC:** Архитектор Разума (Architect of Mind) учит проверке
- **Визуализация:** 2 дороги:
  - Красная: следовать эмоции (импульс)
  - Синяя: обратное действие (осознанность)
- **Формула:**
  ```
  Эмоция → Импульс → [Проверка фактов] → Opposite Action ИЛИ Validate
  ```

**Примеры Opposite Action (игровые сцены):**

#### Сцена 1: Незаслуженный Стыд
```
Ситуация: Ты получил 4 (не 5) за контрольную. Учил, старался.
Эмоция: Стыд (intensity 7/10)
Импульс: Спрятаться, не говорить родителям, избегать учителя

[Проверка фактов с Архитектором]
Архитектор: "Ты сделал что-то плохое или постыдное?"
Игрок: "Нет, я старался..."
Архитектор: "Оценка = неудача всей личности?"
Игрок: "Нет..."
Архитектор: "Стыд НЕОПРАВДАН. Попробуем Opposite Action?"

Opposite Action:
- НЕ прятаться → Поднять голову, идти прямо
- НЕ избегать → Показать работу родителям
- НЕ замолчать → Сказать "Я старался, 4 - хороший результат для меня"

[Если выбрано Opposite Action:]
→ +0.12 Opposite Action Skill, +0.08 Self-Worth, -0.10 Shame
```

#### Сцена 2: Страх перед выступлением
```
Ситуация: Завтра презентация перед классом. Страх 8/10.
Импульс: Притвориться больным, избежать

[Проверка фактов]
Архитектор: "Реальная опасность есть?"
Игрок: "Могут засмеяться..."
Архитектор: "Это опасность для жизни/здоровья?"
Игрок: "Нет..."
Архитектор: "Страх непропорционален. Opposite Action?"

Opposite Action:
- НЕ избегать → Пойти и выступить
- НЕ убегать → Стоять прямо, медленно
- НЕ прятаться → Смотреть в глаза (можно одному человеку)
- Сделать маленький шаг навстречу страху

[Если выбрано:]
→ +0.10 Opposite Action, +0.08 Courage, -0.06 Avoidance
```

#### Сцена 3: Гнев на друга (обоснованный)
```
Ситуация: Друг сломал твою вещь. Гнев 6/10.
Импульс: Накричать, порвать его тетрадь (месть)

[Проверка фактов]
Архитектор: "Твоя граница нарушена?"
Игрок: "Да, он сломал мою вещь"
Архитектор: "Гнев ОБОСНОВАН. НЕ Opposite Action. Problem Solving!"

Правильное действие:
- Не подавлять гнев (он оправдан)
- НО выражать конструктивно:
  "Мне обидно и злобно. Ты сломал мою вещь. Мне нужно извинение."

[Opposite Action НЕ применяется, когда эмоция justified]
→ +0.08 Fact-Checking, +0.10 Assertiveness
```

**Opposite Action Matrix:**
| Эмоция | Импульс | Opposite Action (если неоправданна) |
|--------|---------|-------------------------------------|
| Страх | Убежать | Приблизиться, остаться |
| Гнев | Атаковать | Мягкий тон, отстраниться |
| Стыд | Спрятаться | Поднять голову, сказать вслух |
| Грусть (непропорц.) | Изоляция | Активироваться, социальный контакт |
| Вина (незаслуж.) | Извиняться | Не извиняться, держать позицию |

**Артефакт:**
- **Посох Парадокса** (tier 4, advanced)
- Burden: 0.07
- Эффект: +0.14 Opposite Action, +0.10 Emotion Regulation, +0.08 Fact-Checking

**Школьные предметы:**
- **Физика (7-8 класс):** Противодействие силе, баланс
- **Литература (7-9 класс):** Герои, действующие против импульса
- **Биология (8-9 класс):** Борьба с фобиями через экспозицию
- **Обществознание (8-9 класс):** Гражданское мужество

**Локация:** **Перекрёстки** (активация при высокой эмоции)
- VCEM: До - E=-0.7 (высокая дизрегуляция), после - E=-0.3, C=+0.5

**Коан-переход:**
```
Вход: "Что, если ты можешь держать в сердце два противоположных чувства?"
→
Выход: "Что, если иногда путь через страх - это шаг НАВСТРЕЧУ ему?"
```

**Reality Bridge:**
1. **Дневник Opposite Action** (3 раза/неделю): "Сегодня мой страх говорил 'беги', я подошёл ближе"
2. **Маленький вызов** (ежедневно): 1 действие против неоправданного страха/стыда
3. **Проверка фактов**: Карточка с вопросами в кармане

---

### Technique 2: "TIPP - Кризисная Перезагрузка"
**Источник:** DBT Distress Tolerance, crisis intervention

**Аббревиатура:**
- **T**emperature (изменение температуры тела - холодная вода)
- **I**ntense exercise (интенсивная физическая активность)
- **P**aced breathing (ритмичное дыхание)
- **P**aired muscle relaxation (напряжение-расслабление мышц)

**Психологическая суть:**
- При эмоциональном шторме (intensity 8-10/10) - нужна ФИЗИОЛОГИЧЕСКАЯ перезагрузка
- Когда DBT skills не работают (слишком высокая активация) → TIPP сначала
- Снизить физиологическое возбуждение → потом думать/выбирать
- Для PA: паника, rage episodes, self-harm urges

**Игровая механика:**
- **Квест:** "Остров Бури" (Storm Island) - активируется при E < -0.8 (crisis)
- **Визуализация:** Экран трясётся, красный оттенок, heart rate индикатор зашкаливает
- **NPC:** Штурман Бури (Storm Navigator) показывает 4 выхода
- **Выбор техники** (одна или несколько):

#### T - Temperature
```
Игрок кликает на ледяной водопад
→ Экран становится синим
→ Mini-game: Держать лицо под холодной водой (15-30 сек countdown)
→ Heart rate падает (visual feedback)
→ "Dive Reflex активирован. Пульс замедлился."
→ -0.15 Arousal, +0.10 Crisis Control
```

#### I - Intense Exercise
```
Игрок бежит по острову (клавиши или свайп)
→ 60 секунд интенсивного движения
→ Персонаж делает jumping jacks, бег, отжимания
→ Эмоциональный заряд "сгорает" физически
→ "Адреналин переработан. Тело устало, разум яснее."
→ -0.12 Emotional Intensity, +0.08 Clarity
```

#### P - Paced Breathing
```
Breathing animation (знакомая из Module 08)
→ Но более медленная: 4-7-8 дыхание
→ 5 циклов
→ Вагусный нерв активируется (game lore)
→ "Нервная система переключается в режим покоя."
→ -0.10 Anxiety, +0.12 Calm
```

#### P - Paired Muscle Relaxation
```
Силуэт тела (как в Body Scan)
→ Последовательно: напрячь мышцы 5 сек → расслабить
→ Кулаки → Плечи → Живот → Ноги
→ "Напряжение покидает тело."
→ -0.08 Tension, +0.10 Relaxation
```

**Игровая сцена (полный кризис):**
```
Ситуация: Родители кричат друг на друга. Ты в комнате. Паника 9/10.
Импульс: Self-harm, убежать из дома, закричать

[Активируется Storm Island]
Штурман: "ТЫ В БУРЕ. Сначала тело, потом разум. Выбери TIPP."

Игрок использует:
1. Temperature (холодная вода на лицо) - 30 сек
2. Paced Breathing (4-7-8) - 5 циклов
→ Паника падает: 9/10 → 6/10 → 4/10
→ Экран проясняется
→ Теперь доступны другие skills (STOP, Opposite Action)

Штурман: "Ты выжил. Буря стихла. Теперь можешь выбирать."
→ +0.15 Crisis Survival, +0.10 Self-Harm Prevention
```

**TIPP Decision Tree (когда использовать что):**
```javascript
{
  "Panic (9-10/10)": "T + P (температура + дыхание) - быстрое",
  "Rage (8-9/10)": "I + P (упражнения + расслабление) - сжечь адреналин",
  "Freeze/Dissociation": "T + I (холод + движение) - вернуться в тело",
  "Self-harm urge": "T (temperature) ПЕРВОЕ - dive reflex останавливает импульс"
}
```

**Артефакт:**
- **Компас Бури** (tier 5, кризисный)
- Burden: 0.08
- Эффект: +0.18 Crisis Control, +0.12 Self-Harm Prevention, -0.15 Panic

**Школьные предметы:**
- **Биология (8-9 класс):** Вагусный нерв, парасимпатическая нервная система, dive reflex
- **ОБЖ (7-9 класс):** Первая помощь при панике, шоке
- **Физкультура (5-9 класс):** Влияние упражнений на эмоции
- **Химия (8-9 класс):** Адреналин, кортизол, нейромедиаторы

**Локация:** **Остров Бури (Storm Island)** - кризисная зона
- VCEM: До - V=-0.6, E=-0.9 (crisis), после - V=-0.2, E=-0.4, C=+0.3

**Коан-переход:**
```
Вход: "Что, если иногда путь через страх - это шаг НАВСТРЕЧУ ему?"
→
Выход: "Что, если в самой сильной буре есть якорь - твоё тело, и ты можешь его использовать?"
```

**Reality Bridge:**
1. **TIPP-карточка** (всегда при себе): Холодная вода → Бег → Дыхание → Расслабление
2. **Домашний набор**: Кубики льда в морозилке, резинка на запястье (snap)
3. **Сигнал семье**: "Мне нужна TIPP-пауза" (5 мин без вопросов)

---

### Technique 3: "Радикальное Принятие" (Radical Acceptance)
**Источник:** DBT Distress Tolerance, ACT Acceptance, Buddhist mindfulness

**Психологическая суть:**
- Есть вещи, которые нельзя изменить (развод родителей, смерть, прошлое)
- Отказ принимать = страдание × 2 (боль + борьба с болью)
- Радикальное принятие ≠ одобрение. "Это случилось. Это реальность."
- Освобождает энергию для того, что МОЖНО изменить
- Критично для PA: "Родители НЕ будут вместе" → acceptance → движение вперёд

**Формула:**
```
Боль (неизбежная) + Отказ принять = Страдание
Боль (неизбежная) + Принятие = Боль (но без борьбы, меньше страдания)
```

**Игровая механика:**
- **Квест:** "Врата Реальности" (Gates of Reality) в Болоте Вины
- **Метафора:** Закрытая дверь (непринятие) vs Открытая дверь (принятие)
- **NPC:** Хранитель Врат (Gate Keeper) учит различать:
  - Что можно изменить (Problem Solving)
  - Что нельзя изменить (Radical Acceptance)

**Игровая сцена:**
```
Ситуация: Родители в разводе 2 года. Ты всё ещё надеешься, что они вернутся.
Эмоция: Грусть (7/10), False Hope

Хранитель: "Что ты не можешь принять?"
Игрок: "Что они не вместе"
Хранитель: "Можешь ли ты это изменить?"
Игрок: [Выбор]
  A. "Да! Если я буду хорошим, они..." → False hope, +suffering
  B. "Нет... я не могу" → Reality check ✓
  C. "Не хочу об этом думать" → Avoidance

[Если B:]
Хранитель: "Нет, ты не можешь. Это их выбор. Это реальность.
            Не принимать = страдать дважды.
            Принять = освободить себя."

Игрок: [Ритуал принятия]
  1. Сказать вслух: "Мои родители в разводе. Это реальность."
  2. Почувствовать боль (не убегать)
  3. Открыть дверь (символически)
  4. Шагнуть вперёд

[После ритуала:]
→ -0.12 False Hope, +0.15 Radical Acceptance, +0.10 Reality Orientation
→ "Боль есть. Но ты больше не боришься с реальностью."
```

**Шаги Radical Acceptance (обучение в игре):**
```
1. Observe: Заметить, что ты отказываешься принять
2. Acknowledge: "Я не хочу, чтобы это было правдой"
3. Reality Check: "Но это правда. Это реальность."
4. Allow Pain: Почувствовать боль (не убегать, не подавлять)
5. Commitment: "Это случилось. Что теперь?"
6. Move Forward: Освободить энергию для будущего
```

**Примеры для Radical Acceptance (PA context):**
```javascript
{
  "Развод родителей": "Они не вернутся. Я не виноват. Я могу любить обоих.",
  "Смерть близкого": "Он/она умер. Я не могу это изменить. Горе естественно.",
  "Несправедливость": "Это произошло. Это несправедливо. Я могу двигаться дальше.",
  "Прошлые ошибки": "Я сделал это. Не могу отменить. Могу учиться.",
  "Болезнь/инвалидность": "У меня это есть. Это часть меня. Могу адаптироваться."
}
```

**Отличие от Пассивности:**
```
Пассивность: "Ничего нельзя сделать" → сдаться
Radical Acceptance: "Это нельзя изменить" → фокус на том, что можно
```

**Артефакт:**
- **Ключ Реальности** (tier 4)
- Burden: 0.06
- Эффект: +0.16 Radical Acceptance, +0.10 Reality Orientation, -0.12 False Hope, -0.08 Suffering

**Школьные предметы:**
- **История (7-9 класс):** Исторические травмы, как общества двигались дальше
- **Литература (8-9 класс):** Герои, принимающие потери (Толстой, Достоевский)
- **Обществознание (8-9 класс):** Resilience, посттравматический рост
- **Биология (9 класс):** Stages of Grief (Kübler-Ross)

**Локация:** **Врата Реальности** (новая зона в Swamp of Guilt)
- VCEM: До - V=-0.5, E=-0.7 (suffering), после - V=-0.2, E=-0.4 (pain без борьбы), M=+0.3

**Коан-переход:**
```
Вход: "Что, если в самой сильной буре есть якорь - твоё тело?"
→
Выход: "Что, если свобода начинается с принятия того, что есть, а не борьбы с тем, что было?"
```

**Reality Bridge:**
1. **Ритуал принятия** (когда застрял): Написать "Это случилось. Это реальность." 10 раз
2. **Дневник "Что я могу/не могу"**: Колонки - разделить
3. **Фраза силы**: "Это больно И я могу это вынести"

---

### Technique 4: "Решение Проблем vs Принятие"
**Источник:** DBT Problem-Solving Effectiveness, Decision Tree

**Психологическая суть:**
- Ключевой вопрос: "Могу ли я это изменить?"
  - ДА → Problem Solving
  - НЕТ → Radical Acceptance
- Дети часто:
  - Пытаются изменить неизменяемое (родители, других людей) → страдание
  - Принимают изменяемое (не решают проблемы) → helplessness
- Мудрость = знать разницу (Serenity Prayer adapted)

**Формула Мудрости:**
```
"Дай мне силы изменить то, что я могу,
Принять то, что не могу,
И мудрость отличить одно от другого."
```

**Игровая механика:**
- **Квест:** "Развилка Мудрости" (Fork of Wisdom)
- **NPC:** Мудрец (Sage) задаёт 3 вопроса:
  1. "Что тебя беспокоит?"
  2. "Можешь ли ТЫ это изменить?"
  3. "Если да → План. Если нет → Принятие."

**Decision Tree (визуализация в игре):**
```
                   ПРОБЛЕМА
                      |
           Могу ли я изменить?
           /                 \
        ДА                    НЕТ
         |                     |
   PROBLEM SOLVING      RADICAL ACCEPTANCE
         |                     |
   1. Определить цель     1. Признать реальность
   2. Brainstorm          2. Позволить боли
   3. Выбрать план        3. Двигаться дальше
   4. Действовать         4. Фокус на том, что можно
   5. Оценить
```

**Игровая сцена 1: Problem Solving (можно изменить)**
```
Ситуация: Ты получаешь плохие оценки по математике.
Беспокойство: "Я провалю год"

Мудрец: "Можешь ли ты изменить свои оценки?"
Игрок: "Да, если..."
Мудрец: "Тогда это Problem Solving. Давай план."

[Открывается Problem-Solving Worksheet]
1. Цель: Поднять оценку до 4
2. Варианты:
   - Нанять репетитора
   - Попросить помощь учителя
   - Заниматься с другом
   - YouTube уроки
3. Выбор: Попросить помощь учителя + друг
4. Действие: Подойти к учителю завтра
5. Deadline: Через неделю проверить прогресс

→ +0.12 Problem Solving, +0.08 Agency, -0.10 Helplessness
```

**Игровая сцена 2: Radical Acceptance (нельзя изменить)**
```
Ситуация: Ты не попал в школьную команду по футболу.
Беспокойство: "Это несправедливо!"

Мудрец: "Можешь ли ты изменить решение тренера?"
Игрок: [Честный выбор]
  A. "Да, если я буду умолять..." → False agency
  B. "Нет... это его решение" → Reality ✓

Мудрец: "Нет, это не в твоих руках. Radical Acceptance."

[Открывается Acceptance Path]
1. "Меня не взяли. Это случилось."
2. Почувствовать боль (разочарование, обиду)
3. "Что теперь? Что Я МОГУ?"
   - Тренироваться самостоятельно (готовиться к следующему году)
   - Найти другую команду/секцию
   - Играть для удовольствия, не для команды

→ +0.10 Radical Acceptance, +0.08 Resilience, -0.08 Rumination (на несправедливость)
```

**Частые ошибки (обучение через игру):**
| Ошибка | Пример | Правильно |
|--------|--------|-----------|
| Problem-Solving для неизменяемого | "Заставлю родителей вернуться" | Acceptance + фокус на адаптацию |
| Acceptance для изменяемого | "Буллинг - это жизнь, терпеть" | Problem Solving - сказать взрослым |
| Застревание в "за/против" | "Развод - плохо, я против" | Acceptance + жизнь дальше |

**Артефакт:**
- **Весы Мудрости** (tier 4)
- Burden: 0.06
- Эффект: +0.13 Wisdom (Change/Accept), +0.10 Problem-Solving, +0.08 Acceptance Discrimination

**Школьные предметы:**
- **Математика (7-9 класс):** Задачи с данными vs переменными
- **Литература (8-9 класс):** Герои, решающие vs принимающие
- **Обществознание (8-9 класс):** Локус контроля, agency
- **История (7-9 класс):** Исторические развилки - что было изменяемо?

**Локация:** **Развилка Мудрости** (между любыми двумя локациями)
- VCEM: V=+0.5, C=+0.8 (clarity), M=+0.7

**Коан-переход:**
```
Вход: "Что, если свобода начинается с принятия того, что есть?"
→
Выход: "Что, если мудрость - это знать, когда менять мир, а когда менять себя?"
```

**Reality Bridge:**
1. **Дневник Can/Can't** (3 раза/неделю): 2 колонки - могу изменить / не могу
2. **Фраза-напоминание**: "Могу ли я это изменить?" (на стикере)
3. **Семейная практика**: Обсуждать развилки вместе

---

## Integration Points

### With Other Modules:
- **Module 02 (DBT Basics):** Прогрессия от STOP → Opposite Action, TIPP
- **Module 07 (ACT):** Acceptance дополняется Radical Acceptance
- **Module 08 (Mindfulness):** Body awareness нужна для TIPP
- **Module 09 (Emotional Literacy):** Opposite Action требует знать эмоцию
- **Module 12 (Anxiety):** Opposite Action против avoidance
- **Module 22 (Loyalty Conflict):** Radical Acceptance развода

### Game Progression:
- **Prerequisites:** Module 02 (DBT), Module 08 (Mindfulness), Module 09 (Emotion Literacy)
- **Unlocks:** Module 12 (Anxiety Resilience), Module 19 (Self-Care advanced)

### UCAM Tags:
```json
{
  "dbt_advanced_tags": {
    "emotion_regulation": ["opposite_action", "fact_checking", "proportional_response"],
    "crisis_survival": ["TIPP", "self_harm_prevention", "panic_management"],
    "distress_tolerance": ["radical_acceptance", "pain_vs_suffering"],
    "effectiveness": ["problem_solving", "change_accept_discrimination"]
  },
  "clinical_priority": "HIGH - self-harm prevention, crisis management"
}
```

---

## Technical Specifications

### Vector DB Scenes:
35-40 сцен advanced DBT challenges:
- 12 сцен: Opposite Action (justified vs unjustified emotions)
- 8 сцен: TIPP crisis scenarios (panic, rage, self-harm urge)
- 10 сцен: Radical Acceptance (unchangeable situations)
- 8 сцен: Problem-Solving vs Acceptance discrimination

**Scene example:**
```json
{
  "scene_id": "DBT11-v1.0-opposite-C5B9",
  "ucam_schema": "v1.0",
  "module_id": "11_DBT_Advanced",
  "question": "Одноклассники смеются над твоей причёской. Ты чувствуешь сильный стыд (8/10) и хочешь уйти домой. Что делать?",
  "answers": [
    {"id": 0, "text": "Уйти домой, пропустить уроки", "tag": ["avoidance", "follow_emotion"]},
    {"id": 1, "text": "Накричать на них", "tag": ["impulse", "aggression"]},
    {"id": 2, "text": "Проверить факты: это стыдно? Нет. Opposite Action - остаюсь, поднимаю голову", "tag": ["adaptive", "opposite_action"]},
    {"id": 3, "text": "Ничего, просто терпеть", "tag": ["passive", "suppression"]}
  ],
  "correct_index": 2,
  "tags": {
    "emotion": "shame",
    "intensity": 8,
    "dbt_skill": "opposite_action",
    "fact_check": "unjustified_shame",
    "difficulty": 4
  },
  "followup_tags": ["self_worth", "assertiveness", "opposite_action_mastery"]
}
```

### UI/UX Features:
1. **Opposite Action Checker** (decision tree UI)
2. **TIPP Interactive** (mini-games для T, I, P, P)
3. **Acceptance Ritual** (step-by-step guided)
4. **Problem-Solving Worksheet** (fillable form)
5. **Can/Cannot Matrix** (2-column visual)

### MVP Scope:
- **Content:** ~50-55KB
- **Scenes:** 40 векторных
- **Artifacts:** 4 (Посох, Компас Бури, Ключ, Весы)
- **Locations:** 4 (Crossroads, Storm Island, Gates of Reality, Fork of Wisdom)
- **Mini-games:** 4 (для TIPP components)
- **School subjects:** 9 интеграций

---

## Success Metrics

### Learning Outcomes:
- Использует Opposite Action 3+ раз/неделю при неоправданных эмоциях
- Применяет TIPP при кризисе (8+ intensity) → снижение до 4-5
- Может назвать 3+ ситуации, где нужен Radical Acceptance
- Различает Problem-Solving vs Acceptance situations 80%+ точность

### Game Metrics:
- Opposite Action Skill ≥ 0.7
- Crisis Survival ≥ 0.65
- Radical Acceptance ≥ 0.6
- Problem-Solving Discrimination ≥ 0.7
- Self-Harm Urges снижение на 50%+

### Clinical Markers:
- Emotion Dysregulation (DERS) снижение на 35%
- Self-Harm Incidents снижение на 60%
- Problem-Solving ability рост на 40%
- Acceptance measures (AAQ-II adapted) improvement 30%

---

## References

### Clinical:
- Linehan, M. M. (2015). DBT Skills Training Manual (2nd ed.)
- Miller, A. L., Rathus, J. H., & Linehan, M. M. (2007). Dialectical Behavior Therapy with Suicidal Adolescents
- Rathus, J. H., & Miller, A. L. (2015). DBT Skills Manual for Adolescents
- Hayes, S. C., Strosahl, K. D., & Wilson, K. G. (2011). ACT (для Radical Acceptance)

### Game Design:
- InnerWorld002.txt DBT blocks
- UCAM crisis management protocols
- Gamification of distress tolerance skills

### Research:
- Goldstein, T. R., et al. (2015). Dialectical Behavior Therapy for Adolescents with Bipolar Disorder
- Mazza, J. J., et al. (2016). DBT Skills in Schools (DBT STEPS-A)

---

## Implementation Priority: VERY HIGH

**Rationale:**
- **Crisis management critical** for high-risk PA children (self-harm, suicide ideation)
- **Natural progression** from Module 02 (DBT Basics)
- **High clinical impact** - Opposite Action & TIPP are game-changers
- **Depends on:** Module 09 (emotion ID) - prerequisite met
- **Enables:** Module 12 (Anxiety), Module 19 (Self-Care) - advanced regulation
- **Research-backed** - DBT for adolescents has strongest evidence base

**Dependencies:**
- Requires: Module 02, 08, 09
- Enables: Module 12, 14, 19, 22 (loyalty conflict resolution)

**Safety Note:**
- TIPP & Crisis Survival must have **clinical oversight** for high-risk users
- Self-harm prevention protocol integration required
- Therapist notification triggers for crisis activation

**Next Module:** Module 14 (Communication Skills) - uses emotion regulation for effective expression
