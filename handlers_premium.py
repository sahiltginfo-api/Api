"""
🎯 ULTRA-PREMIUM UNIFIED HANDLERS
Clean, modern, optimized handler system
"""

import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from keyboards import PremiumKeyboards, PremiumReplyKeyboards
from ui_system import PremiumUI, QuickUI, TextFormat

logger = logging.getLogger(__name__)


class PremiumCommandHandlers:
    """Premium unified command handlers"""
    
    def __init__(self, db, api_manager, theme="dark_luxury"):
        self.db = db
        self.api = api_manager
        self.ui = PremiumUI(theme)
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 START COMMAND
    # ═══════════════════════════════════════════════════════════════════
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium start command"""
        user = update.effective_user
        user_id = user.id
        
        # Add user to database if new
        if not self.db.get_user(user_id):
            self.db.add_user(user_id, user.username, user.first_name)
        
        self.db.update_last_seen(user_id)
        
        # Build welcome message
        msg = f"""
✦ SYSTEM INITIALIZED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧿 *Welcome, {user.first_name}!*

Your premium workspace is ready.
Access advanced intelligence features below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*⚡ FEATURES:*
├─ 📞 Phone Number Lookup
├─ 🚗 Vehicle Registration
├─ 📸 Instagram Profiles
├─ 🐙 GitHub Accounts
├─ 🌐 IP Address Lookup
├─ 🎮 Free Fire Stats
├─ ✈️ Telegram Users
└─ 🏦 Bank Information

