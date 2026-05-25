# database/models.py
"""
Neural Database Models
SQLite with optimized queries
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
import sqlite3
import json

class User:
    """User model with all attributes"""
    
    TABLE = "users"
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'en',
                is_premium INTEGER DEFAULT 0,
                premium_tier TEXT DEFAULT 'FREE',
                premium_expiry TEXT,
                is_banned INTEGER DEFAULT 0,
                ban_reason TEXT,
                daily_requests INTEGER DEFAULT 0,
                total_requests INTEGER DEFAULT 0,
                last_request_reset TEXT,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak_days INTEGER DEFAULT 0,
                last_active TEXT,
                referrals INTEGER DEFAULT 0,
                referred_by INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                theme TEXT DEFAULT 'dark_luxury',
                notifications INTEGER DEFAULT 1
            )
        """)
        
        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_premium ON users(is_premium)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_level ON users(level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")


class PremiumKey:
    """Premium key model"""
    
    TABLE = "premium_keys"
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS premium_keys (
                key_id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_code TEXT UNIQUE,
                tier TEXT DEFAULT 'PRO',
                duration_days INTEGER,
                created_at TEXT,
                created_by INTEGER,
                redeemed_by INTEGER,
                redeemed_at TEXT,
                expiry_date TEXT,
                is_used INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_key_code ON premium_keys(key_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON premium_keys(status)")


class SearchLog:
    """Search log model for analytics"""
    
    TABLE = "logs"
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                command TEXT,
                query TEXT,
                result_status TEXT,
                api_endpoint TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                response_time REAL,
                is_premium INTEGER
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_logs ON logs(user_id, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_command ON logs(command)")


class Achievement:
    """Achievement system model"""
    
    TABLE = "achievements"
    
    ACHIEVEMENTS = {
        "first_search": {"name": "First Blood", "xp": 50, "desc": "Complete your first search"},
        "search_master": {"name": "Search Master", "xp": 500, "desc": "Complete 1000 searches"},
        "premium_elite": {"name": "Premium Elite", "xp": 1000, "desc": "Upgrade to Elite tier"},
        "referral_king": {"name": "Referral King", "xp": 300, "desc": "Refer 10 users"},
        "streak_warrior": {"name": "Streak Warrior", "xp": 200, "desc": "7 day streak"},
        "level_10": {"name": "Ascended", "xp": 1000, "desc": "Reach level 10"},
    }
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                achievement_id TEXT,
                unlocked_at TEXT,
                UNIQUE(user_id, achievement_id)
            )
        """)


class Referral:
    """Referral tracking model"""
    
    TABLE = "referrals"
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER UNIQUE,
                created_at TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_referrer ON referrals(referrer_id)")


class Session:
    """Active session tracking"""
    
    TABLE = "sessions"
    
    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id INTEGER,
                started_at TEXT,
                last_heartbeat TEXT,
                expires_at TEXT
            )
        """)