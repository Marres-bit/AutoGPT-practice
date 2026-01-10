"""
Configuration for the SP Testnet agent
Do NOT use this in production. Keys and defaults are for Testnet only.
"""
from pathlib import Path
import os

# Default Testnet API keys (user provided). You can override via env vars.
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "ZhYJ4IflyUlxOjbm4CUpWTTuDHSFgVLuTY42c5cZNITUgxqURkwVWQjlWlVgrBeh")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "uOoGCPNBhLJjgZrzwvQDNuQp2atvv8pAUxi881cLbBZUmyMDperLwmu4NAEWLDu4")

# Testnet base URL (Binance testnet REST endpoint)
# NOTE: We ensure this runs against testnet only.
BINANCE_TESTNET_BASE = os.getenv("BINANCE_TESTNET_BASE", "https://testnet.binance.vision")

# Trading defaults
DEFAULT_PRINCIPAL_USDT = float(os.getenv("SP_DEFAULT_PRINCIPAL_USDT", 10000.0))
FIRST_TRADE_INVEST_PCT = 0.7  # 70% of principal for first trade
WITHDRAW_PCT_AFTER_CLOSURE = 0.2  # 20% of total after each closure moved to principal
STOP_LOSS_PCT = float(os.getenv("SP_STOP_LOSS_PCT", 0.02))  # 2% default stop-loss
TAKE_PROFIT_PCT = float(os.getenv("SP_TAKE_PROFIT_PCT", 0.05))  # 5% default take-profit

# Reporting
REPORT_DESKTOP_DIR = Path.home() / "Desktop"

# Email notifications (SMTP)
EMAIL_RECIPIENT = os.getenv('SP_EMAIL_RECIPIENT', 'Semmeni@yahoo.fr')
SMTP_HOST = os.getenv('SP_SMTP_HOST')  # e.g. smtp.mail.yahoo.com
SMTP_PORT = int(os.getenv('SP_SMTP_PORT', '587'))
SMTP_USER = os.getenv('SP_SMTP_USER')  # SMTP username (often the email)
SMTP_PASS = os.getenv('SP_SMTP_PASS')  # SMTP password or app password
SMTP_USE_TLS = os.getenv('SP_SMTP_USE_TLS', 'True').lower() in ('1', 'true', 'yes')

# Agent mode
SIMULATE_BY_DEFAULT = True  # default: simulate only, no testnet orders executed

# Safety
ALLOW_WITHDRAWALS = False  # Explicitly disabled for Testnet
ENFORCE_TESTNET = True

# Logging
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