*💎 PREMIUM:* Unlimited searches, 0.5s cooldown, priority support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=PremiumKeyboards.main_menu()
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 📊 STATS COMMAND
    # ═══════════════════════════════════════════════════════════════════
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stats panel"""
        user_id = update.effective_user.id
        
        if update.callback_query:
            query = update.callback_query
            await query.answer()
        
        stats = self.db.get_stats()
        msg = self.ui.stats_panel(stats)
        
        if update.callback_query:
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.main_menu()
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.main_menu()
            )
    
    # ═══════════════════════════════════════════════════════════════════
    # 👤 PROFILE COMMAND
    # ═══════════════════════════════════════════════════════════════════
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user profile"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("❌ User not found")
            return
        
        user_data = {
            "user_id": user_id,
            "username": user.get('username', 'anonymous'),
            "status": "🟢 ACTIVE" if not user.get('is_banned') else "🔴 BANNED",
            "level": user.get('level', 1),
            "xp": user.get('xp', 0),
            "searches": user.get('search_count', 0),
            "joined": user.get('created_at', 'N/A'),
            "is_premium": user.get('is_premium', False),
            "premium_expiry": user.get('premium_expiry', 'N/A'),
        }
        
        msg = self.ui.profile_card(user_data)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.main_menu()
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.main_menu()
            )
    
    # ═══════════════════════════════════════════════════════════════════
    # 💎 PREMIUM COMMAND
    # ═══════════════════════════════════════════════════════════════════
    
    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium menu"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        user_premium = {
            "is_premium": user.get('is_premium', False),
            "tier": user.get('tier', 'Free'),
            "expiry": user.get('premium_expiry', 'N/A'),
            "days_left": 0,
            "auto_renew": False,
        }
        
        msg = self.ui.premium_card(user_premium)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.premium_menu()
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=PremiumKeyboards.premium_menu()
            )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🎯 CALLBACK HANDLER
    # ═══════════════════════════════════════════════════════════════════
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all button callbacks"""
        query = update.callback_query
        user_id = query.from_user.id
        callback_data = query.data
        
        await query.answer()
        
        try:
            # Navigation
            if callback_data == "back_main":
                await self.start_command(update, context)
            
            elif callback_data == "stats_panel":
                await self.stats_command(update, context)
            
            elif callback_data == "profile_menu":
                await self.profile_command(update, context)
            
            elif callback_data == "premium_menu":
                await self.premium_command(update, context)
            
            # OSINT Commands
            elif callback_data.startswith("cmd_"):
                await self._handle_osint_command(query, callback_data[4:])
            
            # Admin
            elif callback_data == "admin_analytics":
                await self._admin_analytics(query)
            
            # Settings
            elif callback_data == "settings_theme":
                await query.edit_message_text(
                    "🎨 *Select Theme*\n\nChoose your preferred appearance:",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=PremiumKeyboards.theme_selector()
                )
            
            # Theme selection
            elif callback_data.startswith("theme_"):
                theme = callback_data[6:]
                # Save theme preference
                await query.answer(f"✅ Theme changed to {theme}", show_alert=False)
                await self.start_command(update, context)
            
            # Default
            else:
                await query.answer("Command not recognized", show_alert=True)
        
        except Exception as e:
            logger.error(f"Callback error: {e}")
            await query.answer(f"❌ Error: {str(e)[:100]}", show_alert=True)
    
    # ═══════════════════════════════════════════════════════════════════
    # 🔍 OSINT HANDLER
    # ═══════════════════════════════════════════════════════════════════
    
    async def _handle_osint_command(self, query, cmd_type: str):
        """Handle OSINT commands"""
        user_id = query.from_user.id
        
        prompts = {
            "number": "📞 *Send phone number*\n\nExample: `8002008433`",
            "vehicle": "🚗 *Send vehicle RC*\n\nExample: `DL10CA7539`",
            "instagram": "📸 *Send Instagram username*\n\nExample: `@instagram`",
            "github": "🐙 *Send GitHub username*\n\nExample: `octocat`",
            "ip": "🌐 *Send IP address*\n\nExample: `8.8.8.8`",
            "ff": "🎮 *Send Free Fire UID*\n\nExample: `2701059399`",
            "telegram": "✈️ *Send Telegram ID or username*",
            "bank": "🏦 *Send pincode or IFSC*",
        }
        
        msg = prompts.get(cmd_type, "❌ Unknown command")
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=PremiumKeyboards.quick_actions()
        )
        
        # Set awaiting input
        import copy
        context = copy.copy(query)
        context.user_data = getattr(context, 'user_data', {})
        context.user_data['awaiting_input'] = cmd_type
    
    # ═══════════════════════════════════════════════════════════════════
    # 👑 ADMIN ANALYTICS
    # ═══════════════════════════════════════════════════════════════════
    
    async def _admin_analytics(self, query):
        """Admin analytics panel"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            await query.answer("❌ Admin access required", show_alert=True)
            return
        
        stats = self.db.get_stats()
        msg = self.ui.stats_panel(stats)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=PremiumKeyboards.admin_panel()
        )


class PremiumTextHandlers:
    """Premium text message handlers"""
    
    def __init__(self, db, api_manager, theme="dark_luxury"):
        self.db = db
        self.api = api_manager
        self.ui = PremiumUI(theme)
    
    # ═══════════════════════════════════════════════════════════════════
    # 💬 TEXT MESSAGE HANDLER
    # ═══════════════════════════════════════════════════════════════════
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main text handler"""
        user_id = update.effective_user.id
        text = update.message.text.strip()
        
        # Check ban
        if self.db.is_banned(user_id):
            await update.message.reply_text("🚫 You have been banned")
            return
        
        # Get awaiting input
        awaiting = context.user_data.get('awaiting_input')
        
        if not awaiting:
            await update.message.reply_text(
                "❓ Use the menu buttons or /help",
                reply_markup=PremiumReplyKeyboards.main_menu_reply()
            )
            return
        
        # Route to handler
        handlers = {
            "number": self._handle_number,
            "vehicle": self._handle_vehicle,
            "instagram": self._handle_instagram,
            "github": self._handle_github,
            "ip": self._handle_ip,
            "ff": self._handle_freefire,
            "telegram": self._handle_telegram,
            "bank": self._handle_bank,
        }
        
        handler = handlers.get(awaiting)
        if handler:
            await handler(update, context, text)
        
        context.user_data['awaiting_input'] = None
    
    # ═══════════════════════════════════════════════════════════════════
    # 🔍 OSINT HANDLERS
    # ═══════════════════════════════════════════════════════════════════
    
    async def _handle_number(self, update, context, number: str):
        """Handle phone number"""
        user_id = update.effective_user.id
        is_premium = self.db.is_premium(user_id)
        
        # Cooldown check
        allowed, remaining = self.api.check_cooldown(user_id, is_premium)
        if not allowed:
            await update.message.reply_text(f"⏱️ Cooldown: {remaining:.1f}s")
            return
        
        # API call
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_number_info(number)
            
            if "error" not in result:
                response = f"""
📞 *Phone Info*
├─ Number: `{result.get('number', 'N/A')}`
├─ Country: `{result.get('country', 'N/A')}`
├─ Operator: `{result.get('operator', 'N/A')}`
└─ Region: `{result.get('region', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            
            self.db.increment_daily_requests(user_id)
            self.db.log_search(user_id, update.effective_user.username, "number", 
                             number, "success" if "error" not in result else "failed", 
                             "num_info", 0, int(is_premium))
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_vehicle(self, update, context, rc: str):
        """Handle vehicle lookup"""
        user_id = update.effective_user.id
        is_premium = self.db.is_premium(user_id)
        
        allowed, remaining = self.api.check_cooldown(user_id, is_premium)
        if not allowed:
            await update.message.reply_text(f"⏱️ Cooldown: {remaining:.1f}s")
            return
        
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_vehicle_info(rc)
            
            if "error" not in result:
                response = f"""
