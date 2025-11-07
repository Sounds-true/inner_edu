# Implementation Plan: Module 10 - Anger Management

## Module Overview
**Target:** Дети 7-14 лет с проблемами контроля гнева, вспышками ярости, агрессивным поведением
**Цель:** Научить распознавать триггеры гнева, управлять интенсивностью, выражать злость конструктивно
**Источники:** CBT anger management research (meta-analysis d=0.70), McKay & Rogers "When Anger Hurts", Chapman "Anger: Taming a Powerful Emotion", UCAM emotional regulation framework

## Core Content: Anger as Information

### Anger Understanding Framework:
1. **Гнев как сигнал** - граница нарушена, несправедливость, фрустрация
2. **Физиология гнева** - активация симпатической нервной системы, кортизол/адреналин
3. **Anger escalation ladder** - раздражение (1-3) → злость (4-6) → ярость (7-10)
4. **Healthy vs Unhealthy anger** - конструктивное выражение vs деструктивное поведение

### Research Foundation:
**McKay, Rogers & McKay (2003)** - CBT-based anger control:
- Anger costs: interpersonal damage, health consequences, legal/social risks
- Cognitive restructuring: challenging anger-triggering thoughts
- Emergency anger control: immediate de-escalation techniques

**Chapman (2015)** - Taming anger:
- Anger styles: explosive, stuffed (suppressed), leaking (passive-aggressive)
- Healthy processing: assertive communication, problem-solving
- Personal anger assessment and triggers

**Meta-analysis (Lee & DiGiuseppe, 2018):**
- CBT for anger: effect size d=0.70 (76% better than untreated)
- Risk reduction: 23% general recidivism, 28% violent recidivism
- Techniques: cognitive restructuring, relaxation, skills training

### UCAM Integration:
```json
{
  "anger_management_skills": [
    "trigger_recognition",
    "early_warning_detection",
    "intensity_modulation",
    "cognitive_reframing",
    "assertive_expression",
    "consequence_awareness"
  ],
  "ucam_anger_regulation": {
    "detection_phase": "0-3/10 (early intervention)",
    "modulation_phase": "4-6/10 (active regulation)",
    "crisis_phase": "7-10/10 (emergency control)",
    "recovery_phase": "post-anger processing"
  }
}
```

---

## Techniques to Implement

### Technique 1: "Лестница Гнева" (Anger Ladder)
**Источник:** McKay & Rogers - anger escalation model, UCAM intensity tracking

**Психологическая суть:**
- Гнев нарастает постепенно: раздражение → злость → ярость → потеря контроля
- Дети часто "взрываются" мгновенно - не замечают ранние стадии
- Раннее обнаружение (1-3/10) → легче регулировать
- Для PA: научить замечать гнев ДО эскалации = предотвратить вспышку

**Игровая механика:**
- **Квест:** "Башня Огня" (Tower of Fire) - 10-этажная башня
- **Визуализация:** Вертикальная лестница с 10 ступенями:
  - Ступени 1-3: Зелёные (раздражение) - "Зона Контроля"
  - Ступени 4-6: Жёлтые (злость) - "Зона Выбора"
  - Ступени 7-9: Красные (ярость) - "Зона Опасности"
  - Ступень 10: Чёрная (потеря контроля) - "Взрыв"
- **Интерактив:**
  - В сценах конфликта появляется индикатор лестницы
  - Игрок видит, на какой ступени находится персонаж
  - Задача: использовать техники ДО ступени 7

**Игровая сцена:**
```
Ситуация: Учитель несправедливо обвиняет тебя при всех.
[Лестница Гнева активируется]

Ступень 1-2 (начало):
Гнев-Хранитель (NPC): "Ты на ступени 2. Лёгкое раздражение.
                       Ты МОЖЕШЬ остановить здесь."
Варианты:
  A. Глубокий вдох (техника) → Остаёшься на 2
  B. "Это несправедливо!" (мысль без действия) → Поднимаешься на 4
  C. Промолчать, копить → Поднимаешься на 5

Ступень 5-6 (эскалация):
Гнев-Хранитель: "Жёлтая зона. Гнев растёт. Ещё можно выбирать."
Варианты:
  A. Time-out → Спускаешься на 3 ✓
  B. "Я ТАК ЗОЛ!" (фокус на гневе) → Поднимаешься на 8
  C. Переформулировать мысль → Спускаешься на 4 ✓

Ступень 8-9 (опасность):
Гнев-Хранитель: "СТОП! Красная зона. Сейчас или никогда!"
Emergency options:
  A. Покинуть ситуацию СЕЙЧАС → Выход из башни ✓
  B. Дыхание 4-7-8 (экстренное) → Спуск на 6 ✓
  C. Крик/удар → Ступень 10, взрыв (consequence cutscene)

→ Если игрок регулярно останавливается на 1-4: +0.12 Early Detection
→ Если доходит до 8+: Игра показывает последствия (отношения, репутация)
```

