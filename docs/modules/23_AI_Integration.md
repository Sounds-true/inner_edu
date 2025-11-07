# Implementation Plan: Module 23 - AI Integration & Adaptive Learning

## Module Overview
**Target:** Вся система InnerWorld Edu
**Цель:** Создать адаптивный AI-движок для персонализации контента, генерации сценариев, и непрерывного обучения
**Приоритет:** HIGH - основа для масштабирования и эффективности

## Core Components from InnerWorld002.txt

### Architecture Blueprint:
**Block 5: Vector Database Architecture** (Lines 897-983)
**Block 6: SUPER-PROMPT for o3-pro** (Lines 1095-1396)
**Plus: GPT001.md** - State machine, guardrails, strategy-first generation

### Three Pillars of AI Integration:

1. **VECTOR-MIND DB** - Семантический поиск сценариев
2. **Content Generator Agent** - Автоматическая генерация новых сценариев из источников
3. **Adaptive Learning Engine** - RL-based персонализация пути игрока

---

## Component 1: VECTOR-MIND Database

### Architecture (from InnerWorld002.txt Lines 922-967)

**Pipeline:**
```
Source (PDF/Book)
  → Ingestion-Crawler (Tesseract, pdfplumber)
  → SCENE-Extractor (o3-pro + SUPER-PROMPT)
  → Validator (JSON schema, pytest)
  → Vectorizer (text-embedding-3-large, 1536-D)
  → Tag-Encoder (UCAM multi-hot 40-D)
  → Upsert (Qdrant / Pinecone)
  → Online-Learner (RL-bandit, ClickHouse logs)
  → Re-weigh Index (nightly batch: scene_score update)
  → Retrieval API (FastAPI + LangServe)
```

### Schema (Complete):

```json
{
  "scene_id": "MODULE##-v1.0-tech#-HASH",
  "ucam_schema": "v1.0",
  "module_id": "22_Loyalty_Conflict",
  "lang": "ru",
  "question": "...",
  "answers": [
    {"id": 0, "text": "...", "tag": ["mind_reading"]},
    {"id": 1, "text": "...", "tag": ["adaptive"]},
    {"id": 2, "text": "...", "tag": ["catastrophizing"]}
  ],
  "correct_index": 1,
  "display_order": [2, 0, 1],
  "embedding_text": "question + distortion_answers (no adaptive)",
  "embedding_strategy": "distortion_focus",
  "image_hint": "...",
  "feedback": "...",
  "tags": {
    "emotion": "anxiety",
    "cbt": "mind_reading",
    "dbt": "check_the_facts",
    "love": null,
    "attachment": "anxious"
  },
  "context_trigger": {
    "type": "emotion_spike | tab_event | timer",
    "pattern": "anxiety>0.7 | facebook.com | 3h_idle"
  },
  "prereq_tags": ["catastrophizing>=2", "anxious>=3"],
  "followup_tags": ["check_the_facts", "opposite_action"],
  "difficulty": 1-3,
  "expected_reward": 0.0-1.0,
  "citation": "Author, Year, Page/DOI",
  "ext_tags": {
    "young_schema": "defectiveness",
    "PA_specific": true
  },
  "validation_checklist": {
    "evidence_cbt": true,
    "advice_specific": true,
    "answers_balanced": true
  },
  "new_tags": [],
  "tag_definitions": {}
}
```

### Embedding Model Selection (Lines 997-1028):

**POC/MVP (< 5K scenes):**
- Model: `text-embedding-3-small` (512-1024 dim)
- Cost: x1
- Precision@3: ~0.78-0.80
- Good enough for initial testing

**Production (> 25K scenes, multilingual):**
- Model: `text-embedding-3-large` (1536 dim)
- Cost: x2.2
- Precision@3: ~0.95-0.97
- Better for subtle psychological distinctions (mind-reading vs catastrophizing)

**Hybrid Approach:**
```python
# Indexing: o3-pro (stable, high quality)
# Online ad-hoc generation: o3 → nightly re-embed with o3-pro
```

