"""
Market analysis helpers: compute top gainers/losers, volume, volatility, momentum
"""
from typing import List, Dict, Tuple
import math

def compute_top_gainers_losers(tickers: List[Dict], top_n: int = 10) -> Dict:
    """Compute top gainers and losers by percent change (priceChangePercent)"""
    # Filter USDT pairs for more meaningful comparison
    usdt = [t for t in tickers if t.get('symbol', '').endswith('USDT')]

    # Convert to floats and compute safe metrics
    processed = []
    for t in usdt:
        try:
            change_pct = float(t.get('priceChangePercent', 0.0))
            price = float(t.get('lastPrice', t.get('close', 0.0)))
            vol = float(t.get('volume', 0.0))
            processed.append({
                'symbol': t['symbol'],
                'change_pct': change_pct,
                'last_price': price,
                'volume': vol,
                'raw': t
            })
        except Exception:
            continue

    sorted_gainers = sorted(processed, key=lambda x: x['change_pct'], reverse=True)[:top_n]
    sorted_losers = sorted(processed, key=lambda x: x['change_pct'])[:top_n]

    return {
        'top_gainers': sorted_gainers,
        'top_losers': sorted_losers,
        'universe_size': len(processed)
    }


def estimate_volatility(ticker: Dict) -> float:
    """Simple volatility estimator using high/low if available, otherwise fallback"""
    try:
        high = float(ticker.get('highPrice', 0.0))
        low = float(ticker.get('lowPrice', 0.0))
        if low > 0:
            return (high - low) / low
    except Exception:
        pass
    try:
        # Fallback: use priceChangePercent as proxy
        return abs(float(ticker.get('priceChangePercent', 0.0))) / 100.0
    except Exception:
        return 0.0


def build_market_summary(tickers: List[Dict], top_n: int = 10) -> Dict:
    """Return structured market summary including gainers/losers and notable signals"""
    extremes = compute_top_gainers_losers(tickers, top_n=top_n)

    # Add simple reasons for moves (volume spikes)
    for item in extremes['top_gainers']:
        vol = item['volume']
        item['volatility'] = estimate_volatility(item['raw'])
        item['reason'] = 'high volume' if vol > 10000 else 'normal volume'

    for item in extremes['top_losers']:
        vol = item['volume']
        item['volatility'] = estimate_volatility(item['raw'])
        item['reason'] = 'high volume' if vol > 10000 else 'normal volume'

    # Context: naive market trend estimate
    avg_change = sum(float(t.get('priceChangePercent', 0.0)) for t in tickers) / max(len(tickers),1)
    if avg_change > 0.3:
        context = 'bullish'
    elif avg_change < -0.3:
        context = 'bearish'
    else:
        context = 'sideways'

    return {
        'top_gainers': extremes['top_gainers'],
        'top_losers': extremes['top_losers'],
        'context': context,
        'universe_size': extremes['universe_size']
    }