**Ladder Mapping (игровой дизайн):**
```javascript
{
  "anger_ladder": {
    "1-3": {
      "label": "Раздражение",
      "body_cues": ["лёгкое напряжение", "ускорение пульса"],
      "thoughts": ["это неприятно", "не нравится"],
      "intervention": ["дыхание", "self-talk", "awareness"],
      "success_rate": "95%"
    },
    "4-6": {
      "label": "Злость",
      "body_cues": ["жар в лице", "сжатие кулаков", "громче голос"],
      "thoughts": ["это несправедливо!", "я не позволю!"],
      "intervention": ["time-out", "cognitive_reframe", "assertive_statement"],
      "success_rate": "70%"
    },
    "7-9": {
      "label": "Ярость",
      "body_cues": ["тремор", "туннельное зрение", "потеря логики"],
      "thoughts": ["я НЕНАВИЖУ!", "они заплатят!"],
      "intervention": ["emergency_exit", "intensive_breathing", "physical_release"],
      "success_rate": "30%"
    },
    "10": {
      "label": "Взрыв",
      "body_cues": ["действие без мысли"],
      "thoughts": ["нет мыслей"],
      "intervention": ["too_late", "damage_control_after"],
      "consequence": "relationship_damage, regret, shame"
    }
  }
}
```

**Артефакт:**
- **Компас Ярости** (tier 2)
- Burden: 0.04
- Эффект: +0.12 Anger Early Detection, +0.08 Escalation Awareness, -0.10 Impulsivity

**Школьные предметы:**
- **Биология (7-9 класс):** Симпатическая нервная система, стресс-реакция
- **Физика (7-8 класс):** Энергия, эскалация процессов
- **Математика (5-7 класс):** Шкалы, градации
- **ОБЖ (6-8 класс):** Управление стрессом, конфликты

**Локация:** **Башня Огня (Tower of Fire)** - новая локация
- VCEM: V=-0.3 (mild threat), C=+0.7, E=-0.6 (anger practice), M=+0.8 (empowerment)

**Коан-переход:**
```
Вход: "Что, если гнев - это огонь, и ты можешь заметить искру до пожара?"
→
Выход: "Что, если каждая ступень гнева - это выбор: подняться или остановиться?"
```

**Reality Bridge:**
1. **Anger Log** (ежедневно): Записать гнев дня + ступень (1-10) + что сделал
2. **Early Warning Practice** (утро): "Какие признаки тела я замечу на ступени 2?"
3. **Ladder Review** (вечер): "Где сегодня я был на лестнице? Когда остановился?"

---

### Technique 2: "Детектор Триггеров" (Trigger Detective)
**Источник:** Chapman "Anger: Taming a Powerful Emotion" - personal anger assessment

**Психологическая суть:**
- У каждого свои триггеры гнева (несправедливость, критика, игнорирование)
- Дети не осознают паттерны - "просто взбесился"
- Предсказуемость триггеров → можно подготовиться
- Для PA: триггеры часто связаны с родителями - важно распознать

**Игровая механика:**
- **Квест:** "Детектив Огня" (Fire Detective Quest)
- **Метафора:** Игрок = детектив, расследующий свои вспышки гнева
- **Механика:**
  - После каждого anger incident игра предлагает "Расследование"
  - Вопросы:
    1. Что случилось ПРЯМО ПЕРЕД гневом?
    2. Кто был рядом?
    3. Что было сказано/сделано?
    4. Где ты был?
    5. Какая мысль возникла?
  - После 5-7 расследований → паттерн выявлен → Триггер-карта

