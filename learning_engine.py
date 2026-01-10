"""
Moteur d'apprentissage permanent pour l'agent AI
Analyse les erreurs, identifie les patterns et ajuste la stratégie automatiquement
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict


class LearningEngine:
    """
    Système d'apprentissage continu basé sur:
    - Analyse des erreurs passées
    - Détection des patterns de pertes
    - Ajustement dynamique de la stratégie
    - Mémorisation des leçons apprises
    """
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.learning_file = self.project_root / "learning_state.json"
        self.mistakes_log = self.project_root / "mistakes_log.json"
        self.patterns_file = self.project_root / "error_patterns.json"
        
        self.state = self._load_state()
        self.mistakes = self._load_mistakes()
        self.patterns = self._load_patterns()
    
    def _load_state(self) -> Dict:
        """Charge l'état d'apprentissage ou initialise"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # État par défaut avec paramètres d'apprentissage
        return {
            "min_gain_to_open": 0.5,
            "consecutive_losses": 0,
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0,
            "max_loss_threshold": -50.0,  # perte max acceptée par trade
            "min_win_threshold": 10.0,    # gain min recherché
            "risk_level": 0.5,             # 0-1, ajusté selon performance
            "learning_rate": 0.1,          # vitesse d'ajustement
            "adaptive_threshold": True,    # ajustement automatique
            "avoid_patterns": [],          # patterns à éviter
            "lessons_learned": [],         # leçons importantes
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def _load_mistakes(self) -> List[Dict]:
        """Charge l'historique des erreurs"""
        if self.mistakes_log.exists():
            try:
                with open(self.mistakes_log, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _load_patterns(self) -> Dict:
        """Charge les patterns d'erreurs identifiés"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "loss_patterns": [],
            "market_conditions": {},
            "timing_issues": [],
            "asset_specific": {}
        }
    
    def _save_state(self):
        """Sauvegarde l'état d'apprentissage"""
        self.state["last_updated"] = datetime.utcnow().isoformat()
        try:
            with open(self.learning_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde état: {e}")
    
    def _save_mistakes(self):
        """Sauvegarde l'historique des erreurs"""
        try:
            with open(self.mistakes_log, "w", encoding="utf-8") as f:
                json.dump(self.mistakes[-1000:], f, indent=2)  # garder les 1000 dernières
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde erreurs: {e}")
    
    def _save_patterns(self):
        """Sauvegarde les patterns identifiés"""
        try:
            with open(self.patterns_file, "w", encoding="utf-8") as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde patterns: {e}")
    
    def analyze_trade(self, summary: Dict) -> Dict[str, Any]:
        """
        Analyse un trade et en tire des leçons
        
        Returns:
            Dict avec les ajustements recommandés et leçons apprises
        """
        trade = summary.get("trade")
        if not trade:
            return {"adjusted": False, "reason": "no_trade"}
        
        pnl = trade.get("pnl", 0)
        asset = trade.get("asset")
        market = summary.get("market", {})
        
        # Mise à jour des statistiques
        self.state["total_trades"] += 1
        
        if pnl < 0:
            self.state["losing_trades"] += 1
            self.state["consecutive_losses"] = self.state.get("consecutive_losses", 0) + 1
            
            # Enregistrer l'erreur
            mistake = {
                "timestamp": summary.get("timestamp", datetime.utcnow().isoformat()),
                "asset": asset,
                "pnl": pnl,
                "entry_price": trade.get("entry_price"),
                "exit_price": trade.get("exit_price"),
                "market_conditions": market,
                "lesson": self._generate_lesson(trade, market)
            }
            self.mistakes.append(mistake)
            self._save_mistakes()
            
            # Analyser les patterns d'erreur
            self._analyze_error_pattern(mistake)
            
        else:
            self.state["winning_trades"] += 1
            self.state["consecutive_losses"] = 0
        
        # Calculer le win rate
        if self.state["total_trades"] > 0:
            self.state["win_rate"] = round(
                self.state["winning_trades"] / self.state["total_trades"], 
                3
            )
        
        # Ajustements adaptatifs
        adjustments = self._calculate_adjustments(pnl, asset, market)
        
        self._save_state()
        return adjustments
    
    def _generate_lesson(self, trade: Dict, market: Dict) -> str:
        """Génère une leçon à partir d'un trade perdant"""
        pnl = trade.get("pnl", 0)
        asset = trade.get("asset")
        market_move = market.get(asset, 0)
        
        lessons = []
        
        if market_move < 0 and pnl < 0:
            lessons.append(f"Éviter {asset} quand le marché est négatif ({market_move}%)")
        
        if abs(pnl) > self.state.get("max_loss_threshold", -50):
            lessons.append(f"Perte trop importante sur {asset} - réduire l'exposition")
        
        if trade.get("exit_price", 0) < trade.get("entry_price", 0) * 0.95:
            lessons.append(f"Stop-loss déclenché sur {asset} - revoir le seuil d'entrée")
        
        # Analyser la volatilité
        if max(market.values()) - min(market.values()) > 5:
            lessons.append("Marché très volatile - augmenter la prudence")
        
        return " | ".join(lessons) if lessons else "Perte standard - continuer surveillance"
    
    def _analyze_error_pattern(self, mistake: Dict):
        """Analyse et stocke les patterns d'erreurs"""
        asset = mistake.get("asset")
        pnl = mistake.get("pnl", 0)
        market = mistake.get("market_conditions", {})
        
        # Pattern 1: Asset spécifique perdant
        if asset:
            if asset not in self.patterns["asset_specific"]:
                self.patterns["asset_specific"][asset] = {"losses": 0, "total": 0}
            
            self.patterns["asset_specific"][asset]["losses"] += 1
            self.patterns["asset_specific"][asset]["total"] += 1
            
            # Si un asset perd > 60% du temps, l'éviter
            stats = self.patterns["asset_specific"][asset]
            if stats["total"] >= 5 and stats["losses"] / stats["total"] > 0.6:
                pattern = f"AVOID_{asset}_HIGH_LOSS_RATE"
                if pattern not in self.state.get("avoid_patterns", []):
                    self.state.setdefault("avoid_patterns", []).append(pattern)
                    self.state.setdefault("lessons_learned", []).append(
                        f"Asset {asset} a un taux de perte élevé - réduire exposition"
                    )
        
        # Pattern 2: Conditions de marché défavorables
        market_sum = sum(market.values())
        if market_sum < 0 and pnl < -20:
            pattern_key = "NEGATIVE_MARKET_LARGE_LOSS"
            self.patterns["loss_patterns"].append({
                "type": pattern_key,
                "market_sum": market_sum,
                "loss": pnl,
                "timestamp": mistake.get("timestamp")
            })
            
            # Leçon: ne pas trader en marché négatif global
            if pattern_key not in self.state.get("avoid_patterns", []):
                self.state.setdefault("avoid_patterns", []).append(pattern_key)
                self.state.setdefault("lessons_learned", []).append(
                    "Ne pas ouvrir de position quand le marché global est négatif"
                )
        
        self._save_patterns()
        self._save_state()
    
    def _calculate_adjustments(self, pnl: float, asset: str, market: Dict) -> Dict:
        """Calcule les ajustements de stratégie basés sur la performance"""
        adjustments = {
            "adjusted": True,
            "changes": [],
            "new_parameters": {}
        }
        
        learning_rate = self.state.get("learning_rate", 0.1)
        
        # Ajustement 1: Seuil d'entrée basé sur pertes consécutives
        if self.state.get("consecutive_losses", 0) >= 3:
            old_threshold = self.state.get("min_gain_to_open", 0.5)
            new_threshold = round(old_threshold + 0.3, 2)  # augmentation plus agressive
            self.state["min_gain_to_open"] = min(new_threshold, 3.0)  # max 3%
            
            adjustments["changes"].append(
                f"Seuil d'entrée augmenté: {old_threshold}% → {self.state['min_gain_to_open']}%"
            )
            self.state["consecutive_losses"] = 0
        
        # Ajustement 2: Niveau de risque basé sur win rate
        win_rate = self.state.get("win_rate", 0)
        if win_rate < 0.4 and self.state["total_trades"] >= 10:
            # Performance faible - réduire le risque
            old_risk = self.state.get("risk_level", 0.5)
            self.state["risk_level"] = max(0.2, old_risk - learning_rate)
            adjustments["changes"].append(
                f"Niveau de risque réduit: {old_risk:.2f} → {self.state['risk_level']:.2f}"
            )
        elif win_rate > 0.6 and self.state["total_trades"] >= 10:
            # Bonne performance - augmenter légèrement le risque
            old_risk = self.state.get("risk_level", 0.5)
            self.state["risk_level"] = min(0.8, old_risk + learning_rate * 0.5)
            adjustments["changes"].append(
                f"Niveau de risque augmenté: {old_risk:.2f} → {self.state['risk_level']:.2f}"
            )
        
        # Ajustement 3: Seuils de perte/gain adaptatifs
        if pnl < self.state.get("max_loss_threshold", -50):
            # Perte trop importante - resserrer le stop-loss
            old_max = self.state["max_loss_threshold"]
            self.state["max_loss_threshold"] = max(-30, old_max + 5)
            adjustments["changes"].append(
                f"Stop-loss resserré: {old_max} → {self.state['max_loss_threshold']}"
            )
        
        # Ajustement 4: Éviter les assets problématiques
        if asset and asset in self.patterns.get("asset_specific", {}):
            asset_stats = self.patterns["asset_specific"][asset]
            if asset_stats["total"] >= 3:
                loss_rate = asset_stats["losses"] / asset_stats["total"]
                if loss_rate > 0.5:
                    adjustments["changes"].append(
                        f"⚠️ Asset {asset} a un taux de perte de {loss_rate:.1%} - réduire exposition"
                    )
        
        # Ajustement 5: Conditions de marché
        market_sum = sum(market.values())
        if market_sum < -2 and "NEGATIVE_MARKET_LARGE_LOSS" in self.state.get("avoid_patterns", []):
            adjustments["changes"].append(
                "⚠️ Marché globalement négatif - éviter les nouveaux trades"
            )
            adjustments["skip_trading"] = True
        
        adjustments["new_parameters"] = {
            "min_gain_to_open": self.state.get("min_gain_to_open"),
            "risk_level": self.state.get("risk_level"),
            "max_loss_threshold": self.state.get("max_loss_threshold"),
            "win_rate": self.state.get("win_rate"),
            "total_trades": self.state.get("total_trades")
        }
        
        self._save_state()
        return adjustments
    
    def should_trade(self, asset: str, market: Dict) -> tuple[bool, str]:
        """
        Détermine si un trade doit être ouvert selon les leçons apprises
        
        Returns:
            (bool: should_trade, str: reason)
        """
        # Vérifier les patterns à éviter
        avoid_patterns = self.state.get("avoid_patterns", [])
        
        # Check 1: Asset spécifique problématique
        if f"AVOID_{asset}_HIGH_LOSS_RATE" in avoid_patterns:
            return False, f"Asset {asset} a un historique de pertes élevé"
        
        # Check 2: Marché globalement négatif
        market_sum = sum(market.values())
        if market_sum < -2 and "NEGATIVE_MARKET_LARGE_LOSS" in avoid_patterns:
            return False, f"Marché global négatif ({market_sum:.2f}%) - éviter trading"
        
        # Check 3: Gain minimal requis
        min_gain = self.state.get("min_gain_to_open", 0.5)
        asset_gain = market.get(asset, 0)
        if asset_gain < min_gain:
            return False, f"Gain {asset} ({asset_gain}%) < seuil requis ({min_gain}%)"
        
        # Check 4: Niveau de risque actuel
        risk_level = self.state.get("risk_level", 0.5)
        if risk_level < 0.3 and self.state.get("consecutive_losses", 0) > 0:
            return False, "Niveau de risque trop bas après pertes récentes"
        
        return True, "Conditions favorables selon l'apprentissage"
    
    def get_trading_recommendation(self, market: Dict) -> Dict:
        """
        Fournit une recommandation de trading basée sur l'apprentissage
        """
        recommendations = []
        
        # Analyser chaque asset
        for asset, gain in market.items():
            should_trade, reason = self.should_trade(asset, market)
            
            recommendations.append({
                "asset": asset,
                "gain": gain,
                "should_trade": should_trade,
                "reason": reason,
                "confidence": self._calculate_confidence(asset, gain)
            })
        
        # Trier par confiance
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "recommendations": recommendations,
            "best_choice": recommendations[0] if recommendations else None,
            "current_state": {
                "win_rate": self.state.get("win_rate"),
                "risk_level": self.state.get("risk_level"),
                "total_trades": self.state.get("total_trades"),
                "lessons_count": len(self.state.get("lessons_learned", []))
            }
        }
    
    def _calculate_confidence(self, asset: str, gain: float) -> float:
        """Calcule un score de confiance pour un trade (0-1)"""
        confidence = 0.5  # base
        
        # Bonus pour gain élevé
        if gain > 2:
            confidence += 0.2
        elif gain > 1:
            confidence += 0.1
        
        # Pénalité si asset problématique
        if asset in self.patterns.get("asset_specific", {}):
            stats = self.patterns["asset_specific"][asset]
            if stats["total"] >= 3:
                loss_rate = stats["losses"] / stats["total"]
                confidence -= loss_rate * 0.3
        
        # Bonus pour bon win rate global
        win_rate = self.state.get("win_rate", 0)
        if win_rate > 0.6:
            confidence += 0.15
        elif win_rate < 0.4:
            confidence -= 0.15
        
        # Ajuster selon niveau de risque actuel
        confidence *= self.state.get("risk_level", 0.5) + 0.5
        
        return max(0, min(1, confidence))
    
    def get_summary(self) -> Dict:
        """Retourne un résumé de l'apprentissage"""
        return {
            "total_trades": self.state.get("total_trades", 0),
            "win_rate": self.state.get("win_rate", 0),
            "consecutive_losses": self.state.get("consecutive_losses", 0),
            "lessons_learned": len(self.state.get("lessons_learned", [])),
            "patterns_identified": len(self.state.get("avoid_patterns", [])),
            "risk_level": self.state.get("risk_level", 0.5),
            "min_gain_threshold": self.state.get("min_gain_to_open", 0.5),
            "recent_lessons": self.state.get("lessons_learned", [])[-5:]
        }
