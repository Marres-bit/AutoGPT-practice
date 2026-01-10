"""
Show status of background SP agent runner: PID and recent logs
"""
from pathlib import Path
from crypto_agent import config

LOG = config.LOG_DIR / 'sp_agent.log'
PID = config.LOG_DIR / 'sp_agent.pid'

if __name__ == '__main__':
    if PID.exists():
        print('PID:', PID.read_text())
    else:
        print('No PID file')
    if LOG.exists():
        print('\nLast 80 lines of log:')
        with open(LOG, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        for l in lines[-80:]:
            print(l)
    else:
        print('No log file yet')