**Игровая сцена:**
```
[После конфликта с одноклассником]
Детектив-NPC: "Стоп. Давай расследуем. Что было триггером?"

Вопрос 1: Что случилось прямо перед тем, как ты разозлился?
  A. Он сказал, что я плохо играю
  B. Он не позвал меня в команду
  C. Он смеялся надо мной → Выбрано

Вопрос 2: Какая мысль возникла?
  A. "Он не прав"
  B. "Он меня унижает" → Выбрано (core belief detected)
  C. "Мне всё равно"

Вопрос 3: Где в теле ты почувствовал гнев первым?
  A. Лицо (жар)
  B. Кулаки (сжатие) → Выбрано
  C. Живот

[После 5 расследований]
Детектив: "У меня паттерн! Твой главный триггер: УНИЖЕНИЕ/НАСМЕШКА.
           Когда кто-то смеётся над тобой → мысль 'меня унижают' → гнев 8/10.
           Теперь ты ЗНАЕШЬ. Можешь подготовиться."

→ Триггер добавлен в Личную Карту
→ +0.10 Trigger Awareness, unlocked: Trigger Preparation Quest
```

**Common Triggers (PA children):**
```javascript
{
  "trigger_categories": {
    "Injustice": "Несправедливость, двойные стандарты (особенно от родителей)",
    "Criticism": "Критика, обесценивание, 'ты неправильный'",
    "Ignoring": "Игнорирование, 'тебя нет', невидимость",
    "Humiliation": "Насмешка, публичный стыд, унижение",
    "Control": "Контроль, приказы, 'делай как я сказал'",
    "Loyalty_Demand": "Требование выбрать родителя (PA specific)",
    "Comparison": "Сравнение с братом/сестрой/другим родителем",
    "Broken_Promise": "Нарушенное обещание, обман"
  },
  "trigger_response_plan": {
    "detection": "Я знаю, что НАСМЕШКА - мой триггер",
    "prediction": "Если одноклассник начнёт смеяться, я могу разозлиться",
    "preparation": "Я заранее скажу себе: 'Это триггер. Я замечу его на ступени 2'",
    "intervention": "Использую технику (дыхание, time-out, reframe)"
  }
}
```

**Артефакт:**
- **Карта Триггеров** (tier 3, уникальная для игрока)
- Burden: 0.05
- Эффект: +0.15 Trigger Awareness, +0.10 Predictability, +0.08 Preparedness

**Школьные предметы:**
- **Литература (6-9 класс):** Мотивы героев, что провоцирует конфликт
- **История (7-9 класс):** Причины войн, конфликтов
- **Обществознание (7-9 класс):** Конфликт интересов, переговоры
- **Информатика (7-9 класс):** Паттерны, алгоритмы, причинно-следственные связи

**Локация:** **Кабинет Детектива** (новая микро-зона в Tower of Fire)
- VCEM: V=+0.5, C=+0.9 (ясность паттернов), E=+0.3, M=+0.7

**Коан-переход:**
```
Вход: "Что, если каждая ступень гнева - это выбор: подняться или остановиться?"
→
Выход: "Что, если твой гнев имеет узор, и увидеть узор - значит получить силу?"
```

**Reality Bridge:**
1. **Trigger Journal** (после гнева): "Что было триггером сегодня?"
2. **Prediction Game** (утро): "Где сегодня могут быть мои триггеры?"
3. **Family Trigger Map** (с психологом): Карта триггеров в отношениях с родителями

---

### Technique 3: "Когнитивный Рефрейминг" (Thought Remix)
**Источник:** CBT anger management - cognitive restructuring (McKay & Rogers, Lee & DiGiuseppe meta-analysis)

**Психологическая суть:**
- Гнев запускается не ситуацией, а ИНТЕРПРЕТАЦИЕЙ
- "Он специально!" vs "Может, он не заметил" → разные уровни гнева
- Дети склонны к hostile attribution bias (приписывание злого умысла)
- CBT: изменить мысль → изменить эмоцию

