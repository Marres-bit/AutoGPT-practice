"""
Strategy Analyzer - Module d'Analyse des Stratégies de Trading
Étudie et extrait les méthodes gagnantes de BullX, Photon, Glider et Binance
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class MarketCondition(Enum):
    """Types de conditions de marché"""
    BULL = "bull_market"
    BEAR = "bear_market"
    SIDEWAYS = "sideways_market"
    VOLATILE = "volatile_market"


class StrategyType(Enum):
    """Types de stratégies identifiées"""
    MOMENTUM = "momentum"
    BREAKOUT = "breakout"
    ARBITRAGE = "arbitrage"
    HEDGING = "hedging"
    MEAN_REVERSION = "mean_reversion"
    TREND_FOLLOWING = "trend_following"


@dataclass
class TechnicalIndicator:
    """Indicateur technique avec ses paramètres"""
    name: str
    parameters: Dict[str, Any]
    weight: float  # importance 0-1
    success_rate: float = 0.0
    
    
@dataclass
class TradingRule:
    """Règle de trading formalisée"""
    rule_id: str
    description: str
    condition: str
    action: str
    priority: int
    success_count: int = 0
    fail_count: int = 0
    enabled: bool = True
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.fail_count
        return self.success_count / total if total > 0 else 0.0


@dataclass
class StrategyPattern:
    """Pattern de stratégie extrait d'un bot"""
    pattern_id: str
    source: str  # BullX, Photon, Glider, Binance
    strategy_type: StrategyType
    indicators: List[TechnicalIndicator]
    rules: List[TradingRule]
    risk_parameters: Dict[str, float]
    market_conditions: List[MarketCondition]
    performance_metrics: Dict[str, float]
    last_updated: str
    