### Retrieval Algorithm (Lines 955-967):

```python
def get_next_scene(player_profile, game_state):
    """
    Adaptive scene retrieval based on player's weak skills
    """
    # 1. Form user vector
    user_vec = weighted_avg(
        last_k_embedding_texts,
        weights=response_error  # higher weight for wrong answers
    )

    # 2. Amplify weak skills
    weak_skill = get_top_distortion(player_profile)  # e.g., "mind_reading"
    bonus = one_hot_encode(weak_skill) * lambda_boost

    # 3. Search with filters
    results = qdrant.search(
        vector=user_vec + bonus,
        filter={
            "must": [
                {"key": "difficulty", "match": {"value": player_level}},
                {"key": "module_id", "match": {"any": unlocked_modules}}
            ],
            "must_not": [
                {"key": "scene_id", "match": {"any": recent_seen_ids}}
            ]
        },
        limit=5,
        score_threshold=0.7
    )

    # 4. Select scene with novelty-familiarity balance
    scene = select_best(
        results,
        metric=alpha * similarity + beta * expected_reward - gamma * fatigue
    )

    return scene
```

### Versioning & Taxonomy Migration (Lines 1189-1241):

**Problem:** Когда появляются новые UCAM-теги (например, новый тип когнитивной ошибки из источника), старые сцены устаревают.

**Solution:**
```python
# 1. LLM adds new tags to "new_tags" field during generation
{
  "new_tags": ["anticipatory_guilt"],
  "tag_definitions": {
    "anticipatory_guilt": "Чувство вины за событие, которое ещё не произошло"
  }
}

# 2. Nightly taxonomy-migrator:
def migrate_taxonomy():
    new_scenes_with_tags = db.find({"new_tags": {"$ne": []}})

    for scene in new_scenes_with_tags:
        for tag in scene["new_tags"]:
            # Check for collisions/synonyms
            if is_duplicate(tag, UCAM_master):
                merge_tags(tag, existing_tag)
            else:
                UCAM_master.add(tag, scene["tag_definitions"][tag])

    # Bump schema version
    UCAM_master["version"] = increment_version()  # v1.0 → v1.1

    # Optional: Reclassify old scenes
    old_scenes = db.find({"ucam_schema": {"$lt": "v1.1"}})
    for scene in old_scenes:
        new_tags = llm_reclassify(scene, UCAM_master)
        db.update(scene, {"tags": new_tags, "ucam_schema": "v1.1"})

# 3. Vector store re-index (if tag-vector concatenation used)
reindex_with_new_dimension()
```

### KPI Metrics (Lines 968-973):

```python
KPI_TARGETS = {
    "therapy_gain": {
        "metric": "Δ% adaptive_answers / 7 days",
        "target": "↑ 10% per week"
    },
    "retrieval_precision": {
        "metric": "relevant_scenes in top-3 / 3",
        "target": "> 0.80"
    },
    "scene_fatigue": {
        "metric": "repeated_scenes / total_played",
        "target": "< 15%"
    },
    "engagement": {
        "metric": "avg_daily_scenes",
        "target": "≥ 4"
    },
    "learning_velocity": {
        "metric": "days_to_skill_threshold (e.g., defusion≥0.5)",
        "target": "< 14 days"
    }
}
```

---

## Component 2: Content Generator Agent (o3-pro)

### SUPER-PROMPT (from InnerWorld002.txt Lines 1273-1396)

**Role Definition:**
```
You are an expert in cognitive-behavioral therapy, game design,
emotional semantics, and vector knowledge systems.

Your task: Transform <SOURCE> (book, PDF, CBT manual, DBT guide,
ACT handbook, article) into a set of non-repeating, precisely
annotated, vectorizable interactive scenes for:
- Browser-based CBT/DBT game
- Adaptive therapy and self-reflection
- Gamification of emotional resilience
- Semantic navigation through psychological states
```

**Output Structure (10-step generation process):**

