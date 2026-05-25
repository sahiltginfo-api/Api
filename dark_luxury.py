# themes/dark_luxury.py
"""
Dark Luxury Theme — Premium Visual Identity
Cyberpunk aesthetics with neon accents
"""

from typing import Dict, Any
from datetime import datetime

class DarkLuxuryTheme:
    """Dark Luxury Theme Engine"""
    
    # Color Palette
    COLORS = {
        "primary": "#00FFD1",      # Neon Cyan
        "secondary": "#7000FF",     # Deep Purple
        "accent": "#FF006E",        # Neon Pink
        "premium": "#FFD700",       # Gold
        "success": "#00FF88",       # Mint
        "warning": "#FFB700",       # Amber
        "error": "#FF3366",         # Coral
        "dark": "#0A0A0F",          # Almost Black
        "darker": "#050508",        # Deep Black
        "glass": "rgba(255,255,255,0.05)"  # Glass Effect
    }
    
    # Glassmorphism Styles
    GLASS = "┌──────────────────────────────────────────┐"
    GLASS_BORDER = "├──────────────────────────────────────────┤"
    GLASS_BOTTOM = "└──────────────────────────────────────────┘"
    
    @staticmethod
    def startup_banner() -> str:
        return """
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ██████╗  █████╗ ████████╗ █████╗ ████████╗██████╗  █████╗  ██████╗ ███████╗
║    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝
║    ██║  ██║███████║   ██║   ███████║   ██║   ██████╔╝███████║██║  ███╗█████╗  
║    ██║  ██║██╔══██║   ██║   ██╔══██║   ██║   ██╔══██╗██╔══██║██║   ██║██╔══╝  
║    ██████╔╝██║  ██║   ██║   ██║  ██║   ██║   ██║  ██║██║  ██║╚██████╔╝███████╗
║    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
║                                                                       ║
║                   ✦ AI-POWERED TELEGRAM ECOSYSTEM ✦                    ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║  ⚡ Neural Core Active    🛰️ Secure Channel Open    🧠 AI Engine Ready  ║
╠═══════════════════════════════════════════════════════════════════════╣
║  📡 Build: NEO-24        🌌 Version: 3.0           🎯 Mode: PRODUCTION ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
    
    @staticmethod
    def format_header(title: str, subtitle: str = "") -> str:
        """Format section header"""
        if subtitle:
            return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ {title}                                                   
│  └─ {subtitle}
{DarkLuxuryTheme.GLASS_BORDER}"""
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ {title}
{DarkLuxuryTheme.GLASS_BORDER}"""
    
    @staticmethod
    def format_footer() -> str:
        """Format section footer"""
        return f"\n{DarkLuxuryTheme.GLASS_BOTTOM}"
    
    @staticmethod
    def dashboard(user_data: Dict) -> str:
        """Format user dashboard"""
        name = user_data.get('first_name', 'Operator')
        level = user_data.get('level', 1)
        xp = user_data.get('xp', 0)
        xp_next = level * 100
        premium = user_data.get('is_premium', False)
        
        premium_badge = "💎 ELITE" if premium else "🆓 STANDARD"
        premium_color = DarkLuxuryTheme.COLORS["premium"] if premium else DarkLuxuryTheme.COLORS["primary"]
        
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ NEURAL DASHBOARD — {name.upper()}                         
│  └─ Identity: <code>#{user_data.get('user_id', 'N/A')}</code>
│
│  ════════════════════════════════════════════
│
│  📊 STATUS METRICS
│  ├─ <b>Rank</b>               LEVEL {level} — {DarkLuxuryTheme._get_rank_name(level)}
│  ├─ <b>XP</b>                 {xp} / {xp_next} ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
│  ├─ <b>Tier</b>               <code>{premium_badge}</code>
│  └─ <b>Streak</b>             {user_data.get('streak_days', 0)} days active
│
│  ════════════════════════════════════════════
│
│  🎯 SESSION METRICS
│  ├─ <b>Searches Today</b>     {user_data.get('daily_requests', 0)} / {user_data.get('daily_limit', 50)}
│  ├─ <b>Total Searches</b>     {user_data.get('total_searches', 0):,}
│  ├─ <b>Referrals</b>          {user_data.get('referrals', 0)}
│  └─ <b>Achievements</b>       {user_data.get('achievements', 0)} unlocked
│
{DarkLuxuryTheme.GLASS_BOTTOM}

<code>⚡ AI Core Online | Session Active | Secure Channel Open</code>"""
    
    @staticmethod
    def _get_rank_name(level: int) -> str:
        ranks = ["INITIATE", "OPERATOR", "AGENT", "SPECIALIST", "EXPERT", "MASTER", "LEGEND", "TRANSCENDENT"]
        idx = min(level // 10, len(ranks) - 1)
        return ranks[idx]
    
    @staticmethod
    def format_premium_card(tier: str, features: list, price: str) -> str:
        """Format premium tier card"""
        colors = {
            "PRO": DarkLuxuryTheme.COLORS["primary"],
            "ULTRA": DarkLuxuryTheme.COLORS["secondary"],
            "ELITE": DarkLuxuryTheme.COLORS["premium"]
        }
        
        color = colors.get(tier.upper(), DarkLuxuryTheme.COLORS["primary"])
        
        features_text = "\n".join([f"  ├─ ✓ {f}" for f in features])
        
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b><code>{tier.upper()} TIER</code></b> — <code>{price}</code>                  
{DarkLuxuryTheme.GLASS_BORDER}
│
│  <b>✦ ACCESS GRANTED</b>
│
{features_text}
│
{DarkLuxuryTheme.GLASS_BOTTOM}"""
    
    @staticmethod
    def format_rate_limit() -> str:
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>RATE LIMIT ACTIVE</b>                                
{DarkLuxuryTheme.GLASS_BORDER}
│
│  ⚡ <b>Cooldown in effect</b>
│  └─ Please wait a moment before next operation
│
│  💎 <b>Upgrade to ELITE tier</b>
│  └─ Remove all rate limits instantly
│
{DarkLuxuryTheme.GLASS_BOTTOM}"""
    
    @staticmethod
    def format_admin_only() -> str:
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>ACCESS DENIED</b>                                     
{DarkLuxuryTheme.GLASS_BORDER}
│
│  🔒 <b>Restricted Area</b>
│  └─ Administrator credentials required
│
│  ⚡ <b>Security Logged</b>
│  └─ This incident has been recorded
│
{DarkLuxuryTheme.GLASS_BOTTOM}"""
    
    @staticmethod
    def format_error(error: str) -> str:
        return f"""
{DarkLuxuryTheme.GLASS}
│  ✦ <b>SYSTEM ALERT</b>                                      
{DarkLuxuryTheme.GLASS_BORDER}
│
│  ⚠️ <b>Operation Failed</b>
│  └─ <code>{error[:100]}</code>
│
│  🛠️ <b>Troubleshooting</b>
│  └─ Contact support if persists
│
{DarkLuxuryTheme.GLASS_BOTTOM}"""
    
    @staticmethod
    def format_system_error(error: str) -> str:
        return f"""
⚠️ <b>System Alert</b> — Error logged

┌─────────────────────────────────────────
│ <code>{error[:150]}</code>
└─────────────────────────────────────────

🛡️ <i>Technical team has been notified</i>"""