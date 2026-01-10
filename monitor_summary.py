"""
Monitor `logs/last_cycle_summary.txt` and print its contents when updated.
Also save a copy with timestamp to `logs/last_summary_displayed.txt` for audit.
This script runs indefinitely until killed.
"""
import time
from pathlib import Path
from datetime import datetime
from crypto_agent import config

SUMMARY_PATH = config.LOG_DIR / 'last_cycle_summary.txt'
DISPLAY_PATH = config.LOG_DIR / 'last_summary_displayed.txt'
CHECK_INTERVAL = 10  # seconds


def tail_and_display():
    last_mtime = None
    print("Monitor started: watching", SUMMARY_PATH)
    while True:
        try:
            if SUMMARY_PATH.exists():
                mtime = SUMMARY_PATH.stat().st_mtime
                if last_mtime is None or mtime > last_mtime:
                    last_mtime = mtime
                    content = SUMMARY_PATH.read_text(encoding='utf-8')
                    header = f"\n=== New cycle summary detected at {datetime.utcnow().isoformat()} UTC ===\n"
                    out = header + content + "\n"
                    print(out)
                    # append to displayed log
                    with open(DISPLAY_PATH, 'a', encoding='utf-8') as f:
                        f.write(header)
                        f.write(content)
                        f.write('\n')
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print('Monitor stopped by user')
            break
        except Exception as e:
            print('Monitor error:', e)
            time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    tail_and_display()
