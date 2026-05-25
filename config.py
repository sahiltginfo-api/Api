"""
DATATRACE X — Neural Configuration
Quantum-secure parameters
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CORE IDENTITY ====================
BOT_TOKEN = os.getenv("BOT_TOKEN", "7567122521:AAFjinkRtf1JuNew5WkganbhdEaBIVsdSxg")
BOT_OWNER_ID = int(os.getenv("6512242172", "0"))
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "PRODUCTION")  # DEVELOPMENT | PRODUCTION

# ==================== DATABASE ====================
DATABASE_PATH = "sahil_x.db"

# ==================== PREMIUM CONFIG ====================
PREMIUM_TIERS = {
    "FREE": {"daily_limit": 50, "cooldown": 2.0},
    "PRO": {"daily_limit": 500, "cooldown": 1.0},
    "ULTRA": {"daily_limit": 2000, "cooldown": 0.5},
    "ELITE": {"daily_limit": 10000, "cooldown": 0.1}
}

# ==================== GAMIFICATION ====================
XP_PER_SEARCH = 10
XP_PER_REFERRAL = 100
STREAK_BONUS = 50
LEVEL_FORMULA = lambda xp: int(xp ** 0.5) + 1

# ==================== RATE LIMITING ====================
GLOBAL_RATE_LIMIT = 30  # requests per minute
ANTI_FLOOD_WINDOW = 5  # seconds
ANTI_FLOOD_LIMIT = 5  # messages per window

# ==================== AI RESPONSES ====================
AI_WELCOME_MESSAGES = [
    "🌌 Neural interface established. Welcome back.",
    "⚡ Core systems online. Ready for operation.",
    "🧠 AI engine synchronized. Awaiting commands.",
    "🛰️ Secure channel open. Your session is encrypted.",
]

# ==================== THEMES ====================
AVAILABLE_THEMES = [
    "dark_luxury",
    "neon_glass", 
    "ai_os",
    "aqua_neon",
    "royal_elite"
]

DEFAULT_THEME = "dark_luxury"

# ==================== REFERRAL ====================
REFERRAL_REWARD_XP = 100
REFERRAL_REWARD_DAYS = 3  # Premium days for referral

# ==================== KEY GENERATION ====================
KEY_PREFIX = "DTX"
KEY_SECTIONS = 4
KEY_LENGTH = 6