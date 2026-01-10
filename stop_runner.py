"""
Stop background SP agent runner using stored PID file
"""
import os
import signal
from pathlib import Path
from crypto_agent import config

PID_PATH = config.LOG_DIR / 'sp_agent.pid'

if __name__ == '__main__':
    if not PID_PATH.exists():
        print('No PID file found')
        raise SystemExit(1)
    pid = int(PID_PATH.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f'Sent SIGTERM to PID {pid}')
        PID_PATH.unlink(missing_ok=True)
    except Exception as e:
        print(f'Error stopping process: {e}')
        raise SystemExit(1)
