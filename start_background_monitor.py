"""
Start monitor_summary.py as a detached background process and write a PID file.
"""
import subprocess
import sys
from crypto_agent import config

PID_PATH = config.LOG_DIR / 'summary_monitor.pid'

if __name__ == '__main__':
    cmd = [sys.executable, 'monitor_summary.py']
    DETACHED_PROCESS = 0x00000008
    try:
        proc = subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
        with open(PID_PATH, 'w') as f:
            f.write(str(proc.pid))
        print(f"Started monitor with PID {proc.pid}")
    except Exception as e:
        print(f"Failed to start monitor: {e}")
