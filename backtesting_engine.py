"""
Backtesting Engine - Framework de test sur données historiques
Permet de valider les stratégies sur plusieurs années avant production
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class BacktestTrade:
    """Représentation d'un trade de backtest"""
    entry_time: datetime
    exit_time: datetime
    asset: str
    entry_price: float
    exit_price: float
    position_size: float
    pnl: float
    pnl_percent: float
    reason: str
    

@dataclass
class BacktestMetrics:
    """Métriques de performance d'un backtest"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    total_return_percent: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    max_drawdown_duration_days: int
    avg_trade_pnl: float
    avg_winning_trade: float
    avg_losing_trade: float
    profit_factor: float
    best_trade: float
    worst_trade: float
    final_capital: float
    

class BacktestingEngine:
    """
    Moteur de backtesting pour valider stratégies sur données historiques
    """
    
    def __init__(self, project_root: Path, initial_capital: float = 10000.0):
        """
        Args:
            project_root: Dossier racine du projet
            initial_capital: Capital initial pour le backtest
        """
        self.project_root = Path(project_root)
        self.backtest_dir = self.project_root / "backtest_data"
        self.backtest_dir.mkdir(exist_ok=True)
        self.initial_capital = initial_capital
        
        self.trades: List[BacktestTrade] = []
        self.equity_curve: List[Tuple[datetime, float]] = []
        
    def fetch_historical_data(
        self, 
        symbols: List[str], 
        timeframe: str = "1h",
        lookback_days: int = 180
    ) -> Dict[str, List[Dict]]:
        """
        Récupère les données historiques depuis Binance
        
        Args:
            symbols: Liste des symboles (ex: ["BTC/USDT", "ETH/USDT"])
            timeframe: Intervalle (1m, 5m, 15m, 1h, 4h, 1d)
            lookback_days: Nombre de jours d'historique
            
        Returns:
            Dict {symbol: [candles]} avec candles = {timestamp, open, high, low, close, volume}
        """
        try:
            from exchange_connector import get_exchange_connector
            exchange = get_exchange_connector(testnet=False)  # Utiliser production pour historique
            
            historical_data = {}
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=lookback_days)
            
            print(f"[BACKTEST] Récupération historique {lookback_days}j pour {len(symbols)} assets...")
            
            for symbol in symbols:
                try:
                    # Fetch OHLCV data
                    since = int(start_time.timestamp() * 1000)
                    ohlcv = exchange.exchange.fetch_ohlcv(symbol, timeframe, since=since)
                    
                    # Convertir en format lisible
                    candles = []
                    for candle in ohlcv:
                        candles.append({
                            'timestamp': datetime.fromtimestamp(candle[0] / 1000),
                            'open': candle[1],
                            'high': candle[2],
                            'low': candle[3],
                            'close': candle[4],
                            'volume': candle[5]
                        })
                    
                    historical_data[symbol] = candles
                    print(f"[OK] {symbol}: {len(candles)} candles")
                    
                except Exception as e:
                    print(f"[ERREUR] {symbol}: {e}")
                    
            # Sauvegarder localement
            cache_file = self.backtest_dir / f"historical_{timeframe}_{lookback_days}d.json"
            with open(cache_file, 'w') as f:
                # Convertir datetime en string pour JSON
                serializable_data = {}
                for symbol, candles in historical_data.items():
                    serializable_data[symbol] = [
                        {**c, 'timestamp': c['timestamp'].isoformat()} 
                        for c in candles
                    ]
                json.dump(serializable_data, f, indent=2)
                
            print(f"[OK] Données sauvegardées: {cache_file}")
            return historical_data
            
        except Exception as e:
            print(f"[ERREUR] fetch_historical_data: {e}")
            return {}
    
    def load_historical_data(self, timeframe: str = "1h", lookback_days: int = 180) -> Dict[str, List[Dict]]:
        """Charge les données historiques depuis le cache"""
        cache_file = self.backtest_dir / f"historical_{timeframe}_{lookback_days}d.json"
        
        if not cache_file.exists():
            print("[BACKTEST] Pas de cache trouvé, récupération depuis Binance...")
            symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"]
            return self.fetch_historical_data(symbols, timeframe, lookback_days)
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
            
        # Reconvertir timestamps
        for symbol in data:
            for candle in data[symbol]:
                candle['timestamp'] = datetime.fromisoformat(candle['timestamp'])
                
        print(f"[OK] Données chargées: {len(data)} assets, {len(data[list(data.keys())[0]])} candles")
        return data
    
    def run_backtest(
        self,
        strategy_func,
        historical_data: Dict[str, List[Dict]],
        risk_per_trade: float = 0.02,
        min_gain_threshold: float = 0.005
    ) -> BacktestMetrics:
        """
        Exécute un backtest complet
        
        Args:
            strategy_func: Fonction stratégie (data, capital) -> (asset, entry_price, position_size) ou None
            historical_data: Données historiques
            risk_per_trade: Risque par trade (2% par défaut)
            min_gain_threshold: Seuil minimal de gain pour trader (0.5%)
            
        Returns:
            Métriques de performance
        """
        capital = self.initial_capital
        self.trades = []
        self.equity_curve = [(historical_data[list(historical_data.keys())[0]][0]['timestamp'], capital)]
        
        # Obtenir toutes les timestamps communes
        all_timestamps = sorted(set(
            candle['timestamp'] 
            for symbol_data in historical_data.values() 
            for candle in symbol_data
        ))
        
        print(f"[BACKTEST] Simulation sur {len(all_timestamps)} périodes...")
        
        open_position = None
        
        for i, timestamp in enumerate(all_timestamps):
            # Construire état du marché à cette timestamp
            market_state = {}
            for symbol, candles in historical_data.items():
                # Trouver la candle la plus proche
                for candle in candles:
                    if candle['timestamp'] == timestamp:
                        market_state[symbol] = candle
                        break
            
            if len(market_state) < 2:  # Pas assez de données
                continue
            
            # Si position ouverte, vérifier clôture
            if open_position:
                asset, entry_time, entry_price, pos_size = open_position
                
                if asset in market_state:
                    current_price = market_state[asset]['close']
                    pnl_percent = (current_price - entry_price) / entry_price
                    
                    # Clôture si gain >0.5% ou perte >-2% ou après 24h
                    hours_open = (timestamp - entry_time).total_seconds() / 3600
                    
                    should_close = (
                        pnl_percent >= 0.005 or  # Take profit 0.5%
                        pnl_percent <= -0.02 or  # Stop loss -2%
                        hours_open >= 24         # Max holding 24h
                    )
                    
                    if should_close:
                        pnl = pos_size * pnl_percent
                        capital += pnl
                        
                        trade = BacktestTrade(
                            entry_time=entry_time,
                            exit_time=timestamp,
                            asset=asset,
                            entry_price=entry_price,
                            exit_price=current_price,
                            position_size=pos_size,
                            pnl=pnl,
                            pnl_percent=pnl_percent * 100,
                            reason="TP" if pnl_percent >= 0.005 else ("SL" if pnl_percent <= -0.02 else "Timeout")
                        )
                        self.trades.append(trade)
                        self.equity_curve.append((timestamp, capital))
                        
                        open_position = None
                        
            # Si pas de position, chercher entrée
            else:
                # Calculer % changes pour décision
                price_changes = {}
                for symbol, candle in market_state.items():
                    if i > 0:  # Comparer avec période précédente
                        prev_candles = [c for c in historical_data[symbol] if c['timestamp'] < timestamp]
                        if prev_candles:
                            prev_price = prev_candles[-1]['close']
                            change_pct = (candle['close'] - prev_price) / prev_price * 100
                            price_changes[symbol.replace("/USDT", "")] = change_pct
                
                if not price_changes:
                    continue
                
                # Appeler stratégie
                decision = strategy_func(price_changes, capital, min_gain_threshold)
                
                if decision:
                    asset_short = decision['asset']
                    asset_full = f"{asset_short}/USDT"
                    
                    if asset_full in market_state:
                        entry_price = market_state[asset_full]['close']
                        position_size = capital * risk_per_trade  # 2% du capital
                        
                        open_position = (asset_short, timestamp, entry_price, position_size)
        
        # Clôture position si encore ouverte
        if open_position:
            asset, entry_time, entry_price, pos_size = open_position
            asset_full = f"{asset}/USDT"
            if asset_full in historical_data and historical_data[asset_full]:
                last_price = historical_data[asset_full][-1]['close']
                pnl_percent = (last_price - entry_price) / entry_price
                pnl = pos_size * pnl_percent
                capital += pnl
                
                trade = BacktestTrade(
                    entry_time=entry_time,
                    exit_time=all_timestamps[-1],
                    asset=asset,
                    entry_price=entry_price,
                    exit_price=last_price,
                    position_size=pos_size,
                    pnl=pnl,
                    pnl_percent=pnl_percent * 100,
                    reason="End"
                )
                self.trades.append(trade)
                self.equity_curve.append((all_timestamps[-1], capital))
        
        # Calculer métriques
        metrics = self._calculate_metrics(capital)
        
        print(f"\n[BACKTEST] Résultats:")
        print(f"  Trades: {metrics.total_trades} (Win: {metrics.winning_trades}, Loss: {metrics.losing_trades})")
        print(f"  Win Rate: {metrics.win_rate:.1%}")
        print(f"  Total P&L: ${metrics.total_pnl:.2f} ({metrics.total_return_percent:.1f}%)")
        print(f"  Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        print(f"  Max Drawdown: {metrics.max_drawdown:.1%}")
        print(f"  Final Capital: ${metrics.final_capital:.2f}")
        
        return metrics
    
    def _calculate_metrics(self, final_capital: float) -> BacktestMetrics:
        """Calcule les métriques de performance"""
        if not self.trades:
            return BacktestMetrics(
                total_trades=0, winning_trades=0, losing_trades=0, win_rate=0.0,
                total_pnl=0.0, total_return_percent=0.0, sharpe_ratio=0.0, sortino_ratio=0.0,
                max_drawdown=0.0, max_drawdown_duration_days=0, avg_trade_pnl=0.0,
                avg_winning_trade=0.0, avg_losing_trade=0.0, profit_factor=0.0,
                best_trade=0.0, worst_trade=0.0, final_capital=final_capital
            )
        
        winning_trades = [t for t in self.trades if t.pnl > 0]
        losing_trades = [t for t in self.trades if t.pnl <= 0]
        
        total_pnl = sum(t.pnl for t in self.trades)
        returns = [t.pnl_percent / 100 for t in self.trades]
        
        # Sharpe Ratio
        avg_return = np.mean(returns) if returns else 0
        std_return = np.std(returns) if len(returns) > 1 else 0
        sharpe = (avg_return / std_return * np.sqrt(252)) if std_return > 0 else 0
        
        # Sortino Ratio (downside deviation)
        downside_returns = [r for r in returns if r < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 1 else 0
        sortino = (avg_return / downside_std * np.sqrt(252)) if downside_std > 0 else 0
        
        # Max Drawdown
        peak = self.initial_capital
        max_dd = 0
        for _, equity in self.equity_curve:
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak
            if dd > max_dd:
                max_dd = dd
        
        # Profit Factor
        gross_profit = sum(t.pnl for t in winning_trades)
        gross_loss = abs(sum(t.pnl for t in losing_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        return BacktestMetrics(
            total_trades=len(self.trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            win_rate=len(winning_trades) / len(self.trades) if self.trades else 0,
            total_pnl=total_pnl,
            total_return_percent=(final_capital - self.initial_capital) / self.initial_capital * 100,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            max_drawdown=max_dd,
            max_drawdown_duration_days=0,  # TODO: calculer durée
            avg_trade_pnl=total_pnl / len(self.trades) if self.trades else 0,
            avg_winning_trade=np.mean([t.pnl for t in winning_trades]) if winning_trades else 0,
            avg_losing_trade=np.mean([t.pnl for t in losing_trades]) if losing_trades else 0,
            profit_factor=profit_factor,
            best_trade=max([t.pnl for t in self.trades]) if self.trades else 0,
            worst_trade=min([t.pnl for t in self.trades]) if self.trades else 0,
            final_capital=final_capital
        )
    
    def export_results(self, filename: str = "backtest_results.json"):
        """Exporte les résultats du backtest"""
        results = {
            'trades': [asdict(t) for t in self.trades],
            'equity_curve': [(ts.isoformat(), eq) for ts, eq in self.equity_curve]
        }
        
        output_file = self.backtest_dir / filename
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"[OK] Résultats exportés: {output_file}")


def simple_strategy(market: Dict[str, float], capital: float, threshold: float = 0.5) -> Optional[Dict]:
    """
    Stratégie simple pour backtesting: trade l'asset avec le meilleur gain >threshold
    """
    if not market:
        return None
    
    best_asset = max(market.items(), key=lambda x: x[1])
    
    if best_asset[1] >= threshold:
        return {'asset': best_asset[0], 'reason': f'Best asset +{best_asset[1]:.2f}%'}
    
    return None


if __name__ == "__main__":
    # Test du backtesting engine
    print("=== TEST BACKTESTING ENGINE ===\n")
    
    engine = BacktestingEngine(Path('.'), initial_capital=10000)
    
    # Récupérer données historiques
    historical = engine.fetch_historical_data(
        symbols=["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"],
        timeframe="1h",
        lookback_days=30  # 1 mois pour test rapide
    )
    
    if historical:
        # Run backtest
        metrics = engine.run_backtest(
            strategy_func=simple_strategy,
            historical_data=historical,
            risk_per_trade=0.02,
            min_gain_threshold=0.005
        )
        
        # Export
        engine.export_results()
