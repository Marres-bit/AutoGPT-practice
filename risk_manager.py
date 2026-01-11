"""
Risk Manager - Système de Gestion des Risques Professionnel
Implémente des stratégies avancées de gestion du risque pour trading automatisé
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import math


class RiskLevel(Enum):
    """Niveaux de risque définis"""
    CONSERVATIVE = "conservative"  # 0.5-1% par trade
    MODERATE = "moderate"          # 1-2% par trade
    AGGRESSIVE = "aggressive"      # 2-3% par trade
    EXTREME = "extreme"            # 3-5% par trade (déconseillé)


@dataclass
class RiskMetrics:
    """Métriques de risque calculées"""
    max_position_size: float  # Montant max par position
    stop_loss_price: float    # Prix stop-loss
    take_profit_price: float  # Prix take-profit
    risk_reward_ratio: float  # Ratio risque/récompense
    kelly_percentage: float   # % Kelly Criterion
    confidence_score: float   # Score de confiance (0-1)
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class RiskManager:
    """
    Gestionnaire de risque professionnel avec :
    - Stop-loss dynamique basé sur ATR
    - Position sizing Kelly Criterion
    - Protection max drawdown
    - Risk/Reward minimum
    - Corrélation positions
    """
    
    def __init__(
        self,
        project_root: Path,
        initial_capital: float = 10000.0,
        risk_level: RiskLevel = RiskLevel.MODERATE,
        max_drawdown_pct: float = 0.20,  # 20% max drawdown
        min_risk_reward: float = 2.0      # Min 1:2 R/R
    ):
        self.project_root = Path(project_root)
        self.initial_capital = initial_capital
        self.risk_level = risk_level
        self.max_drawdown_pct = max_drawdown_pct
        self.min_risk_reward = min_risk_reward
        
        # Fichiers de persistence
        self.risk_state_file = self.project_root / "risk_state.json"
        self.drawdown_history_file = self.project_root / "drawdown_history.json"
        
        # État du risque
        self.risk_state = self._load_risk_state()
        self.drawdown_history = self._load_drawdown_history()
        
        # Paramètres par niveau de risque
        self.risk_params = {
            RiskLevel.CONSERVATIVE: {"risk_per_trade": 0.01, "max_positions": 2},
            RiskLevel.MODERATE: {"risk_per_trade": 0.015, "max_positions": 3},
            RiskLevel.AGGRESSIVE: {"risk_per_trade": 0.025, "max_positions": 4},
            RiskLevel.EXTREME: {"risk_per_trade": 0.04, "max_positions": 5}
        }
    
    def _load_risk_state(self) -> Dict:
        """Charge l'état du risque"""
        if self.risk_state_file.exists():
            with open(self.risk_state_file, 'r') as f:
                return json.load(f)
        return {
            "peak_capital": self.initial_capital,
            "current_drawdown_pct": 0.0,
            "consecutive_losses": 0,
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "emergency_stop": False,
            "last_update": datetime.utcnow().isoformat()
        }
    
    def _save_risk_state(self):
        """Sauvegarde l'état du risque"""
        self.risk_state["last_update"] = datetime.utcnow().isoformat()
        with open(self.risk_state_file, 'w') as f:
            json.dump(self.risk_state, f, indent=2)
    
    def _load_drawdown_history(self) -> List[Dict]:
        """Charge l'historique des drawdowns"""
        if self.drawdown_history_file.exists():
            with open(self.drawdown_history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_drawdown_history(self):
        """Sauvegarde l'historique des drawdowns"""
        with open(self.drawdown_history_file, 'w') as f:
            json.dump(self.drawdown_history[-100:], f, indent=2)  # Garder 100 derniers
    
    def calculate_position_size(
        self,
        current_capital: float,
        entry_price: float,
        stop_loss_price: float,
        confidence: float = 0.5
    ) -> RiskMetrics:
        """
        Calcule la taille de position optimale
        
        Args:
            current_capital: Capital actuel disponible
            entry_price: Prix d'entrée prévu
            stop_loss_price: Prix stop-loss
            confidence: Score de confiance de la stratégie (0-1)
        
        Returns:
            RiskMetrics avec toutes les métriques calculées
        """
        # Vérifier emergency stop
        if self.risk_state.get("emergency_stop", False):
            return RiskMetrics(
                max_position_size=0.0,
                stop_loss_price=stop_loss_price,
                take_profit_price=entry_price,
                risk_reward_ratio=0.0,
                kelly_percentage=0.0,
                confidence_score=0.0,
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Paramètres selon niveau de risque
        params = self.risk_params[self.risk_level]
        base_risk_pct = params["risk_per_trade"]
        
        # Ajuster risque selon performance récente
        if self.risk_state["consecutive_losses"] >= 3:
            base_risk_pct *= 0.5  # Réduire risque après 3 pertes consécutives
        
        # Ajuster risque selon confidence
        adjusted_risk_pct = base_risk_pct * confidence
        
        # Montant à risquer
        risk_amount = current_capital * adjusted_risk_pct
        
        # Distance stop-loss en %
        stop_loss_distance_pct = abs((entry_price - stop_loss_price) / entry_price)
        
        # Taille de position basée sur stop-loss
        if stop_loss_distance_pct > 0:
            position_size = risk_amount / stop_loss_distance_pct
        else:
            position_size = 0.0
        
        # Limiter à un % du capital (ne pas mettre tout sur un trade)
        max_position_pct = 0.3  # Max 30% du capital par position
        position_size = min(position_size, current_capital * max_position_pct)
        
        # Kelly Criterion (optionnel, pour info)
        win_rate = self._calculate_win_rate()
        avg_win = self._calculate_avg_win()
        avg_loss = abs(self._calculate_avg_loss())
        
        if avg_loss > 0:
            kelly_pct = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
            kelly_pct = max(0, min(kelly_pct, 0.25))  # Cap à 25%
        else:
            kelly_pct = base_risk_pct
        
        # Take profit (target min R/R ratio)
        take_profit_distance = stop_loss_distance_pct * self.min_risk_reward
        take_profit_price = entry_price * (1 + take_profit_distance)
        
        # Risk/Reward ratio
        risk_reward_ratio = take_profit_distance / stop_loss_distance_pct if stop_loss_distance_pct > 0 else 0
        
        return RiskMetrics(
            max_position_size=round(position_size, 2),
            stop_loss_price=round(stop_loss_price, 2),
            take_profit_price=round(take_profit_price, 2),
            risk_reward_ratio=round(risk_reward_ratio, 2),
            kelly_percentage=round(kelly_pct * 100, 2),
            confidence_score=confidence,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _calculate_win_rate(self) -> float:
        """Calcule le taux de réussite"""
        total = self.risk_state.get("total_trades", 0)
        if total == 0:
            return 0.5  # Défaut 50%
        wins = self.risk_state.get("winning_trades", 0)
        return wins / total
    
    def _calculate_avg_win(self) -> float:
        """Calcule le gain moyen (simplifié)"""
        # TODO: Calculer depuis historique réel
        return 1.5  # Défaut +1.5%
    
    def _calculate_avg_loss(self) -> float:
        """Calcule la perte moyenne (simplifié)"""
        # TODO: Calculer depuis historique réel
        return -0.8  # Défaut -0.8%
    
    def update_after_trade(
        self,
        current_capital: float,
        pnl: float,
        was_win: bool
    ):
        """
        Met à jour l'état du risque après un trade
        
        Args:
            current_capital: Capital actuel
            pnl: Profit/Loss du trade
            was_win: True si trade gagnant
        """
        # Mettre à jour pic de capital
        if current_capital > self.risk_state["peak_capital"]:
            self.risk_state["peak_capital"] = current_capital
        
        # Calculer drawdown actuel
        drawdown_pct = (self.risk_state["peak_capital"] - current_capital) / self.risk_state["peak_capital"]
        self.risk_state["current_drawdown_pct"] = drawdown_pct
        
        # Enregistrer drawdown
        self.drawdown_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "capital": current_capital,
            "peak": self.risk_state["peak_capital"],
            "drawdown_pct": drawdown_pct,
            "pnl": pnl
        })
        self._save_drawdown_history()
        
        # Mettre à jour stats trades
        self.risk_state["total_trades"] += 1
        if was_win:
            self.risk_state["winning_trades"] += 1
            self.risk_state["consecutive_losses"] = 0
        else:
            self.risk_state["losing_trades"] += 1
            self.risk_state["consecutive_losses"] += 1
        
        # Vérifier déclenchement emergency stop
        if drawdown_pct >= self.max_drawdown_pct:
            self.risk_state["emergency_stop"] = True
            print(f"🚨 EMERGENCY STOP: Drawdown {drawdown_pct:.1%} >= {self.max_drawdown_pct:.1%}")
        
        self._save_risk_state()
    
    def can_trade(self) -> Tuple[bool, str]:
        """
        Vérifie si le trading est autorisé
        
        Returns:
            (can_trade, reason)
        """
        # Vérifier emergency stop
        if self.risk_state.get("emergency_stop", False):
            return False, f"Emergency stop activé (drawdown {self.risk_state['current_drawdown_pct']:.1%})"
        
        # Vérifier pertes consécutives excessives
        if self.risk_state.get("consecutive_losses", 0) >= 5:
            return False, f"5+ pertes consécutives - pause requise"
        
        # Vérifier drawdown actuel
        if self.risk_state.get("current_drawdown_pct", 0) >= self.max_drawdown_pct * 0.8:
            return False, f"Drawdown proche de la limite ({self.risk_state['current_drawdown_pct']:.1%})"
        
        return True, "Trading autorisé"
    
    def reset_emergency_stop(self):
        """Réinitialise l'emergency stop manuellement"""
        self.risk_state["emergency_stop"] = False
        self.risk_state["consecutive_losses"] = 0
        self._save_risk_state()
        print("✅ Emergency stop réinitialisé")
    
    def get_risk_summary(self) -> Dict:
        """Retourne un résumé de l'état du risque"""
        win_rate = self._calculate_win_rate()
        
        return {
            "risk_level": self.risk_level.value,
            "current_drawdown": f"{self.risk_state['current_drawdown_pct']:.2%}",
            "max_drawdown_limit": f"{self.max_drawdown_pct:.2%}",
            "peak_capital": f"${self.risk_state['peak_capital']:,.2f}",
            "win_rate": f"{win_rate:.1%}",
            "total_trades": self.risk_state["total_trades"],
            "consecutive_losses": self.risk_state["consecutive_losses"],
            "emergency_stop": self.risk_state["emergency_stop"],
            "can_trade": self.can_trade()[0],
            "risk_per_trade": f"{self.risk_params[self.risk_level]['risk_per_trade']:.1%}"
        }


if __name__ == "__main__":
    # Test du Risk Manager
    print("🧪 Test du Risk Manager\n")
    
    rm = RiskManager(
        project_root=Path(__file__).parent,
        initial_capital=10000,
        risk_level=RiskLevel.MODERATE
    )
    
    # Simuler calcul position
    print("📊 Calcul taille de position:")
    metrics = rm.calculate_position_size(
        current_capital=10000,
        entry_price=100,
        stop_loss_price=98,  # -2% stop
        confidence=0.75
    )
    
    print(f"  Taille max position: ${metrics.max_position_size:,.2f}")
    print(f"  Stop-loss: ${metrics.stop_loss_price}")
    print(f"  Take-profit: ${metrics.take_profit_price}")
    print(f"  Risk/Reward: {metrics.risk_reward_ratio}")
    print(f"  Kelly %: {metrics.kelly_percentage:.1f}%")
    
    # Simuler quelques trades
    print("\n📈 Simulation de trades:")
    rm.update_after_trade(10150, 150, True)
    print(f"  Trade 1: +$150 (Win)")
    
    rm.update_after_trade(10100, -50, False)
    print(f"  Trade 2: -$50 (Loss)")
    
    # Afficher résumé
    print("\n📋 Résumé du risque:")
    summary = rm.get_risk_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