**Игровая механика:**
- **Квест:** "Студия Ремикса Мыслей" (Thought Remix Studio)
- **Метафора:** Мысли = музыка, можно сделать другой ремикс
- **Механика:**
  - В anger-провоцирующей сцене игра показывает 3 мысли:
    1. **Hostile** (враждебная): "Он нарочно! Он хочет меня унизить!"
    2. **Neutral** (нейтральная): "Может, он не подумал"
    3. **Alternative** (альтернативная): "Возможно, у него был плохой день"
  - Игрок выбирает мысль → гнев меняется (10/10 → 5/10 → 2/10)
  - NPC Ремиксёр Мыслей помогает создавать альтернативы

**Игровая сцена:**
```
Ситуация: Друг не ответил на твоё сообщение 3 часа.

[Автоматическая мысль (default):]
"Он игнорирует меня! Я ему не важен! Он плохой друг!"
→ Гнев: 8/10

Ремиксёр: "Стоп. Это ONE версия мысли. Давай сделаем ремикс."

[Студия открывается - 3 трека:]

Track 1 (Hostile):
"Он специально не отвечает, чтобы меня наказать!"
→ Гнев: 9/10

Track 2 (Neutral):
"Возможно, он занят. Или телефон разрядился."
→ Гнев: 3/10

Track 3 (Alternative):
"Может, у него проблемы, и он не может ответить."
→ Гнев: 1/10, +concern for friend

Игрок выбирает Track 2 или 3 → гнев снижается
Ремиксёр: "Видишь? Одна ситуация, разные мысли, разный гнев.
           Ты можешь выбирать мысль."

→ +0.08 Cognitive Flexibility, +0.10 Anger Reduction
```

**CBT Cognitive Distortions (PA context):**
```javascript
{
  "common_anger_distortions": {
    "Mind_Reading": {
      "distortion": "Он думает, что я плохой!",
      "challenge": "Откуда ты знаешь? Какие доказательства?",
      "reframe": "Я не знаю, что он думает. Могу спросить."
    },
    "Catastrophizing": {
      "distortion": "Она не позвонила = она меня бросила!",
      "challenge": "Одно действие = всё разрушено?",
      "reframe": "Одно действие - не приговор."
    },
    "Personalization": {
      "distortion": "Папа опоздал - ему на меня плевать!",
      "challenge": "Может, другая причина?",
      "reframe": "Возможно, пробки. Не обязательно про меня."
    },
    "Should_Statements": {
      "distortion": "Он ДОЛЖЕН был понять!",
      "challenge": "'Должен' = реальность?",
      "reframe": "Хотелось бы, чтобы понял. Но люди не всегда понимают."
    },
    "Hostile_Attribution": {
      "distortion": "Она нарочно забыла пригласить!",
      "challenge": "Злой умысел или ошибка?",
      "reframe": "Возможно, забыла. Люди ошибаются."
    }
  }
}
```

**Артефакт:**
- **Пластинка Ремикса** (tier 3)
- Burden: 0.05
- Эффект: +0.14 Cognitive Flexibility, +0.11 Anger Reduction, -0.09 Hostile Attribution Bias

**Школьные предметы:**
- **Литература (7-9 класс):** Точка зрения, интерпретация событий
- **Обществознание (7-9 класс):** Критическое мышление, предрассудки
- **История (8-9 класс):** Разные версии событий, пропаганда
- **Философия (9 класс):** Субъективность восприятия

**Локация:** **Студия Ремикса** (в Tower of Fire)
- VCEM: V=+0.6, C=+0.8, E=-0.3 → +0.2 (change through reframe), M=+0.7

**Коан-переход:**
```
Вход: "Что, если твой гнев имеет узор, и увидеть узор - значит получить силу?"
→
Выход: "Что, если одна история может быть рассказана тремя голосами, и ты выбираешь, какой слушать?"
```

**Reality Bridge:**
1. **Thought Record** (при гневе): Записать автоматическую мысль + альтернативу
2. **Evidence Check**: "Какие доказательства ЗА и ПРОТИВ этой мысли?"
3. **Reframe Practice** (3 раза/неделю): Взять гнев-ситуацию, сделать 3 ремикса

---

### Technique 4: "Конструктивный Канал Гнева" (Anger Outlet)
**Источник:** Chapman - healthy vs unhealthy anger expression, DBT Emotion Regulation

