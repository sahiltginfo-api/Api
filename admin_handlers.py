"""
👑 ULTRA-PREMIUM ADMIN CONTROL CENTER
Advanced management, analytics, and security
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from datetime import datetime, timedelta

from keyboards import PremiumKeyboards
from ui_system import PremiumUI

logger = logging.getLogger(__name__)


class PremiumAdminHandlers:
    """Advanced admin control center"""
    
    def __init__(self, db, theme="dark_luxury"):
        self.db = db
        self.ui = PremiumUI(theme)
    
    # ═══════════════════════════════════════════════════════════════
    # 👑 ADMIN PANEL
    # ═══════════════════════════════════════════════════════════════
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main admin panel"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ Admin access required")
            return
        
        msg = """
👑 *ADMIN CONTROL CENTER*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*⚙️ Management Options:*

📊 Analytics - Bot statistics & metrics
👥 Users - User management & search
🔑 Keys - Premium key generation
📢 Broadcast - Send messages
🚫 Ban - Ban/unban users
📝 Logs - View activity logs
🛡️ Security - Security settings
🔧 Config - Bot configuration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.admin_panel()
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.admin_panel()
            )
    
    # ═══════════════════════════════════════════════════════════════
    # 📊 ANALYTICS DASHBOARD
    # ═══════════════════════════════════════════════════════════════
    
    async def analytics_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Detailed analytics dashboard"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        stats = self.db.get_stats()
        key_stats = self.db.get_key_stats()
        
        # Calculate growth
        yesterday_users = stats.get('yesterday_users', 0)
        today_users = stats.get('total_users', 0)
        growth = ((today_users - yesterday_users) / max(yesterday_users, 1)) * 100
        
        msg = f"""
📊 *ANALYTICS DASHBOARD*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*👥 USER METRICS*
├─ Total Users: `{stats.get('total_users', 0)}`
├─ Premium Users: `{stats.get('premium_users', 0)}`
├─ Daily Active: `{stats.get('active_users', 0)}`
├─ New Today: `{stats.get('new_users_today', 0)}`
├─ Growth: `{growth:.1f}%`
└─ Banned: `{stats.get('banned_users', 0)}`

*🔍 SEARCH ACTIVITY*
├─ Total Searches: `{stats.get('total_searches', 0)}`
├─ Today: `{stats.get('searches_today', 0)}`
├─ Avg/User: `{stats.get('avg_searches', 0)}`
└─ Success Rate: `{stats.get('success_rate', 0)}%`

*💎 PREMIUM*
├─ Premium Users: `{stats.get('premium_users', 0)}`
├─ Revenue: `₹{stats.get('revenue', 0)}`
├─ Keys Generated: `{key_stats.get('total', 0)}`
├─ Keys Redeemed: `{key_stats.get('used', 0)}`
└─ Keys Unused: `{key_stats.get('unused', 0)}`

*⚙️ SYSTEM*
├─ Uptime: `{stats.get('uptime', 'N/A')}`
├─ Latency: `{stats.get('latency', 0)}ms`
├─ Database: `{stats.get('db_size', 'N/A')}`
└─ Errors Today: `{stats.get('errors_today', 0)}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.navigation(1, 1)
            )
        else:
            await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    # ═══════════════════════════════════════════════════════════════
    # 👥 USER MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    async def user_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """User management panel"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        msg = """
👥 *USER MANAGEMENT*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Available Actions:*

1️⃣ Search User - Find by ID/username
2️⃣ List Users - Show all users (paginated)
3️⃣ Promote - Make user premium
4️⃣ Ban - Ban user
5️⃣ Unban - Unban user
6️⃣ Reset - Reset user data
7️⃣ Broadcast - Send to users

*Search Format:*
`/search USERID` or `/search @username`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    # ═══════════════════════════════════════════════════════════════
    # 🔑 PREMIUM KEY GENERATION
    # ═══════════════════════════════════════════════════════════════
    
    async def key_generation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium key generation"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                """
🔑 *PREMIUM KEY GENERATION*

*Usage:*
`/genkey COUNT DURATION`

*Examples:*
• `/genkey 10 30d` - 10 keys for 30 days
• `/genkey 5 365d` - 5 keys for 1 year
• `/genkey 100 7d` - 100 keys for 7 days

*Valid Durations:*
• 7d, 14d, 30d, 90d, 180d, 365d

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            count = int(context.args[0])
            duration_str = context.args[1]
            
            if not duration_str.endswith('d'):
                raise ValueError("Duration must end with 'd' (e.g., '30d')")
            
            duration_days = int(duration_str[:-1])
            
            if not (1 <= count <= 1000):
                raise ValueError("Count must be 1-1000")
            
            if not (1 <= duration_days <= 365):
                raise ValueError("Duration must be 1-365 days")
            
            # Generate keys
            keys = self.db.generate_keys(count, duration_days, user_id)
            
            if not keys:
                await update.message.reply_text("❌ Error generating keys")
                return
            
            # Format response
            msg = f"""
✅ *KEYS GENERATED*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Generated:* `{count}` keys
*Duration:* `{duration_days}` days
*Expires:* `{(datetime.now() + timedelta(days=duration_days)).strftime('%Y-%m-%d')}`

*Keys:*
"""
            
            for i, key in enumerate(keys[:10], 1):
                msg += f"{i}. `{key}`\n"
            
            if count > 10:
                msg += f"\n... and {count - 10} more keys\n"
            
            msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            
            # Log action
            self.db.log_search(user_id, update.effective_user.username, "genkey",
                             f"{count}x{duration_days}d", "success", "admin", 0, 1)
        
        except ValueError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Key generation error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    # ═══════════════════════════════════════════════════════════════
    # 📢 BROADCAST SYSTEM
    # ═══════════════════════════════════════════════════════════════
    
    async def broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Broadcast to all users"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        if not context.args:
            await update.message.reply_text(
                """
📢 *BROADCAST MESSAGE*

*Usage:*
`/broadcast Your message here`

*Features:*
• Sends to all active users
• Shows delivery stats
• Tracks failures
• Supports formatting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        message = ' '.join(context.args)
        users = self.db.get_all_users(limit=10000)
        
        confirm_msg = f"""
📢 *CONFIRM BROADCAST*

*Message:*
{message}

*Recipients:* `{len(users)}` users

Reply with: `CONFIRM` to send
Reply with: `CANCEL` to cancel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        context.user_data['broadcast_message'] = message
        context.user_data['broadcast_users'] = users
        context.user_data['awaiting_confirmation'] = 'broadcast'
        
        await update.message.reply_text(confirm_msg, parse_mode=ParseMode.MARKDOWN)
    
    # ═══════════════════════════════════════════════════════════════
    # 🚫 BAN SYSTEM
    # ═══════════════════════════════════════════════════════════════
    
    async def ban_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ban a user"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: `/ban USERID [reason]`\n\n"
                "Example: `/ban 123456789 Spam`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            ban_user_id = int(context.args[0])
            reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason"
            
            if self.db.ban_user(ban_user_id, reason):
                msg = f"""
✅ *USER BANNED*

*User ID:* `{ban_user_id}`
*Reason:* `{reason}`
*Banned At:* `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                
                await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                
                self.db.log_search(user_id, update.effective_user.username, "ban",
                                 str(ban_user_id), "success", "admin", 0, 1)
            else:
                await update.message.reply_text("❌ Error banning user")
        
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID")
        except Exception as e:
            logger.error(f"Ban error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    # ═══════════════════════════════════════════════════════════════
    # 📝 LOGS VIEWER
    # ═══════════════════════════════════════════════════════════════
    
    async def view_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View activity logs"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        logs = self.db.get_logs(limit=20)
        
        msg = "📝 *RECENT ACTIVITY LOGS*\n\n"
        msg += "`User  | Command      | Status | Time`\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for log in logs:
            timestamp = log['timestamp'].split('T')[1][:5] if log['timestamp'] else "N/A"
            status = "✅" if log['result_status'] == "success" else "❌"
            cmd = log['command'][:10].ljust(10)
            
            msg += f"`{log['user_id']:<8} | {cmd} | {status} | {timestamp}`\n"
        
        msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    # ═══════════════════════════════════════════════════════════════
    # 🔐 SECURITY SETTINGS
    # ═══════════════════════════════════════════════════════════════
    
    async def security_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Security settings panel"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        msg = """
🔐 *SECURITY SETTINGS*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Available Options:*

🚨 Anti-Spam - Enable/disable spam detection
🔄 Rate Limiter - Adjust rate limits
🛡️ 2FA - Two-factor authentication
📋 IP Whitelist - Allow specific IPs
🔐 API Keys - Manage API credentials
🚫 Blacklist - User/IP blacklist

*Status:*
✅ Anti-Spam: ENABLED
✅ Rate Limiter: ENABLED
✅ 2FA: DISABLED
✅ IP Whitelist: DISABLED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    # ═══════════════════════════════════════════════════════════════
    # ⚙️ BOT CONFIGURATION
    # ═══════════════════════════════════════════════════════════════
    
    async def bot_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot configuration panel"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            return
        
        msg = """
⚙️ *BOT CONFIGURATION*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Current Settings:*

🔐 API Settings:
├─ Endpoint: `sbsakib.eu.cc`
├─ Timeout: `15s`
├─ Cooldown: `2s` (Free) / `0.5s` (Premium)
└─ Status: ✅ ACTIVE

📊 Database:
├─ Location: `osint_bot.db`
├─ Tables: `5`
├─ Users: `[STAT]`
└─ Status: ✅ ACTIVE

💎 Premium:
├─ Free Limit: `50/day`
├─ Premium Limit: `unlimited`
├─ Auto Expiry: ✅ ENABLED
└─ Renewal: ✅ AUTO

🔔 Notifications:
├─ Alerts: ✅ ENABLED
├─ Logs: ✅ ENABLED
└─ Metrics: ✅ ENABLED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

