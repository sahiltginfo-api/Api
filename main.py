"""
DATATRACE X — AI-Powered Telegram Intelligence Ecosystem
Version: 3.0 | Build: NEO-24
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A next-generation OSINT platform with premium features,
gamification, and cyberpunk aesthetics.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)
from telegram.constants import ParseMode

# Core Configuration
from config import *

# Database Layer
from database.db import Database
from database.models import User, PremiumKey, SearchLog, Achievement

# Core Engine
from core.ai_engine import AIResponseEngine
from core.session_manager import SessionManager
from core.event_bus import EventBus

# Handlers
from handlers.start import StartHandler
from handlers.admin import AdminHandler
from handlers.premium import PremiumHandler
from handlers.referral import ReferralHandler
from handlers.analytics import AnalyticsHandler
from handlers.settings import SettingsHandler
from handlers.help import HelpHandler
from handlers.osint import OSINTHandler

# UI Components
from keyboards.inline import InlineKeyboards
from keyboards.reply import ReplyKeyboards
from themes.dark_luxury import DarkLuxuryTheme
from animations.loading import LoadingAnimations

# Middlewares
from middlewares.antiflood import AntiFloodMiddleware
from middlewares.ratelimit import RateLimitMiddleware
from middlewares.auth import AuthMiddleware

# Utils
from utils.logger import setup_logger
from utils.formatter import Formatter
from utils.badges import BadgeSystem

logger = setup_logger(__name__)


class DataTraceX:
    """
    DATATRACE X — Main Application Class
    Neural Intelligence Core
    """
    
    def __init__(self):
        # Initialize Core Components
        self.db = Database()
        self.ai_engine = AIResponseEngine()
        self.session_manager = SessionManager()
        self.event_bus = EventBus()
        
        # Initialize Handlers
        self.start_handler = StartHandler(self.db, self.ai_engine)
        self.admin_handler = AdminHandler(self.db, self.ai_engine)
        self.premium_handler = PremiumHandler(self.db, self.ai_engine)
        self.referral_handler = ReferralHandler(self.db)
        self.analytics_handler = AnalyticsHandler(self.db)
        self.settings_handler = SettingsHandler(self.db)
        self.help_handler = HelpHandler(self.db, self.ai_engine)
        self.osint_handler = OSINTHandler(self.db, self.ai_engine)
        
        # Initialize UI Components
        self.inline_keyboards = InlineKeyboards()
        self.reply_keyboards = ReplyKeyboards()
        self.theme = DarkLuxuryTheme()
        self.animations = LoadingAnimations()
        
        # Initialize Middlewares
        self.antiflood = AntiFloodMiddleware()
        self.ratelimit = RateLimitMiddleware(self.db)
        self.auth = AuthMiddleware(self.db)
        
        # Initialize Badge System
        self.badge_system = BadgeSystem(self.db)
        
        # Initialize Formatter
        self.formatter = Formatter(self.theme)
        
    async def initialize(self):
        """Initialize all systems"""
        logger.info(self.theme.startup_banner())
        
        # Initialize Database
        self.db.initialize()
        logger.info("✓ Neural Database Online")
        
        # Load Active Sessions
        self.session_manager.load_sessions()
        logger.info("✓ Session Manager Active")
        
        # Initialize Event Bus
        self.event_bus.initialize()
        logger.info("✓ Event Bus Connected")
        
        # Start Background Tasks
        asyncio.create_task(self._background_tasks())
        
        logger.info("✓ All Systems Operational")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info(f"🌌 DATATRACE X — Ready | Mode: {DEPLOYMENT_MODE}")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    async def _background_tasks(self):
        """Background maintenance tasks"""
        while True:
            try:
                # Reset daily limits at midnight
                now = datetime.now()
                if now.hour == 0 and now.minute == 0:
                    self.db.reset_daily_limits()
                    logger.info("⟳ Daily limits reset")
                
                # Clean expired sessions every hour
                if now.minute == 0:
                    self.session_manager.clean_expired()
                
                # Update metrics every 5 minutes
                if now.minute % 5 == 0:
                    self.event_bus.emit("metrics.update", {
                        "online": self.session_manager.active_count(),
                        "timestamp": now.isoformat()
                    })
                
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Background task error: {e}")
    
    def setup_application(self) -> Application:
        """Configure and build the application"""
        app = Application.builder().token(BOT_TOKEN).build()
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # COMMAND HANDLERS
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        # Core Commands
        app.add_handler(CommandHandler("start", self._with_middleware(self.start_handler.start)))
        app.add_handler(CommandHandler("dashboard", self._with_middleware(self.start_handler.dashboard)))
        app.add_handler(CommandHandler("help", self._with_middleware(self.help_handler.help)))
        
        # OSINT Commands
        app.add_handler(CommandHandler("lookup", self._with_middleware(self.osint_handler.lookup)))
        app.add_handler(CommandHandler("phone", self._with_middleware(self.osint_handler.phone)))
        app.add_handler(CommandHandler("vehicle", self._with_middleware(self.osint_handler.vehicle)))
        app.add_handler(CommandHandler("ip", self._with_middleware(self.osint_handler.ip)))
        app.add_handler(CommandHandler("github", self._with_middleware(self.osint_handler.github)))
        app.add_handler(CommandHandler("instagram", self._with_middleware(self.osint_handler.instagram)))
        
        # Premium Commands
        app.add_handler(CommandHandler("premium", self._with_middleware(self.premium_handler.show)))
        app.add_handler(CommandHandler("redeem", self._with_middleware(self.premium_handler.redeem)))
        app.add_handler(CommandHandler("profile", self._with_middleware(self.premium_handler.profile)))
        
        # Referral Commands
        app.add_handler(CommandHandler("refer", self._with_middleware(self.referral_handler.show)))
        app.add_handler(CommandHandler("rewards", self._with_middleware(self.referral_handler.rewards)))
        
        # Settings Commands
        app.add_handler(CommandHandler("settings", self._with_middleware(self.settings_handler.show)))
        app.add_handler(CommandHandler("theme", self._with_middleware(self.settings_handler.theme)))
        
        # Analytics Commands
        app.add_handler(CommandHandler("stats", self._with_middleware(self.analytics_handler.stats)))
        app.add_handler(CommandHandler("leaderboard", self._with_middleware(self.analytics_handler.leaderboard)))
        
        # Admin Commands
        app.add_handler(CommandHandler("admin", self._with_middleware(self.admin_handler.panel, admin_only=True)))
        app.add_handler(CommandHandler("broadcast", self._with_middleware(self.admin_handler.broadcast, admin_only=True)))
        app.add_handler(CommandHandler("genkey", self._with_middleware(self.admin_handler.genkey, admin_only=True)))
        app.add_handler(CommandHandler("ban", self._with_middleware(self.admin_handler.ban, admin_only=True)))
        app.add_handler(CommandHandler("unban", self._with_middleware(self.admin_handler.unban, admin_only=True)))
        app.add_handler(CommandHandler("logs", self._with_middleware(self.admin_handler.logs, admin_only=True)))
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # MESSAGE & CALLBACK HANDLERS
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        app.add_handler(CallbackQueryHandler(self._handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # ERROR HANDLER
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        app.add_error_handler(self._error_handler)
        
        return app
    
    def _with_middleware(self, handler, admin_only: bool = False):
        """Apply middlewares to handler"""
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Apply Anti-Flood
            if not await self.antiflood.check(update):
                return
            
            # Apply Rate Limit
            if not await self.ratelimit.check(update):
                await self._rate_limit_response(update)
                return
            
            # Apply Authentication
            if admin_only and not await self.auth.is_admin(update):
                await self._admin_only_response(update)
                return
            
            # Execute Handler
            try:
                return await handler(update, context)
            except Exception as e:
                logger.error(f"Handler error: {e}")
                await self._error_response(update, str(e))
        
        return wrapper
    
    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        # Route to appropriate handler
        if data.startswith("premium_"):
            await self.premium_handler.handle_callback(query, context, data)
        elif data.startswith("settings_"):
            await self.settings_handler.handle_callback(query, context, data)
        elif data.startswith("admin_"):
            await self.admin_handler.handle_callback(query, context, data)
        elif data.startswith("osint_"):
            await self.osint_handler.handle_callback(query, context, data)
        elif data == "dashboard":
            await self.start_handler.dashboard(update, context)
        elif data == "back_home":
            await self.start_handler.start(update, context)
        else:
            await query.edit_message_text(
                self.ai_engine.generate_response("unknown_action"),
                parse_mode=ParseMode.HTML
            )
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text
        
        # Check if awaiting OSINT input
        user_data = context.user_data
        if user_data.get("awaiting_osint"):
            await self.osint_handler.process_input(update, context, text)
            user_data["awaiting_osint"] = False
        else:
            # AI-powered response for unknown messages
            response = self.ai_engine.generate_response("unknown", text)
            await update.message.reply_text(
                response,
                parse_mode=ParseMode.HTML,
                reply_markup=self.reply_keyboards.main_menu()
            )
    
    async def _rate_limit_response(self, update: Update):
        """Send rate limit response"""
        msg = self.theme.format_rate_limit()
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    
    async def _admin_only_response(self, update: Update):
        """Send admin only response"""
        msg = self.theme.format_admin_only()
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    
    async def _error_response(self, update: Update, error: str):
        """Send error response"""
        msg = self.theme.format_error(error)
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    
    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Global error handler"""
        logger.error(f"Update {update} caused error {context.error}")
        
        try:
            if update and update.effective_chat:
                msg = self.theme.format_system_error(str(context.error)[:200])
                await update.effective_chat.send_message(msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def set_bot_commands(self, app: Application):
        """Set bot commands"""
        commands = [
            BotCommand("start", "⚡ Initialize System"),
            BotCommand("dashboard", "🎛️ AI Control Center"),
            BotCommand("lookup", "🔍 Neural Search"),
            BotCommand("premium", "💎 Ascend to Elite"),
            BotCommand("profile", "👤 Neural Identity"),
            BotCommand("stats", "📊 Quantum Analytics"),
            BotCommand("refer", "🎁 Summon Allies"),
            BotCommand("settings", "⚙️ Configure System"),
            BotCommand("help", "🛰️ AI Assistance"),
        ]
        
        await app.bot.set_my_commands(commands)
        logger.info("✓ Neural Commands Registered")
    
    def run(self):
        """Launch the application"""
        # Validate configuration
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ BOT_TOKEN not configured")
            sys.exit(1)
        
        # Setup and run
        app = self.setup_application()
        
        # Set commands after startup
        asyncio.create_task(self.set_bot_commands(app))
        
        # Run initialization
        asyncio.run(self.initialize())
        
        logger.info("🌌 DATATRACE X — ONLINE")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            logger.info("🛑 System Shutdown — Initiated")
            sys.exit(0)
        except Exception as e:
            logger.error(f"❌ Fatal Error: {e}")
            sys.exit(1)


def main():
    """Entry point"""
    bot = DataTraceX()
    bot.run()


if __name__ == "__main__":
    main()