**Психологическая суть:**
- Гнев несёт энергию - нужен ВЫХОД (не подавление)
- Unhealthy outlets: агрессия, разрушение, passive-aggressive
- Healthy outlets: физическая активность, творчество, assertive communication
- Для PA: учить выражать гнев безопасно (не на родителей, не на себя)

**Игровая механика:**
- **Квест:** "Каналы Силы" (Channels of Power)
- **Метафора:** Гнев = река, нужен правильный канал (не разлив)
- **Механика:**
  - Когда гнев достигает 5+/10, активируется "Outlet Menu"
  - Игрок выбирает канал:
    1. **Физический:** Побить подушку, пробежка, спорт
    2. **Творческий:** Рисовать гнев, написать письмо (не отправлять)
    3. **Вербальный:** Assertive I-statement, диалог
    4. **Деструктивный:** Крик на кого-то, удар → негативные последствия
  - Правильный канал → гнев снижается + сохранение отношений

**Игровая сцена:**
```
Ситуация: Мама отменила обещанную поездку. Гнев 7/10.

[Outlet Menu появляется]
Хранитель Каналов: "Гнев силён. Куда направишь реку?"

Опции:
A. Физический Канал:
   - "Побить подушку в комнате" → Гнев 7→4, энергия выпущена ✓
   - "Пробежаться вокруг дома" → Гнев 7→3, +endorphins ✓

B. Творческий Канал:
   - "Нарисовать гнев (красный, чёрный)" → Гнев 7→5, +insight ✓
   - "Написать письмо (не отправлять)" → Гнев 7→4, организация мыслей ✓

C. Вербальный Канал:
   - "Я зол, что ты отменила. Я рассчитывал" (I-statement) → Гнев 7→5, диалог начат ✓
   - "Я поговорю, когда успокоюсь" (timeout) → Гнев 7→4, мудрый выбор ✓

D. Деструктивный Канал:
   - "Ты ВСЕГДА так! Я тебя ненавижу!" → Гнев 7→9, конфликт эскалировал
   - "Хлопнуть дверью, молчать 3 дня" → Гнев 7→6, passive-aggressive, отношения хуже
   - "Сломать что-то" → Гнев 7→4, но последствия (стыд, ущерб)

[Если выбран A, B или C:]
Хранитель: "Река нашла канал. Энергия выпущена, мосты целы."
→ +0.12 Healthy Outlet, +0.08 Relationship Preservation

[Если выбран D:]
Хранитель: "Река разлилась. Теперь чинить мосты..."
→ Cutscene последствий (отношения ухудшились, стыд, сожаление)
```

**Anger Outlets Framework:**
```javascript
{
  "healthy_outlets": {
    "Physical": {
      "options": ["pillow_punch", "run", "sports", "dance", "cleanup"],
      "effect": "Releases cortisol/adrenaline, -40% anger intensity",
      "preserves": "relationships"
    },
    "Creative": {
      "options": ["draw_anger", "write_letter", "music", "craft"],
      "effect": "Transforms emotion, +insight, -30% anger",
      "preserves": "relationships + gains understanding"
    },
    "Verbal_Assertive": {
      "options": ["I_statement", "timeout_then_talk", "problem_solving"],
      "effect": "Direct communication, -50% anger + resolution",
      "preserves": "relationships + strengthens"
    },
    "Mindful": {
      "options": ["breathing", "meditation", "body_scan"],
      "effect": "Parasympathetic activation, -35% anger",
      "preserves": "relationships + self-regulation"
    }
  },
  "unhealthy_outlets": {
    "Aggressive": {
      "options": ["yell", "hit_person", "destroy"],
      "short_term": "-40% anger",
      "long_term": "relationship_damage, guilt, shame, escalation"
    },
    "Passive_Aggressive": {
      "options": ["silent_treatment", "sabotage", "sarcasm"],
      "short_term": "-10% anger",
      "long_term": "relationship_erosion, unresolved_conflict"
    },
    "Suppression": {
      "options": ["deny", "stuff", "smile"],
      "short_term": "0% anger reduction",
      "long_term": "somatic_symptoms, explosion_later, depression"
    }
  }
}
```

**Артефакт:**
- **Ключ Каналов** (tier 3)
- Burden: 0.05
- Эффект: +0.13 Healthy Expression, +0.10 Energy Release, -0.11 Aggression