🚗 *Vehicle Info*
├─ RC: `{result.get('rc', 'N/A')}`
├─ Owner: `{result.get('owner_name', 'N/A')}`
├─ Color: `{result.get('color', 'N/A')}`
└─ Type: `{result.get('vehicle_type', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            
            self.db.increment_daily_requests(user_id)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_instagram(self, update, context, username: str):
        """Handle Instagram lookup"""
        user_id = update.effective_user.id
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_instagram_info(username)
            
            if "error" not in result:
                response = f"""
📸 *Instagram Profile*
├─ Username: `@{result.get('username', 'N/A')}`
├─ Followers: `{result.get('followers', 'N/A')}`
├─ Following: `{result.get('following', 'N/A')}`
└─ Posts: `{result.get('posts', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_github(self, update, context, username: str):
        """Handle GitHub lookup"""
        user_id = update.effective_user.id
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_github_info(username)
            
            if "error" not in result:
                response = f"""
🐙 *GitHub Profile*
├─ Username: `{result.get('login', 'N/A')}`
├─ Name: `{result.get('name', 'N/A')}`
├─ Repos: `{result.get('public_repos', 'N/A')}`
└─ Followers: `{result.get('followers', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_ip(self, update, context, ip: str):
        """Handle IP lookup"""
        user_id = update.effective_user.id
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_ip_info(ip)
            
            if "error" not in result:
                response = f"""
🌐 *IP Information*
├─ IP: `{result.get('ip', 'N/A')}`
├─ Country: `{result.get('country', 'N/A')}`
├─ City: `{result.get('city', 'N/A')}`
└─ ISP: `{result.get('isp', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_freefire(self, update, context, uid: str):
        """Handle Free Fire lookup"""
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_freefire_info(uid)
            
            if "error" not in result:
                response = f"""
🎮 *Free Fire Account*
├─ UID: `{result.get('uid', 'N/A')}`
├─ Level: `{result.get('level', 'N/A')}`
├─ Rank: `{result.get('rank', 'N/A')}`
└─ Wins: `{result.get('wins', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_telegram(self, update, context, user_input: str):
        """Handle Telegram user lookup"""
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            result = self.api.get_telegram_user(user_input)
            
            if "error" not in result:
                response = f"""
✈️ *Telegram User*
├─ ID: `{result.get('id', 'N/A')}`
├─ Username: `@{result.get('username', 'N/A')}`
└─ Name: `{result.get('first_name', 'N/A')}`
"""
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
    
    async def _handle_bank(self, update, context, query: str):
        """Handle bank lookup"""
        msg = await update.message.reply_text(self.ui.loading("process"))
        
        try:
            if len(query) == 6 and query.isdigit():
                result = self.api.get_pincode_info(query)
                title = "Pincode"
            else:
                result = self.api.get_ifsc_info(query)
                title = "Bank Info"
            
            if "error" not in result:
                response = f"✅ *{title}*\n```json\n{str(result)}\n```"
            else:
                response = f"❌ {result.get('error', 'Unknown error')}"
            
            await msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:100]}")
