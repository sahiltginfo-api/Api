# handlers/premium.py
"""
Premium Ecosystem Handler
Tier management, key redemption, elite features
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import secrets

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from keyboards.inline import InlineKeyboards
from themes.dark_luxury import DarkLuxuryTheme

logger = logging.getLogger(__name__)


class PremiumHandler:
    """Premium system handler"""
    
    # Premium tiers configuration
    TIERS = {
        "PRO": {
            "price": "₹99",
            "duration": 30,
            "color": "#00FFD1",
            "features": [
                "500 searches/day",
                "1s cooldown",
                "Priority support",
                "Basic analytics"
            ],
            "daily_limit": 500,
            "cooldown": 1.0
        },
        "ULTRA": {
            "price": "₹249",
            "duration": 90,
            "color": "#7000FF",
            "features": [
                "2000 searches/day",
                "0.5s cooldown",
                "Priority support",
                "Advanced analytics",
                "Export data",
                "Custom themes"
            ],
            "daily_limit": 2000,
            "cooldown": 0.5
        },
        "ELITE": {
            "price": "₹499",
            "duration": 365,
            "color": "#FFD700",
            "features": [
                "Unlimited searches",
                "Instant cooldown",
                "24/7 priority support",
                "Real-time analytics",
                "Bulk operations",
                "Custom API access",
                "White-label option",
                "Beta features access"
            ],
            "daily_limit": 10000,
            "cooldown": 0.1
        }
    }
    
    def __init__(self, db, ai_engine):
        self.db = db
        self.ai = ai_engine
        self.theme = DarkLuxuryTheme()
        self.keyboards = InlineKeyboards()
    
    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show premium upgrade options"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        is_premium = user.get('is_premium', False) if user else False
        
        if is_premium:
            await self._show_active_premium(update, user)
        else:
            await self._show_upgrade_options(update)
    
    async def _show_active_premium(self, update: Update, user: Dict):
        """Show active premium status"""
        tier = user.get('premium_tier', 'PRO')
        expiry = user.get('premium_expiry')
        
        days_left = 0
        if expiry:
            expiry_date = datetime.fromisoformat(expiry)
            days_left = (expiry_date - datetime.now()).days
        
        msg = self.theme.format_premium_card(
            tier,
            self.TIERS[tier]["features"],
            self.TIERS[tier]["price"]
        )
        
        msg += f"""
        
<code>📅 Expires in {days_left} days
🎯 Daily limit: {self.TIERS[tier]['daily_limit']}
⚡ Cooldown: {self.TIERS[tier]['cooldown']}s</code>
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 RENEW", callback_data="premium_renew")],
            [InlineKeyboardButton("◀️ BACK", callback_data="dashboard")]
        ]
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def _show_upgrade_options(self, update: Update):
        """Show upgrade options for free users"""
        msg = f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>ASCEND TO ELITE</b>                                  
{DarkLuxuryTheme.GLASS_BORDER}
│
│  ⚡ <b>Choose your path</b>
│  └─ Select a tier below to unlock enhanced capabilities
│
{DarkLuxuryTheme.GLASS_BOTTOM}
"""
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=self.keyboards.premium_selector()
        )
    
    async def redeem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redeem premium key"""
        if not context.args:
            await update.message.reply_text(
                f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>REDEEM KEY</b>                                        
{DarkLuxuryTheme.GLASS_BORDER}
│
│  📝 <b>Format</b>
│  └─ <code>/redeem KEY-XXXXX-XXXXX-XXXXX</code>
│
│  🔑 <b>Where to get?</b>
│  └─ Contact @admin for purchase
│
{DarkLuxuryTheme.GLASS_BOTTOM}""",
                parse_mode=ParseMode.HTML
            )
            return
        
        key_code = context.args[0].upper()
        user_id = update.effective_user.id
        
        # Validate key
        key = self.db.get_key(key_code)
        if not key:
            await update.message.reply_text(
                self.theme.format_error("Invalid key code"),
                parse_mode=ParseMode.HTML
            )
            return
        
        if key['is_used']:
            await update.message.reply_text(
                self.theme.format_error("Key already redeemed"),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Redeem key
        tier = key['tier']
        days = key['duration_days']
        
        success = self.db.redeem_key(user_id, key_code, tier, days)
        
        if success:
            msg = f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>ELITE STATUS GRANTED</b>                             
{DarkLuxuryTheme.GLASS_BORDER}
│
│  ✅ <b>Premium Activated</b>
│  └─ Tier: <code>{tier}</code> | Duration: {days} days
│
│  ✨ <b>Unlocked Features</b>
"""
            for feature in self.TIERS[tier]["features"]:
                msg += f"  ├─ ✓ {feature}\n"
            
            msg += f"""
│
{DarkLuxuryTheme.GLASS_BOTTOM}

<code>⚡ Welcome to the elite network. Your capabilities have been enhanced.</code>"""
            
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(
                self.theme.format_error("Redemption failed. Contact support."),
                parse_mode=ParseMode.HTML
            )
    
    async def profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user profile with stats"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text(
                self.theme.format_error("Profile not found"),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Get additional stats
        total_searches = self.db.get_user_searches(user_id)
        achievements_count = self.db.get_achievements_count(user_id)
        
        user['total_searches'] = total_searches
        user['achievements'] = achievements_count
        
        msg = self.theme.dashboard(user)
        
        keyboard = [
            [
                InlineKeyboardButton("📊 FULL STATS", callback_data="stats_full"),
                InlineKeyboardButton("🏆 ACHIEVEMENTS", callback_data="achievements_show"),
            ],
            [InlineKeyboardButton("◀️ BACK", callback_data="dashboard")]
        ]
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def handle_callback(self, query, context, data):
        """Handle premium-related callbacks"""
        if data == "premium_show":
            await self.show(query.message, context)
        
        elif data == "premium_redeem":
            await query.edit_message_text(
                f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>ENTER KEY CODE</b>                                    
{DarkLuxuryTheme.GLASS_BORDER}
│
│  🔑 <b>Send your key:</b>
│  └─ <code>/redeem YOUR-KEY-HERE</code>
│
{DarkLuxuryTheme.GLASS_BOTTOM}""",
                parse_mode=ParseMode.HTML
            )
        
        elif data in ["premium_pro", "premium_ultra", "premium_elite"]:
            tier = data.split("_")[1].upper()
            await self._show_tier_details(query, tier)
    
    async def _show_tier_details(self, query, tier: str):
        """Show detailed tier information"""
        config = self.TIERS[tier]
        
        msg = f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>{tier} TIER — {config['price']}</b>                     
{DarkLuxuryTheme.GLASS_BORDER}
│
│  ✨ <b>Features</b>
"""
        for feature in config["features"]:
            msg += f"  ├─ ✓ {feature}\n"
        
        msg += f"""
│
│  📅 <b>Duration</b>
│  └─ {config['duration']} days
│
│  🎯 <b>Limits</b>
│  ├─ Daily: {config['daily_limit']} searches
│  └─ Cooldown: {config['cooldown']}s
│
{DarkLuxuryTheme.GLASS_BOTTOM}

<code>🔑 Contact @admin to purchase {tier} tier</code>"""
        
        keyboard = [
            [InlineKeyboardButton("🔑 I HAVE A KEY", callback_data="premium_redeem")],
            [InlineKeyboardButton("◀️ BACK", callback_data="premium_show")]
        ]
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )