"""
Simple Binance Testnet client helpers (read-only market data)
Uses public REST endpoints of Binance Testnet to fetch 24h tickers and symbol prices.
"""
import requests
from typing import List, Dict, Optional
from . import config

BASE = config.BINANCE_TESTNET_BASE

class BinanceTestnetClient:
    def __init__(self, base_url: str = BASE, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        # For rate-limited endpoints we'd set headers; public endpoints don't need auth

    def fetch_24h_tickers(self) -> List[Dict]:
        """Return list of 24h ticker dicts from /api/v3/ticker/24hr"""
        url = f"{self.base_url}/api/v3/ticker/24hr"
        resp = self.session.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()

    def get_price(self, symbol: str) -> Optional[float]:
        """Return current price for given symbol (e.g., BTCUSDT)"""
        url = f"{self.base_url}/api/v3/ticker/price"
        params = {"symbol": symbol}
        resp = self.session.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return float(data['price'])

    def list_symbols(self) -> List[str]:
        """Return list of active trading symbols (USDT pairs prioritized)"""
        tickers = self.fetch_24h_tickers()
        return [t['symbol'] for t in tickers]


if __name__ == '__main__':
    c = BinanceTestnetClient()
    tickers = c.fetch_24h_tickers()
    print(f"Fetched {len(tickers)} tickers")
