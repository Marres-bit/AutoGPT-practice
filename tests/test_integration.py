import os
import sys
# Ensure repo root is on sys.path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto_agent.capital import CapitalManager
from crypto_agent.analyzer import compute_top_gainers_losers
from crypto_agent.report import generate_docx_report
from crypto_agent.engine import TradingEngine
from pathlib import Path


def test_capital_first_trade():
    cm = CapitalManager(10000)
    amt = cm.allocate_first_trade()
    assert abs(amt - 7000) < 1e-6
    cm.on_first_trade_closed(500)
    snap = cm.snapshot()
    assert snap.principal > 0
    assert snap.investment_balance >= 500


def test_analyzer_basic():
    sample = [
        {'symbol': 'AAAUSDT', 'priceChangePercent': '10', 'lastPrice': '1', 'volume': '20000', 'highPrice': '1.2', 'lowPrice': '0.8'},
        {'symbol': 'BBBUSDT', 'priceChangePercent': '-5', 'lastPrice': '2', 'volume': '15000', 'highPrice': '2.3', 'lowPrice': '1.9'},
    ]
    res = compute_top_gainers_losers(sample, top_n=1)
    assert res['top_gainers'][0]['symbol'] == 'AAAUSDT'
    assert res['top_losers'][0]['symbol'] == 'BBBUSDT'


class DummyClient:
    def fetch_24h_tickers(self):
        return [{'symbol':'BTCUSDT','priceChangePercent':'6','lastPrice':'50000','volume':'5000','highPrice':'50500','lowPrice':'48000'}]
    def get_price(self, symbol):
        return 50000.0


def test_engine_simulation_and_capital():
    client = DummyClient()
    cm = CapitalManager(10000)
    engine = TradingEngine(client, cm, simulate=True)
    ticks = client.fetch_24h_tickers()
    from crypto_agent.analyzer import build_market_summary
    ms = build_market_summary(ticks)
    decision = engine.evaluate_and_trade(ms)
    assert decision is not None
    pos = decision['position']
    assert pos['symbol'] == 'BTCUSDT'
    closed = engine.simulate_close_for_take_profit(pos)
    # after first trade closed, capital should be adjusted
    snap = cm.snapshot()
    assert snap.principal > 0


def test_report_generation(tmp_path):
    market_summary = {'context':'bullish','top_gainers':[{'symbol':'BTCUSDT','change_pct':6,'volume':5000,'reason':'high volume'}],'top_losers':[],'universe_size':1}
    report_path = tmp_path / 'test_report.docx'
    filename = generate_docx_report(report_path, market_summary, {'action':'open_simulated','candidate':{'symbol':'BTCUSDT'}}, [], {'principal':10000,'investment_balance':0,'cumulative_profits':0})
    assert filename.exists()


if __name__ == '__main__':
    test_capital_first_trade()
    test_analyzer_basic()
    test_engine_simulation_and_capital()
    import tempfile
    test_report_generation(Path(tempfile.gettempdir()))
    print('All tests passed')