1. **Unique situation** - Life/metaphorical context triggering internal choice
2. **Question to player** - ≤150 chars, 2nd person, neutral
3. **3 answer variants:**
   - A = Cognitive distortion 1
   - B = Adaptive, healthy response
   - C = Cognitive distortion 2 (different type)
4. **Randomize positions** - Add `correct_index` field
5. **CBT/DBT feedback** - ≤100 chars
6. **UCAM annotation** - 5 dimensions (emotion, cbt, dbt, love, attachment)
7. **Visual hint** - One-line illustration description
8. **Citation** - Author, year, page/DOI
9. **Embedding text** - question + error answers (exclude adaptive)
10. **Full JSON** - All fields from schema above

**Extensibility & Meta-data (Lines 1212-1230):**
```json
{
  "ucam_schema": "v1.0",
  "scene_id": "<SRC>-v1.0-<page>-<hash4>",
  "lang": "ru",
  "display_order": [random permutation],
  "prereq_tags": ["catastrophizing>=2"],
  "followup_tags": ["check_the_facts"],
  "difficulty": 1-3,
  "context_trigger": {"type": "tab_event", "pattern": "facebook.com"},
  "expected_reward": 0.6,
  "ext_tags": {},
  "validation_checklist": {
    "evidence_cbt": true,
    "advice_specific": true,
    "answers_balanced": true
  },
  "new_tags": [],
  "tag_definitions": {}
}
```

### Quality Control (Lines 1384-1388):

```python
VALIDATION_RULES = {
    "scientific_accuracy": "Only verified CBT/DBT/ACT techniques",
    "non_judgmental": "No 'this is right/wrong', only gentle feedback",
    "non_clinical": "No diagnoses, no medical terms",
    "uniqueness": "Each scene unique by meaning and UCAM tags",
    "child_appropriate": "Language and scenarios for ages 7-14"
}
```

### Invocation Example:

```python
def generate_scenes_from_source(source_file, module_id, count=30):
    """
    Generate scenes using o3-pro and SUPER-PROMPT
    """
    source_text = extract_text(source_file)

    prompt = f"""
    {SUPER_PROMPT_TEMPLATE}

    <SOURCE>
    Title: {source_file.name}
    Module: {module_id}
    Text: {source_text[:50000]}  # o3-pro: 256k context
    </SOURCE>

    Generate {count} unique scenes following the schema.
    Focus on {MODULE_THEMES[module_id]}.
    """

    response = openai.ChatCompletion.create(
        model="o3-pro",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"}
    )

    scenes = json.loads(response.choices[0].message.content)

    # Validate
    validated_scenes = [s for s in scenes if validate_scene(s)]

    return validated_scenes
```

### Batch Processing Pipeline:

```bash
# For 23 modules × 30 scenes = 690 scenes
python scripts/generate_all_modules.py \
  --sources dna/*.pdf \
  --model o3-pro \
  --batch-size 30 \
  --output data/scenes/ \
  --validate

# Cost estimate: 690 scenes × ~500 tokens/scene × $0.03/1K ≈ $10-15
```

---

## Component 3: Adaptive Learning Engine (RL-based)

### Reinforcement Learning Loop (Lines 907-919, 955-967)

**Problem:** Каждый ребёнок уникален. Один застревает на mind-reading, другой на catastrophizing. Нужен адаптивный путь.

**Solution:** Multi-Armed Bandit + Contextual RL

### Algorithm: Contextual Bandit

