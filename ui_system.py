"""
✨ ULTRA-PREMIUM UI SYSTEM
Modern, futuristic message formatting with glassmorphism effects
"""

from typing import Dict, Any, List
from datetime import datetime
import json

class UIThemes:
    """Futuristic theme system"""
    
    # ═════════════════════════════════════════════════════════════
    # 🌑 DARK LUXURY THEME (Default)
    # ═════════════════════════════════════════════════════════════
    
    DARK_LUXURY = {
        "divider": "╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌",
        "top_bar": "✦ ",
        "accent": "◆",
        "premium": "💎",
        "status_on": "🟢",
        "status_off": "🔴",
        "loading": "⚙️",
        "success": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️",
    }
    
    # ═════════════════════════════════════════════════════════════
    # 🔮 NEON GLASS THEME
    # ═════════════════════════════════════════════════════════════
    
    NEON_GLASS = {
        "divider": "━━━━━━━━━━━━━━━━━━━",
        "top_bar": "█ ",
        "accent": "▓",
        "premium": "🔮",
        "status_on": "💫",
        "status_off": "☆",
        "loading": "⚡",
        "success": "✔️",
        "error": "✘",
        "info": "▸",
        "warning": "⧗",
    }
    
    # ═════════════════════════════════════════════════════════════
    # 💧 AQUA NEON THEME
    # ═════════════════════════════════════════════════════════════
    
    AQUA_NEON = {
        "divider": "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈",
        "top_bar": "≋ ",
        "accent": "◇",
        "premium": "💠",
        "status_on": "💧",
        "status_off": "💤",
        "loading": "🌀",
        "success": "🌊",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️",
    }