**Школьные предметы:**
- **Физкультура (5-9 класс):** Спорт как выход энергии
- **ИЗО (5-8 класс):** Выражение эмоций через искусство
- **Литература (7-9 класс):** Конфликт и разрешение
- **Обществознание (7-9 класс):** Коммуникация, ассертивность

**Локация:** **Зал Каналов** (в Tower of Fire)
- VCEM: V=+0.6, C=+0.7, E=-0.5 → +0.3 (after outlet), M=+0.8

**Коан-переход:**
```
Вход: "Что, если одна история может быть рассказана тремя голосами?"
→
Выход: "Что, если гнев - это река, и мудрость - не остановить её, а направить?"
```

**Reality Bridge:**
1. **Outlet Menu** (на холодильник/стену): Список healthy outlets при гневе
2. **Physical Practice** (3 раза/неделю): Пробовать разные outlets (подушка, бег, рисование)
3. **Family Anger Plan**: Договориться, как выражать гнев дома (time-out, I-statements)

---

### Technique 5: "Последствия и Ремонт" (Consequences & Repair)
**Источник:** Chapman - costs of anger, Restorative Justice principles

**Психологическая суть:**
- Неконтролируемый гнев имеет цену (отношения, репутация, здоровье)
- Дети не видят долгосрочные последствия - импульсивность
- После вспышки нужен "ремонт" (извинения, восстановление)
- Для PA: понимание, что гнев на родителя (даже заслуженный) имеет цену

**Игровая механика:**
- **Квест:** "Цена Огня" (Cost of Fire)
- **Механика:**
  - Если игрок выбирает деструктивный гнев (крик, агрессия) → cutscene последствий
  - Последствия показываются в 3 измерениях:
    1. **Отношения:** NPC обиделся, доверие снизилось
    2. **Репутация:** Другие NPC узнали, избегают игрока
    3. **Внутреннее:** Стыд, вина, сожаление (эмоция после гнева)
  - После последствий → квест "Ремонт Моста" (repair quest)

**Игровая сцена (последствия):**
```
[Игрок накричал на друга из-за мелочи]

[Cutscene: Consequences]
1. Друг отворачивается, лицо грустное.
   → Relationship score: -15
   → Диалог закрыт на 2 игровых дня

2. Одноклассник видел сцену:
   → Репутация: "Вспыльчивый" (negative trait added)
   → Другие NPC осторожнее в диалогах

3. Внутреннее состояние игрока:
   → Guilt +0.6, Shame +0.4
   → Мысль: "Зачем я так сказал... Я плохой друг"

[Appears: Хранитель Ремонта]
"Огонь обжёг мост. Но мосты можно чинить. Готов к ремонту?"

[Repair Quest активируется]
Шаги ремонта:
1. **Признание:** "Я был не прав. Я накричал."
2. **Ответственность:** "Это моя вина, не твоя."
3. **Извинение:** "Мне жаль. Прости."
4. **План:** "Я буду работать над гневом. Если снова злюсь - возьму паузу."

[Если все шаги пройдены:]
Друг: "Спасибо, что сказал. Я всё ещё обижен, но принимаю извинение."
→ Relationship восстанавливается до -5 (не сразу 0, нужно время)
→ +0.10 Repair Skills, +0.08 Accountability

[Если игрок отказывается от ремонта:]
→ Relationship остаётся -15
→ Друг избегает игрока
→ Последующие квесты закрыты
```

**Costs of Uncontrolled Anger (визуализация в игре):**
```javascript
{
  "anger_costs": {
    "Relationship_Damage": {
      "immediate": "Hurt feelings, trust broken",
      "long_term": "Friendship lost, isolation",
      "PA_context": "Parent alienated further, child feels worse"
    },
    "Reputation": {
      "immediate": "Labeled as 'angry kid'",
      "long_term": "Social avoidance, fewer opportunities",
      "PA_context": "Seen as 'problem child' by court/therapists"
    },
    "Internal_Cost": {
      "immediate": "Guilt, shame, regret",
      "long_term": "Low self-esteem, 'I'm bad' belief",
      "PA_context": "Reinforces PA narrative ('you're broken')"
    },
    "Physical_Health": {
      "immediate": "Elevated cortisol, exhaustion",
      "long_term": "Cardiovascular risk, weakened immune system"
    }
  },
  "repair_framework": {
    "step_1": "Acknowledge (what I did)",
    "step_2": "Responsibility (it's my fault)",
    "step_3": "Apologize (I'm sorry)",
    "step_4": "Amends (how I'll fix/prevent)",
    "outcome": "Relationship restored (not erased, but healed)"
  }
}
```

