"""
Trading engine: decision logic, simulation and optional Testnet execution (requires explicit consent)
"""
from typing import Optional, Dict
from .binance_client import BinanceTestnetClient
from .capital import CapitalManager
from . import config
import time
import math

class TradingEngine:
    def __init__(self, client: BinanceTestnetClient, capital: CapitalManager, simulate: bool = True, trader=None):
        self.client = client
        self.capital = capital
        self.simulate = simulate
        self.open_positions = []  # store open positions (simulated or real)
        
        # If running real Testnet execution, create trader instance
        self.trader = trader
        if not self.simulate and self.trader is None:
            from .trader import BinanceTestnetTrader
            self.trader = BinanceTestnetTrader(api_key=config.BINANCE_API_KEY, api_secret=config.BINANCE_API_SECRET)

    def _choose_candidate(self, market_summary: Dict) -> Optional[Dict]:
        # Simple strategy: pick top gainer with reasonable volume
        candidates = market_summary.get('top_gainers', [])
        for c in candidates:
            if c['volume'] > 1000 and c['change_pct'] > 4.0:
                return c
        # fallback to top gainer
        return candidates[0] if candidates else None

    def simulate_open_position(self, symbol: str, usd_amount: float, stop_loss_pct: float, take_profit_pct: float) -> Dict:
        price = self.client.get_price(symbol)
        if price is None:
            raise RuntimeError(f"Cannot get price for {symbol}")
        quantity = usd_amount / price
        entry = {
            'symbol': symbol,
            'entry_price': price,
            'quantity': quantity,
            'usd_allocated': usd_amount,
            'stop_loss': price * (1 - stop_loss_pct),
            'take_profit': price * (1 + take_profit_pct),
            'open_ts': time.time(),
            'status': 'open',
            'source': 'simulated'
        }
        self.open_positions.append(entry)
        return entry

    def place_testnet_open(self, symbol: str, usd_amount: float, stop_loss_pct: float, take_profit_pct: float) -> Dict:
        """Place a real market buy on Binance Testnet and setup OCO sell for TP/SL"""
        # place market buy with quoteOrderQty
        order = self.trader.place_market_buy(symbol, quoteOrderQty=usd_amount)
        # Determine executed quantity and average price
        executed_qty = float(order.get('executedQty', 0) or 0)
        # If executedQty missing try to compute from fills
        if executed_qty == 0 and 'fills' in order and order['fills']:
            executed_qty = sum(float(f.get('qty', 0)) for f in order['fills'])
        # Try to get average price (cummulativeQuoteQty / executedQty)
        avg_price = 0.0
        if executed_qty > 0:
            cumsum = float(order.get('cummulativeQuoteQty', 0) or sum(float(f.get('commission',0)) for f in order.get('fills', [])))
            # fallback: take lastPrice
            avg_price = self.client.get_price(symbol) or 0.0
        else:
            avg_price = self.client.get_price(symbol) or 0.0
        # compute TP/SL prices
        take_profit_price = avg_price * (1 + take_profit_pct)
        stop_price = avg_price * (1 - stop_loss_pct)

        # create OCO sell to manage TP/SL (quantity = executed_qty)
        oco = None
        if executed_qty > 0:
            try:
                oco = self.trader.create_oco_sell(symbol, executed_qty, price=take_profit_price, stopPrice=stop_price)
            except Exception as e:
                oco = {'error': str(e)}

        position = {
            'symbol': symbol,
            'entry_price': avg_price,
            'quantity': executed_qty,
            'usd_allocated': usd_amount,
            'stop_loss': stop_price,
            'take_profit': take_profit_price,
            'open_ts': time.time(),
            'status': 'open',
            'source': 'testnet',
            'market_order': order,
            'oco_order': oco
        }
        self.open_positions.append(position)
        return position

    def close_position_simulated(self, pos: Dict, exit_price: float) -> Dict:
        # compute P&L in USD
        pnl = (exit_price - pos['entry_price']) * pos['quantity']
        pos['status'] = 'closed'
        pos['exit_price'] = exit_price
        pos['pnl'] = pnl
        pos['close_ts'] = time.time()
        return pos

    def evaluate_and_trade(self, market_summary: Dict) -> Optional[Dict]:
        # Decide whether to open a trade
        candidate = self._choose_candidate(market_summary)
        if not candidate:
            return None

        symbol = candidate['symbol']
        if not self.capital.first_trade_done:
            amount = self.capital.allocate_first_trade()
        else:
            # allocate entire current investment balance for a trade (could be adjusted)
            amount = self.capital.allocate_trade_from_investment(pct=1.0)

        # enforce stop-loss/take-profit
        sl = config.STOP_LOSS_PCT
        tp = config.TAKE_PROFIT_PCT

        if self.simulate:
            pos = self.simulate_open_position(symbol, amount, stop_loss_pct=sl, take_profit_pct=tp)
            return {
                'action': 'open_simulated',
                'position': pos,
                'candidate': candidate
            }
        else:
            # Place actual Testnet market buy and setup OCO
            pos = self.place_testnet_open(symbol, amount, stop_loss_pct=sl, take_profit_pct=tp)
            return {
                'action': 'open_testnet',
                'position': pos,
                'candidate': candidate
            }

    def simulate_close_for_take_profit(self, pos: Dict) -> Dict:
        # simple simulation: assume TP is hit
        exit = pos['take_profit']
        closed = self.close_position_simulated(pos, exit)
        # update capital according to whether it was the first trade
        pnl = closed['pnl']
        if not self.capital.first_trade_done:
            self.capital.on_first_trade_closed(pnl)
        else:
            self.capital.on_trade_closed(pnl)
        # Persist open positions after closure (remove closed)
        try:
            self.save_open_positions(self._positions_path)
        except Exception:
            pass
        return closed

    def save_open_positions(self, path):
        """Persist open positions to JSON"""
        import json
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.open_positions, f, default=str, indent=2)

    def load_open_positions(self, path):
        """Load open positions from JSON if exists"""
        import json
        from pathlib import Path
        if not Path(path).exists():
            self.open_positions = []
            return self.open_positions
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.open_positions = data
        return self.open_positions

    def poll_and_update_positions(self, path):
        """Poll Testnet orders to identify filled sales (OCO triggered) and update capital + positions"""
        if self.simulate:
            # nothing to poll in simulation
            return []
        closed = []
        # For each open testnet position, check all orders for the symbol
        for pos in list(self.open_positions):
            try:
                if pos.get('source') != 'testnet' or pos.get('status') != 'open':
                    continue
                symbol = pos['symbol']
                all_orders = self.trader.get_all_orders(symbol)
                # Find SELL orders filled after the open timestamp
                sells = [o for o in all_orders if o.get('side') == 'SELL' and o.get('status') == 'FILLED']
                # Find a sell post-dating the open
                found = None
                for s in sells:
                    t = s.get('time') or s.get('updateTime')
                    if t and t/1000.0 >= pos.get('open_ts', 0):
                        found = s
                        break
                if found:
                    # Determine exit price from fills or price field
                    exit_price = None
                    if found.get('price') and float(found.get('price')) > 0:
                        exit_price = float(found.get('price'))
                    elif 'fills' in found and found['fills']:
                        total_qty = sum(float(f.get('qty',0)) for f in found['fills'])
                        total_quote = sum(float(f.get('price',0)) * float(f.get('qty',0)) for f in found['fills'])
                        if total_qty > 0:
                            exit_price = total_quote / total_qty
                    if exit_price is None:
                        # fallback to current price
                        exit_price = self.client.get_price(symbol)
                    closed_pos = self.close_position_simulated(pos, exit_price)
                    pnl = closed_pos['pnl']
                    if not self.capital.first_trade_done:
                        self.capital.on_first_trade_closed(pnl)
                    else:
                        self.capital.on_trade_closed(pnl)
                    closed.append(closed_pos)
                    self.open_positions.remove(pos)
            except Exception:
                continue
        # persist positions
        try:
            self.save_open_positions(path)
        except Exception:
            pass
        return closed

    # helper to set path for positions
    def set_positions_path(self, path):
        self._positions_path = path
        # ensure file exists
        try:
            self.save_open_positions(path)
        except Exception:
            pass


if __name__ == '__main__':
    from .binance_client import BinanceTestnetClient
    client = BinanceTestnetClient()
    from .capital import CapitalManager
    cm = CapitalManager(10000)
    engine = TradingEngine(client, cm, simulate=True)
    # Example usage omitted
    print("Engine ready")