class PremiumUI:
    """Ultra-premium UI formatting"""
    
    def __init__(self, theme="dark_luxury"):
        """Initialize with theme"""
        self.theme = self._get_theme(theme)
    
    def _get_theme(self, theme_name):
        """Get theme by name"""
        themes = {
            "dark_luxury": UIThemes.DARK_LUXURY,
            "neon_glass": UIThemes.NEON_GLASS,
            "aqua_neon": UIThemes.AQUA_NEON,
        }
        return themes.get(theme_name, UIThemes.DARK_LUXURY)
    
    # ═════════════════════════════════════════════════════════════
    # 📦 HEADER BUILDER
    # ═════════════════════════════════════════════════════════════
    
    def header(self, title: str, emoji: str = "✦") -> str:
        """Build premium header"""
        return f"{emoji} {title}\n{self.theme['divider']}\n"
    
    # ═════════════════════════════════════════════════════════════
    # 📊 STAT BOX
    # ═════════════════════════════════════════════════════════════
    
    def stat_line(self, label: str, value: str, emoji: str = "") -> str:
        """Build stat line"""
        icon = f"{emoji} " if emoji else ""
        return f"{icon}{label}: `{value}`\n"
    
    # ═════════════════════════════════════════════════════════════
    # 📋 PROFILE CARD
    # ═════════════════════════════════════════════════════════════
    
    def profile_card(self, user_data: Dict[str, Any]) -> str:
        """Build beautiful profile card"""
        msg = self.header("YOUR PROFILE", "👤")
        
        msg += f"""
{self.theme['accent']} *User ID:* `{user_data.get('user_id', 'N/A')}`
{self.theme['accent']} *Username:* @{user_data.get('username', 'anonymous')}
{self.theme['accent']} *Status:* {user_data.get('status', 'Active')}

{self.theme['divider']}

"""
        
        # Stats section
        msg += f"""*📊 STATISTICS*
├─ Level: *{user_data.get('level', 1)}*
├─ XP: *{user_data.get('xp', 0)}*
├─ Searches: *{user_data.get('searches', 0)}*
└─ Joined: *{user_data.get('joined', 'N/A')}*

"""
        
        # Premium section
        premium_status = "🟢 ACTIVE" if user_data.get('is_premium') else "🔴 INACTIVE"
        msg += f"*💎 PREMIUM:* {premium_status}\n"
        
        if user_data.get('premium_expiry'):
            msg += f"├─ Expires: `{user_data.get('premium_expiry')}`\n"
        
        msg += f"\n{self.theme['divider']}\n"
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 📈 STATS PANEL
    # ═════════════════════════════════════════════════════════════
    
    def stats_panel(self, stats: Dict[str, Any]) -> str:
        """Build statistics panel"""
        msg = self.header("BOT STATISTICS", "📊")
        
        msg += f"""
*👥 USERS*
├─ Total: `{stats.get('total_users', 0)}`
├─ Premium: `{stats.get('premium_users', 0)}`
├─ Active: `{stats.get('active_users', 0)}`
└─ Banned: `{stats.get('banned_users', 0)}`

*🔍 ACTIVITY*
├─ Searches: `{stats.get('total_searches', 0)}`
├─ Commands: `{stats.get('total_commands', 0)}`
└─ Avg Response: `{stats.get('avg_response_time', 0)}ms`

*⚙️ SYSTEM*
├─ Uptime: `{stats.get('uptime', 'N/A')}`
├─ Latency: `{stats.get('latency', 'N/A')}ms`
└─ Database: `{stats.get('db_size', 'N/A')}`

{self.theme['divider']}
"""
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 💎 PREMIUM SHOWCASE
    # ═════════════════════════════════════════════════════════════
    
    def premium_card(self, user_premium: Dict[str, Any] = None) -> str:
        """Build premium card"""
        msg = self.header("PREMIUM FEATURES", "💎")
        
        if user_premium and user_premium.get('is_premium'):
            msg += f"""
✅ *YOUR PREMIUM IS ACTIVE*

├─ Tier: *{user_premium.get('tier', 'Pro')}*
├─ Expires: *{user_premium.get('expiry', 'N/A')}*
├─ Days Left: *{user_premium.get('days_left', 0)}*
└─ Auto Renew: *{'Yes' if user_premium.get('auto_renew') else 'No'}*

"""
        else:
            msg += """
❌ *FREE ACCOUNT*

"""
        
        msg += f"""*🎁 ACTIVE BENEFITS*
├─ Searches: `{'Unlimited' if user_premium and user_premium.get('is_premium') else '50/day'}`
├─ Cooldown: `{'0.5s' if user_premium and user_premium.get('is_premium') else '2s'}`
├─ Support: `Priority` if user_premium and user_premium.get('is_premium') else 'Standard'`
└─ Badge: `{'✨ VIP' if user_premium and user_premium.get('is_premium') else '⭐ Free'}`

*💰 PRICING*
├─ Pro: 30d → ₹99
├─ Ultra: 90d → ₹249
├─ Elite: 365d → ₹999
└─ Lifetime: ∞ → ₹4999

{self.theme['divider']}
"""
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 🏆 LEADERBOARD
    # ═════════════════════════════════════════════════════════════
    
    def leaderboard(self, users: List[Dict], user_rank: int = 0) -> str:
        """Build leaderboard"""
        msg = self.header("GLOBAL LEADERBOARD", "🏆")
        
        msg += "*Top 10 Users*\n"
        
        for idx, user in enumerate(users[:10], 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}️⃣"
            msg += f"{medal} {user['username']} - XP: {user['xp']}\n"
        
        msg += f"\n*Your Rank:* `#{user_rank}`\n"
        msg += f"\n{self.theme['divider']}\n"
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 🔐 SECURITY PANEL
    # ═════════════════════════════════════════════════════════════
    
    def security_panel(self, security_data: Dict[str, Any]) -> str:
        """Build security panel"""
        msg = self.header("SECURITY STATUS", "🔐")
        
        msg += f"""
*🛡️ ACCOUNT SECURITY*
├─ Status: {security_data.get('status', '🟢 SECURE')}
├─ 2FA: {'🟢 ENABLED' if security_data.get('2fa') else '🔴 DISABLED'}
├─ Last Login: `{security_data.get('last_login', 'N/A')}`
└─ Suspicious Activity: `{security_data.get('suspicious', 'None')}`

*🚨 RECENT ACTIVITIES*
"""
        
        for activity in security_data.get('recent_activities', [])[:5]:
            msg += f"├─ {activity}\n"
        
        msg += f"\n{self.theme['divider']}\n"
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # ⭐ ACHIEVEMENTS
    # ═════════════════════════════════════════════════════════════
    
    def achievements(self, achievements_data: List[Dict]) -> str:
        """Build achievements display"""
        msg = self.header("ACHIEVEMENTS", "⭐")
        
        for achievement in achievements_data:
            status = "🔓" if achievement.get('unlocked') else "🔒"
            msg += f"{status} {achievement['name']} - {achievement['description']}\n"
        
        msg += f"\n{self.theme['divider']}\n"
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 🎯 REFERRAL SYSTEM
    # ═════════════════════════════════════════════════════════════
    
    def referral_panel(self, referral_data: Dict[str, Any]) -> str:
        """Build referral panel"""
        msg = self.header("REFERRAL PROGRAM", "🎯")
        
        msg += f"""
*🔗 YOUR REFERRAL LINK*
`{referral_data.get('ref_link', 'Loading...')}`

*📊 STATISTICS*
├─ Referred: `{referral_data.get('referred_count', 0)}`
├─ Rewards: `{referral_data.get('rewards', 0)}`
├─ Commission: `{referral_data.get('commission', '0')}%`
└─ Earned: `₹{referral_data.get('earned', 0)}`

*🎁 BONUSES*
├─ First Referral: +100 XP
├─ 5 Referrals: +500 XP + Coupon
├─ 10 Referrals: +1000 XP + Premium 7d
└─ 50 Referrals: VIP Badge + Lifetime 10% Off

{self.theme['divider']}
"""
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 🚀 LOADING STATES
    # ═════════════════════════════════════════════════════════════
    
    def loading(self, stage: str = "initializing") -> str:
        """Loading animation text"""
        stages = {
            "init": "⚙️ Initializing system...",
            "verify": "🔐 Verifying credentials...",
            "sync": "🛰️ Syncing data...",
            "load": "📡 Loading workspace...",
            "auth": "🧿 Authenticating...",
            "process": "⚡ Processing request...",
        }
        return stages.get(stage, "⏳ Please wait...")
    
    # ═════════════════════════════════════════════════════════════
    # ✅ SUCCESS MESSAGES
    # ═════════════════════════════════════════════════════════════
    
    def success(self, title: str, details: Dict[str, str] = None) -> str:
        """Success message"""
        msg = f"✅ *{title}*\n\n"
        
        if details:
            for key, value in details.items():
                msg += f"├─ {key}: `{value}`\n"
            msg += f"\n{self.theme['divider']}\n"
        
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # ❌ ERROR MESSAGES
    # ═════════════════════════════════════════════════════════════
    
    def error(self, title: str, message: str = "") -> str:
        """Error message"""
        msg = f"❌ *{title}*\n"
        if message:
            msg += f"\n{message}\n"
        msg += f"\n{self.theme['divider']}\n"
        return msg
    
    # ═════════════════════════════════════════════════════════════
    # 📋 LIST DISPLAY
    # ═════════════════════════════════════════════════════════════
    
    def list_display(self, title: str, items: List[str], emoji: str = "") -> str:
        """Display list"""
        msg = self.header(title, emoji)
        
        for idx, item in enumerate(items, 1):
            msg += f"{idx}. {item}\n"
        
        msg += f"\n{self.theme['divider']}\n"
        
        return msg


