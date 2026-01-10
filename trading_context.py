"""
Module de contexte de trading pour l'agent conversationnel
Permet à l'agent d'accéder à ses propres données de performance
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class TradingContextProvider:
    """
    Fournit le contexte de trading à l'agent conversationnel
    pour qu'il puisse discuter de ses performances
    """
    
    def __init__(self, project_root: Path = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        self.learning_file = self.project_root / "learning_state.json"
        self.mistakes_log = self.project_root / "mistakes_log.json"
        self.patterns_file = self.project_root / "error_patterns.json"
        self.summary_file = self.project_root / "last_cycle_summary.txt"
        self.capital_file = self.project_root / "capital_state.json"
        self.log_file = self.project_root / "sp_agent.log"
    
    def get_full_context(self) -> str:
        """
        Génère un contexte complet pour l'agent conversationnel
        Returns: Texte formaté avec toutes les infos de trading
        """
        context_parts = []
        
        context_parts.append("=== CONTEXTE DE TRADING (Mes Performances) ===\n")
        
        # 1. État d'apprentissage
        learning_context = self._get_learning_context()
        if learning_context:
            context_parts.append(learning_context)
        
        # 2. Capital actuel
        capital_context = self._get_capital_context()
        if capital_context:
            context_parts.append(capital_context)
        
        # 3. Dernier cycle
        summary_context = self._get_summary_context()
        if summary_context:
            context_parts.append(summary_context)
        
        # 4. Erreurs récentes
        mistakes_context = self._get_mistakes_context()
        if mistakes_context:
            context_parts.append(mistakes_context)
        
        # 5. Patterns détectés
        patterns_context = self._get_patterns_context()
        if patterns_context:
            context_parts.append(patterns_context)
        
        # 6. Logs récents
        logs_context = self._get_recent_logs()
        if logs_context:
            context_parts.append(logs_context)
        
        context_parts.append("\n=== FIN DU CONTEXTE ===\n")
        context_parts.append("\nJe peux maintenant discuter de mes performances, expliquer mes décisions, ")
        context_parts.append("analyser mes erreurs et répondre à tes questions sur mon trading.\n")
        
        return "\n".join(context_parts)
    
    def _get_learning_context(self) -> Optional[str]:
        """Charge l'état d'apprentissage"""
        if not self.learning_file.exists():
            return None
        
        try:
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            text = ["\n📊 ÉTAT D'APPRENTISSAGE:"]
            text.append(f"  - Trades totaux: {state.get('total_trades', 0)}")
            text.append(f"  - Trades gagnants: {state.get('winning_trades', 0)}")
            text.append(f"  - Trades perdants: {state.get('losing_trades', 0)}")
            text.append(f"  - Win Rate: {state.get('win_rate', 0):.1%}")
            text.append(f"  - Pertes consécutives: {state.get('consecutive_losses', 0)}")
            text.append(f"  - Niveau de risque: {state.get('risk_level', 0.5):.2f}")
            text.append(f"  - Seuil d'entrée: {state.get('min_gain_to_open', 0.5)}%")
            text.append(f"  - Stop-loss max: {state.get('max_loss_threshold', -50)}€")
            
            if state.get('avoid_patterns'):
                text.append(f"\n  ⚠️ Patterns que j'évite:")
                for pattern in state['avoid_patterns']:
                    text.append(f"    • {pattern}")
            
            if state.get('lessons_learned'):
                text.append(f"\n  🎓 Leçons que j'ai apprises ({len(state['lessons_learned'])}):")
                for lesson in state['lessons_learned'][-5:]:  # 5 dernières
                    text.append(f"    • {lesson}")
            
            text.append(f"\n  📅 Dernière mise à jour: {state.get('last_updated', 'N/A')}")
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture apprentissage: {e}"
    
    def _get_capital_context(self) -> Optional[str]:
        """Charge l'état du capital"""
        if not self.capital_file.exists():
            return None
        
        try:
            with open(self.capital_file, 'r', encoding='utf-8') as f:
                capital = json.load(f)
            
            principal = capital.get('principal', 0)
            investment = capital.get('investment', 0)
            total = principal + investment
            
            text = ["\n💰 CAPITAL ACTUEL:"]
            text.append(f"  - Capital principal: {principal:,.2f}€".replace(',', ' '))
            text.append(f"  - Capital investi: {investment:,.2f}€".replace(',', ' '))
            text.append(f"  - Total: {total:,.2f}€".replace(',', ' '))
            
            # Calculer le profit/perte depuis le début (si on connaît le capital initial)
            # Supposons capital initial = 10000€
            initial_capital = 10000.0
            if total != initial_capital:
                pnl = total - initial_capital
                pnl_pct = (pnl / initial_capital) * 100
                text.append(f"  - P&L total: {pnl:+,.2f}€ ({pnl_pct:+.2f}%)".replace(',', ' '))
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture capital: {e}"
    
    def _get_summary_context(self) -> Optional[str]:
        """Charge le dernier cycle"""
        if not self.summary_file.exists():
            return None
        
        try:
            with open(self.summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            text = ["\n📋 DERNIER CYCLE:"]
            # Extraire les infos importantes
            lines = content.split('\n')
            for line in lines[:15]:  # Premières 15 lignes
                if line.strip():
                    text.append(f"  {line}")
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture résumé: {e}"
    
    def _get_mistakes_context(self) -> Optional[str]:
        """Charge les erreurs récentes"""
        if not self.mistakes_log.exists():
            return None
        
        try:
            with open(self.mistakes_log, 'r', encoding='utf-8') as f:
                mistakes = json.load(f)
            
            if not mistakes:
                return "\n✅ Aucune erreur enregistrée (ou pas encore de trades perdants)"
            
            text = [f"\n❌ MES DERNIÈRES ERREURS ({len(mistakes)} total):"]
            
            # Afficher les 3 dernières
            for mistake in mistakes[-3:]:
                text.append(f"\n  Trade perdant:")
                text.append(f"    • Asset: {mistake.get('asset')}")
                text.append(f"    • Perte: {mistake.get('pnl', 0):.2f}€")
                text.append(f"    • Date: {mistake.get('timestamp', 'N/A')[:19]}")
                text.append(f"    • Leçon: {mistake.get('lesson', 'N/A')}")
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture erreurs: {e}"
    
    def _get_patterns_context(self) -> Optional[str]:
        """Charge les patterns détectés"""
        if not self.patterns_file.exists():
            return None
        
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
            
            text = ["\n🔍 PATTERNS DÉTECTÉS:"]
            
            # Assets spécifiques
            if patterns.get('asset_specific'):
                text.append("\n  📊 Performance par Asset:")
                for asset, stats in patterns['asset_specific'].items():
                    if stats['total'] > 0:
                        loss_rate = stats['losses'] / stats['total']
                        text.append(f"    • {asset}: {stats['losses']}/{stats['total']} pertes ({loss_rate:.1%})")
            
            # Patterns de perte
            if patterns.get('loss_patterns'):
                text.append(f"\n  ⚠️ Patterns de perte identifiés ({len(patterns['loss_patterns'])}):")
                for pattern in patterns['loss_patterns'][-3:]:
                    text.append(f"    • {pattern.get('type')}")
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture patterns: {e}"
    
    def _get_recent_logs(self, lines: int = 20) -> Optional[str]:
        """Charge les logs récents"""
        if not self.log_file.exists():
            return None
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            recent = all_lines[-lines:]
            
            text = [f"\n📝 LOGS RÉCENTS ({lines} dernières lignes):"]
            for line in recent:
                if line.strip():
                    # Simplifier la ligne pour le contexte
                    text.append(f"  {line.strip()}")
            
            return "\n".join(text)
        except Exception as e:
            return f"\n⚠️ Erreur lecture logs: {e}"
    
    def get_statistics_summary(self) -> Dict:
        """
        Retourne un résumé statistique pour analyse
        """
        stats = {
            "available": False,
            "total_trades": 0,
            "win_rate": 0.0,
            "total_pnl": 0.0,
            "current_capital": 0.0,
            "lessons_learned": 0,
            "patterns_detected": 0
        }
        
        try:
            # Learning state
            if self.learning_file.exists():
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    learning = json.load(f)
                stats["total_trades"] = learning.get("total_trades", 0)
                stats["win_rate"] = learning.get("win_rate", 0.0)
                stats["lessons_learned"] = len(learning.get("lessons_learned", []))
                stats["patterns_detected"] = len(learning.get("avoid_patterns", []))
            
            # Capital
            if self.capital_file.exists():
                with open(self.capital_file, 'r', encoding='utf-8') as f:
                    capital = json.load(f)
                stats["current_capital"] = capital.get("principal", 0) + capital.get("investment", 0)
                stats["total_pnl"] = stats["current_capital"] - 10000  # Initial assumed 10k
            
            stats["available"] = True
        except Exception:
            pass
        
        return stats
    
    def format_context_for_prompt(self) -> str:
        """
        Formate le contexte pour l'inclure dans le prompt système
        """
        return f"""
Tu es un agent de trading AI autonome. Tu as accès à tes propres données de performance.

IMPORTANT: Quand l'utilisateur te pose des questions sur tes trades, tes performances, 
tes erreurs ou ton apprentissage, tu DOIS utiliser les informations ci-dessous pour 
répondre de manière précise et détaillée.

{self.get_full_context()}

Tu peux maintenant:
- Expliquer tes décisions de trading
- Analyser tes erreurs passées
- Discuter de ton apprentissage
- Donner des statistiques précises
- Parler de ta stratégie actuelle

Réponds toujours en te basant sur tes VRAIES données ci-dessus, pas sur des hypothèses.
"""


def get_trading_context() -> str:
    """Fonction helper pour obtenir le contexte rapidement"""
    provider = TradingContextProvider()
    return provider.format_context_for_prompt()


def get_trading_stats() -> Dict:
    """Fonction helper pour obtenir les stats rapidement"""
    provider = TradingContextProvider()
    return provider.get_statistics_summary()