```python
class AdaptiveLearningEngine:
    def __init__(self):
        self.scene_rewards = defaultdict(lambda: {"plays": 0, "success": 0})
        self.player_profiles = {}

    def select_scene(self, player_id, context):
        """
        ε-greedy bandit with context
        """
        profile = self.player_profiles[player_id]

        # Context: player's current skills, emotion state, time of day, etc.
        candidate_scenes = self.filter_by_context(context)

        # Epsilon-greedy exploration
        if random.random() < self.epsilon:
            # Explore: random scene
            scene = random.choice(candidate_scenes)
        else:
            # Exploit: scene with highest expected reward
            scene = max(
                candidate_scenes,
                key=lambda s: self.expected_value(s, profile, context)
            )

        return scene

    def expected_value(self, scene, profile, context):
        """
        UCB1 formula: mean_reward + sqrt(2*ln(total_plays)/scene_plays)
        """
        stats = self.scene_rewards[scene.id]
        if stats["plays"] == 0:
            return float('inf')  # Prioritize unexplored

        mean_reward = stats["success"] / stats["plays"]
        exploration_bonus = sqrt(2 * log(self.total_plays) / stats["plays"])

        # Context adjustment
        skill_match_bonus = self.skill_alignment(scene, profile)

        return mean_reward + exploration_bonus + skill_match_bonus

    def update(self, player_id, scene_id, outcome):
        """
        Update after player completes scene
        """
        # Outcome: 1 if adaptive answer chosen, 0 otherwise
        self.scene_rewards[scene_id]["plays"] += 1
        self.scene_rewards[scene_id]["success"] += outcome

        # Update player profile
        profile = self.player_profiles[player_id]
        for tag in scene.tags:
            profile[tag] = profile.get(tag, 0) + (1 if outcome else -0.5)

        # Log for analytics
        self.log_event(player_id, scene_id, outcome)
```

### Learning Velocity Optimization:

**Goal:** Minimize time to reach skill thresholds while maximizing engagement.

```python
def optimize_path(player_profile, target_skills):
    """
    Find optimal sequence of scenes to build target skills
    """
    # Current skill levels
    current = {skill: player_profile.get(skill, 0) for skill in target_skills}

    # Target thresholds
    targets = {skill: 0.7 for skill in target_skills}

    # Build graph of scenes
    scene_graph = build_prerequisite_graph()

    # Dynamic programming: shortest path with skill gains
    path = []
    while not all(current[s] >= targets[s] for s in target_skills):
        # Select scene with max skill gain / difficulty ratio
        best_scene = max(
            available_scenes(current, scene_graph),
            key=lambda s: skill_gain(s, current) / s.difficulty
        )

        path.append(best_scene)
        current = apply_scene_effects(current, best_scene)

    return path
```

### Player Profile Tracking:

```python
class PlayerProfile:
    def __init__(self, player_id):
        self.player_id = player_id
        self.skills = defaultdict(float)  # UCAM dimensions
        self.emotion_baseline = {}
        self.play_history = []
        self.weak_skills = []
        self.strong_skills = []

    def update_from_scene(self, scene, answer_chosen):
        """
        Update profile after scene completion
        """
        is_correct = (answer_chosen == scene.correct_index)

        # Update skill counters
        if is_correct:
            for tag in scene.followup_tags:
                self.skills[tag] += 0.05
        else:
            for tag in answer_chosen.tags:
                self.skills[tag] -= 0.03  # Identify weakness

        # Update weak/strong lists
        self.weak_skills = sorted(self.skills.items(), key=lambda x: x[1])[:5]
        self.strong_skills = sorted(self.skills.items(), key=lambda x: -x[1])[:5]

        # Emotion tracking
        self.emotion_baseline[scene.tags["emotion"]] = moving_avg(
            self.emotion_baseline.get(scene.tags["emotion"], 0.5),
            is_correct,
            alpha=0.1
        )

        self.play_history.append({
            "scene_id": scene.id,
            "timestamp": now(),
            "correct": is_correct,
            "time_spent": scene.time_spent
        })

    def get_next_focus(self):
        """
        Determine what to work on next
        """
        # Priority: worst skill below threshold
        for skill, level in self.weak_skills:
            if level < 0.4:  # Critical threshold
                return skill

        # If all above threshold: rotate through moderate skills
        moderate_skills = [s for s, l in self.skills.items() if 0.4 <= l < 0.7]
        return random.choice(moderate_skills) if moderate_skills else None
```

---

