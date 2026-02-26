"""
AUTO02_SECURE.PY - MotoGP 2025 Interactive Telegram Bot (PRODUCTION-READY)

Security Improvements:
✓ Command rate limiting
✓ User whitelist/blacklist
✓ Input validation
✓ Error handling
✓ Secure scraping
✓ Logging & monitoring
✓ Graceful shutdown

Commands:
/start  - Welcome message
/help   - Command list
/top10  - Top 10 standings
/team   - Team rankings
/delta  - Position changes
/best   - Best performers
/stats  - Bot statistics
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import asyncio

# Third-party imports
try:
    from telegram import Update, BotCommand
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        filters
    )
    from telegram.error import TelegramError, NetworkError, TimedOut
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install: pip install python-telegram-bot undetected-chromedriver --break-system-packages")
    sys.exit(1)

# ==================== CONFIGURATION ====================
class BotConfig:
    """Bot configuration with validation"""
    
    def __init__(self, config_path: str = "config.json"):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.bot_token = data['telegram']['bot_token']
            self.allowed_chat_ids = data.get('allowed_chat_ids', [])
            self.admin_chat_ids = data.get('admin_chat_ids', [])
            
            self.motogp_url = data['scraping']['motogp_url']
            self.chrome_version = data['chrome'].get('force_version', 145)
            self.headless = data['chrome'].get('headless', True)
            
            self.rate_limit_window = data.get('bot', {}).get('rate_limit_window', 60)
            self.rate_limit_max_calls = data.get('bot', {}).get('rate_limit_max_calls', 10)
            
            self.validate()
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except KeyError as e:
            raise ValueError(f"Missing config key: {e}")
    
    def validate(self):
        """Validate configuration"""
        if not self.bot_token or len(self.bot_token) < 20:
            raise ValueError("Invalid bot token")
        
        if not self.motogp_url.startswith('https://'):
            raise ValueError("URL must use HTTPS")

# ==================== RATE LIMITER ====================
class CommandRateLimiter:
    """Rate limiting for bot commands per user"""
    
    def __init__(self, max_calls: int = 10, window: int = 60):
        self.max_calls = max_calls
        self.window = window
        self.user_calls: Dict[int, List[datetime]] = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def is_allowed(self, user_id: int) -> tuple[bool, Optional[int]]:
        """
        Check if user is allowed to make request
        Returns: (allowed, wait_time_seconds)
        """
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window)
        
        # Remove old calls
        self.user_calls[user_id] = [
            t for t in self.user_calls[user_id]
            if t > cutoff
        ]
        
        if len(self.user_calls[user_id]) < self.max_calls:
            self.user_calls[user_id].append(now)
            return True, None
        
        # Calculate wait time
        oldest_call = min(self.user_calls[user_id])
        wait_time = int((oldest_call + timedelta(seconds=self.window) - now).total_seconds())
        
        self.logger.warning(f"Rate limit hit for user {user_id}")
        return False, max(wait_time, 1)
    
    def reset_user(self, user_id: int):
        """Reset rate limit for user (admin only)"""
        if user_id in self.user_calls:
            del self.user_calls[user_id]

# ==================== ACCESS CONTROL ====================
class AccessControl:
    """User access control with whitelist/blacklist"""
    
    def __init__(self, allowed_ids: List[int], admin_ids: List[int]):
        self.allowed_ids = set(allowed_ids) if allowed_ids else None
        self.admin_ids = set(admin_ids)
        self.blacklist = set()
        self.logger = logging.getLogger(__name__)
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed"""
        # Check blacklist first
        if user_id in self.blacklist:
            self.logger.warning(f"Blacklisted user attempted access: {user_id}")
            return False
        
        # Check admin (always allowed)
        if user_id in self.admin_ids:
            return True
        
        # Check whitelist (if configured)
        if self.allowed_ids is not None:
            return user_id in self.allowed_ids
        
        # If no whitelist, allow all
        return True
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_ids
    
    def add_to_blacklist(self, user_id: int):
        """Add user to blacklist"""
        self.blacklist.add(user_id)
        self.logger.warning(f"User added to blacklist: {user_id}")