class StrategyAnalyzer:
    """
    Analyseur de stratégies de trading inspirées des meilleurs bots
    Identifie, formalise et stocke les méthodes gagnantes
    """
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.strategies_file = self.project_root / "trading_strategies.json"
        self.patterns_file = self.project_root / "strategy_patterns.json"
        self.performance_file = self.project_root / "strategy_performance.json"
        
        self.strategies = self._load_strategies()
        self.patterns = self._load_patterns()
        self.performance = self._load_performance()
        
        # Initialiser les stratégies de base
        self._initialize_base_strategies()
    
    def _load_strategies(self) -> Dict:
        """Charge les stratégies enregistrées"""
        if self.strategies_file.exists():
            try:
                with open(self.strategies_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _load_patterns(self) -> List[Dict]:
        """Charge les patterns identifiés"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _load_performance(self) -> Dict:
        """Charge les métriques de performance"""
        if self.performance_file.exists():
            try:
                with open(self.performance_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "by_strategy": {},
            "by_market_condition": {},
            "by_indicator": {},
            "overall": {"total_trades": 0, "winning_trades": 0}
        }
    
    def _save_strategies(self):
        """Sauvegarde les stratégies"""
        try:
            with open(self.strategies_file, "w", encoding="utf-8") as f:
                json.dump(self.strategies, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde stratégies: {e}")
    
    def _save_patterns(self):
        """Sauvegarde les patterns"""
        try:
            with open(self.patterns_file, "w", encoding="utf-8") as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde patterns: {e}")
    
    def _save_performance(self):
        """Sauvegarde les performances"""
        try:
            with open(self.performance_file, "w", encoding="utf-8") as f:
                json.dump(self.performance, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde performance: {e}")
    
    def _initialize_base_strategies(self):
        """Initialise les stratégies de base inspirées des meilleurs bots"""
        
        if not self.strategies:
            # ═══════════════════════════════════════════════════════
            # 1️⃣ STRATÉGIES BULLX - Momentum et Breakout
            # ═══════════════════════════════════════════════════════
            self.strategies["bullx_momentum"] = {
                "name": "BullX Momentum Strategy",
                "source": "BullX",
                "type": "momentum",
                "description": "Détection de momentum et cassures de résistances avec confirmation volume",
                "indicators": [
                    {
                        "name": "RSI",
                        "parameters": {"period": 14, "overbought": 70, "oversold": 30},
                        "weight": 0.3,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Volume_Confirmation",
                        "parameters": {"threshold_multiplier": 1.5, "lookback": 20},
                        "weight": 0.4,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Price_Breakout",
                        "parameters": {"resistance_period": 24, "confirmation_candles": 2},
                        "weight": 0.3,
                        "success_rate": 0.0
                    }
                ],
                "rules": [
                    {
                        "rule_id": "BX_M1",
                        "description": "Entrée sur breakout avec volume élevé",
                        "condition": "price > resistance AND volume > 1.5 * avg_volume",
                        "action": "OPEN_LONG",
                        "priority": 1,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "BX_M2",
                        "description": "Stop loss agressif mais contrôlé",
                        "condition": "price < entry * 0.97",
                        "action": "CLOSE_POSITION",
                        "priority": 2,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "BX_M3",
                        "description": "Take profit sur momentum faibli",
                        "condition": "price > entry * 1.05 AND rsi > 70",
                        "action": "CLOSE_POSITION",
                        "priority": 3,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    }
                ],
                "risk_parameters": {
                    "max_position_size": 0.15,  # 15% max du capital
                    "stop_loss_pct": 0.03,      # 3% stop loss
                    "take_profit_pct": 0.05,    # 5% take profit
                    "risk_reward_ratio": 1.67,
                    "max_trades_per_day": 8
                },
                "market_conditions": ["bull_market", "volatile_market"],
                "performance": {
                    "win_rate": 0.0,
                    "avg_profit": 0.0,
                    "total_trades": 0,
                    "sharpe_ratio": 0.0
                }
            }
            
            # ═══════════════════════════════════════════════════════
            # 2️⃣ STRATÉGIES PHOTON - Arbitrage et Speed
            # ═══════════════════════════════════════════════════════
            self.strategies["photon_arbitrage"] = {
                "name": "Photon Speed Arbitrage",
                "source": "Photon",
                "type": "arbitrage",
                "description": "Optimisation vitesse, arbitrage, gestion slippage et routing intelligent",
                "indicators": [
                    {
                        "name": "Price_Spread",
                        "parameters": {"min_spread_pct": 0.3, "exchanges": ["binance", "coinbase"]},
                        "weight": 0.5,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Slippage_Estimator",
                        "parameters": {"max_acceptable_slippage": 0.002, "liquidity_threshold": 100000},
                        "weight": 0.3,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Execution_Speed",
                        "parameters": {"target_latency_ms": 50, "timeout_ms": 200},
                        "weight": 0.2,
                        "success_rate": 0.0
                    }
                ],
                "rules": [
                    {
                        "rule_id": "PH_A1",
                        "description": "Arbitrage si spread > 0.3% après slippage",
                        "condition": "spread > 0.003 AND liquidity > threshold",
                        "action": "EXECUTE_ARBITRAGE",
                        "priority": 1,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "PH_A2",
                        "description": "Annulation si latence > 200ms",
                        "condition": "execution_time > 200ms",
                        "action": "CANCEL_ORDER",
                        "priority": 2,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "PH_A3",
                        "description": "Routing intelligent vers exchange le plus liquide",
                        "condition": "order_size > 0",
                        "action": "ROUTE_TO_BEST_EXCHANGE",
                        "priority": 3,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    }
                ],
                "risk_parameters": {
                    "max_position_size": 0.10,
                    "max_slippage": 0.002,
                    "min_profit_after_fees": 0.001,
                    "execution_timeout": 0.2,
                    "max_concurrent_trades": 3
                },
                "market_conditions": ["bull_market", "bear_market", "sideways_market"],
                "performance": {
                    "win_rate": 0.0,
                    "avg_profit": 0.0,
                    "total_trades": 0,
                    "sharpe_ratio": 0.0
                }
            }
            
            # ═══════════════════════════════════════════════════════
            # 3️⃣ STRATÉGIES GLIDER - Hedging et Risk Management
            # ═══════════════════════════════════════════════════════
            self.strategies["glider_hedging"] = {
                "name": "Glider Conservative Hedging",
                "source": "Glider",
                "type": "hedging",
                "description": "Gestion risque conservatrice, position sizing dynamique, hedging, multi-timeframe",
                "indicators": [
                    {
                        "name": "Volatility_ATR",
                        "parameters": {"period": 14, "multiplier": 2.0},
                        "weight": 0.3,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Multi_Timeframe_Trend",
                        "parameters": {"timeframes": ["5m", "15m", "1h"], "confirmation_required": 2},
                        "weight": 0.4,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Risk_Adjusted_Size",
                        "parameters": {"base_risk_pct": 0.01, "max_risk_pct": 0.02},
                        "weight": 0.3,
                        "success_rate": 0.0
                    }
                ],
                "rules": [
                    {
                        "rule_id": "GL_H1",
                        "description": "Position sizing basé sur volatilité",
                        "condition": "always",
                        "action": "CALCULATE_POSITION_SIZE",
                        "priority": 1,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "GL_H2",
                        "description": "Hedge si exposition > 20%",
                        "condition": "total_exposure > 0.20",
                        "action": "OPEN_HEDGE_POSITION",
                        "priority": 2,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "GL_H3",
                        "description": "Entrée uniquement si confirmation multi-timeframe",
                        "condition": "trend_5m == trend_15m == trend_1h",
                        "action": "ALLOW_ENTRY",
                        "priority": 3,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    }
                ],
                "risk_parameters": {
                    "max_position_size": 0.05,  # Très conservateur
                    "stop_loss_pct": 0.02,
                    "take_profit_pct": 0.04,
                    "max_portfolio_risk": 0.10,
                    "hedge_threshold": 0.20,
                    "max_correlated_positions": 2
                },
                "market_conditions": ["bear_market", "volatile_market", "sideways_market"],
                "performance": {
                    "win_rate": 0.0,
                    "avg_profit": 0.0,
                    "total_trades": 0,
                    "sharpe_ratio": 0.0
                }
            }
            
            # ═══════════════════════════════════════════════════════
            # 4️⃣ STRATÉGIES BINANCE - Mean Reversion et Trend Following
            # ═══════════════════════════════════════════════════════
            self.strategies["binance_hybrid"] = {
                "name": "Binance Hybrid Strategy",
                "source": "Binance",
                "type": "trend_following",
                "description": "Combinaison mean reversion et trend following avec gestion spot/futures",
                "indicators": [
                    {
                        "name": "EMA_Crossover",
                        "parameters": {"fast_period": 9, "slow_period": 21},
                        "weight": 0.3,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Bollinger_Bands",
                        "parameters": {"period": 20, "std_dev": 2},
                        "weight": 0.3,
                        "success_rate": 0.0
                    },
                    {
                        "name": "Funding_Rate",
                        "parameters": {"threshold": 0.0001, "market": "futures"},
                        "weight": 0.4,
                        "success_rate": 0.0
                    }
                ],
                "rules": [
                    {
                        "rule_id": "BN_H1",
                        "description": "Long si prix touche BB inférieur + EMA haussière",
                        "condition": "price < bb_lower AND ema_fast > ema_slow",
                        "action": "OPEN_LONG",
                        "priority": 1,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "BN_H2",
                        "description": "Short si funding rate excessif",
                        "condition": "funding_rate > 0.0001",
                        "action": "CONSIDER_SHORT",
                        "priority": 2,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    },
                    {
                        "rule_id": "BN_H3",
                        "description": "TP progressif par paliers",
                        "condition": "profit > 0",
                        "action": "SCALE_OUT_GRADUALLY",
                        "priority": 3,
                        "success_count": 0,
                        "fail_count": 0,
                        "enabled": True
                    }
                ],
                "risk_parameters": {
                    "max_position_size": 0.12,
                    "stop_loss_pct": 0.025,
                    "take_profit_pct": 0.06,
                    "scale_out_levels": [0.03, 0.05, 0.08],
                    "max_leverage": 3
                },
                "market_conditions": ["bull_market", "sideways_market"],
                "performance": {
                    "win_rate": 0.0,
                    "avg_profit": 0.0,
                    "total_trades": 0,
                    "sharpe_ratio": 0.0
                }
            }
            
            self._save_strategies()
            print("🎯 Stratégies de base initialisées (BullX, Photon, Glider, Binance)")
    
    def detect_market_condition(self, market: Dict, price_history: List[float] = None) -> MarketCondition:
        """
        Détecte la condition actuelle du marché
        
        Args:
            market: Dict avec les mouvements actuels par asset
            price_history: Historique des prix (optionnel)
        
        Returns:
            MarketCondition identifiée
        """
        # Calculer la moyenne des mouvements
        avg_movement = sum(market.values()) / len(market) if market else 0
        
        # Calculer la volatilité (écart-type des mouvements)
        if len(market) > 1:
            variance = sum((x - avg_movement) ** 2 for x in market.values()) / len(market)
            volatility = variance ** 0.5
        else:
            volatility = 0
        
        # Classification
        if volatility > 3:
            return MarketCondition.VOLATILE
        elif avg_movement > 2:
            return MarketCondition.BULL
        elif avg_movement < -2:
            return MarketCondition.BEAR
        else:
            return MarketCondition.SIDEWAYS
    
    def get_best_strategy(self, market_condition: MarketCondition, 
                         current_performance: Dict = None) -> Dict:
        """
        Sélectionne la meilleure stratégie pour les conditions actuelles
        
        Args:
            market_condition: Condition de marché détectée
            current_performance: Performance actuelle (optionnel)
        
        Returns:
            Stratégie recommandée
        """
        suitable_strategies = []
        
        for strategy_name, strategy in self.strategies.items():
            # Vérifier si la stratégie est adaptée aux conditions
            if market_condition.value in strategy.get("market_conditions", []):
                # Calculer un score basé sur la performance
                performance = strategy.get("performance", {})
                win_rate = performance.get("win_rate", 0)
                total_trades = performance.get("total_trades", 0)
                
                # Score composite
                score = win_rate
                if total_trades > 10:
                    score += 0.2  # bonus pour historique conséquent
                
                suitable_strategies.append({
                    "name": strategy_name,
                    "strategy": strategy,
                    "score": score,
                    "win_rate": win_rate,
                    "total_trades": total_trades
                })
        
        # Trier par score
        suitable_strategies.sort(key=lambda x: x["score"], reverse=True)
        
        if suitable_strategies:
            best = suitable_strategies[0]
            print(f"📊 Meilleure stratégie: {best['name']} (score: {best['score']:.2f}, "
                  f"win_rate: {best['win_rate']:.1%}, trades: {best['total_trades']})")
            return best["strategy"]
        else:
            # Fallback sur stratégie équilibrée
            return self.strategies.get("glider_hedging", {})
    
    def update_strategy_performance(self, strategy_name: str, trade_result: Dict):
        """
        Met à jour les performances d'une stratégie après un trade
        
        Args:
            strategy_name: Nom de la stratégie utilisée
            trade_result: Résultat du trade (pnl, asset, etc.)
        """
        if strategy_name not in self.strategies:
            return
        
        strategy = self.strategies[strategy_name]
        performance = strategy.get("performance", {})
        
        # Mettre à jour les compteurs
        total_trades = performance.get("total_trades", 0) + 1
        pnl = trade_result.get("pnl", 0)
        
        if pnl > 0:
            winning_trades = performance.get("winning_trades", 0) + 1
        else:
            winning_trades = performance.get("winning_trades", 0)
        
        # Calculer win rate
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # Calculer profit moyen
        total_profit = performance.get("total_profit", 0) + pnl
        avg_profit = total_profit / total_trades if total_trades > 0 else 0
        
        # Mettre à jour
        strategy["performance"] = {
            "win_rate": round(win_rate, 3),
            "avg_profit": round(avg_profit, 2),
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "total_profit": round(total_profit, 2),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Mettre à jour les règles utilisées
        rules_used = trade_result.get("rules_used", [])
        for rule_id in rules_used:
            for rule in strategy.get("rules", []):
                if rule["rule_id"] == rule_id:
                    if pnl > 0:
                        rule["success_count"] = rule.get("success_count", 0) + 1
                    else:
                        rule["fail_count"] = rule.get("fail_count", 0) + 1
        
        self._save_strategies()
        
        # Mettre à jour les métriques globales
        self._update_global_performance(strategy_name, trade_result)
    
    def _update_global_performance(self, strategy_name: str, trade_result: Dict):
        """Met à jour les métriques de performance globales"""
        pnl = trade_result.get("pnl", 0)
        
        # Par stratégie
        if strategy_name not in self.performance["by_strategy"]:
            self.performance["by_strategy"][strategy_name] = {
                "total_trades": 0,
                "winning_trades": 0,
                "total_pnl": 0
            }
        
        self.performance["by_strategy"][strategy_name]["total_trades"] += 1
        self.performance["by_strategy"][strategy_name]["total_pnl"] += pnl
        if pnl > 0:
            self.performance["by_strategy"][strategy_name]["winning_trades"] += 1
        
        # Global
        self.performance["overall"]["total_trades"] += 1
        if pnl > 0:
            self.performance["overall"]["winning_trades"] += 1
        
        self._save_performance()
    
    def get_strategy_statistics(self) -> Dict:
        """Retourne des statistiques sur toutes les stratégies"""
        stats = {
            "total_strategies": len(self.strategies),
            "strategies": {}
        }
        
        for name, strategy in self.strategies.items():
            perf = strategy.get("performance", {})
            stats["strategies"][name] = {
                "source": strategy.get("source"),
                "type": strategy.get("type"),
                "win_rate": perf.get("win_rate", 0),
                "total_trades": perf.get("total_trades", 0),
                "avg_profit": perf.get("avg_profit", 0),
                "market_conditions": strategy.get("market_conditions", [])
            }
        
        return stats
    
    def identify_winning_patterns(self, min_win_rate: float = 0.6, 
                                  min_trades: int = 10) -> List[Dict]:
        """
        Identifie les patterns gagnants avec un taux de succès élevé
        
        Args:
            min_win_rate: Win rate minimum requis
            min_trades: Nombre minimum de trades pour considérer le pattern
        
        Returns:
            Liste des patterns gagnants
        """
        winning_patterns = []
        
        for strategy_name, strategy in self.strategies.items():
            perf = strategy.get("performance", {})
            win_rate = perf.get("win_rate", 0)
            total_trades = perf.get("total_trades", 0)
            
            if win_rate >= min_win_rate and total_trades >= min_trades:
                # Extraire les règles les plus performantes
                top_rules = []
                for rule in strategy.get("rules", []):
                    success = rule.get("success_count", 0)
                    fail = rule.get("fail_count", 0)
                    total = success + fail
                    
                    if total >= 5:
                        rule_win_rate = success / total
                        if rule_win_rate >= min_win_rate:
                            top_rules.append({
                                "rule_id": rule["rule_id"],
                                "description": rule["description"],
                                "win_rate": round(rule_win_rate, 3),
                                "total_uses": total
                            })
                
                winning_patterns.append({
                    "strategy": strategy_name,
                    "source": strategy.get("source"),
                    "win_rate": win_rate,
                    "total_trades": total_trades,
                    "avg_profit": perf.get("avg_profit", 0),
                    "top_rules": top_rules,
                    "indicators": [ind["name"] for ind in strategy.get("indicators", [])],
                    "risk_params": strategy.get("risk_parameters", {})
                })
        
        # Trier par win rate
        winning_patterns.sort(key=lambda x: x["win_rate"], reverse=True)
        
        return winning_patterns
    
    def export_best_practices(self) -> Dict:
        """
        Exporte les meilleures pratiques identifiées
        
        Returns:
            Dict avec règles de risque, timing, indicateurs, money management
        """
        winning_patterns = self.identify_winning_patterns(min_win_rate=0.55, min_trades=5)
        
        best_practices = {
            "risk_management": {},
            "entry_timing": [],
            "exit_timing": [],
            "technical_indicators": {},
            "money_management": {},
            "generated_at": datetime.utcnow().isoformat()
        }
        
        if not winning_patterns:
            return best_practices
        
        # Agréger les meilleures pratiques
        risk_params_sum = {}
        indicator_counts = {}
        
        for pattern in winning_patterns:
            # Risk management
            risk = pattern.get("risk_params", {})
            for key, value in risk.items():
                if key not in risk_params_sum:
                    risk_params_sum[key] = []
                risk_params_sum[key].append(value)
            
            # Indicateurs
            for indicator in pattern.get("indicators", []):
                indicator_counts[indicator] = indicator_counts.get(indicator, 0) + 1
            
            # Règles de timing
            for rule in pattern.get("top_rules", []):
                if "entry" in rule["description"].lower() or "open" in rule["description"].lower():
                    best_practices["entry_timing"].append(rule["description"])
                elif "exit" in rule["description"].lower() or "close" in rule["description"].lower():
                    best_practices["exit_timing"].append(rule["description"])
        
        # Moyennes des paramètres de risque
        for key, values in risk_params_sum.items():
            best_practices["risk_management"][key] = round(sum(values) / len(values), 4)
        
        # Top indicateurs
        sorted_indicators = sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True)
        best_practices["technical_indicators"] = {
            ind: {"usage_count": count, "effectiveness": "high" if count >= len(winning_patterns) * 0.5 else "medium"}
            for ind, count in sorted_indicators[:10]
        }
        
        # Money management
        best_practices["money_management"] = {
            "max_position_size": best_practices["risk_management"].get("max_position_size", 0.10),
            "stop_loss": best_practices["risk_management"].get("stop_loss_pct", 0.03),
            "take_profit": best_practices["risk_management"].get("take_profit_pct", 0.05),
            "risk_reward_min": 1.5
        }
        
        return best_practices
