"""
Moteur d'apprentissage permanent pour l'agent AI
Analyse les erreurs, identifie les patterns et ajuste la stratégie automatiquement
Version améliorée avec auto-amélioration continue et analyse post-trade avancée
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter


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
        self.post_trade_analysis_file = self.project_root / "post_trade_analysis.json"
        self.recurring_errors_file = self.project_root / "recurring_errors.json"
        self.invalid_signals_file = self.project_root / "invalid_signals.json"
        self.avoidable_losses_file = self.project_root / "avoidable_losses.json"
        
        self.state = self._load_state()
        self.mistakes = self._load_mistakes()
        self.patterns = self._load_patterns()
        self.post_trade_analyses = self._load_post_trade_analyses()
        self.recurring_errors = self._load_recurring_errors()
        self.invalid_signals = self._load_invalid_signals()
        self.avoidable_losses = self._load_avoidable_losses()
    
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
    
    def _load_post_trade_analyses(self) -> List[Dict]:
        """Charge les analyses post-trade"""
        if self.post_trade_analysis_file.exists():
            try:
                with open(self.post_trade_analysis_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _save_post_trade_analyses(self):
        """Sauvegarde les analyses post-trade"""
        try:
            with open(self.post_trade_analysis_file, "w", encoding="utf-8") as f:
                json.dump(self.post_trade_analyses[-200:], f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde analyses: {e}")
    
    def _load_recurring_errors(self) -> Dict:
        """Charge les erreurs récurrentes"""
        if self.recurring_errors_file.exists():
            try:
                with open(self.recurring_errors_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"error_types": {}, "patterns": [], "last_updated": None}
    
    def _save_recurring_errors(self):
        """Sauvegarde les erreurs récurrentes"""
        try:
            self.recurring_errors["last_updated"] = datetime.utcnow().isoformat()
            with open(self.recurring_errors_file, "w", encoding="utf-8") as f:
                json.dump(self.recurring_errors, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde erreurs récurrentes: {e}")
    
    def _load_invalid_signals(self) -> List[Dict]:
        """Charge les signaux invalides détectés"""
        if self.invalid_signals_file.exists():
            try:
                with open(self.invalid_signals_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _save_invalid_signals(self):
        """Sauvegarde les signaux invalides"""
        try:
            with open(self.invalid_signals_file, "w", encoding="utf-8") as f:
                json.dump(self.invalid_signals[-100:], f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde signaux invalides: {e}")
    
    def _load_avoidable_losses(self) -> Dict:
        """Charge l'analyse des pertes évitables"""
        if self.avoidable_losses_file.exists():
            try:
                with open(self.avoidable_losses_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "total_avoidable": 0,
            "total_amount": 0,
            "categories": {},
            "improvements_suggested": []
        }
    
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
        Logique hybride: Seuil de gain OU haute confiance
        
        Returns:
            (bool: should_trade, str: reason)
        """
        # Vérifier les patterns à éviter
        avoid_patterns = self.state.get("avoid_patterns", [])
        
        # Check 1: Asset spécifique problématique (blocage absolu)
        if f"AVOID_{asset}_HIGH_LOSS_RATE" in avoid_patterns:
            return False, f"Asset {asset} a un historique de pertes élevé"
        
        # Check 2: Marché globalement négatif (blocage absolu)
        market_sum = sum(market.values())
        if market_sum < -2 and "NEGATIVE_MARKET_LARGE_LOSS" in avoid_patterns:
            return False, f"Marché global négatif ({market_sum:.2f}%) - éviter trading"
        
        # Check 3: Gain minimal absolu (protection contre micro-gains)
        asset_gain = market.get(asset, 0)
        if asset_gain < 0.3:  # Blocage absolu si <0.3%
            return False, f"Gain {asset} ({asset_gain}%) trop faible (min absolu: 0.3%)"
        
        # Check 4: Niveau de risque actuel (après pertes)
        risk_level = self.state.get("risk_level", 0.5)
        if risk_level < 0.3 and self.state.get("consecutive_losses", 0) > 0:
            return False, "Niveau de risque trop bas après pertes récentes"
        
        # ====== LOGIQUE HYBRIDE INTELLIGENTE ======
        min_gain = self.state.get("min_gain_to_open", 0.5)
        win_rate = self.state.get("win_rate", 0)
        
        # Voie 1: Gain suffisant (méthode classique)
        if asset_gain >= min_gain:
            return True, f"Gain {asset_gain:.2f}% >= seuil {min_gain:.2f}%"
        
        # Voie 2: Opportunisme intelligent (gain modéré + conditions favorables)
        # Permet de trader 0.3-0.8% si contexte excellent
        if asset_gain >= 0.4:  # Entre 0.4% et min_gain
            # Condition 2a: Excellent historique récent
            if win_rate > 0.80 and self.state.get("consecutive_losses", 0) == 0:
                return True, f"Opportunité: Gain {asset_gain:.2f}% + Win rate excellent ({win_rate:.1%})"
            
            # Condition 2b: Asset est le meilleur du marché par large marge
            best_gain = max(market.values())
            if asset == max(market.items(), key=lambda x: x[1])[0] and best_gain - asset_gain < 0.1:
                # C'est le meilleur asset ET pas d'autre bien meilleur
                return True, f"Meilleur asset disponible: {asset_gain:.2f}%"
        
        # Rejet avec raison détaillée
        return False, f"Gain {asset_gain:.2f}% insuffisant (seuil: {min_gain:.2f}%, min opportuniste: 0.4%)"
    
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
    # ═══════════════════════════════════════════════════════════
    # NOUVELLES FONCTIONNALITÉS D'AUTO-AMÉLIORATION
    # ═══════════════════════════════════════════════════════════
    
    def perform_post_trade_analysis(self, trade_result: Dict, market: Dict) -> Dict:
        """
        Analyse post-trade complète pour identifier les améliorations
        
        Args:
            trade_result: Résultat du trade avec tous les détails
            market: État du marché au moment du trade
        
        Returns:
            Analyse complète avec recommandations
        """
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "trade_id": trade_result.get("timestamp", "unknown"),
            "asset": trade_result.get("asset"),
            "pnl": trade_result.get("pnl", 0),
            "entry_price": trade_result.get("entry_price"),
            "exit_price": trade_result.get("exit_price"),
            "market_conditions": market.copy(),
            "errors_identified": [],
            "lessons": [],
            "avoidable": False,
            "improvement_score": 0.0
        }
        
        pnl = trade_result.get("pnl", 0)
        asset = trade_result.get("asset")
        entry = trade_result.get("entry_price", 0)
        exit = trade_result.get("exit_price", 0)
        
        # Analyse seulement si perte
        if pnl >= 0:
            analysis["lessons"].append("Trade gagnant - renforcer ce pattern")
            self.post_trade_analyses.append(analysis)
            self._save_post_trade_analyses()
            return analysis
        
        # 1️⃣ Identifier les erreurs de timing
        asset_movement = market.get(asset, 0)
        
        if asset_movement < -1 and pnl < 0:
            analysis["errors_identified"].append({
                "type": "timing_error",
                "description": f"Entrée alors que {asset} était en baisse ({asset_movement:.2f}%)",
                "severity": "high",
                "avoidable": True
            })
            analysis["avoidable"] = True
            analysis["lessons"].append(f"Éviter d'entrer sur {asset} quand mouvement < -1%")
        
        # 2️⃣ Identifier les signaux invalides
        market_sentiment = sum(market.values()) / len(market) if market else 0
        
        if market_sentiment < -1 and pnl < 0:
            analysis["errors_identified"].append({
                "type": "invalid_signal",
                "description": f"Trade durant marché négatif (sentiment: {market_sentiment:.2f}%)",
                "severity": "high",
                "avoidable": True
            })
            analysis["avoidable"] = True
            analysis["lessons"].append("Ne jamais trader quand le marché global est négatif")
            
            # Enregistrer le signal invalide
            self.invalid_signals.append({
                "timestamp": analysis["timestamp"],
                "asset": asset,
                "market_sentiment": market_sentiment,
                "pnl": pnl,
                "reason": "negative_market_sentiment"
            })
            self._save_invalid_signals()
        
        # 3️⃣ Détecter les pertes évitables
        if entry > 0 and exit > 0:
            price_drop = ((exit - entry) / entry) * 100
            
            if price_drop < -5:
                analysis["errors_identified"].append({
                    "type": "avoidable_loss",
                    "description": f"Chute importante du prix: {price_drop:.2f}%",
                    "severity": "critical",
                    "avoidable": True
                })
                analysis["avoidable"] = True
                analysis["lessons"].append(f"Stop-loss trop large pour {asset} - réduire à 3%")
                
                # Enregistrer la perte évitable
                category = "large_drawdown"
                self.avoidable_losses["total_avoidable"] += 1
                self.avoidable_losses["total_amount"] += abs(pnl)
                
                if category not in self.avoidable_losses["categories"]:
                    self.avoidable_losses["categories"][category] = {"count": 0, "total_loss": 0}
                
                self.avoidable_losses["categories"][category]["count"] += 1
                self.avoidable_losses["categories"][category]["total_loss"] += abs(pnl)
                
                self._save_avoidable_losses()
        
        # 4️⃣ Identifier les biais stratégiques
        if asset in self.patterns.get("asset_specific", {}):
            asset_stats = self.patterns["asset_specific"][asset]
            if asset_stats["total"] >= 3:
                loss_rate = asset_stats["losses"] / asset_stats["total"]
                
                if loss_rate > 0.60:
                    analysis["errors_identified"].append({
                        "type": "strategic_bias",
                        "description": f"Asset {asset} a un taux de perte de {loss_rate:.1%}",
                        "severity": "medium",
                        "avoidable": True
                    })
                    analysis["avoidable"] = True
                    analysis["lessons"].append(f"Biais négatif confirmé sur {asset} - réduire exposition")
        
        # 5️⃣ Calculer le score d'amélioration
        # Plus le score est élevé, plus il y a de marge d'amélioration
        if analysis["avoidable"]:
            analysis["improvement_score"] = min(
                len(analysis["errors_identified"]) * 0.3 + abs(pnl) / 100,
                1.0
            )
        
        # Enregistrer l'analyse
        self.post_trade_analyses.append(analysis)
        self._save_post_trade_analyses()
        
        # Mettre à jour les erreurs récurrentes
        self._update_recurring_errors(analysis)
        
        # Générer des recommandations d'amélioration
        if analysis["errors_identified"]:
            self._generate_improvement_recommendations(analysis)
        
        return analysis
    
    def _update_recurring_errors(self, analysis: Dict):
        """Met à jour le suivi des erreurs récurrentes"""
        for error in analysis.get("errors_identified", []):
            error_type = error["type"]
            
            if error_type not in self.recurring_errors["error_types"]:
                self.recurring_errors["error_types"][error_type] = {
                    "count": 0,
                    "total_loss": 0,
                    "severity_distribution": Counter(),
                    "first_seen": datetime.utcnow().isoformat(),
                    "last_seen": None
                }
            
            self.recurring_errors["error_types"][error_type]["count"] += 1
            self.recurring_errors["error_types"][error_type]["total_loss"] += abs(analysis.get("pnl", 0))
            self.recurring_errors["error_types"][error_type]["severity_distribution"][error["severity"]] += 1
            self.recurring_errors["error_types"][error_type]["last_seen"] = datetime.utcnow().isoformat()
        
        self._save_recurring_errors()
    
    def _generate_improvement_recommendations(self, analysis: Dict):
        """Génère des recommandations d'amélioration basées sur l'analyse"""
        recommendations = []
        
        for error in analysis.get("errors_identified", []):
            error_type = error["type"]
            
            if error_type == "timing_error":
                recommendations.append({
                    "type": "rule_modification",
                    "priority": "high",
                    "action": "Ajouter filtre: ne pas entrer si mouvement asset < -1%",
                    "expected_impact": "Réduction des pertes de timing de ~30%"
                })
            
            elif error_type == "invalid_signal":
                recommendations.append({
                    "type": "signal_filtering",
                    "priority": "critical",
                    "action": "Bloquer trading si sentiment marché < -1%",
                    "expected_impact": "Élimination des trades en marché baissier"
                })
            
            elif error_type == "avoidable_loss":
                recommendations.append({
                    "type": "risk_adjustment",
                    "priority": "high",
                    "action": "Réduire stop-loss de 5% à 3%",
                    "expected_impact": "Protection contre drawdowns importants"
                })
            
            elif error_type == "strategic_bias":
                recommendations.append({
                    "type": "asset_filtering",
                    "priority": "medium",
                    "action": f"Blacklister temporairement {analysis.get('asset')}",
                    "expected_impact": "Éviter assets à biais négatif confirmé"
                })
        
        # Ajouter aux suggestions d'amélioration
        for rec in recommendations:
            if rec not in self.avoidable_losses.get("improvements_suggested", []):
                self.avoidable_losses.setdefault("improvements_suggested", []).append(rec)
        
        self._save_avoidable_losses()
    
    def detect_recurring_errors(self, min_occurrences: int = 3) -> List[Dict]:
        """
        Détecte les erreurs qui se répètent
        
        Args:
            min_occurrences: Nombre minimum d'occurrences pour considérer comme récurrent
        
        Returns:
            Liste des erreurs récurrentes avec détails
        """
        recurring = []
        
        for error_type, stats in self.recurring_errors.get("error_types", {}).items():
            if stats["count"] >= min_occurrences:
                recurring.append({
                    "error_type": error_type,
                    "occurrences": stats["count"],
                    "total_loss": round(stats["total_loss"], 2),
                    "avg_loss": round(stats["total_loss"] / stats["count"], 2),
                    "severity": max(stats["severity_distribution"], key=stats["severity_distribution"].get),
                    "first_seen": stats["first_seen"],
                    "last_seen": stats["last_seen"]
                })
        
        # Trier par nombre d'occurrences
        recurring.sort(key=lambda x: x["occurrences"], reverse=True)
        
        return recurring
    
    def auto_modify_trading_rules(self) -> Dict:
        """
        Modifie automatiquement les règles de trading basé sur les analyses
        
        Returns:
            Dict avec les modifications effectuées
        """
        modifications = {
            "timestamp": datetime.utcnow().isoformat(),
            "rules_modified": [],
            "new_filters_added": [],
            "parameters_adjusted": [],
            "justifications": []
        }
        
        # Analyser les erreurs récurrentes
        recurring_errors = self.detect_recurring_errors(min_occurrences=3)
        
        for error in recurring_errors:
            error_type = error["error_type"]
            
            # 1️⃣ Modifier les règles selon le type d'erreur
            if error_type == "timing_error" and error["occurrences"] >= 3:
                # Augmenter le seuil d'entrée
                old_threshold = self.state.get("min_gain_to_open", 0.5)
                new_threshold = min(old_threshold + 0.3, 2.0)
                self.state["min_gain_to_open"] = new_threshold
                
                modifications["parameters_adjusted"].append({
                    "parameter": "min_gain_to_open",
                    "old_value": old_threshold,
                    "new_value": new_threshold,
                    "reason": f"Erreur de timing récurrente ({error['occurrences']}x)"
                })
                modifications["justifications"].append(
                    f"Seuil d'entrée augmenté de {old_threshold}% à {new_threshold}% pour réduire erreurs de timing"
                )
            
            elif error_type == "invalid_signal" and error["occurrences"] >= 3:
                # Ajouter un filtre de sentiment de marché
                if "BLOCK_NEGATIVE_MARKET" not in self.state.get("avoid_patterns", []):
                    self.state.setdefault("avoid_patterns", []).append("BLOCK_NEGATIVE_MARKET")
                    
                    modifications["new_filters_added"].append({
                        "filter": "BLOCK_NEGATIVE_MARKET",
                        "condition": "market_sentiment < -1%",
                        "reason": f"Signaux invalides récurrents ({error['occurrences']}x)"
                    })
                    modifications["justifications"].append(
                        f"Ajout filtre bloquant trading en marché négatif (erreurs: {error['occurrences']}x, pertes: ${error['total_loss']:.2f})"
                    )
            
            elif error_type == "avoidable_loss" and error["occurrences"] >= 4:
                # Resserrer le stop-loss
                old_stop = self.state.get("max_loss_threshold", -50.0)
                new_stop = max(old_stop + 10, -25.0)  # Resserrer progressivement
                self.state["max_loss_threshold"] = new_stop
                
                modifications["parameters_adjusted"].append({
                    "parameter": "max_loss_threshold",
                    "old_value": old_stop,
                    "new_value": new_stop,
                    "reason": f"Pertes évitables récurrentes ({error['occurrences']}x)"
                })
                modifications["justifications"].append(
                    f"Stop-loss resserré de {old_stop} à {new_stop} pour limiter drawdowns (pertes évitées: ${error['total_loss']:.2f})"
                )
            
            elif error_type == "strategic_bias":
                # Augmenter la prudence sur certains assets
                modifications["rules_modified"].append({
                    "rule": "asset_filtering_enhanced",
                    "description": "Augmentation période d'observation avant trading asset à biais négatif",
                    "reason": f"Biais stratégique détecté ({error['occurrences']}x)"
                })
        
        # 2️⃣ Ajustements basés sur les pertes évitables
        avoidable_ratio = 0
        if self.state.get("total_trades", 0) > 0:
            avoidable_count = self.avoidable_losses.get("total_avoidable", 0)
            avoidable_ratio = avoidable_count / self.state["total_trades"]
        
        if avoidable_ratio > 0.30:  # Plus de 30% des pertes sont évitables
            # Réduire le niveau de risque global
            old_risk = self.state.get("risk_level", 0.5)
            new_risk = max(old_risk - 0.15, 0.3)
            self.state["risk_level"] = new_risk
            
            modifications["parameters_adjusted"].append({
                "parameter": "risk_level",
                "old_value": old_risk,
                "new_value": new_risk,
                "reason": f"Taux de pertes évitables élevé: {avoidable_ratio:.1%}"
            })
            modifications["justifications"].append(
                f"Réduction risque global: {avoidable_ratio:.1%} des trades sont des pertes évitables"
            )
        
        # Sauvegarder les changements
        if modifications["rules_modified"] or modifications["new_filters_added"] or modifications["parameters_adjusted"]:
            self._save_state()
            
            # Logger les modifications
            print(f"\n🔧 Modifications automatiques des règles de trading:")
            for justif in modifications["justifications"]:
                print(f"   ✓ {justif}")
        
        return modifications
    
    def get_improvement_metrics(self) -> Dict:
        """Retourne des métriques d'amélioration du système"""
        total_trades = self.state.get("total_trades", 0)
        
        return {
            "total_trades": total_trades,
            "total_analyses": len(self.post_trade_analyses),
            "recurring_errors": len(self.detect_recurring_errors()),
            "invalid_signals_detected": len(self.invalid_signals),
            "avoidable_losses": {
                "count": self.avoidable_losses.get("total_avoidable", 0),
                "total_amount": round(self.avoidable_losses.get("total_amount", 0), 2),
                "ratio": round(
                    self.avoidable_losses.get("total_avoidable", 0) / total_trades if total_trades > 0 else 0,
                    3
                )
            },
            "improvements_suggested": len(self.avoidable_losses.get("improvements_suggested", [])),
            "learning_rate": self.state.get("learning_rate", 0.1),
            "adaptive_adjustments": len(self.state.get("lessons_learned", []))
        }
    
    def _save_avoidable_losses(self):
        """Sauvegarde l'analyse des pertes évitables"""
        try:
            with open(self.avoidable_losses_file, "w", encoding="utf-8") as f:
                json.dump(self.avoidable_losses, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde pertes évitables: {e}")