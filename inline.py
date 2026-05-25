# keyboards/inline.py
"""
Colored Inline Keyboard System
Premium button styling with neon aesthetics
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class InlineKeyboards:
    """Premium inline keyboard factory"""
    
    # Button Color Presets
    PRIMARY = "primary"
    SUCCESS = "success"
    DANGER = "danger"
    PREMIUM = "premium"
    NEUTRAL = "neutral"
    
    @staticmethod
    def dashboard() -> InlineKeyboardMarkup:
        """Main dashboard keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔍 NEURAL SEARCH", callback_data="osint_menu"),
                InlineKeyboardButton("💎 ELITE ACCESS", callback_data="premium_show"),
            ],
            [
                InlineKeyboardButton("📊 QUANTUM STATS", callback_data="stats_show"),
                InlineKeyboardButton("🎁 REFERRAL NEXUS", callback_data="referral_show"),
            ],
            [
                InlineKeyboardButton("👤 NEURAL ID", callback_data="profile_show"),
                InlineKeyboardButton("⚙️ SYSTEM CONFIG", callback_data="settings_show"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def premium_selector() -> InlineKeyboardMarkup:
        """Premium tier selector"""
        keyboard = [
            [
                InlineKeyboardButton("🟢 PRO", callback_data="premium_pro"),
                InlineKeyboardButton("🟣 ULTRA", callback_data="premium_ultra"),
                InlineKeyboardButton("🟡 ELITE", callback_data="premium_elite"),
            ],
            [
                InlineKeyboardButton("🔑 REDEEM KEY", callback_data="premium_redeem"),
            ],
            [
                InlineKeyboardButton("◀️ BACK TO DASHBOARD", callback_data="dashboard"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def osint_menu() -> InlineKeyboardMarkup:
        """OSINT operations menu"""
        keyboard = [
            [
                InlineKeyboardButton("📞 PHONE", callback_data="osint_phone"),
                InlineKeyboardButton("🚗 VEHICLE", callback_data="osint_vehicle"),
                InlineKeyboardButton("🌐 IP", callback_data="osint_ip"),
            ],
            [
                InlineKeyboardButton("🐙 GITHUB", callback_data="osint_github"),
                InlineKeyboardButton("📸 INSTAGRAM", callback_data="osint_instagram"),
                InlineKeyboardButton("👤 TELEGRAM", callback_data="osint_telegram"),
            ],
            [
                InlineKeyboardButton("◀️ BACK", callback_data="dashboard"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_panel() -> InlineKeyboardMarkup:
        """Admin control panel"""
        keyboard = [
            [
                InlineKeyboardButton("📡 MONITOR", callback_data="admin_monitor"),
                InlineKeyboardButton("👥 USERS", callback_data="admin_users"),
            ],
            [
                InlineKeyboardButton("🔑 GEN KEYS", callback_data="admin_genkey"),
                InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
            ],
            [
                InlineKeyboardButton("🚫 BAN", callback_data="admin_ban"),
                InlineKeyboardButton("📊 ANALYTICS", callback_data="admin_analytics"),
            ],
            [
                InlineKeyboardButton("🧾 LOGS", callback_data="admin_logs"),
                InlineKeyboardButton("⚙️ CONFIG", callback_data="admin_config"),
            ],
            [
                InlineKeyboardButton("◀️ EXIT", callback_data="dashboard"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def pagination(page: int, total: int, prefix: str) -> InlineKeyboardMarkup:
        """Pagination system"""
        keyboard = []
        
        # Page navigation
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️", callback_data=f"{prefix}_prev"))
        nav_buttons.append(InlineKeyboardButton(f"{page + 1}/{total}", callback_data="noop"))
        if page < total - 1:
            nav_buttons.append(InlineKeyboardButton("▶️", callback_data=f"{prefix}_next"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Back button
        keyboard.append([InlineKeyboardButton("◀️ BACK", callback_data="dashboard")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def settings_menu(current_theme: str) -> InlineKeyboardMarkup:
        """Settings menu with theme selector"""
        themes = ["DARK LUXURY", "NEON GLASS", "AI OS", "AQUA NEON", "ROYAL ELITE"]
        
        keyboard = []
        for theme in themes:
            indicator = "✓ " if theme.lower().replace(" ", "_") == current_theme else "  "
            keyboard.append([
                InlineKeyboardButton(f"{indicator}{theme}", callback_data=f"theme_{theme.lower().replace(' ', '_')}")
            ])
        
        keyboard.append([InlineKeyboardButton("◀️ BACK", callback_data="dashboard")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_action(action: str, item_id: str = None) -> InlineKeyboardMarkup:
        """Confirmation dialog"""
        keyboard = [
            [
                InlineKeyboardButton("✅ CONFIRM", callback_data=f"confirm_{action}_{item_id}" if item_id else f"confirm_{action}"),
                InlineKeyboardButton("❌ CANCEL", callback_data="dashboard"),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def rewards_menu() -> InlineKeyboardMarkup:
        """Rewards and achievements"""
        keyboard = [
            [
                InlineKeyboardButton("🎖️ ACHIEVEMENTS", callback_data="rewards_achievements"),
                InlineKeyboardButton("📅 DAILY", callback_data="rewards_daily"),
            ],
            [
                InlineKeyboardButton("🏆 LEADERBOARD", callback_data="rewards_leaderboard"),
                InlineKeyboardButton("🎁 CLAIM", callback_data="rewards_claim"),
            ],
            [
                InlineKeyboardButton("◀️ BACK", callback_data="dashboard"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)