**Артефакт:**
- **Набор Ремонта Мостов** (tier 3)
- Burden: 0.04
- Эффект: +0.12 Repair Skills, +0.10 Accountability, +0.08 Consequence Awareness

**Школьные предметы:**
- **Обществознание (7-9 класс):** Restorative justice, ответственность
- **Литература (6-9 класс):** Последствия действий героев
- **История (7-9 класс):** Последствия решений лидеров
- **Право (9 класс):** Ответственность, возмещение ущерба

**Локация:** **Мост Ремонта** (между локациями, появляется после anger damage)
- VCEM: V=+0.3, C=+0.7, E=mixed (shame+hope), M=+0.5

**Коан-переход:**
```
Вход: "Что, если гнев - это река, и мудрость - направить её?"
→
Выход: "Что, если каждый обожжённый мост можно починить, и это требует больше смелости, чем разрушить?"
```

**Reality Bridge:**
1. **Anger Consequence Log** (после вспышки): "Какая была цена? (отношения, чувства)"
2. **Repair Practice** (сразу после гнева): 4 шага ремонта с человеком
3. **Prevention Plan** (еженедельно): "Как я могу предотвратить вспышку на следующей неделе?"

---

## Integration Points

### With Other Modules:
- **Module 09 (Emotional Literacy):** Нужно распознать гнев, чтобы регулировать его
- **Module 02 (DBT):** Opposite Action, Distress Tolerance для anger emergencies
- **Module 08 (Mindfulness):** Body awareness для early detection гнева
- **Module 14 (Communication):** Assertive expression вместо агрессии
- **Module 22 (Loyalty Conflict):** Гнев на отчуждающего родителя - ключевая тема

### Game Progression:
- **Prerequisite:** Module 09 (Emotional Literacy - anger identification)
- **Unlocks:** Module 14 (Communication - assertive anger expression)

### UCAM Tags:
```json
{
  "anger_management_dimensions": {
    "detection": ["triggers", "early_warning", "ladder_awareness"],
    "regulation": ["cognitive_reframe", "intensity_modulation"],
    "expression": ["healthy_outlets", "assertive_communication"],
    "repair": ["consequence_awareness", "apology", "restoration"]
  },
  "clinical_targets": ["aggression", "impulsivity", "hostile_attribution", "relationship_damage"],
  "developmental_stage": ["7-14 years", "impulse_control_development"]
}
```

---

## Technical Specifications

### Vector DB Scenes:
30-35 anger management scenes:
- 10 scenes: Anger Ladder (escalation detection)
- 8 scenes: Trigger Detective (pattern recognition)
- 7 scenes: Cognitive Reframing (thought alternatives)
- 5 scenes: Healthy Outlets (expression choice)
- 5 scenes: Consequences & Repair (restoration)

**Scene example:**
```json
{
  "scene_id": "ANG10-v1.0-reframe-B2F8",
  "ucam_schema": "v1.0",
  "module_id": "10_Anger_Management",
  "question": "Учитель поставил тебе тройку, хотя ты старался. Первая мысль: 'Он несправедливый! Он меня ненавидит!' Гнев: 8/10. Какую мысль ты выберешь?",
  "answers": [
    {"id": 0, "text": "Он ДЕЙСТВИТЕЛЬНО меня ненавидит! (усиление)", "tag": ["hostile_attribution", "escalation"]},
    {"id": 1, "text": "Возможно, он оценивал строго. Не обязательно про меня.", "tag": ["adaptive", "reframe", "anger_reduction"]},
    {"id": 2, "text": "Может, я могу спросить, как улучшить?", "tag": ["adaptive", "problem_solving", "best"]},
    {"id": 3, "text": "Мне всё равно (подавление)", "tag": ["suppression", "avoidance"]}
  ],
  "correct_index": 2,
  "tags": {
    "emotion": "anger",
    "intensity": 8,
    "technique": "cognitive_reframing",
    "difficulty": 3
  }
}
```

