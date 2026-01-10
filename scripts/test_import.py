import traceback
try:
    from crypto_agent.runner import run_cycle
    print('IMPORT_OK')
except Exception as e:
    print('ERROR', type(e).__name__, e)
    traceback.print_exc()