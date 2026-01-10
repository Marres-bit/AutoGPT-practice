import json, traceback

try:
    from crypto_agent.runner import run_cycle
    r = run_cycle(simulate=True, do_report=True)

    print("REPORT_PATH::", r.get('report') or 'None')
    print('\n---TOP GAINERS---')
    for g in r['market_summary'].get('top_gainers', [])[:10]:
        print(f"{g.get('symbol')}: {g.get('change_pct')}% vol={g.get('volume')}")

    print('\n---TOP LOSERS---')
    for g in r['market_summary'].get('top_losers', [])[:10]:
        print(f"{g.get('symbol')}: {g.get('change_pct')}% vol={g.get('volume')}")

    print('\n---DECISION---')
    print(json.dumps(r.get('decision'), default=str, indent=2))

    print('\n---TRADES---')
    for t in r.get('trades', []):
        print(json.dumps(t, default=str))

    print('\n---CAPITAL---')
    print(json.dumps(r.get('capital'), indent=2))

    # Persist a machine-readable result and a concise summary in logs for robust retrieval
    out = {
        'report': r.get('report'),
        'top_gainers': r['market_summary'].get('top_gainers', [])[:10],
        'top_losers': r['market_summary'].get('top_losers', [])[:10],
        'decision': r.get('decision'),
        'trades': r.get('trades', []),
        'capital': r.get('capital')
    }
    import os
    os.makedirs('logs', exist_ok=True)
    with open('logs/one_shot_result.json', 'w', encoding='utf-8') as fout:
        json.dump(out, fout, default=str, indent=2)

    # Also write a concise textual summary
    lines = []
    lines.append(f"Report: {out.get('report')}")
    lines.append('Top Gainers:')
    for g in out['top_gainers']:
        lines.append(f" - {g.get('symbol')}: {g.get('change_pct')}% vol={g.get('volume')}")
    lines.append('Decision: ' + (str(out.get('decision')) if out.get('decision') else 'none'))
    cap = out.get('capital') or {}
    lines.append(f"Capital - Principal: {cap.get('principal',0):.2f} USDT | Investment: {cap.get('investment_balance',0):.2f} USDT | Cumulative Profits: {cap.get('cumulative_profits',0):.2f} USDT")
    with open('logs/one_shot_summary.txt', 'w', encoding='utf-8') as fsum:
        fsum.write('\n'.join(lines))

    print('\nWROTE logs/one_shot_result.json and logs/one_shot_summary.txt')

except Exception as e:
    print('ERROR:', type(e).__name__, e)
    traceback.print_exc()