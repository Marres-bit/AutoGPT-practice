"""
Multi-Timeframe Analyzer - Analyse de marché sur plusieurs périodes
Combine signaux 15m, 1h, 4h pour confirmation et confluence
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class Timeframe(Enum):
    """Timeframes supportés"""
    M15 = "15m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


class TrendDirection(Enum):
    """Direction de tendance"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class TimeframeSignal:
    """Signal sur un timeframe spécifique"""
    timeframe: Timeframe
    trend: TrendDirection
    strength: float  # 0-1
    price_change_pct: float
    volume_change_pct: float
    momentum_score: float  # -1 à +1
    timestamp: datetime


@dataclass
class ConfluenceSignal:
    """Signal de confluence multi-timeframe"""
    asset: str
    overall_trend: TrendDirection
    confidence: float  # 0-1
    signals: List[TimeframeSignal]
    recommendation: str  # "STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"
    score: float  # Score global pondéré
    timestamp: datetime


class MultiTimeframeAnalyzer:
    """
    Analyse le marché sur plusieurs timeframes pour confluence de signaux
    """
    
    def __init__(self, project_root: Path):
        """
        Args:
            project_root: Dossier racine du projet
        """
        self.project_root = Path(project_root)
        self.cache_dir = self.project_root / "mtf_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Pondération par timeframe (plus long = plus important)
        self.timeframe_weights = {
            Timeframe.M15: 0.15,
            Timeframe.H1: 0.30,
            Timeframe.H4: 0.40,
            Timeframe.D1: 0.15
        }
        
    def fetch_multi_timeframe_data(
        self, 
        symbols: List[str],
        timeframes: List[Timeframe] = None
    ) -> Dict[str, Dict[Timeframe, List[Dict]]]:
        """
        Récupère les données sur plusieurs timeframes
        
        Args:
            symbols: Liste des symboles
            timeframes: Liste des timeframes (défaut: 15m, 1h, 4h)
            
        Returns:
            {symbol: {timeframe: [candles]}}
        """
        if timeframes is None:
            timeframes = [Timeframe.M15, Timeframe.H1, Timeframe.H4]
        
        try:
            from exchange_connector import get_exchange_connector
            exchange = get_exchange_connector(testnet=True)
            
            multi_data = {}
            
            print(f"[MTF] Récupération {len(timeframes)} timeframes pour {len(symbols)} assets...")
            
            for symbol in symbols:
                multi_data[symbol] = {}
                
                for tf in timeframes:
                    try:
                        # Nombre de candles selon timeframe
                        limit_map = {
                            Timeframe.M15: 100,  # ~25h
                            Timeframe.H1: 48,    # 2 jours
                            Timeframe.H4: 24,    # 4 jours
                            Timeframe.D1: 14     # 2 semaines
                        }
                        limit = limit_map.get(tf, 50)
                        
                        ohlcv = exchange.exchange.fetch_ohlcv(
                            symbol, 
                            timeframe=tf.value, 
                            limit=limit
                        )
                        
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
                        
                        multi_data[symbol][tf] = candles
                        
                    except Exception as e:
                        print(f"[ERREUR] {symbol} {tf.value}: {e}")
                
                if multi_data[symbol]:
                    print(f"[OK] {symbol}: {len(multi_data[symbol])} timeframes")
            
            return multi_data
            
        except Exception as e:
            print(f"[ERREUR] fetch_multi_timeframe_data: {e}")
            return {}
    
    def analyze_timeframe(
        self, 
        candles: List[Dict], 
        timeframe: Timeframe
    ) -> TimeframeSignal:
        """
        Analyse un timeframe spécifique
        
        Args:
            candles: Liste des candles OHLCV
            timeframe: Timeframe analysé
            
        Returns:
            Signal pour ce timeframe
        """
        if len(candles) < 3:
            return TimeframeSignal(
                timeframe=timeframe,
                trend=TrendDirection.NEUTRAL,
                strength=0.0,
                price_change_pct=0.0,
                volume_change_pct=0.0,
                momentum_score=0.0,
                timestamp=datetime.utcnow()
            )
        
        latest = candles[-1]
        prev = candles[-2]
        oldest = candles[0]
        
        # 1. Calcul de la tendance
        price_change = (latest['close'] - oldest['close']) / oldest['close'] * 100
        recent_change = (latest['close'] - prev['close']) / prev['close'] * 100
        
        # Déterminer tendance
        if price_change > 2.0:
            trend = TrendDirection.BULLISH
            strength = min(price_change / 10, 1.0)
        elif price_change < -2.0:
            trend = TrendDirection.BEARISH
            strength = min(abs(price_change) / 10, 1.0)
        else:
            trend = TrendDirection.NEUTRAL
            strength = abs(price_change) / 2.0
        
        # 2. Volume change
        avg_volume = sum(c['volume'] for c in candles[:-1]) / (len(candles) - 1)
        volume_change = (latest['volume'] - avg_volume) / avg_volume * 100 if avg_volume > 0 else 0
        
        # 3. Momentum (simple RSI-like)
        gains = []
        losses = []
        for i in range(1, len(candles)):
            change = candles[i]['close'] - candles[i-1]['close']
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 0
        
        if avg_gain + avg_loss > 0:
            momentum = (avg_gain - avg_loss) / (avg_gain + avg_loss)
        else:
            momentum = 0
        
        return TimeframeSignal(
            timeframe=timeframe,
            trend=trend,
            strength=strength,
            price_change_pct=price_change,
            volume_change_pct=volume_change,
            momentum_score=momentum,
            timestamp=latest['timestamp']
        )
    
    def calculate_confluence(
        self, 
        asset: str,
        signals: List[TimeframeSignal]
    ) -> ConfluenceSignal:
        """
        Calcule la confluence entre plusieurs timeframes
        
        Args:
            asset: Nom de l'asset
            signals: Liste des signaux par timeframe
            
        Returns:
            Signal de confluence global
        """
        if not signals:
            return ConfluenceSignal(
                asset=asset,
                overall_trend=TrendDirection.NEUTRAL,
                confidence=0.0,
                signals=[],
                recommendation="HOLD",
                score=0.0,
                timestamp=datetime.utcnow()
            )
        
        # Calcul score pondéré
        weighted_score = 0.0
        total_weight = 0.0
        
        bullish_count = 0
        bearish_count = 0
        
        for signal in signals:
            weight = self.timeframe_weights.get(signal.timeframe, 0.25)
            
            # Score basé sur tendance et force
            if signal.trend == TrendDirection.BULLISH:
                score_contribution = signal.strength * weight
                bullish_count += 1
            elif signal.trend == TrendDirection.BEARISH:
                score_contribution = -signal.strength * weight
                bearish_count += 1
            else:
                score_contribution = 0
            
            weighted_score += score_contribution
            total_weight += weight
        
        # Normaliser score (-1 à +1)
        final_score = weighted_score / total_weight if total_weight > 0 else 0
        
        # Déterminer tendance globale
        if bullish_count > bearish_count and final_score > 0.3:
            overall_trend = TrendDirection.BULLISH
        elif bearish_count > bullish_count and final_score < -0.3:
            overall_trend = TrendDirection.BEARISH
        else:
            overall_trend = TrendDirection.NEUTRAL
        
        # Confidence basée sur consensus
        total_signals = len(signals)
        consensus = max(bullish_count, bearish_count) / total_signals
        confidence = consensus * abs(final_score)
        
        # Recommandation
        if final_score >= 0.7 and confidence > 0.6:
            recommendation = "STRONG_BUY"
        elif final_score >= 0.4 and confidence > 0.5:
            recommendation = "BUY"
        elif final_score <= -0.7 and confidence > 0.6:
            recommendation = "STRONG_SELL"
        elif final_score <= -0.4 and confidence > 0.5:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
        
        return ConfluenceSignal(
            asset=asset,
            overall_trend=overall_trend,
            confidence=confidence,
            signals=signals,
            recommendation=recommendation,
            score=final_score,
            timestamp=datetime.utcnow()
        )
    
    def analyze_assets(
        self,
        symbols: List[str],
        timeframes: List[Timeframe] = None
    ) -> List[ConfluenceSignal]:
        """
        Analyse complète de plusieurs assets sur multi-timeframes
        
        Args:
            symbols: Liste des symboles
            timeframes: Timeframes à analyser
            
        Returns:
            Liste des signaux de confluence par asset
        """
        if timeframes is None:
            timeframes = [Timeframe.M15, Timeframe.H1, Timeframe.H4]
        
        # Récupérer données
        multi_data = self.fetch_multi_timeframe_data(symbols, timeframes)
        
        confluence_signals = []
        
        print(f"\n[MTF] Analyse confluence pour {len(symbols)} assets...")
        
        for symbol in symbols:
            if symbol not in multi_data or not multi_data[symbol]:
                continue
            
            # Analyser chaque timeframe
            tf_signals = []
            for tf, candles in multi_data[symbol].items():
                if candles:
                    signal = self.analyze_timeframe(candles, tf)
                    tf_signals.append(signal)
            
            # Calculer confluence
            if tf_signals:
                asset_name = symbol.replace("/USDT", "")
                confluence = self.calculate_confluence(asset_name, tf_signals)
                confluence_signals.append(confluence)
                
                print(f"[{asset_name}] {confluence.recommendation} "
                      f"(Score: {confluence.score:+.2f}, Confidence: {confluence.confidence:.1%})")
                for sig in tf_signals:
                    print(f"  └─ {sig.timeframe.value}: {sig.trend.value} "
                          f"({sig.price_change_pct:+.1f}%, momentum: {sig.momentum_score:+.2f})")
        
        return confluence_signals
    
    def get_best_opportunity(
        self,
        confluence_signals: List[ConfluenceSignal],
        min_confidence: float = 0.5
    ) -> Optional[ConfluenceSignal]:
        """
        Trouve la meilleure opportunité de trading
        
        Args:
            confluence_signals: Liste des signaux de confluence
            min_confidence: Confidence minimale requise
            
        Returns:
            Meilleur signal ou None
        """
        # Filtrer par confidence
        valid_signals = [
            s for s in confluence_signals 
            if s.confidence >= min_confidence and s.recommendation in ["BUY", "STRONG_BUY"]
        ]
        
        if not valid_signals:
            return None
        
        # Trier par score
        best_signal = max(valid_signals, key=lambda s: s.score * s.confidence)
        
        print(f"\n[MTF] Meilleure opportunité: {best_signal.asset} "
              f"({best_signal.recommendation}, score: {best_signal.score:+.2f})")
        
        return best_signal
    
    def export_analysis(self, confluence_signals: List[ConfluenceSignal], filename: str = "mtf_analysis.json"):
        """Exporte l'analyse multi-timeframe"""
        output = []
        for signal in confluence_signals:
            output.append({
                'asset': signal.asset,
                'trend': signal.overall_trend.value,
                'confidence': signal.confidence,
                'recommendation': signal.recommendation,
                'score': signal.score,
                'timestamp': signal.timestamp.isoformat(),
                'timeframes': [
                    {
                        'tf': tf_sig.timeframe.value,
                        'trend': tf_sig.trend.value,
                        'price_change': tf_sig.price_change_pct,
                        'momentum': tf_sig.momentum_score
                    }
                    for tf_sig in signal.signals
                ]
            })
        
        output_file = self.cache_dir / filename
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"[OK] Analyse exportée: {output_file}")


if __name__ == "__main__":
    # Test du multi-timeframe analyzer
    print("=== TEST MULTI-TIMEFRAME ANALYZER ===\n")
    
    analyzer = MultiTimeframeAnalyzer(Path('.'))
    
    symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"]
    timeframes = [Timeframe.M15, Timeframe.H1, Timeframe.H4]
    
    # Analyse
    confluence_signals = analyzer.analyze_assets(symbols, timeframes)
    
    # Meilleure opportunité
    best_opp = analyzer.get_best_opportunity(confluence_signals, min_confidence=0.5)
    
    # Export
    if confluence_signals:
        analyzer.export_analysis(confluence_signals)
