"""
Start the run_testnet_loop.py process in background (detached) and write a PID file
"""
import subprocess
import sys
from pathlib import Path
from crypto_agent import config

LOG_DIR = config.LOG_DIR
LOG_DIR.mkdir(parents=True, exist_ok=True)
PID_PATH = LOG_DIR / 'sp_agent.pid'

if __name__ == '__main__':
    cmd = [sys.executable, 'run_testnet_loop.py']
    # DETACHED_PROCESS flag for Windows
    DETACHED_PROCESS = 0x00000008
    try:
        proc = subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
        with open(PID_PATH, 'w') as f:
            f.write(str(proc.pid))
        print(f"Started background runner with PID {proc.pid}")
    except Exception as e:
        print(f"Failed to start background process: {e}")