## Integration with Game Systems

### 1. Scene Injection Points:

```python
# When to serve AI-selected scenes:

TRIGGER_CONTEXTS = {
    "emotion_spike": {
        "condition": lambda state: state.anxiety > 0.7,
        "scene_filter": {"tags.emotion": "anxiety", "tags.dbt": ["STOPP", "grounding"]}
    },
    "skill_practice": {
        "condition": lambda state: state.location == "practice_arena",
        "scene_filter": {"prereq_tags": {"$all": state.player.unlocked_skills}}
    },
    "random_challenge": {
        "condition": lambda state: hours_since_last_scene >= 3,
        "scene_filter": {"difficulty": state.player.level}
    },
    "story_progression": {
        "condition": lambda state: state.quest == "loyalty_conflict_arc",
        "scene_filter": {"module_id": "22_Loyalty_Conflict"}
    }
}

def should_trigger_scene(game_state):
    for trigger_name, config in TRIGGER_CONTEXTS.items():
        if config["condition"](game_state):
            return trigger_name, config["scene_filter"]
    return None, None
```

### 2. NPC Integration:

**Each NPC becomes scene delivery vehicle:**

```python
NPC_SCENE_AFFINITY = {
    "Mirror_Fox": ["decision_science", "manipulation_detection", "cognitive_bias"],
    "Architect_of_Mind": ["cbt", "cognitive_restructuring", "STOPP"],
    "Musician_of_Heart": ["dbt", "emotion_regulation", "mindfulness"],
    "Echo_Child": ["ifs", "parts_work", "self_compassion", "PA_specific"]
}

def deliver_scene_via_npc(scene, game_state):
    """
    Match scene to appropriate NPC for thematic consistency
    """
    best_npc = None
    max_affinity = 0

    for npc, affinities in NPC_SCENE_AFFINITY.items():
        affinity_score = len(set(scene.tags.values()) & set(affinities))
        if affinity_score > max_affinity:
            max_affinity = affinity_score
            best_npc = npc

    return {
        "npc": best_npc,
        "location": game_state.get_npc_location(best_npc),
        "scene": scene,
        "dialogue_intro": generate_npc_intro(best_npc, scene)
    }
```

### 3. Artifact & Location System:

**Artifacts amplify specific skills** → feedback loop with RL engine

```python
def calculate_effective_difficulty(scene, player):
    """
    Adjust scene difficulty based on equipped artifacts
    """
    base_difficulty = scene.difficulty

    # Check artifact effects
    artifact_bonus = 0
    for artifact in player.equipped_artifacts:
        if artifact.skill_bonus.intersection(scene.tags):
            artifact_bonus += artifact.effect_magnitude

    effective_difficulty = base_difficulty * (1 - artifact_bonus)
    return max(1, effective_difficulty)  # Minimum difficulty 1
```

---

## Technical Implementation

### Stack:

```yaml
Vector Database: Qdrant (self-hosted) or Pinecone (cloud)
Embeddings: OpenAI text-embedding-3-large (1536-D)
LLM: o3-pro for generation, o3 for on-the-fly
RL Engine: Custom Python (scikit-learn, numpy)
Logging: ClickHouse (time-series player actions)
API: FastAPI + LangChain
Frontend: React (communicates via WebSocket for real-time)
```

### Data Flow:

```
[Player Action]
  → Game State Update
  → Trigger Check (emotion spike? timer? location?)
  → If trigger:
      → Query Vector DB (user_vec + weak_skill_boost)
      → Retrieve top-5 scenes
      → RL Engine selects best (exploration vs exploitation)
      → Render scene via NPC dialogue
  → Player answers
  → Log outcome (ClickHouse)
  → Update player profile
  → Update scene reward stats
  → (Nightly) Re-weigh scene index
```

### API Endpoints:

