"""
Configuration for InnerWorld Edu Bot
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "src" / "data"
SCENARIOS_DIR = DATA_DIR / "scenarios"
QUESTS_DIR = DATA_DIR / "quests"
LOCATIONS_DIR = DATA_DIR / "locations"
USER_PROFILES_DIR = DATA_DIR / "user_profiles"
PARENTS_DIR = DATA_DIR / "parents"
LINKS_DIR = DATA_DIR / "links"

# Bot tokens (from environment variables)
CHILD_BOT_TOKEN = os.getenv("CHILD_BOT_TOKEN", "")
PARENT_BOT_TOKEN = os.getenv("PARENT_BOT_TOKEN", "")

# Mode configuration
DEFAULT_MODE = "educational"  # educational | therapeutic

# Educational Mode settings
EDUCATIONAL_MODULES = [2, 4, 5, 6, 8, 9, 14, 15, 16, 17, 19, 20]  # 12 modules
EDUCATIONAL_LOCATIONS = [
    "tower_confusion",
    "valley_words",
    "mountain_emptiness",
    "forest_calm",
    "city_mind",
    "workshop_creator",
    "bridge_actions"
]

# Therapeutic Mode settings (activated on demand)
THERAPEUTIC_MODULES = list(range(1, 24))  # All 23 modules
THERAPEUTIC_LOCATIONS = [
    "desert_fear",
    "swamp_guilt",
    "mountain_control",
    "island_dependency",
    "forest_interest",
    "city_relations",
    "harbor_acceptance",
    "peak_ecstasy",
    "cave_shadow",
    "zen_garden",
    "gate_self"
]

# Screening thresholds for transition
SCREENING_THRESHOLDS = {
    "mild_concern": {
        "self_worth": 0.4,
        "self_criticism": 0.6,
        "emotional_volatility": 0.5,
        "manipulation_score": 5
    },
    "moderate_concern": {
        "self_worth": 0.35,
        "self_criticism": 0.65,
        "emotional_volatility": 0.6,
        "manipulation_score": 7
    },
    "high_concern": {
        "self_worth": 0.3,
        "self_criticism": 0.7,
        "emotional_volatility": 0.7,
        "manipulation_score": 10
    },
    "critical": {
        "self_harm_keywords": ["навредить себе", "умереть", "покончить", "не хочу жить"],
        "emotional_storm_threshold": 10,
        "emotional_storm_duration_minutes": 60
    }
}

# Parent Dashboard settings
WEEKLY_REPORT_DAY = 0  # Monday (0=Monday, 6=Sunday)
WEEKLY_REPORT_HOUR = 9  # 9:00 AM
LINK_EXPIRATION_HOURS = 48

# Time limits (in minutes)
DEFAULT_TIME_LIMIT = None  # No limit
TIME_LIMIT_OPTIONS = [30, 60, 120, None]

# Emotional states
EMOTIONAL_STATES = ["tiredness", "anxiety", "anger", "interest", "doubt"]

# Learning profile dimensions
LEARNING_DIMENSIONS = ["understanding_meaning", "memory", "attention", "motivation"]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "bot.log"

# Database (for Therapeutic Mode - not used in MVP)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Feature flags
FEATURES = {
    "parent_dashboard": True,
    "screening_system": True,
    "therapeutic_mode": False,  # Not yet implemented
    "reality_bridge": True,
    "achievements": True,
}
