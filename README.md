<img width="1925" height="985" alt="debug_screenshot" src="https://github.com/user-attachments/assets/59487473-9fd4-4b88-b77c-83ecd3b7cef1" /># 🏍️ MotoGP 2025 Monitoring Bot - Production Ready

**Secure, robust, and production-ready MotoGP standings monitoring system with Telegram integration.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-green.svg)](https://selenium.dev/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

---

## 📸 Screenshots

### 🌐 Website Source (motorsport.com)
<img width="1925" height="985" alt="debug_screenshot" src="https://github.com/user-attachments/assets/6ab74f89-31c0-4742-91a7-3f9f7f0e6e98" />

### 📱 Telegram Bot Features

#### `/top10` - Top 10 Standings
<img width="1070" height="712" alt="TOP10" src="https://github.com/user-attachments/assets/b9f21994-e460-49bb-8929-53f04682a1ca" />

#### `/team` - Team Rankings
<img width="1031" height="767" alt="TEAM" src="https://github.com/user-attachments/assets/9e7ed886-2e8d-461f-a9b6-f898c69c5268" />

#### `/best` - Best Performers
<img width="917" height="376" alt="BEST" src="https://github.com/user-attachments/assets/7d444f27-daee-4e19-8733-ce9611c8e9ab" />

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Demo](#-demo)
- [Security](#-security-features)
- [Requirements](#-requirements)
- [Installation](#️-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Telegram Commands](#-telegram-commands)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Features

### 🤖 AUTO01_SECURE.PY - Automated Monitoring Bot

✅ **Real-time Scraping**
- Fetch latest MotoGP 2025 standings from [motorsport.com](https://id.motorsport.com/motogp/standings/2025/)
- Parse rider positions, points, and teams
- Multiple selector fallback for reliability

✅ **Rider of the Week**
- Automatically detect best performing rider
- Calculate point gains and position changes
- Send weekly highlights to Telegram

✅ **Keyword Alerts**
- Monitor your favorite riders
- Get notified on position changes
- Track point progression

✅ **Consistency Rate**
- Calculate rider performance consistency
- Visual progress bars
- Top 8 rider analysis

✅ **Automatic Notifications**
- Send comprehensive reports to Telegram
- Daily/weekly summaries
- Real-time alerts

✅ **Data Persistence**
- Save current standings
- Compare with previous data
- Historical tracking

✅ **Smart Caching**
- Efficient data storage
- Automatic backup mechanism
- Recovery from failures

---

### 💬 AUTO02_SECURE.PY - Interactive Telegram Bot

✅ **7 Interactive Commands**

| Command | Description | Example Output |
|---------|-------------|----------------|
| `/start` | Welcome message | Bot introduction & commands |
| `/help` | Command list | Complete reference guide |
| `/top10` | Top 10 standings | Real-time top 10 riders |
| `/team` | Team rankings | Aggregated team points |
| `/delta` | Position changes | Compare with previous data |
| `/best` | Best performers | Top 3 riders highlighted |
| `/stats` | Bot statistics | Usage analytics & uptime |

✅ **Smart Features**

- **5-minute caching** - Reduce load, improve response time
- **Per-user rate limiting** - Prevent abuse (10 calls/60s)
- **Access control** - Whitelist/blacklist support
- **User analytics** - Track command usage
- **Error recovery** - Automatic retry with backoff
- **Real-time updates** - Always fresh data
- **Emoji support** - Visual and engaging

---

## 🎬 Demo

### Automated Monitoring (auto01_secure.py)

**First Run:**
```
✅ Chrome driver initialized (v145)
🌐 Opening: https://id.motorsport.com/motogp/standings/2025/
⏳ Waiting for page to load...
📜 Scrolling to load content...
🔍 Looking for standings table...
✅ Found elements with selector: table.ms-table--standings
✅ Scraped 29 riders
💾 Saved: data/current.json (29 riders)
```

**Telegram Notification:**
```
🏁 MotoGP Bot Initialized

✅ First data collected
👥 29 riders found

🏆 Leader: M. Marquez
📊 Points: 545
```

**Subsequent Runs with Analysis:**
```
📊 MOTOGP 2025 UPDATE
📅 24 February 2026, 08:00 WIB

👥 Total Pembalap: 29
🔺 Naik: 5
🔻 Turun: 3
➖ Tetap: 21

🏆 TOP 3
🥇 M. Marquez - 545 pts
🥈 A. Marquez - 467 pts
🥉 M. Bezzecchi - 353 pts

───────────────────

🏆 RIDER OF THE WEEK

👤 M. Marquez
📊 Poin: +37
📈 Posisi: ↑ 0
🎯 Posisi Sekarang: #1
💯 Total Poin: 545

───────────────────

🔔 ALERT: A. Marquez

📍 Posisi: #3 → #2 (NAIK)
📊 Poin: 438 → 467 (+29)
🏁 Tim: Gresini Racing

───────────────────

🧮 CONSISTENCY RATE
Top 8 Riders

M. Marquez
  ██████████ 100.0%
  #1 • 545 pts

A. Marquez
  ████████░░ 85.4%
  #2 • 467 pts

M. Bezzecchi
  ██████░░░░ 64.8%
  #3 • 353 pts

[... and so on]
```

---

### Interactive Bot (auto02_secure.py)

**Command: `/start`**
```
🏍️ MotoGP 2025 Bot

Bot monitoring klasemen MotoGP 2025 secara real-time!

📌 Commands:
/help - Daftar command
/top10 - Top 10 klasemen
/team - Klasemen per tim
/delta - Deteksi perubahan
/best - Best performers

🔒 Secure & Fast | Data from motorsport.com
```

**Command: `/top10`** _(See screenshot above)_
```
🏆 TOP 10 MotoGP 2025

🥇 1. M. Marquez
   📊 545 pts | Ducati Team

🥈 2. A. Marquez
   📊 467 pts | Gresini Racing

🥉 3. M. Bezzecchi
   📊 353 pts | Aprilia Racing Team

4. P. Acosta
   📊 307 pts | Red Bull KTM Factory Racing

5. F. Bagnaia
   📊 288 pts | Ducati Team

6. F. Di Giannantonio
   📊 262 pts | Team VR46

7. F. Morbidelli
   📊 231 pts | Team VR46

8. F. Aldeguer
   📊 214 pts | Gresini Racing

9. F. Quartararo
   📊 201 pts | Yamaha Factory Racing

10. R. Fernández
   📊 172 pts | Trackhouse Racing Team

📅 Updated: 10:46:14
```

**Command: `/team`** _(See screenshot above)_
```
🏁 TEAM RANKINGS

1. Ducati Team
   📊 835 pts | 3 riders
   👥 M. Marquez, F. Bagnaia

2. Gresini Racing
   📊 681 pts | 2 riders
   👥 A. Marquez, F. Aldeguer

3. Team VR46
   📊 493 pts | 2 riders
   👥 F. Di Giannantonio, F. Morbidelli

4. Red Bull KTM Factory Racing
   📊 462 pts | 2 riders
   👥 P. Acosta, B. Binder

5. Aprilia Racing Team
   📊 395 pts | 3 riders
   👥 M. Bezzecchi, J. Martin

[... and so on]
```

**Command: `/best`** _(See screenshot above)_
```
⭐ BEST PERFORMERS

🥇 M. Marquez
   Position: #1
   Points: 545
   Team: Ducati Team

🥈 A. Marquez
   Position: #2
   Points: 467
   Team: Gresini Racing

🥉 M. Bezzecchi
   Position: #3
   Points: 353
   Team: Aprilia Racing Team
```

---

## 🔒 Security Features

### ✅ Input Validation & Sanitization

**Pattern Matching:**
```python
ALLOWED_PATTERNS = {
    'rider_name': r'^[\w\s\.\-\'áéíóúñü]+$',
    'team_name': r'^[\w\s\.\-&]+$',
    'numeric': r'^\d+$'
}
```

**Security Measures:**
- XSS prevention (removes `<>"';(){}`)
- SQL injection prevention
- Length enforcement (100 chars max for riders)
- Type validation

### ✅ Rate Limiting

**Per-User Limits:**
- 10 calls per 60 seconds
- Automatic backoff
- Wait time calculation
- Admin bypass available

**Example:**
```python
class RateLimiter:
    def __init__(self, max_calls=10, window=60):
        self.max_calls = max_calls
        self.window = window
```

### ✅ Access Control

**Whitelist/Blacklist:**
```json
{
  "allowed_chat_ids": [1250352771, 9876543210],
  "admin_chat_ids": [1250352771]
}
```

**Features:**
- User tracking
- Audit trail
- Admin privileges
- Automatic blacklist

### ✅ Error Handling

**Comprehensive:**
- Try-catch everywhere
- Graceful degradation
- Retry with exponential backoff
- Timeout protection
- Resource cleanup

### ✅ Secure Operations

**Best Practices:**
- Environment variables for secrets
- Atomic file writes
- HTTPS-only connections
- Domain whitelisting
- Hash logging for sensitive data

---

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+
- **Python**: 3.8 or higher
- **Chrome**: Version 145.0.7632.110 (or compatible)
- **RAM**: Minimum 2GB, Recommended 4GB
- **Disk Space**: 100MB for application, logs, and data
- **Internet**: Stable connection required

### Python Dependencies

```txt
selenium>=4.15.0              # Browser automation
undetected-chromedriver>=3.5.4  # Anti-detection ChromeDriver
beautifulsoup4>=4.12.0        # HTML parsing
lxml>=4.9.3                   # Fast XML/HTML parser
requests>=2.31.0              # HTTP library
python-telegram-bot>=20.7     # Telegram Bot API
urllib3>=2.0.0                # HTTP client
certifi>=2023.7.22            # SSL certificates
```

---

## ⚙️ Installation

### Step 1: Clone/Download Repository
```bash
git clone <repository-url>
cd motogp-bot
```

Or download ZIP and extract.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

### Step 3: Get Telegram Bot Token

1. Open Telegram
2. Search for **@BotFather**
3. Send `/newbot`
4. Follow prompts:
   ```
   Name: MotoGP 2025 Bot
   Username: motogp2025_bot (must end in _bot)
   ```
5. **Copy the token** (format: `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`)

### Step 4: Get Your Chat ID

1. Search for **@userinfobot** in Telegram
2. Send `/start`
3. Bot will reply with your ID
4. **Copy the numeric ID** (e.g., `1250352771`)

### Step 5: Configure Bot

Edit `config.json`:

```json
{
  "telegram": {
    "bot_token": "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ",
    "chat_id": "1250352771"
  },
  "chrome": {
    "force_version": 145,
    "headless": true
  },
  "favorite_riders": [
    "Marc Marquez",
    "Jorge Martin",
    "Fabio Quartararo"
  ]
}
```

### Step 6: Clear Chrome Driver Cache

**Windows (PowerShell):**
```powershell
Remove-Item -Path "$env:APPDATA\undetected_chromedriver" -Recurse -Force
```

**Linux/Mac:**
```bash
rm -rf ~/.local/share/undetected_chromedriver
```

### Step 7: Test Installation

**Debug Mode:**
```bash
python debug_scraper.py
```

This will:
- ✅ Open browser (non-headless)
- ✅ Take screenshot
- ✅ Save HTML source
- ✅ Test selectors

---

## 🔧 Configuration

### Complete config.json Reference

```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN_HERE",
    "chat_id": "YOUR_CHAT_ID_HERE"
  },
  
  "scraping": {
    "motogp_url": "https://id.motorsport.com/motogp/standings/2025/",
    "max_attempts": 3,
    "request_timeout": 30,
    "rate_limit_delay": 5,
    "page_load_timeout": 60,
    "scroll_delay_min": 2,
    "scroll_delay_max": 4
  },
  
  "chrome": {
    "auto_detect_version": false,
    "force_version": 145,
    "headless": true,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  },
  
  "favorite_riders": [
    "Marc Marquez",
    "Alex Marquez",
    "Fabio Quartararo",
    "Jorge Martin"
  ],
  
  "allowed_chat_ids": [],
  "admin_chat_ids": [],
  
  "bot": {
    "rate_limit_max_calls": 10,
    "rate_limit_window": 60
  },
  
  "paths": {
    "data_dir": "data",
    "logs_dir": "logs",
    "current_file": "current.json",
    "previous_file": "previous.json"
  },
  
  "logging": {
    "level": "INFO",
    "max_bytes": 10485760,
    "backup_count": 5
  },
  
  "security": {
    "max_input_length": 200,
    "max_team_name_length": 80,
    "max_rider_name_length": 100,
    "allowed_domains": [
      "motorsport.com",
      "www.motorsport.com",
      "id.motorsport.com"
    ]
  }
}
```

### Key Configuration Options

#### 1. Favorite Riders (Keyword Alerts)
```json
"favorite_riders": [
  "Marc Marquez",
  "Jorge Martin",
  "Fabio Quartararo",
  "Enea Bastianini"
]
```

#### 2. Access Control

**Public (Default):**
```json
"allowed_chat_ids": []
```

**Whitelist Specific Users:**
```json
"allowed_chat_ids": [1250352771, 9876543210]
```

**Set Admins:**
```json
"admin_chat_ids": [1250352771]
```

#### 3. Chrome Settings

**Production (Headless):**
```json
"chrome": {
  "force_version": 145,
  "headless": true
}
```

**Debug (Visible Browser):**
```json
"chrome": {
  "force_version": 145,
  "headless": false
}
```

#### 4. Scraping Timeouts

**Default:**
```json
"scraping": {
  "page_load_timeout": 60,
  "request_timeout": 30,
  "max_attempts": 3
}
```

**Slow Internet:**
```json
"scraping": {
  "page_load_timeout": 120,
  "request_timeout": 60,
  "max_attempts": 5
}
```

#### 5. Rate Limiting

**Permissive:**
```json
"bot": {
  "rate_limit_max_calls": 20,
  "rate_limit_window": 60
}
```

**Strict:**
```json
"bot": {
  "rate_limit_max_calls": 5,
  "rate_limit_window": 60
}
```

---

## 🚀 Usage

### AUTO01_SECURE.PY - Automated Monitoring

#### Manual Run

```bash
python auto01_secure.py
```

**First Run Output:**
```
======================================================================
AUTO01 SECURE - MotoGP Monitoring Bot Started
======================================================================
✅ Chrome driver initialized (v145)
🌐 Opening: https://id.motorsport.com/motogp/standings/2025/
✅ Scraped 29 riders
💾 Saved: data/current.json (29 riders)
ℹ️  First run - no previous data
🏁 MotoGP Bot Initialized
```

**Subsequent Runs:**
```
======================================================================
📈 RUNNING ANALYSIS
======================================================================
📋 Generating summary...
✅ Telegram sent: 📊 MOTOGP 2025 UPDATE...
🏆 Analyzing best rider...
✅ Telegram sent: 🏆 RIDER OF THE WEEK...
🔔 Checking keyword alerts...
✅ Alert sent for A. Marquez
🧮 Calculating consistency...
✅ Telegram sent: 🧮 CONSISTENCY RATE...

✅ All analysis completed!
```

#### Schedule with Cron (Linux)

```bash
# Edit crontab
crontab -e

# Run every 6 hours
0 */6 * * * cd /path/to/motogp-bot && /usr/bin/python3 auto01_secure.py >> /path/to/logs/cron.log 2>&1

# Run daily at 8 AM
0 8 * * * cd /path/to/motogp-bot && /usr/bin/python3 auto01_secure.py >> /path/to/logs/cron.log 2>&1
```

#### Schedule with Task Scheduler (Windows)

1. Open **Task Scheduler**
2. Action → **Create Basic Task**
3. Name: `MotoGP Bot Monitoring`
4. Trigger: **Daily** at `8:00 AM`
5. Action: **Start a program**
   - Program/script: `python.exe`
   - Add arguments: `C:\path\to\auto01_secure.py`
   - Start in: `C:\path\to\motogp-bot`
6. Finish → **Open Properties**
7. Run whether user is logged on or not
8. Run with highest privileges

---

### AUTO02_SECURE.PY - Interactive Telegram Bot

#### Start Bot

```bash
python auto02_secure.py
```

**Expected Output:**
```
2026-02-24 10:00:00 | INFO     | __main__ | Loading configuration...
2026-02-24 10:00:00 | INFO     | __main__ | Initializing bot...
2026-02-24 10:00:01 | INFO     | __main__ | ======================================================================
2026-02-24 10:00:01 | INFO     | __main__ | 🏍️  MotoGP Bot Started Successfully!
2026-02-24 10:00:01 | INFO     | __main__ | ======================================================================
2026-02-24 10:00:01 | INFO     | __main__ | Bot is running... Press Ctrl+C to stop
```

#### Keep Running in Background

**Linux (screen):**
```bash
screen -S motogp-bot
python auto02_secure.py
# Press Ctrl+A then D to detach
```

**Linux (systemd service):**
```bash
# Create service file
sudo nano /etc/systemd/system/motogp-bot.service
```

```ini
[Unit]
Description=MotoGP Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/motogp-bot
ExecStart=/usr/bin/python3 /path/to/motogp-bot/auto02_secure.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable motogp-bot
sudo systemctl start motogp-bot
sudo systemctl status motogp-bot
```

**Windows (NSSM):**
```bash
# Download NSSM from nssm.cc
nssm install MotoGPBot

# GUI opens - configure:
Path: python.exe
Startup directory: C:\path\to\motogp-bot
Arguments: auto02_secure.py
```

---

## 🤖 Telegram Commands

### Available Commands

| Command | Description | Access | Rate Limited |
|---------|-------------|--------|--------------|
| `/start` | Welcome message | Public | Yes |
| `/help` | Command list | Public | Yes |
| `/top10` | Top 10 standings | Public | Yes |
| `/team` | Team rankings | Public | Yes |
| `/delta` | Position changes | Public | Yes |
| `/best` | Best performers | Public | Yes |
| `/stats` | Bot statistics | Public | Yes |

### Command Examples

#### `/start`
```
🏍️ MotoGP 2025 Bot

Bot monitoring klasemen MotoGP 2025 secara real-time!

📌 Commands:
/help - Daftar command
/top10 - Top 10 klasemen
/team - Klasemen per tim
/delta - Deteksi perubahan
/best - Best performers

🔒 Secure & Fast | Data from motorsport.com
```

#### `/help`
```
📋 Available Commands

🏆 /top10
   Tampilkan top 10 klasemen real-time

🏁 /team
   Klasemen berdasarkan tim

📊 /delta
   Deteksi perubahan posisi

⭐ /best
   Top 3 pembalap terbaik

📈 /stats
   Statistik bot

ℹ️ Data di-cache 5 menit untuk performa optimal
```

#### `/stats`
```
📈 BOT STATISTICS

⏰ Uptime: 5h 23m
📊 Commands: 147
👥 Users: 12

Command Usage:
/top10: 64
/team: 32
/best: 28
/help: 15
/start: 8
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### ❌ Error: "Timeout waiting for table"

**Symptoms:**
```
ERROR | Timeout waiting for table
💡 Try running with headless=false in config to debug
```

**Causes:**
1. Slow internet connection
2. Website taking too long to load
3. Lazy loading not triggered
4. Anti-bot detection

**Solutions:**

**Solution 1: Run Debug Script**
```bash
python debug_scraper.py
```

Files generated:
- `debug_screenshot.png` - What browser sees
- `debug_page_source.html` - Full HTML source

**Solution 2: Increase Timeout**
```json
{
  "scraping": {
    "page_load_timeout": 120,
    "request_timeout": 60
  }
}
```

**Solution 3: Disable Headless Mode**
```json
{
  "chrome": {
    "headless": false
  }
}
```

**Solution 4: Check Internet**
```bash
ping motorsport.com
curl -I https://id.motorsport.com/motogp/standings/2025/
```

---

#### ❌ Error: "Chrome version mismatch"

**Symptoms:**
```
This version of ChromeDriver only supports Chrome version 145
Current browser version is 150 with binary path...
```

**Solution:**

**Step 1: Check Chrome Version**
- Open Chrome
- Navigate to `chrome://version`
- Note the version number (e.g., **150**.0.xxxx.xx)

**Step 2: Update config.json**
```json
{
  "chrome": {
    "force_version": 150
  }
}
```

**Step 3: Clear Cache**
```powershell
# Windows
Remove-Item -Path "$env:APPDATA\undetected_chromedriver" -Recurse -Force

# Linux/Mac
rm -rf ~/.local/share/undetected_chromedriver
```

**Step 4: Retry**
```bash
python auto01_secure.py
```

---

#### ❌ Error: "Telegram error: 401 Unauthorized"

**Symptoms:**
```
Telegram error: 401 Unauthorized
```

**Causes:**
1. Invalid bot token
2. Token has extra spaces/newlines
3. Bot was deleted/revoked by BotFather

**Solutions:**

**Solution 1: Verify Token**
```json
{
  "telegram": {
    "bot_token": "1234567890:ABCdef-NO_SPACES_OR_NEWLINES"
  }
}
```

**Solution 2: Test Token Manually**
```bash
# Replace with your token
curl https://api.telegram.org/bot1234567890:ABCdef/getMe
```

**Solution 3: Get New Token**
1. Open Telegram → @BotFather
2. Send `/token`
3. Select your bot
4. Copy new token
5. Update config.json

**Solution 4: Create New Bot**
1. @BotFather → `/newbot`
2. Follow prompts
3. Update config.json with new token

---

#### ❌ Error: "Rate limit exceeded"

**Symptoms:**
```
⏱️ Rate limit exceeded. Try again in 45s
```

**Cause:**
User sent too many commands in short time (default: 10/60s)

**Solutions:**

**Solution 1: Wait**
Wait the specified time (usually ≤60 seconds)

**Solution 2: Adjust Limits (Admin)**
```json
{
  "bot": {
    "rate_limit_max_calls": 20,
    "rate_limit_window": 60
  }
}
```

**Solution 3: Add to Whitelist**
```json
{
  "admin_chat_ids": [1250352771]
}
```
Admins bypass rate limiting.

---

#### ❌ Error: "Module not found"

**Symptoms:**
```
ModuleNotFoundError: No module named 'selenium'
ModuleNotFoundError: No module named 'undetected_chromedriver'
```

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --break-system-packages

# Or install individually
pip install selenium undetected-chromedriver beautifulsoup4 lxml requests python-telegram-bot
```

---

#### ❌ Error: "No data scraped"

**Symptoms:**
```
⚠️ No table found with any selector
❌ No data scraped
```

**Debugging:**

**Step 1: Run debug_scraper.py**
```bash
python debug_scraper.py
```

**Step 2: Check Screenshot**
```bash
# Windows
start debug_screenshot.png

# Linux
xdg-open debug_screenshot.png

# Mac
open debug_screenshot.png
```

**Step 3: Check HTML Source**
Look for table in `debug_page_source.html`:
- Search for `ms-table--standings`
- Search for `ms-table`
- Search for any `<table>` tag

**Step 4: Update Selector (if needed)**

If website changed structure, update `auto01_secure.py`:
```python
# Around line 375
selectors = [
    "table.NEW_CLASS_NAME",  # Add new selector
    "table.ms-table--standings",
    "table.ms-table",
]
```

---

## 📁 Project Structure

```
motogp-bot/
│
├── 📄 auto01_secure.py          # Automated monitoring bot
├── 📄 auto02_secure.py          # Interactive Telegram bot
├── 🔧 debug_scraper.py          # Debug tool for troubleshooting
│
├── ⚙️ config.json               # Configuration file (EDIT THIS!)
├── 📋 requirements.txt          # Python dependencies
│
├── 📚 README.md                 # This file
├── 🚀 QUICKSTART.md             # 5-minute setup guide
│
├── 🔒 .env.example              # Environment variables template
├── 🚫 .gitignore                # Git ignore rules
│
├── 📊 data/                     # Auto-created on first run
│   ├── current.json             # Latest scraped data
│   └── previous.json            # Previous data for comparison
│
├── 📝 logs/                     # Auto-created on first run
│   ├── auto01_20260224.log      # Daily log rotation
│   └── auto02_20260224.log
│
└── 🖼️ screenshots/              # Bot screenshots (documentation)
    ├── debug_screenshot.png     # Website screenshot
    ├── TOP10.png                # /top10 command
    ├── TEAM.png                 # /team command
    └── BEST.png                 # /best command
```

---

## 📊 Data Files

### data/current.json
```json
[
  {
    "position": 1,
    "rider": "M. Marquez",
    "team": "Ducati Team",
    "points": 545
  },
  {
    "position": 2,
    "rider": "A. Marquez",
    "team": "Gresini Racing",
    "points": 467
  },
  ...
]
```

### data/previous.json
Same format as `current.json`, used for comparison in analysis.

---

## 📈 Logging & Monitoring

### Log Files

**Location:** `logs/auto01_YYYYMMDD.log`

**Log Levels:**
- **INFO**: Normal operations
- **WARNING**: Rate limits, retries
- **ERROR**: Failed operations
- **CRITICAL**: Fatal errors

**Example:**
```
2026-02-24 08:00:00 | INFO     | __main__ | ✅ Chrome driver initialized (v145)
2026-02-24 08:00:05 | INFO     | __main__ | 🌐 Opening: https://id.motorsport.com/...
2026-02-24 08:00:12 | INFO     | __main__ | ✅ Scraped 29 riders
2026-02-24 08:00:13 | INFO     | __main__ | 💾 Saved: data/current.json
2026-02-24 08:05:30 | INFO     | __main__ | Command: /top10 | User: 1250352771
2026-02-24 08:06:15 | WARNING  | __main__ | Rate limit hit for user 9876543210
2026-02-24 08:10:00 | ERROR    | __main__ | Timeout waiting for table
```

### Monitoring Best Practices

1. **Check logs daily** for errors
2. **Monitor disk space** (logs rotate but grow)
3. **Set up alerts** for CRITICAL errors
4. **Review rate limit hits**
5. **Track success rate** of scraping

---

## 🔐 Security Best Practices

### ✅ DO:

✓ **Keep config.json private**  
✓ **Use environment variables** for tokens  
✓ **Enable whitelist** in production  
✓ **Monitor logs** regularly  
✓ **Update dependencies** monthly  
✓ **Use HTTPS** only (default)  
✓ **Rotate bot token** periodically  
✓ **Limit admin access**  
✓ **Review rate limits**  
✓ **Backup data** regularly  

### ❌ DON'T:

✗ **Commit bot token** to version control  
✗ **Share config.json** publicly  
✗ **Disable rate limiting**  
✗ **Run as root/administrator**  
✗ **Ignore error logs**  
✗ **Use public WiFi** without VPN  
✗ **Share bot publicly** without whitelist  
✗ **Hardcode secrets** in code  

---

## 📈 Performance

### Resource Usage

**Typical:**
- **RAM**: ~200MB (headless Chrome)
- **CPU**: <5% idle, ~30% scraping
- **Network**: ~500KB per scrape
- **Disk**: ~1MB/day (logs + data)

### Optimization Tips

1. **Use headless mode** (less RAM)
2. **Increase cache TTL** (fewer scrapes)
3. **Disable debug logging** in production
4. **Rotate logs** to prevent disk fill
5. **Schedule scraping** during off-peak hours

---

## ❓ FAQ

### Q: How often should I run auto01_secure.py?

**A:** Depends on your needs:
- **Real-time**: Every 6 hours during race weekends
- **Daily updates**: Once per day (morning)
- **Weekly**: Once per week (after major races)

Recommended: **Daily at 8 AM**

### Q: Can I run both bots simultaneously?

**A:** Yes! 
- `auto01_secure.py` - Runs once and exits
- `auto02_secure.py` - Runs continuously

Schedule `auto01` to run periodically while keeping `auto02` running as a service.

### Q: What if my favorite rider isn't detected?

**A:** Check spelling in `config.json`:
```json
"favorite_riders": [
  "Marquez",  // ✅ Partial match works
  "Marc Márquez",  // ✅ Full name with accents
  "M. Marquez"  // ✅ As shown in standings
]
```

Use partial matches for flexibility.

### Q: How do I stop receiving notifications?

**A:**

**Option 1:** Stop auto01
- Remove scheduled task/cron job
- Don't run `auto01_secure.py`

**Option 2:** Disable features
```json
"favorite_riders": []  // Disable keyword alerts
```

**Option 3:** Blacklist yourself (temporary)
Ask admin to add your chat_id to blacklist.

### Q: Can I use this for other racing series?

**A:** Yes! Change URL in config:
```json
{
  "scraping": {
    "motogp_url": "https://id.motorsport.com/f1/standings/2025/"
  }
}
```

**Note:** May need selector adjustments if HTML structure differs.

### Q: Is my data secure?

**A:** Yes!
- ✅ All data stored locally
- ✅ No cloud storage
- ✅ Bot token in config (keep private)
- ✅ No data sent to third parties
- ✅ HTTPS-only connections

### Q: How much does it cost to run?

**A:** Free!
- ✅ Python (free)
- ✅ Chrome (free)
- ✅ Telegram Bot (free)
- ✅ Open source libraries (free)

Only cost: **Internet connection**

### Q: Can I run this on a Raspberry Pi?

**A:** Yes! But:
- ✅ Use headless mode (required)
- ⚠️ May be slower (ARM architecture)
- ⚠️ Need ARM-compatible Chrome/Chromium
- ⚠️ Recommended: RPi 4 with 4GB+ RAM

### Q: How do I contribute?

**A:** See [Contributing](#-contributing) section below!

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Reporting Bugs

1. **Search existing issues** first
2. **Create new issue** with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Log excerpts (remove sensitive data!)
   - Screenshots if applicable
   - Environment (OS, Python version, Chrome version)

### Feature Requests

1. **Search existing requests**
2. **Create issue** with:
   - Use case description
   - Proposed solution
   - Impact assessment
   - Mockups/examples if applicable

### Pull Requests

1. Fork the repository
2. Create feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Make changes
4. Commit with clear messages
   ```bash
   git commit -m 'Add AmazingFeature: description'
   ```
5. Push to branch
   ```bash
   git push origin feature/AmazingFeature
   ```
6. Open Pull Request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Include tests
- Update documentation

---

## 📜 License

MIT License

Copyright (c) 2026 MotoGP Bot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🙏 Acknowledgments

- **Data Source**: [Motorsport.com](https://id.motorsport.com/motogp/standings/2025/)
- **Browser Automation**: [Selenium](https://selenium.dev/)
- **Anti-Detection**: [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- **Telegram API**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **HTML Parsing**: [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- **HTTP Requests**: [Requests](https://requests.readthedocs.io/)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐!

---

**Built with ❤️ for MotoGP fans | Secure, Fast, Reliable**

**Star ⭐ this repo if you find it useful!**

---

*Last Updated: February 24, 2026*
*Version: 2.0.0*
*Contributors: [List]((https://github.com/yourusername/motogp-bot/graphs/contributors))*