```python
# FastAPI routes

@app.post("/api/scenes/next")
def get_next_scene(player_id: str, context: GameContext):
    """
    Get adaptively selected next scene
    """
    profile = player_service.get_profile(player_id)
    trigger, filters = detect_trigger(context)

    scene = adaptive_engine.select_scene(profile, filters)

    return {
        "scene": scene,
        "npc": match_npc(scene),
        "location": scene.location
    }

@app.post("/api/scenes/complete")
def complete_scene(player_id: str, scene_id: str, answer_chosen: int):
    """
    Log scene completion and update player profile
    """
    scene = scene_service.get(scene_id)
    is_correct = (answer_chosen == scene.correct_index)

    # Update RL engine
    adaptive_engine.update(player_id, scene_id, is_correct)

    # Update player profile
    profile = player_service.get_profile(player_id)
    profile.update_from_scene(scene, answer_chosen)

    # Return feedback
    return {
        "correct": is_correct,
        "feedback": scene.feedback,
        "skill_change": profile.get_recent_skill_changes()
    }

@app.get("/api/player/{player_id}/dashboard")
def get_player_dashboard(player_id: str):
    """
    Analytics dashboard for player/therapist
    """
    profile = player_service.get_profile(player_id)

    return {
        "skills": profile.skills,
        "weak_skills": profile.weak_skills[:5],
        "strong_skills": profile.strong_skills[:5],
        "therapy_gain": calculate_therapy_gain(profile),
        "emotion_baseline": profile.emotion_baseline,
        "streak": profile.get_streak(),
        "total_scenes": len(profile.play_history)
    }

@app.post("/api/admin/generate_scenes")
@requires_auth
def generate_scenes(source_file: UploadFile, module_id: str, count: int = 30):
    """
    Admin endpoint: Generate scenes from new source
    """
    text = extract_text(source_file)
    scenes = content_generator.generate(text, module_id, count)

    # Validate and upsert
    validated = [s for s in scenes if validator.check(s)]
    vector_db.upsert_batch(validated)

    return {"generated": len(scenes), "valid": len(validated)}
```

### Privacy & Security:

```python
PRIVACY_RULES = {
    "PII": "Stored locally (chrome.storage), never sent to server",
    "Embeddings": "Anonymous vectors, no reverse-engineering to original text",
    "Logs": "Player actions logged with hashed IDs, no names",
    "Encryption": "All API calls over HTTPS, tokens JWT-based",
    "Retention": "Player can delete all data anytime (GDPR compliance)"
}
```

---

## MVP Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Set up Qdrant vector database
- [ ] Implement scene JSON schema & validation
- [ ] Generate initial 200 scenes (Modules 01-06) using o3-pro
- [ ] Build basic retrieval API (no RL yet)
- [ ] Simple random scene selection

**Deliverable:** 200 scenes searchable by UCAM tags

### Phase 2: Adaptive Engine (Weeks 5-8)
- [ ] Implement ε-greedy bandit algorithm
- [ ] Build player profile tracking system
- [ ] Add logging pipeline (ClickHouse)
- [ ] Connect scene selection to player weaknesses
- [ ] A/B test: random vs adaptive scene delivery

**Deliverable:** Adaptive scene selection working, measurable improvement in therapy gain

### Phase 3: Content Generation (Weeks 9-12)
- [ ] Finalize SUPER-PROMPT for all 23 modules
- [ ] Batch-generate remaining ~500 scenes
- [ ] Implement taxonomy migration system
- [ ] Build admin dashboard for scene management
- [ ] Quality assurance (human review of 10% scenes)

**Deliverable:** 700+ scenes covering all modules, extensible system

### Phase 4: Optimization & Scale (Weeks 13-16)
- [ ] Implement UCB1 for exploration-exploitation balance
- [ ] Add context triggers (emotion spikes, location, time)
- [ ] Optimize retrieval performance (<100ms)
- [ ] Multi-language support (EN/RU initially)
- [ ] Load testing (1000 concurrent players)

**Deliverable:** Production-ready, scalable system

---

## Success Metrics

