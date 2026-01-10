import json, traceback, os
from pathlib import Path

out_path_temp = Path('C:/Temp')
out_path_temp.mkdir(parents=True, exist_ok=True)
repo_root = Path(__file__).resolve().parents[1]
repo_logs = repo_root / 'logs'
repo_logs.mkdir(parents=True, exist_ok=True)

try:
    from crypto_agent.runner import run_cycle
    res = run_cycle(simulate=True, do_report=True)

    # Write to repo logs
    with open(repo_logs / 'one_shot_debug.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, default=str, indent=2)
    with open(repo_logs / 'one_shot_debug_summary.txt', 'w', encoding='utf-8') as f:
        f.write('Report: ' + str(res.get('report')) + '\n')

    # Also write to C:\Temp for visibility
    with open(out_path_temp / 'one_shot_debug.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, default=str, indent=2)
    with open(out_path_temp / 'one_shot_debug_summary.txt', 'w', encoding='utf-8') as f:
        f.write('Report: ' + str(res.get('report')) + '\n')

    print('OK-WROTE')
except Exception as e:
    err = traceback.format_exc()
    with open(out_path_temp / 'one_shot_debug_error.txt', 'w', encoding='utf-8') as f:
        f.write(err)
    with open(repo_logs / 'one_shot_debug_error.txt', 'w', encoding='utf-8') as f:
        f.write(err)
    print('ERROR-WROTE')