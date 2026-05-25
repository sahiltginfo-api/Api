"""
🎛️ ULTRA-PREMIUM KEYBOARD SYSTEM
Modern, compact, glassmorphism-style inline keyboards
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

class PremiumKeyboards:
    """Modern, compact keyboard layouts"""

    # ═══════════════════════════════════════════════════════════════
    # 🏠 MAIN MENU - Compact 2x2 grid
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Premium main menu"""
        buttons = [
            [
                InlineKeyboardButton("⚡ LAUNCH", callback_data="launch_menu"),
                InlineKeyboardButton("📊 STATS", callback_data="stats_panel"),
            ],
            [
                InlineKeyboardButton("💎 PREMIUM", callback_data="premium_menu"),
                InlineKeyboardButton("🎁 REWARDS", callback_data="rewards_menu"),
            ],
            [
                InlineKeyboardButton("👤 PROFILE", callback_data="profile_menu"),
                InlineKeyboardButton("⚙️ SETTINGS", callback_data="settings_menu"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 🚀 LAUNCH MENU - OSINT Commands
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def launch_menu() -> InlineKeyboardMarkup:
        """Launch/OSINT commands menu"""
        buttons = [
            [
                InlineKeyboardButton("📞 NUMBER", callback_data="cmd_number"),
                InlineKeyboardButton("🚗 VEHICLE", callback_data="cmd_vehicle"),
            ],
            [
                InlineKeyboardButton("📸 INSTAGRAM", callback_data="cmd_instagram"),
                InlineKeyboardButton("🐙 GITHUB", callback_data="cmd_github"),
            ],
            [
                InlineKeyboardButton("🌐 IP LOOKUP", callback_data="cmd_ip"),
                InlineKeyboardButton("🎮 FREE FIRE", callback_data="cmd_ff"),
            ],
            [
                InlineKeyboardButton("✈️ TELEGRAM", callback_data="cmd_telegram"),
                InlineKeyboardButton("🏦 BANK INFO", callback_data="cmd_bank"),
            ],
            [InlineKeyboardButton("◀️ BACK", callback_data="back_main")],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 💎 PREMIUM MENU
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def premium_menu() -> InlineKeyboardMarkup:
        """Premium subscription menu"""
        buttons = [
            [
                InlineKeyboardButton("💰 PRICING", callback_data="premium_pricing"),
                InlineKeyboardButton("🔑 REDEEM", callback_data="premium_redeem"),
            ],
            [
                InlineKeyboardButton("📊 MY PLAN", callback_data="premium_myplan"),
                InlineKeyboardButton("🎯 BENEFITS", callback_data="premium_benefits"),
            ],
            [
                InlineKeyboardButton("📞 SUPPORT", url="https://t.me/support"),
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 🎁 REWARDS MENU
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def rewards_menu() -> InlineKeyboardMarkup:
        """Gamification and rewards menu"""
        buttons = [
            [
                InlineKeyboardButton("🏆 RANK", callback_data="rewards_rank"),
                InlineKeyboardButton("⭐ ACHIEVEMENTS", callback_data="rewards_achievements"),
            ],
            [
                InlineKeyboardButton("🎯 REFERRAL", callback_data="rewards_referral"),
                InlineKeyboardButton("📅 DAILY", callback_data="rewards_daily"),
            ],
            [
                InlineKeyboardButton("🎫 COUPONS", callback_data="rewards_coupons"),
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 👤 PROFILE MENU
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def profile_menu() -> InlineKeyboardMarkup:
        """User profile menu"""
        buttons = [
            [
                InlineKeyboardButton("📋 VIEW PROFILE", callback_data="profile_view"),
                InlineKeyboardButton("📈 STATISTICS", callback_data="profile_stats"),
            ],
            [
                InlineKeyboardButton("🎨 THEME", callback_data="profile_theme"),
                InlineKeyboardButton("🔔 NOTIFY", callback_data="profile_notify"),
            ],
            [
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # ⚙️ SETTINGS MENU
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Settings menu"""
        buttons = [
            [
                InlineKeyboardButton("🎨 THEME", callback_data="settings_theme"),
                InlineKeyboardButton("🔔 ALERTS", callback_data="settings_alerts"),
            ],
            [
                InlineKeyboardButton("🔐 SECURITY", callback_data="settings_security"),
                InlineKeyboardButton("❓ HELP", callback_data="settings_help"),
            ],
            [
                InlineKeyboardButton("📞 SUPPORT", url="https://t.me/support"),
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 👑 ADMIN PANEL
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def admin_panel() -> InlineKeyboardMarkup:
        """Admin control center"""
        buttons = [
            [
                InlineKeyboardButton("📊 ANALYTICS", callback_data="admin_analytics"),
                InlineKeyboardButton("👥 USERS", callback_data="admin_users"),
            ],
            [
                InlineKeyboardButton("🔑 KEYS", callback_data="admin_keys"),
                InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
            ],
            [
                InlineKeyboardButton("🚫 BAN", callback_data="admin_ban"),
                InlineKeyboardButton("📝 LOGS", callback_data="admin_logs"),
            ],
            [
                InlineKeyboardButton("🛡️ SECURITY", callback_data="admin_security"),
                InlineKeyboardButton("🔧 CONFIG", callback_data="admin_config"),
            ],
            [
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 📱 QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def quick_actions(is_premium: bool = False) -> InlineKeyboardMarkup:
        """Quick action buttons"""
        buttons = [
            [
                InlineKeyboardButton("🚀 START", callback_data="action_start"),
                InlineKeyboardButton("📞 SUPPORT", url="https://t.me/support"),
            ],
        ]
        if not is_premium:
            buttons.append([InlineKeyboardButton("💎 UPGRADE", callback_data="upgrade_premium")])
        buttons.append([InlineKeyboardButton("🏠 HOME", callback_data="back_main")])
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # ⏮️ NAVIGATION BUTTONS
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def navigation(page: int = 1, max_pages: int = 1) -> InlineKeyboardMarkup:
        """Navigation with pagination"""
        buttons = []
        nav_row = []
        
        if page > 1:
            nav_row.append(InlineKeyboardButton("⏪ PREV", callback_data=f"page_{page-1}"))
        
        nav_row.append(InlineKeyboardButton(f"📍 {page}/{max_pages}", callback_data="page_info"))
        
        if page < max_pages:
            nav_row.append(InlineKeyboardButton("NEXT ⏩", callback_data=f"page_{page+1}"))
        
        if nav_row:
            buttons.append(nav_row)
        
        buttons.append([InlineKeyboardButton("🏠 HOME", callback_data="back_main")])
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 🎯 CONFIRMATION DIALOGS
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def confirm_dialog(callback_yes: str, callback_no: str = "back_main") -> InlineKeyboardMarkup:
        """Confirmation dialog"""
        buttons = [
            [
                InlineKeyboardButton("✅ YES", callback_data=callback_yes),
                InlineKeyboardButton("❌ NO", callback_data=callback_no),
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    # ═══════════════════════════════════════════════════════════════
    # 🎨 THEME SELECTOR
    # ═══════════════════════════════════════════════════════════════
    
    @staticmethod
    def theme_selector() -> InlineKeyboardMarkup:
        """Theme selection"""
        buttons = [
            [
                InlineKeyboardButton("🌑 Dark Luxury", callback_data="theme_dark"),
                InlineKeyboardButton("🔮 Neon Glass", callback_data="theme_neon"),
            ],
            [
                InlineKeyboardButton("💧 Aqua Neon", callback_data="theme_aqua"),
                InlineKeyboardButton("🧠 AI OS", callback_data="theme_ai"),
            ],
            [
                InlineKeyboardButton("👑 Royal Elite", callback_data="theme_royal"),
                InlineKeyboardButton("🚀 Space", callback_data="theme_space"),
            ],
            [
                InlineKeyboardButton("🔙 BACK", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(buttons)


class PremiumReplyKeyboards:
    """Reply keyboard markup for menus (ReplyKeyboardMarkup style)"""

    @staticmethod
    def main_menu_reply() -> ReplyKeyboardMarkup:
        """Main menu reply keyboard"""
        keyboard = [
            ["⚡ LAUNCH", "📊 STATS"],
            ["💎 PREMIUM", "🎁 REWARDS"],
            ["👤 PROFILE", "⚙️ SETTINGS"],
            ["🛰️ ADMIN", "❓ HELP"],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    @staticmethod
    def back_button() -> ReplyKeyboardMarkup:
        """Simple back button"""
        keyboard = [["🏠 HOME"]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ QUICK KEYBOARD BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_button_row(*buttons_data):
    """Build a custom button row"""
    return [
        InlineKeyboardButton(text, callback_data=callback)
        for text, callback in buttons_data
    ]

def build_custom_keyboard(rows):
    """Build custom keyboard from rows"""
    return InlineKeyboardMarkup(rows)
