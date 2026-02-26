"""
AUTO01_SECURE.PY - MotoGP 2025 Standings Monitoring Bot (PRODUCTION-READY)

FIXED VERSION
- Stable React scraping
- Proper Chrome cleanup (no WinError 6)
- Headless safe
"""

import os
import sys
import json
import time
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import hashlib

# ==================== THIRD PARTY ====================
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==================== CONFIG ====================
@dataclass
class Config:
    bot_token: str
    chat_id: str
    motogp_url: str
    favorite_riders: List[str]
    chrome_version: int
    headless: bool
    timeout: int
    data_dir: Path
    logs_dir: Path

    @classmethod
    def from_file(cls, path="config.json"):
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)

        return cls(
            bot_token=d["telegram"]["bot_token"],
            chat_id=d["telegram"]["chat_id"],
            motogp_url=d["scraping"]["motogp_url"],
            favorite_riders=d.get("favorite_riders", []),
            chrome_version=d["chrome"].get("force_version", 145),
            headless=d["chrome"].get("headless", True),
            timeout=d["scraping"].get("request_timeout", 30),
            data_dir=Path(d.get("paths", {}).get("data_dir", "data")),
            logs_dir=Path(d.get("paths", {}).get("logs_dir", "logs")),
        )

# ==================== LOGGING ====================
def setup_logging(logs_dir: Path):
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / f"auto01_{datetime.now():%Y%m%d}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("=" * 70)
    logger.info("AUTO01 SECURE - MotoGP Monitoring Bot Started")
    logger.info("=" * 70)
    return logger

# ==================== SECURITY ====================
class SecurityValidator:
    @staticmethod
    def sanitize(text: str) -> str:
        return re.sub(r"[<>'\"{}();\\]", "", text).strip()

# ==================== TELEGRAM ====================
class SecureTelegramClient:
    def __init__(self, token: str, chat_id: str):
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1)
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.logger = logging.getLogger(__name__)

    def send(self, text: str):
        try:
            r = self.session.post(
                self.api_url,
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"},
                timeout=10,
            )
            r.raise_for_status()
            self.logger.info("✅ Telegram sent")
        except Exception as e:
            self.logger.error(f"Telegram error: {e}")

# ==================== CHROME ====================
class SecureChromeDriver:
    def __init__(self, config: Config):
        self.config = config
        self.driver = None
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        options = uc.ChromeOptions()
        if self.config.headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            f"user-agent=Mozilla/5.0 Chrome/{self.config.chrome_version}.0.0.0"
        )

        self.driver = uc.Chrome(
            version_main=self.config.chrome_version,
            options=options,
        )
        self.driver.set_page_load_timeout(self.config.timeout)
        self.driver.set_script_timeout(self.config.timeout)

        self.logger.info(f"✅ Chrome driver initialized (v{self.config.chrome_version})")
        return self.driver

    def __exit__(self, exc_type, exc, tb):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                self.logger.info("✅ Chrome driver closed")

# disable UC destructor (fix WinError 6)
uc.Chrome.__del__ = lambda self: None

# ==================== SCRAPER ====================
class SecureMotoGPScraper:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.validator = SecurityValidator()

    def scrape(self, driver) -> List[Dict]:
        try:
            self.logger.info(f"🌐 Opening: {self.config.motogp_url}")
            driver.get(self.config.motogp_url)

            wait = WebDriverWait(driver, 40)

            # DOM ready
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

            # trigger lazy load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(1)

            # wait for real table
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "table.ms-table--standings")
                )
            )

            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "table.ms-table--standings tbody tr")
                )
            )

            rows = driver.find_elements(
                By.CSS_SELECTOR, "table.ms-table--standings tbody tr"
            )

            self.logger.info(f"Found {len(rows)} rows")

            data = []
            for row in rows:
                try:
                    pos = row.find_element(By.CSS_SELECTOR, "td.ms-table_field--pos").text
                    rider = row.find_element(
                        By.CSS_SELECTOR, "span.name-short"
                    ).text
                    team = row.find_element(
                        By.CSS_SELECTOR, "span.team"
                    ).text
                    pts = row.find_element(
                        By.CSS_SELECTOR, "td.ms-table_field--total_points"
                    ).text

                    if not pos.isdigit() or not pts.isdigit():
                        continue

                    data.append(
                        {
                            "position": int(pos),
                            "rider": self.validator.sanitize(rider),
                            "team": self.validator.sanitize(team),
                            "points": int(pts),
                        }
                    )
                except Exception:
                    continue

            self.logger.info(f"✅ Scraped {len(data)} riders")
            return data

        except Exception as e:
            self.logger.error(f"Scraping failed: {e}", exc_info=True)
            return []

# ==================== DATA ====================
class SecureDataManager:
    def __init__(self, path: Path):
        self.path = path
        self.path.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save(self, data: List[Dict], name: str):
        file = self.path / name
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"💾 Saved: {file} ({len(data)} riders)")

    def load(self, name: str) -> List[Dict]:
        file = self.path / name
        if not file.exists():
            return []
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

# ==================== ANALYSIS ====================
class StandingsAnalyzer:
    def __init__(self, telegram: SecureTelegramClient):
        self.telegram = telegram

    def summary(self, current: List[Dict]):
        msg = "<b>MOTOGP 2025 UPDATE</b>\n\n"
        for r in current[:3]:
            msg += f"🏁 {r['position']}. {r['rider']} - {r['points']} pts\n"
        self.telegram.send(msg)

# ==================== MAIN ====================
def main():
    config = Config.from_file()
    logger = setup_logging(config.logs_dir)

    telegram = SecureTelegramClient(config.bot_token, config.chat_id)
    scraper = SecureMotoGPScraper(config)
    data = SecureDataManager(config.data_dir)
    analyzer = StandingsAnalyzer(telegram)

    previous = data.load("previous.json")

    with SecureChromeDriver(config) as driver:
        current = scraper.scrape(driver)

    if not current:
        logger.error("❌ No data scraped")
        return 1

    data.save(current, "current.json")
    analyzer.summary(current)
    data.save(current, "previous.json")

    logger.info("=" * 70)
    logger.info("✅ AUTO01 SECURE COMPLETED SUCCESSFULLY")
    logger.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())