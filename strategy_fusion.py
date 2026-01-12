"""
Strategy Fusion Engine - Moteur de Fusion Adaptatif des Stratégies
Fusionne automatiquement les meilleures techniques et adapte selon les conditions
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from enum import Enum
import math


class AdaptationMode(Enum):
    """Modes d'adaptation stratégique"""
    CONSERVATIVE = "conservative"  # Changements progressifs
    MODERATE = "moderate"          # Équilibre prudence/réactivité
    AGGRESSIVE = "aggressive"      # Adaptation rapide


class StrategyFusionEngine:
    """
    Moteur de fusion stratégique qui:
    - Détecte les patterns gagnants de chaque stratégie
    - Fusionne automatiquement les meilleures techniques
    - Adapte dynamiquement selon les performances
    - Ajuste les paramètres aux conditions de marché
    """
    
    def __init__(self, project_root: Path, strategy_analyzer):
        self.project_root = Path(project_root)
        self.strategy_analyzer = strategy_analyzer
        self.fusion_state_file = self.project_root / "fusion_state.json"
        self.adaptation_log_file = self.project_root / "adaptation_log.json"
        
        self.fusion_state = self._load_fusion_state()
        self.adaptation_log = self._load_adaptation_log()
        
    def _load_fusion_state(self) -> Dict:
        """Charge l'état de fusion ou initialise"""
        if self.fusion_state_file.exists():
            try:
                with open(self.fusion_state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "current_fusion": None,
            "active_strategies": [],
            "fusion_history": [],
            "adaptation_mode": "moderate",
            "performance_window": 20,  # nombre de trades pour évaluer
            "last_fusion_date": None,
            "fusion_parameters": {
                "risk_multiplier": 1.0,
                "confidence_threshold": 0.6,
                "min_strategies_to_fuse": 2
            }
        }
    
    def _load_adaptation_log(self) -> List[Dict]:
        """Charge l'historique des adaptations"""
        if self.adaptation_log_file.exists():
            try:
                with open(self.adaptation_log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _save_fusion_state(self):
        """Sauvegarde l'état de fusion"""
        try:
            with open(self.fusion_state_file, "w", encoding="utf-8") as f:
                json.dump(self.fusion_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde fusion state: {e}")
    
    def _save_adaptation_log(self):
        """Sauvegarde l'historique des adaptations"""
        try:
            # Garder seulement les 500 dernières adaptations
            with open(self.adaptation_log_file, "w", encoding="utf-8") as f:
                json.dump(self.adaptation_log[-500:], f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde adaptation log: {e}")
    
    def fuse_strategies(self, market_condition: str, 
                       force_refusion: bool = False) -> Dict:
        """
        Fusionne les meilleures stratégies adaptées aux conditions actuelles
        
        Args:
            market_condition: Condition de marché actuelle
            force_refusion: Force une nouvelle fusion même si une existe
        
        Returns:
            Stratégie fusionnée optimale
        """
        # Vérifier si on a besoin d'une nouvelle fusion
        if not force_refusion and self.fusion_state.get("current_fusion"):
            current = self.fusion_state["current_fusion"]
            if market_condition in current.get("valid_conditions", []):
                # Fusion actuelle toujours valide
                return current
        
        print(f"🔄 Fusion de stratégies pour condition: {market_condition}")
        
        # Obtenir les patterns gagnants
        winning_patterns = self.strategy_analyzer.identify_winning_patterns(
            min_win_rate=0.50,
            min_trades=3
        )
        
        if not winning_patterns:
            print("⚠️ Aucun pattern gagnant identifié - utilisation stratégie par défaut")
            return self._create_default_fusion()
        
        # Filtrer par condition de marché
        suitable_patterns = [
            p for p in winning_patterns 
            if self._is_suitable_for_market(p, market_condition)
        ]
        
        if not suitable_patterns:
            suitable_patterns = winning_patterns[:3]  # Top 3 si aucun match exact
        
        # Fusionner les patterns
        fused_strategy = self._merge_patterns(suitable_patterns, market_condition)
        
        # Enregistrer la fusion
        self.fusion_state["current_fusion"] = fused_strategy
        self.fusion_state["last_fusion_date"] = datetime.utcnow().isoformat()
        self.fusion_state["active_strategies"] = [p["strategy"] for p in suitable_patterns]
        self._save_fusion_state()
        
        # Logger l'adaptation
        self._log_adaptation({
            "type": "strategy_fusion",
            "market_condition": market_condition,
            "strategies_fused": len(suitable_patterns),
            "fusion_result": {
                "rules_count": len(fused_strategy.get("rules", [])),
                "indicators_count": len(fused_strategy.get("indicators", [])),
                "confidence": fused_strategy.get("confidence", 0)
            }
        })
        
        print(f"✅ Fusion complète: {len(suitable_patterns)} stratégies combinées")
        return fused_strategy
    
    def _is_suitable_for_market(self, pattern: Dict, market_condition: str) -> bool:
        """Vérifie si un pattern est adapté à la condition de marché"""
        # Obtenir la stratégie complète
        strategy_name = pattern.get("strategy")
        if strategy_name not in self.strategy_analyzer.strategies:
            return False
        
        strategy = self.strategy_analyzer.strategies[strategy_name]
        valid_conditions = strategy.get("market_conditions", [])
        
        return market_condition in valid_conditions
    
    def _merge_patterns(self, patterns: List[Dict], market_condition: str) -> Dict:
        """
        Fusionne plusieurs patterns en une stratégie unifiée
        
        Args:
            patterns: Liste des patterns à fusionner
            market_condition: Condition de marché cible
        
        Returns:
            Stratégie fusionnée
        """
        fused = {
            "name": f"Fused_Strategy_{datetime.utcnow().strftime('%Y%m%d_%H%M')}",
            "type": "adaptive_fusion",
            "market_condition": market_condition,
            "source_strategies": [p["strategy"] for p in patterns],
            "created_at": datetime.utcnow().isoformat(),
            "rules": [],
            "indicators": [],
            "risk_parameters": {},
            "confidence": 0.0,
            "valid_conditions": [market_condition]
        }
        
        # 1. Fusionner les règles (éliminer doublons, prioriser par performance)
        all_rules = []
        for pattern in patterns:
            strategy_name = pattern["strategy"]
            strategy = self.strategy_analyzer.strategies[strategy_name]
            
            for rule in pattern.get("top_rules", []):
                all_rules.append({
                    "rule_id": f"{strategy_name}_{rule['rule_id']}",
                    "description": rule["description"],
                    "win_rate": rule["win_rate"],
                    "priority": rule["win_rate"],  # prioriser par win rate
                    "source": strategy_name,
                    "enabled": True
                })
        
        # Trier par win rate et garder les meilleures
        all_rules.sort(key=lambda x: x["win_rate"], reverse=True)
        fused["rules"] = all_rules[:15]  # Top 15 règles
        
        # 2. Fusionner les indicateurs (par fréquence d'utilisation)
        indicator_usage = {}
        for pattern in patterns:
            for indicator in pattern.get("indicators", []):
                indicator_usage[indicator] = indicator_usage.get(indicator, 0) + 1
        
        # Trier et sélectionner top indicateurs
        sorted_indicators = sorted(indicator_usage.items(), key=lambda x: x[1], reverse=True)
        fused["indicators"] = [
            {"name": ind, "usage_frequency": count, "weight": count / len(patterns)}
            for ind, count in sorted_indicators[:8]
        ]
        
        # 3. Fusionner les paramètres de risque (moyenne pondérée par performance)
        risk_params = {}
        total_weight = sum(p["win_rate"] for p in patterns)
        
        for pattern in patterns:
            weight = pattern["win_rate"] / total_weight if total_weight > 0 else 1 / len(patterns)
            
            for key, value in pattern.get("risk_params", {}).items():
                if isinstance(value, (int, float)):
                    if key not in risk_params:
                        risk_params[key] = 0
                    risk_params[key] += value * weight
        
        # Arrondir les paramètres
        fused["risk_parameters"] = {
            key: round(value, 4) for key, value in risk_params.items()
        }
        
        # Ajuster selon le mode d'adaptation
        fused["risk_parameters"] = self._adjust_risk_for_adaptation_mode(
            fused["risk_parameters"]
        )
        
        # 4. Calculer la confiance globale
        avg_win_rate = sum(p["win_rate"] for p in patterns) / len(patterns)
        total_trades = sum(p["total_trades"] for p in patterns)
        
        # Confiance basée sur performance et volume de données
        confidence = avg_win_rate * 0.7
        if total_trades > 50:
            confidence += 0.2
        elif total_trades > 20:
            confidence += 0.1
        
        fused["confidence"] = round(min(confidence, 1.0), 3)
        
        return fused
    
    def _adjust_risk_for_adaptation_mode(self, risk_params: Dict) -> Dict:
        """Ajuste les paramètres de risque selon le mode d'adaptation"""
        mode = self.fusion_state.get("adaptation_mode", "moderate")
        multiplier = self.fusion_state.get("fusion_parameters", {}).get("risk_multiplier", 1.0)
        
        adjusted = risk_params.copy()
        
        if mode == "conservative":
            # Réduire les risques
            if "max_position_size" in adjusted:
                adjusted["max_position_size"] *= 0.8
            if "stop_loss_pct" in adjusted:
                adjusted["stop_loss_pct"] *= 0.9  # Stop loss plus serré
            if "max_leverage" in adjusted:
                adjusted["max_leverage"] = min(adjusted.get("max_leverage", 1), 2)
        
        elif mode == "aggressive":
            # Augmenter légèrement les risques
            if "max_position_size" in adjusted:
                adjusted["max_position_size"] = min(adjusted["max_position_size"] * 1.2, 0.25)
            if "take_profit_pct" in adjusted:
                adjusted["take_profit_pct"] *= 1.1
        
        # Appliquer le multiplicateur global
        for key in ["max_position_size", "stop_loss_pct", "take_profit_pct"]:
            if key in adjusted:
                adjusted[key] *= multiplier
                adjusted[key] = round(adjusted[key], 4)
        
        return adjusted
    
    def _create_default_fusion(self) -> Dict:
        """Crée une fusion par défaut équilibrée"""
        return {
            "name": "Moderate_Balanced_Strategy",
            "type": "moderate",
            "created_at": datetime.utcnow().isoformat(),
            "rules": [
                {
                    "rule_id": "DEFAULT_1",
                    "description": "Entrée uniquement si gain > 1%",
                    "priority": 1,
                    "enabled": True
                },
                {
                    "rule_id": "DEFAULT_2",
                    "description": "Stop loss à -2%",
                    "priority": 2,
                    "enabled": True
                }
            ],
            "indicators": [
                {"name": "Price_Movement", "weight": 1.0}
            ],
            "risk_parameters": {
                "max_position_size": 0.10,
                "stop_loss_pct": 0.02,
                "take_profit_pct": 0.04
            },
            "confidence": 0.5,
            "valid_conditions": ["bull_market", "bear_market", "sideways_market", "volatile_market"]
        }
    
    def adapt_to_performance(self, recent_trades: List[Dict]) -> Dict:
        """
        Adapte la stratégie fusionnée selon les performances récentes
        
        Args:
            recent_trades: Liste des derniers trades avec résultats
        
        Returns:
            Dict avec les ajustements effectués
        """
        if not recent_trades:
            return {"adjusted": False, "reason": "no_recent_trades"}
        
        window_size = self.fusion_state.get("performance_window", 20)
        trades_to_analyze = recent_trades[-window_size:]
        
        # Calculer les métriques
        total = len(trades_to_analyze)
        winning = sum(1 for t in trades_to_analyze if t.get("pnl", 0) > 0)
        win_rate = winning / total if total > 0 else 0
        
        avg_pnl = sum(t.get("pnl", 0) for t in trades_to_analyze) / total if total > 0 else 0
        
        # Analyser les pertes consécutives
        consecutive_losses = 0
        for trade in reversed(trades_to_analyze):
            if trade.get("pnl", 0) < 0:
                consecutive_losses += 1
            else:
                break
        
        adjustments = {
            "adjusted": False,
            "changes": [],
            "new_mode": None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Décision d'adaptation
        current_mode = self.fusion_state.get("adaptation_mode", "moderate")
        
        # 1. Performance excellente (win rate > 70%)
        if win_rate > 0.70 and total >= 10:
            if current_mode != "aggressive":
                adjustments["adjusted"] = True
                adjustments["new_mode"] = "aggressive"
                adjustments["changes"].append(
                    f"Performance excellente ({win_rate:.1%}) - passage en mode AGGRESSIVE"
                )
                self.fusion_state["adaptation_mode"] = "aggressive"
                self.fusion_state["fusion_parameters"]["risk_multiplier"] = 1.2
        
        # 2. Performance faible (win rate < 40%)
        elif win_rate < 0.40 and total >= 10:
            if current_mode != "conservative":
                adjustments["adjusted"] = True
                adjustments["new_mode"] = "conservative"
                adjustments["changes"].append(
                    f"Performance faible ({win_rate:.1%}) - passage en mode CONSERVATIVE"
                )
                self.fusion_state["adaptation_mode"] = "conservative"
                self.fusion_state["fusion_parameters"]["risk_multiplier"] = 0.7
        
        # 3. Pertes consécutives (>= 4)
        elif consecutive_losses >= 4:
            adjustments["adjusted"] = True
            adjustments["changes"].append(
                f"⚠️ {consecutive_losses} pertes consécutives - réduction risque temporaire"
            )
            self.fusion_state["fusion_parameters"]["risk_multiplier"] = max(
                self.fusion_state["fusion_parameters"].get("risk_multiplier", 1.0) * 0.8,
                0.5
            )
        
        # 4. Retour à la normale si performance stable
        elif 0.50 <= win_rate <= 0.65 and total >= 15 and current_mode != "moderate":
            adjustments["adjusted"] = True
            adjustments["new_mode"] = "moderate"
            adjustments["changes"].append(
                f"Performance stabilisée ({win_rate:.1%}) - retour en mode MODERATE"
            )
            self.fusion_state["adaptation_mode"] = "moderate"
            self.fusion_state["fusion_parameters"]["risk_multiplier"] = 1.0
        
        if adjustments["adjusted"]:
            self._save_fusion_state()
            self._log_adaptation({
                "type": "performance_adaptation",
                "trigger": "recent_performance_analysis",
                "metrics": {
                    "win_rate": round(win_rate, 3),
                    "avg_pnl": round(avg_pnl, 2),
                    "consecutive_losses": consecutive_losses,
                    "trades_analyzed": total
                },
                "adjustments": adjustments["changes"]
            })
            
            print(f"📊 Adaptation stratégique effectuée:")
            for change in adjustments["changes"]:
                print(f"   - {change}")
        
        return adjustments
    
    def adapt_to_market_conditions(self, market: Dict, 
                                   price_history: List[float] = None) -> Dict:
        """
        Adapte la stratégie selon les conditions de marché en temps réel
        
        Args:
            market: État actuel du marché
            price_history: Historique des prix (optionnel)
        
        Returns:
            Recommandations d'adaptation
        """
        # Détecter la condition de marché
        from strategy_analyzer import MarketCondition
        
        condition = self.strategy_analyzer.detect_market_condition(market, price_history)
        
        # Vérifier si la fusion actuelle est adaptée
        current_fusion = self.fusion_state.get("current_fusion")
        
        if not current_fusion or condition.value not in current_fusion.get("valid_conditions", []):
            # Nécessite une nouvelle fusion
            print(f"🔄 Condition de marché changée: {condition.value}")
            new_fusion = self.fuse_strategies(condition.value, force_refusion=True)
            
            return {
                "adapted": True,
                "reason": "market_condition_change",
                "new_condition": condition.value,
                "fusion_updated": True,
                "new_fusion": new_fusion
            }
        
        return {
            "adapted": False,
            "reason": "current_fusion_valid",
            "condition": condition.value
        }
    
    def _log_adaptation(self, adaptation_entry: Dict):
        """Enregistre une adaptation dans l'historique"""
        adaptation_entry["timestamp"] = datetime.utcnow().isoformat()
        self.adaptation_log.append(adaptation_entry)
        self._save_adaptation_log()
    
    def get_current_strategy(self) -> Dict:
        """Retourne la stratégie fusionnée actuellement active"""
        current = self.fusion_state.get("current_fusion")
        if current and isinstance(current, dict):
            return current
        return self._create_default_fusion()
    
    def get_adaptation_summary(self) -> Dict:
        """Retourne un résumé des adaptations récentes"""
        recent_adaptations = self.adaptation_log[-20:] if self.adaptation_log else []
        
        return {
            "total_adaptations": len(self.adaptation_log),
            "current_mode": self.fusion_state.get("adaptation_mode"),
            "risk_multiplier": self.fusion_state.get("fusion_parameters", {}).get("risk_multiplier", 1.0),
            "last_fusion": self.fusion_state.get("last_fusion_date"),
            "active_strategies": self.fusion_state.get("active_strategies", []),
            "recent_adaptations": recent_adaptations,
            "current_fusion_confidence": self.fusion_state.get("current_fusion", {}).get("confidence", 0)
        }
    
    def should_trigger_refusion(self, performance_metrics: Dict) -> Tuple[bool, str]:
        """
        Détermine si une nouvelle fusion doit être déclenchée
        
        Args:
            performance_metrics: Métriques de performance récentes
        
        Returns:
            (bool: should_refuse, str: reason)
        """
        current_fusion = self.fusion_state.get("current_fusion")
        
        if not current_fusion:
            return True, "no_current_fusion"
        
        # Vérifier le temps depuis la dernière fusion
        last_fusion = self.fusion_state.get("last_fusion_date")
        if last_fusion:
            last_date = datetime.fromisoformat(last_fusion)
            hours_since = (datetime.utcnow() - last_date).total_seconds() / 3600
            
            # Refusion automatique après 48h
            if hours_since > 48:
                return True, f"auto_refusion_after_{hours_since:.1f}h"
        
        # Vérifier la performance
        win_rate = performance_metrics.get("win_rate", 0)
        total_trades = performance_metrics.get("total_trades", 0)
        
        # Si performance très faible avec données suffisantes
        if win_rate < 0.35 and total_trades >= 15:
            return True, f"poor_performance_win_rate_{win_rate:.1%}"
        
        # Si confiance de la fusion actuelle est faible
        confidence = current_fusion.get("confidence", 0)
        if confidence < 0.4:
            return True, f"low_fusion_confidence_{confidence:.2f}"
        
        return False, "current_fusion_performing_well"
    
    def get_trading_signals(self, market: Dict, asset: str) -> Dict:
        """
        Génère des signaux de trading basés sur la stratégie fusionnée
        
        Args:
            market: État du marché
            asset: Asset à trader
        
        Returns:
            Signaux de trading avec confiance
        """
        current_strategy = self.get_current_strategy()
        
        if not current_strategy or not isinstance(current_strategy, dict):
            current_strategy = self._create_default_fusion()
        
        signals = {
            "asset": asset,
            "action": "HOLD",
            "confidence": 0.0,
            "reasons": [],
            "risk_params": current_strategy.get("risk_parameters", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Analyser selon les règles fusionnées
        asset_movement = market.get(asset, 0)
        
        # Règle basique: entrée si mouvement positif suffisant
        min_gain = current_strategy.get("risk_parameters", {}).get("min_gain_threshold", 0.8)
        
        if asset_movement >= min_gain:
            signals["action"] = "OPEN_LONG"
            signals["confidence"] = min(
                current_strategy.get("confidence", 0.5) * (1 + asset_movement / 10),
                1.0
            )
            signals["reasons"].append(f"Mouvement positif {asset_movement:.2f}% > seuil {min_gain:.2f}%")
        elif asset_movement < -2:
            signals["action"] = "AVOID"
            signals["confidence"] = 0.8
            signals["reasons"].append(f"Mouvement négatif important {asset_movement:.2f}%")
        else:
            signals["reasons"].append(f"Mouvement insuffisant {asset_movement:.2f}%")
        
        return signals