### Technical KPIs:
- **Retrieval Precision@3:** ≥ 0.80 (relevant scenes in top-3)
- **API Latency:** < 100ms (99th percentile)
- **Scene Fatigue:** < 15% repeated scenes in 30-day window
- **Uptime:** 99.5%

### Learning KPIs:
- **Therapy Gain:** +10% adaptive answers per week
- **Learning Velocity:** Skill threshold (0.5 → 0.7) in ≤ 14 days
- **Engagement:** ≥ 4 scenes/day average
- **Retention:** 70% players active after 30 days

### Clinical KPIs (long-term):
- **Symptom Reduction:** 40-50% decrease in anxiety/depression scores (validated scales)
- **Skill Transfer:** 60% report using techniques in real life
- **Satisfaction:** NPS ≥ 50

---

## Safety & Ethics

### Algorithmic Fairness:
- **No discrimination:** RL engine must not disadvantage any demographic
- **Audit trail:** All scene selections logged for review
- **Human oversight:** Therapist can override AI suggestions

### Content Safety:
- **Validation:** All AI-generated scenes reviewed by clinical expert sample (10%)
- **Red flags:** System detects concerning patterns (suicidal ideation) → alert
- **Opt-out:** Player can always skip AI scenes, choose manual progression

### Transparency:
- **Explainability:** Player dashboard shows "Why this scene?" reasoning
- **Control:** Player can adjust difficulty, pace, focus areas
- **Data access:** Full export of player data anytime

---

## References

### Technical:
- **Sutton & Barto** (2018). Reinforcement Learning: An Introduction
- **Auer et al.** (2002). Finite-time Analysis of the Multiarmed Bandit Problem (UCB1)
- **Pinecone/Qdrant Docs** - Vector database architectures

### AI Safety:
- **Anthropic** (2024). Constitutional AI principles
- **OpenAI** (2023). GPT-4 System Card - safety mitigations

### Clinical AI:
- **Fitzpatrick et al.** (2017). Woebot - effectiveness of AI mental health chatbot
- **Ly et al.** (2017). Behavioral Insights on Mental Health App Engagement

### Sources:
- **InnerWorld002.txt** Lines 897-983 (Vector DB), 1095-1396 (SUPER-PROMPT)
- **GPT001.md** - State machine, guardrails, strategy patterns

---

## Integration with Other Modules

### Module Dependencies:
- **ALL modules** → Generate scenes → Feed into Vector DB
- **Module 06** (Decision Science) → Manipulation detection patterns
- **Module 22** (Loyalty Conflict) → Priority scenes for PA cases
- **Modules 01-05** → Foundation scenes must be in DB first

### Feedback Loops:
```
Player plays scene → Profile updated → Next scene adapted
      ↓
  Scene reward updated → Influences future selections
      ↓
  Low-performing scenes → Reviewed/improved/replaced
```

---

## Implementation Priority: CRITICAL

**Rationale:**
- **Force multiplier** - Makes all other modules adaptive and personalized
- **Scalability** - Can ingest new sources without manual scene creation
- **Clinical efficacy** - Adaptive learning proven more effective than fixed curriculum
- **Technical foundation** - Enables data-driven improvements
- **Clear ROI** - Reduces content creation time by 80%

**Dependencies:**
- Requires Modules 01-06 created first (source scenes)
- UCAM framework finalized
- Infrastructure (vector DB, API) set up

**Timeline:** 16 weeks for full MVP, but can start Phase 1 immediately with existing modules

---

## Next Steps

1. **Immediate:**
   - Set up Qdrant instance
   - Implement scene JSON validator
   - Generate first 50 scenes from existing modules using o3-pro

2. **Week 1-2:**
   - Build basic retrieval API
   - Create player profile data model
   - Integrate with game state

3. **Week 3-4:**
   - Implement ε-greedy bandit
   - Add logging pipeline
   - Run first A/B test

4. **Ongoing:**
   - Generate scenes for remaining modules
   - Tune RL hyperparameters (ε, α, λ)
   - Collect user feedback and iterate
