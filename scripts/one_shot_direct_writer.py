"""Run a simulated one-shot cycle and write machine-readable outputs directly to disk.
This avoids relying on stdout which appears unstable in the current terminal.
"""
import json
from crypto_agent.runner import run_cycle

out = run_cycle(simulate=True, do_report=True)

res = {
    'report': out.get('report'),
    'market_summary_top_gainers': out['market_summary'].get('top_gainers', [])[:10],
    'market_summary_top_losers': out['market_summary'].get('top_losers', [])[:10],
    'decision': out.get('decision'),
    'trades': out.get('trades'),
    'capital': out.get('capital')
}

from pathlib import Path
base_dir = Path(__file__).resolve().parents[1]
logs_dir = base_dir / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)

p_json = logs_dir / 'one_shot_direct.json'
with open(p_json, 'w', encoding='utf-8') as f:
    json.dump(res, f, default=str, indent=2)

# concise summary
lines = []
lines.append(f"Report: {res.get('report')}")
lines.append('Top Gainers:')
for g in res['market_summary_top_gainers']:
    lines.append(f" - {g.get('symbol')}: {g.get('change_pct')}% vol={g.get('volume')}")
lines.append('Top Losers:')
for g in res['market_summary_top_losers']:
    lines.append(f" - {g.get('symbol')}: {g.get('change_pct')}% vol={g.get('volume')}")
lines.append('Decision: ' + (str(res.get('decision')) if res.get('decision') else 'none'))
cap = res.get('capital') or {}
lines.append(f"Capital - Principal: {cap.get('principal',0):.2f} USDT | Investment: {cap.get('investment_balance',0):.2f} USDT | Cumulative Profits: {cap.get('cumulative_profits',0):.2f} USDT")

p_summary = logs_dir / 'one_shot_direct_summary.txt'
with open(p_summary, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'WROTE {p_json} and {p_summary}')