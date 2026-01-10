"""
Binance Testnet trader: place signed orders on spot Testnet
This helper implements minimal signed REST calls for placing market buys and OCO sell orders.
"""
import time
import hmac
import hashlib
import requests
from typing import Dict, Optional
from urllib.parse import urlencode
from . import config

BASE = config.BINANCE_TESTNET_BASE

class BinanceTestnetTrader:
    def __init__(self, api_key: str = None, api_secret: str = None, base_url: str = BASE):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or config.BINANCE_API_KEY
        self.api_secret = api_secret or config.BINANCE_API_SECRET
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: Dict) -> str:
        qs = urlencode(params, doseq=True)
        return hmac.new(self.api_secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256).hexdigest()

    def _send_signed(self, method: str, path: str, params: Dict) -> Dict:
        params = dict(params)
        params['timestamp'] = int(time.time() * 1000)
        qs = urlencode(params, doseq=True)
        signature = hmac.new(self.api_secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        url = f"{self.base_url}{path}"
        if method.upper() == 'POST':
            resp = self.session.post(url, params=params, timeout=30)
        else:
            resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def place_market_buy(self, symbol: str, quoteOrderQty: float) -> Dict:
        """Place a market buy using quoteOrderQty in USDT space. Returns order result."""
        path = '/api/v3/order'
        params = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'MARKET',
            'quoteOrderQty': str(round(quoteOrderQty, 6)),
            'recvWindow': 5000
        }
        return self._send_signed('POST', path, params)

    def place_market_sell(self, symbol: str, quantity: float) -> Dict:
        path = '/api/v3/order'
        params = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': str(quantity),
            'recvWindow': 5000
        }
        return self._send_signed('POST', path, params)

    def create_oco_sell(self, symbol: str, quantity: float, price: float, stopPrice: float, stopLimitPrice: Optional[float] = None) -> Dict:
        """Create OCO sell order (take-profit limit + stop-loss limit)
        Note: stopLimitPrice defaults to stopPrice * 0.995 if not provided.
        """
        path = '/api/v3/order/oco'
        if stopLimitPrice is None:
            stopLimitPrice = stopPrice * 0.995
        params = {
            'symbol': symbol,
            'side': 'SELL',
            'quantity': str(quantity),
            'price': str(round(price, 8)),
            'stopPrice': str(round(stopPrice, 8)),
            'stopLimitPrice': str(round(stopLimitPrice, 8)),
            'stopLimitTimeInForce': 'GTC',
            'recvWindow': 5000
        }
        return self._send_signed('POST', path, params)

    def get_account(self) -> Dict:
        path = '/api/v3/account'
        return self._send_signed('GET', path, {})

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict:
        path = '/api/v3/openOrders'
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._send_signed('GET', path, params)

    def get_all_orders(self, symbol: str, limit: int = 50) -> Dict:
        path = '/api/v3/allOrders'
        params = {'symbol': symbol, 'limit': limit}
        return self._send_signed('GET', path, params)

if __name__ == '__main__':
    t = BinanceTestnetTrader()
    acc = t.get_account()
    print('Account keys present. Balances sample:', acc.get('balances', [])[:5])