# ═════════════════════════════════════════════════════════════════════════════════
# 🎨 QUICK UI GENERATORS
# ═════════════════════════════════════════════════════════════════════════════════

class QuickUI:
    """Quick UI generation helpers"""
    
    @staticmethod
    def box(title: str, content: str = "") -> str:
        """Create a box"""
        header = f"╔{'═' * 40}╗\n║ {title:^38} ║\n╚{'═' * 40}╝\n"
        return header + content
    
    @staticmethod
    def divider(length: int = 42) -> str:
        """Create divider"""
        return "─" * length + "\n"
    
    @staticmethod
    def status_badge(status: str, emoji: str = "🟢") -> str:
        """Create status badge"""
        return f"{emoji} {status}"
    
    @staticmethod
    def progress_bar(current: int, total: int, length: int = 10) -> str:
        """Create progress bar"""
        filled = int(length * current / total)
        bar = "█" * filled + "░" * (length - filled)
        percentage = int(100 * current / total)
        return f"[{bar}] {percentage}%"


# ═════════════════════════════════════════════════════════════════════════════════
# 🔤 TEXT FORMATTING HELPERS
# ═════════════════════════════════════════════════════════════════════════════════

class TextFormat:
    """Text formatting utilities"""
    
    @staticmethod
    def bold(text: str) -> str:
        return f"*{text}*"
    
    @staticmethod
    def italic(text: str) -> str:
        return f"_{text}_"
    
    @staticmethod
    def code(text: str) -> str:
        return f"`{text}`"
    
    @staticmethod
    def code_block(text: str, language: str = "") -> str:
        return f"```{language}\n{text}\n```"
    
    @staticmethod
    def link(text: str, url: str) -> str:
        return f"[{text}]({url})"
    
    @staticmethod
    def mention(user_id: int, name: str = "") -> str:
        if name:
            return f"@{name}"
        return f"[User](tg://user?id={user_id})"

