"""
Launcher: starts the 2-day Testnet execution loop (Testnet orders will be placed)
This script requires explicit user consent (you already provided it).
"""
from crypto_agent.runner import start_loop

if __name__ == '__main__':
    # Start 2 days, hourly interval, simulate=False to execute Testnet orders
    start_loop(days=2, interval_sec=3600, simulate=False)