# ==================== SCRAPER ====================
class SecureScraper:
    """Secure MotoGP scraper with caching"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cache = None
        self.cache_time = None
        self.cache_ttl = 300  # 5 minutes
    
    def get_standings(self, force_refresh: bool = False) -> List[Dict]:
        """Get standings with caching"""
        # Check cache
        if not force_refresh and self.cache and self.cache_time:
            age = (datetime.now() - self.cache_time).total_seconds()
            if age < self.cache_ttl:
                self.logger.info(f"Using cache (age: {age:.0f}s)")
                return self.cache
        
        # Scrape fresh data
        self.logger.info("Scraping fresh data...")
        standings = self._scrape()
        
        if standings:
            self.cache = standings
            self.cache_time = datetime.now()
        
        return standings
    
    def _scrape(self) -> List[Dict]:
        """Scrape standings"""
        driver = None
        try:
            # Setup Chrome
            options = uc.ChromeOptions()
            if self.config.headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            driver = uc.Chrome(
                version_main=self.config.chrome_version,
                options=options
            )
            driver.set_page_load_timeout(30)
            
            # Load page
            driver.get(self.config.motogp_url)
            
            # Wait for table
            wait = WebDriverWait(driver, 20)
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "table.ms-table--standings")
                )
            )
            
            # Parse data
            standings = []
            rows = driver.find_elements(
                By.CSS_SELECTOR,
                "table.ms-table--standings tbody tr"
            )
            
            for row in rows:
                try:
                    pos_elem = row.find_element(By.CSS_SELECTOR, "td.ms-table_field--pos")
                    name_elem = row.find_element(By.CSS_SELECTOR, "td.ms-table_field--driver span.name-short")
                    team_elem = row.find_element(By.CSS_SELECTOR, "td.ms-table_field--driver span.team")
                    points_elem = row.find_element(By.CSS_SELECTOR, "td.ms-table_field--total_points")
                    
                    position = int(pos_elem.text.strip())
                    rider = name_elem.text.strip()
                    team = team_elem.text.strip()
                    points = int(points_elem.text.strip())
                    
                    standings.append({
                        "position": position,
                        "rider": rider,
                        "team": team,
                        "points": points
                    })
                except Exception as e:
                    self.logger.debug(f"Row parse error: {e}")
                    continue
            
            self.logger.info(f"Scraped {len(standings)} riders")
            return standings
            
        except Exception as e:
            self.logger.error(f"Scraping error: {e}")
            return []
        finally:
            if driver:
                driver.quit()

# ==================== BOT HANDLERS ====================
class MotoGPBot:
    """Main bot class with all command handlers"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.scraper = SecureScraper(config)
        self.rate_limiter = CommandRateLimiter(
            max_calls=config.rate_limit_max_calls,
            window=config.rate_limit_window
        )
        self.access_control = AccessControl(
            config.allowed_chat_ids,
            config.admin_chat_ids
        )
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = {
            "commands_total": 0,
            "commands_by_type": defaultdict(int),
            "users": set(),
            "start_time": datetime.now()
        }
    
    def _check_access(self, update: Update) -> bool:
        """Check user access"""
        user_id = update.effective_user.id
        
        if not self.access_control.is_allowed(user_id):
            update.message.reply_text("❌ Access denied")
            return False
        
        allowed, wait_time = self.rate_limiter.is_allowed(user_id)
        if not allowed:
            update.message.reply_text(
                f"⏱️ Rate limit exceeded. Try again in {wait_time}s"
            )
            return False
        
        return True
    
    def _log_command(self, update: Update, command: str):
        """Log command usage"""
        user = update.effective_user
        self.stats["commands_total"] += 1
        self.stats["commands_by_type"][command] += 1
        self.stats["users"].add(user.id)
        
        self.logger.info(
            f"Command: /{command} | User: {user.id} ({user.first_name})"
        )
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "start")
        
        message = (
            "🏍️ <b>MotoGP 2025 Bot</b>\n\n"
            "Bot monitoring klasemen MotoGP 2025 secara real-time!\n\n"
            "📌 <b>Commands:</b>\n"
            "/help - Daftar command\n"
            "/top10 - Top 10 klasemen\n"
            "/team - Klasemen per tim\n"
            "/delta - Deteksi perubahan\n"
            "/best - Best performers\n\n"
            "🔒 Secure & Fast | Data from motorsport.com"
        )
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "help")
        
        message = (
            "📋 <b>Available Commands</b>\n\n"
            "🏆 <b>/top10</b>\n"
            "   Tampilkan top 10 klasemen real-time\n\n"
            "🏁 <b>/team</b>\n"
            "   Klasemen berdasarkan tim\n\n"
            "📊 <b>/delta</b>\n"
            "   Deteksi perubahan posisi\n\n"
            "⭐ <b>/best</b>\n"
            "   Top 3 pembalap terbaik\n\n"
            "📈 <b>/stats</b>\n"
            "   Statistik bot\n\n"
            "ℹ️ Data di-cache 5 menit untuk performa optimal"
        )
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_top10(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top10 command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "top10")
        
        # Send "loading" message
        loading_msg = await update.message.reply_text("⏳ Fetching data...")
        
        try:
            standings = self.scraper.get_standings()
            
            if not standings:
                await loading_msg.edit_text("❌ Failed to fetch data")
                return
            
            message = "🏆 <b>TOP 10 MotoGP 2025</b>\n\n"
            
            for i, rider in enumerate(standings[:10], 1):
                medal = ""
                if i == 1:
                    medal = "🥇 "
                elif i == 2:
                    medal = "🥈 "
                elif i == 3:
                    medal = "🥉 "
                
                message += (
                    f"{medal}<b>{i}. {rider['rider']}</b>\n"
                    f"   📊 {rider['points']} pts | {rider['team']}\n\n"
                )
            
            message += f"📅 Updated: {datetime.now().strftime('%H:%M:%S')}"
            
            await loading_msg.edit_text(message, parse_mode="HTML")
            
        except Exception as e:
            self.logger.error(f"Error in /top10: {e}")
            await loading_msg.edit_text("❌ Error occurred")
    
    async def cmd_team(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /team command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "team")
        
        loading_msg = await update.message.reply_text("⏳ Calculating team rankings...")
        
        try:
            standings = self.scraper.get_standings()
            
            if not standings:
                await loading_msg.edit_text("❌ Failed to fetch data")
                return
            
            # Calculate team points
            team_points = defaultdict(int)
            team_riders = defaultdict(list)
            
            for rider in standings:
                team = rider['team']
                team_points[team] += rider['points']
                team_riders[team].append(rider)
            
            # Sort teams by points
            sorted_teams = sorted(
                team_points.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            message = "🏁 <b>TEAM RANKINGS</b>\n\n"
            
            for i, (team, points) in enumerate(sorted_teams[:10], 1):
                riders = team_riders[team]
                rider_names = ", ".join([r['rider'] for r in riders[:2]])
                
                message += (
                    f"<b>{i}. {team}</b>\n"
                    f"   📊 {points} pts | {len(riders)} riders\n"
                    f"   👥 {rider_names}\n\n"
                )
            
            await loading_msg.edit_text(message, parse_mode="HTML")
            
        except Exception as e:
            self.logger.error(f"Error in /team: {e}")
            await loading_msg.edit_text("❌ Error occurred")
    
    async def cmd_delta(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /delta command - show position changes"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "delta")
        
        await update.message.reply_text(
            "📊 Delta detector requires previous data.\n"
            "This feature tracks position changes over time.\n\n"
            "Run the monitoring bot (auto01_secure.py) first!"
        )
    
    async def cmd_best(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /best command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "best")
        
        loading_msg = await update.message.reply_text("⏳ Analyzing...")
        
        try:
            standings = self.scraper.get_standings()
            
            if not standings:
                await loading_msg.edit_text("❌ Failed to fetch data")
                return
            
            message = "⭐ <b>BEST PERFORMERS</b>\n\n"
            
            for i, rider in enumerate(standings[:3], 1):
                medal = ["🥇", "🥈", "🥉"][i-1]
                
                message += (
                    f"{medal} <b>{rider['rider']}</b>\n"
                    f"   Position: #{rider['position']}\n"
                    f"   Points: {rider['points']}\n"
                    f"   Team: {rider['team']}\n\n"
                )
            
            await loading_msg.edit_text(message, parse_mode="HTML")
            
        except Exception as e:
            self.logger.error(f"Error in /best: {e}")
            await loading_msg.edit_text("❌ Error occurred")
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        if not self._check_access(update):
            return
        
        self._log_command(update, "stats")
        
        uptime = datetime.now() - self.stats["start_time"]
        hours = int(uptime.total_seconds() / 3600)
        minutes = int((uptime.total_seconds() % 3600) / 60)
        
        message = (
            "📈 <b>BOT STATISTICS</b>\n\n"
            f"⏰ Uptime: {hours}h {minutes}m\n"
            f"📊 Commands: {self.stats['commands_total']}\n"
            f"👥 Users: {len(self.stats['users'])}\n\n"
            "<b>Command Usage:</b>\n"
        )
        
        for cmd, count in sorted(
            self.stats["commands_by_type"].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            message += f"/{cmd}: {count}\n"
        
        await update.message.reply_text(message, parse_mode="HTML")

# ==================== ERROR HANDLER ====================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger = logging.getLogger(__name__)
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ An error occurred. Please try again later."
        )

# ==================== MAIN ====================
def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Load config
        logger.info("Loading configuration...")
        config = BotConfig("config.json")
        
        # Create bot
        logger.info("Initializing bot...")
        bot = MotoGPBot(config)
        
        # Build application
        app = Application.builder().token(config.bot_token).build()
        
        # Register command handlers
        app.add_handler(CommandHandler("start", bot.cmd_start))
        app.add_handler(CommandHandler("help", bot.cmd_help))
        app.add_handler(CommandHandler("top10", bot.cmd_top10))
        app.add_handler(CommandHandler("team", bot.cmd_team))
        app.add_handler(CommandHandler("delta", bot.cmd_delta))
        app.add_handler(CommandHandler("best", bot.cmd_best))
        app.add_handler(CommandHandler("stats", bot.cmd_stats))
        
        # Register error handler
        app.add_error_handler(error_handler)
        
        # Set bot commands (for UI)
        async def post_init(application: Application):
            commands = [
                BotCommand("start", "Start bot"),
                BotCommand("help", "Show help"),
                BotCommand("top10", "Top 10 standings"),
                BotCommand("team", "Team rankings"),
                BotCommand("delta", "Position changes"),
                BotCommand("best", "Best performers"),
                BotCommand("stats", "Bot statistics"),
            ]
            await application.bot.set_my_commands(commands)
        
        app.post_init = post_init
        
        # Start bot
        logger.info("=" * 70)
        logger.info("🏍️  MotoGP Bot Started Successfully!")
        logger.info("=" * 70)
        logger.info("Bot is running... Press Ctrl+C to stop")
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())