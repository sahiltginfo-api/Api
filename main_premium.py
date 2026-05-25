"""
🚀 ULTRA-PREMIUM TELEGRAM BOT v3.0
Next-generation OSINT intelligence system
Production-ready, optimized, futuristic
"""

import logging
import sys
from pathlib import Path

from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)
from telegram.constants import ParseMode

# ═══════════════════════════════════════════════════════════════════
# IMPORTS - Keep minimal, modular
# ═══════════════════════════════════════════════════════════════════

from config import (
    BOT_TOKEN, BOT_OWNER_ID, DATABASE_PATH, STARTUP_MESSAGE, 
    API_KEY, BASE_API
)
from database import Database
from utils_api import APIManager
from handlers_premium import PremiumCommandHandlers, PremiumTextHandlers
from keyboards import PremiumReplyKeyboards
from ui_system import PremiumUI

# ═══════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 🎯 MAIN BOT CLASS
# ═══════════════════════════════════════════════════════════════════

class UltraPremiumBot:
    """Ultra-premium OSINT bot v3.0"""
    
    def __init__(self):
        """Initialize bot"""
        logger.info("✦ Initializing Ultra-Premium Bot v3.0...")
        
        # Initialize core systems
        self.db = Database(DATABASE_PATH)
        self.api = APIManager(self.db)
        self.ui = PremiumUI("dark_luxury")
        
        # Initialize handlers
        self.cmd_handlers = PremiumCommandHandlers(self.db, self.api)
        self.text_handlers = PremiumTextHandlers(self.db, self.api)
        
        logger.info("✓ All systems initialized")
    
    # ═══════════════════════════════════════════════════════════════
    # 🏗️ SETUP APPLICATION
    # ═══════════════════════════════════════════════════════════════
    
    def setup_application(self) -> Application:
        """Setup bot application with all handlers"""
        app = Application.builder().token(BOT_TOKEN).build()
        
        # ═══════════════════════════════════════════════════════════
        # 📝 COMMAND HANDLERS
        # ═══════════════════════════════════════════════════════════
        
        app.add_handler(CommandHandler("start", self.cmd_handlers.start_command))
        app.add_handler(CommandHandler("stats", self.cmd_handlers.stats_command))
        app.add_handler(CommandHandler("profile", self.cmd_handlers.profile_command))
        app.add_handler(CommandHandler("premium", self.cmd_handlers.premium_command))
        
        # Help command
        app.add_handler(CommandHandler("help", self._help_command))
        
        # ═══════════════════════════════════════════════════════════
        # 🔘 CALLBACK HANDLERS
        # ═══════════════════════════════════════════════════════════
        
        app.add_handler(CallbackQueryHandler(self.cmd_handlers.button_callback))
        
        # ═══════════════════════════════════════════════════════════
        # 💬 MESSAGE HANDLERS
        # ═══════════════════════════════════════════════════════════
        
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.text_handlers.handle_text
        ))
        
        # ═══════════════════════════════════════════════════════════
        # ⚠️ ERROR HANDLER
        # ═══════════════════════════════════════════════════════════
        
        app.add_error_handler(self._error_handler)
        
        return app
    
    # ═══════════════════════════════════════════════════════════════
    # ❓ HELP COMMAND
    # ═══════════════════════════════════════════════════════════════
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        msg = """
✦ COMMAND REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*🚀 MAIN COMMANDS:*
├─ /start - Start bot
├─ /stats - Bot statistics
├─ /profile - Your profile
└─ /premium - Premium info

*🔍 QUICK SEARCH:*
├─ /num 8002008433 - Phone lookup
├─ /vehicle DL10CA7539 - RC lookup
├─ /github username - GitHub profile
├─ /insta username - Instagram profile
├─ /ip 8.8.8.8 - IP lookup
└─ /ff 2701059399 - Free Fire stats

*💎 PREMIUM:*
├─ /redeem KEY - Redeem premium
└─ /myinfo - Check subscription

*👑 ADMIN:*
├─ /admin - Admin panel
├─ /stats - Statistics
├─ /genkey 10 30d - Generate keys
└─ /ban USER REASON - Ban user

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*💡 TIPS:*
• Use menu buttons for easy navigation
• Premium users get unlimited searches
• Cooldown: 2s (free) / 0.5s (premium)
• Daily limit: 50 (free) / unlimited (premium)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=PremiumReplyKeyboards.main_menu_reply()
        )
    
    # ═══════════════════════════════════════════════════════════════
    # 🚨 ERROR HANDLER
    # ═══════════════════════════════════════════════════════════════
    
    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Error handler"""
        logger.error(f"Exception: {context.error}")
        
        try:
            if update and update.effective_chat:
                error_msg = f"❌ System error occurred\n\n`{str(context.error)[:150]}`"
                await update.effective_chat.send_message(
                    error_msg,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 🎯 SET BOT COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    async def _set_bot_commands(self, app: Application):
        """Set bot commands menu"""
        commands = [
            BotCommand("start", "🚀 Start bot"),
            BotCommand("help", "❓ Help & commands"),
            BotCommand("stats", "📊 Statistics"),
            BotCommand("profile", "👤 Your profile"),
            BotCommand("premium", "💎 Premium info"),
            BotCommand("admin", "👑 Admin panel"),
        ]
        
        await app.bot.set_my_commands(commands)
        logger.info("✓ Bot commands set")
    
    # ═══════════════════════════════════════════════════════════════
    # 🖨️ PRINT STARTUP BANNER
    # ═══════════════════════════════════════════════════════════════
    
    def print_banner(self):
        """Print startup banner"""
        banner = f"""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║             🚀 ULTRA-PREMIUM BOT v3.0 STARTED 🚀             ║
║                                                                ║
║          Next-Generation OSINT Intelligence System            ║
║                  Production Deployment Ready                 ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Database System Online                                    ║
║  ✅ API Manager Ready                                         ║
║  ✅ Premium Handlers Active                                   ║
║  ✅ Modern UI System Loaded                                   ║
║  ✅ Admin Panel Active                                        ║
║  ✅ Logging System Ready                                      ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  👤 Bot Owner: {BOT_OWNER_ID}                                  ║
║  💾 Database: {DATABASE_PATH}                                  ║
║  🔌 API: {BASE_API}                                            ║
║  🌐 Status: READY                                              ║
║                                                                ║
║  🎯 Ready to serve premium OSINT queries!                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        logger.info(banner)
    
    # ═══════════════════════════════════════════════════════════════
    # ▶️ RUN BOT
    # ═══════════════════════════════════════════════════════════════
    
    def run(self):
        """Run bot"""
        # Validation
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ BOT_TOKEN not configured!")
            sys.exit(1)
        
        if BOT_OWNER_ID == 0:
            logger.error("❌ BOT_OWNER_ID not configured!")
            sys.exit(1)
        
        # Print banner
        self.print_banner()
        
        # Setup application
        app = self.setup_application()
        
        # Set commands
        app.job_queue.run_once(self._set_bot_commands, when=0, data=app)
        
        # Run polling
        logger.info("✦ Starting polling...")
        
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"❌ Bot error: {e}")
            sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# 🎬 ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    bot = UltraPremiumBot()
    bot.run()


if __name__ == "__main__":
    main()