### UI/UX Features:
1. **Anger Ladder** (vertical 10-step indicator, color-coded)
2. **Trigger Map** (personal, updates as player discovers patterns)
3. **Thought Remix Studio** (3 thought tracks to choose)
4. **Outlet Menu** (appears at 5+ anger, shows options)
5. **Consequence Cutscenes** (relationship/reputation impact visualization)
6. **Repair Quest Interface** (4-step guided process)

### MVP Scope:
- **Content:** ~50-55KB
- **Scenes:** 35 vector scenes
- **Artifacts:** 5 (Компас Ярости, Карта Триггеров, Пластинка Ремикса, Ключ Каналов, Набор Ремонта)
- **Locations:** 4 (Tower of Fire, Detective Office, Remix Studio, Channels Hall, Repair Bridge)
- **NPCs:** 4 (Anger Keeper, Detective, Remixer, Repair Keeper)
- **School subjects:** 11 integrations

---

## Success Metrics

### Learning Outcomes:
- Ребёнок распознаёт гнев на ступенях 1-3 (раннее обнаружение)
- Знает 3+ личных триггера гнева
- Может сделать cognitive reframe в 70%+ ситуаций
- Использует healthy outlet вместо агрессии 4+ раз/неделю
- Выполняет repair после вспышки (извинение, план)

### Game Metrics:
- Anger Early Detection ≥ 0.70
- Trigger Awareness ≥ 0.65
- Cognitive Flexibility ≥ 0.60
- Healthy Expression ≥ 0.70
- Aggression снижение на 50%

### Clinical Markers:
- Aggression Questionnaire (AQ) снижение на 35%
- Anger escalation frequency снижение на 40%
- Relationship conflict снижение на 30%
- Repair attempts увеличение на 60%

---

## References

### Clinical:
- Lee, A. H., & DiGiuseppe, R. (2018). Anger and aggression treatments: a review of meta-analyses. *Current Opinion in Psychology*, 19, 65-74.
- McKay, M., Rogers, P. D., & McKay, J. (2003). *When Anger Hurts: Quieting the Storm Within* (2nd ed.). New Harbinger Publications.
- Blake, C. S., & Hamrin, V. (2007). Current approaches to the assessment and management of anger and aggression in youth: a review. *Journal of Child and Adolescent Psychiatric Nursing*, 20(4), 209-221.
- Sukhodolsky, D. G., Kassinove, H., & Gorman, B. S. (2004). Cognitive-behavioral therapy for anger in children and adolescents: A meta-analysis. *Aggression and Violent Behavior*, 9(3), 247-269.

### Books:
- Chapman, G. (2015). *Anger: Taming a Powerful Emotion*. Moody Publishers. ISBN: 9780802413147
- Lerner, H. (2014). *The Dance of Anger*. William Morrow Paperbacks.
- Novaco, R. W. (2007). Anger dysregulation. In T. A. Cavell & K. T. Malcolm (Eds.), *Anger, aggression, and interventions for interpersonal violence* (pp. 3-54). Lawrence Erlbaum Associates.

### Game Design:
- UCAM anger regulation framework
- Research on gamification of SEL (anger management modules)
- DBT skills for adolescents (distress tolerance, emotion regulation)

---

## Implementation Priority: VERY HIGH

**Rationale:**
- **Critical for PA children** - anger at alienating parent, outbursts common
- **Strong research base** - CBT meta-analysis shows d=0.70 effect size
- **Clear game mechanics** - Ladder, Triggers, Reframe, Outlets, Repair are implementable
- **Prerequisite for social skills** - need anger control before communication training
- **Aligns with school curriculum** - biology (stress response), social studies (conflict)
- **Immediate safety impact** - reduces aggression, prevents relationship damage

**Dependencies:**
- Requires: Module 09 (Emotional Literacy - anger identification)
- Enables: Module 14 (Communication Skills - assertive expression), Module 22 (Loyalty Conflict)

**Next Module:** Module 13 (Grief Processing) - processing loss of family structure
