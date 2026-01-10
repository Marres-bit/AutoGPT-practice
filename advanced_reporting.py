"""
Advanced Reporting System - Système de Reporting Automatisé Avancé
Génère des rapports détaillés toutes les 4h et quotidiens avec P&L, analyses et justifications
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


class AdvancedReportingSystem:
    """
    Système de reporting automatisé qui génère:
    - Rapports toutes les 4h avec analyse du cycle
    - Rapports quotidiens récapitulatifs
    - Rapports détaillés avec justifications et métriques
    """
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        self.daily_summary_file = self.project_root / "daily_summary.json"
        self.cycle_history_file = self.project_root / "cycle_history.json"
        
        self.daily_summary = self._load_daily_summary()
        self.cycle_history = self._load_cycle_history()
        
        # Déterminer le dossier Desktop
        self.desktop_path = Path.home() / "Desktop"
    
    def _load_daily_summary(self) -> Dict:
        """Charge le résumé quotidien ou initialise"""
        if self.daily_summary_file.exists():
            try:
                with open(self.daily_summary_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "date": datetime.utcnow().date().isoformat(),
            "trades": [],
            "total_pnl": 0.0,
            "winning_trades": 0,
            "losing_trades": 0,
            "best_trade": None,
            "worst_trade": None,
            "strategies_used": {},
            "adaptations_made": []
        }
    
    def _load_cycle_history(self) -> List[Dict]:
        """Charge l'historique des cycles"""
        if self.cycle_history_file.exists():
            try:
                with open(self.cycle_history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _save_daily_summary(self):
        """Sauvegarde le résumé quotidien"""
        try:
            with open(self.daily_summary_file, "w", encoding="utf-8") as f:
                json.dump(self.daily_summary, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde résumé quotidien: {e}")
    
    def _save_cycle_history(self):
        """Sauvegarde l'historique des cycles"""
        try:
            # Garder seulement les 100 derniers cycles
            with open(self.cycle_history_file, "w", encoding="utf-8") as f:
                json.dump(self.cycle_history[-100:], f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde historique: {e}")
    
    def generate_4h_report(self, cycle_data: Dict, learning_summary: Dict,
                          strategy_info: Dict) -> str:
        """
        Génère un rapport de cycle (toutes les 4h)
        
        Args:
            cycle_data: Données du cycle (trade, market, etc.)
            learning_summary: Résumé de l'apprentissage
            strategy_info: Informations sur la stratégie utilisée
        
        Returns:
            Chemin du rapport généré
        """
        timestamp = datetime.utcnow()
        filename = f"Rapport_Cycle_{timestamp.strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = self.desktop_path / filename
        
        # Créer le document
        doc = Document()
        
        # Style du document
        self._setup_document_style(doc)
        
        # ═══════════════════════════════════════════════════════
        # 📊 EN-TÊTE
        # ═══════════════════════════════════════════════════════
        title = doc.add_heading('📊 RAPPORT DE CYCLE - AGENT TRADING AI', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        subtitle = doc.add_paragraph(f"Généré le {timestamp.strftime('%d/%m/%Y à %H:%M:%S UTC')}")
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph("_" * 80)
        
        # ═══════════════════════════════════════════════════════
        # 📈 RÉSUMÉ FINANCIER
        # ═══════════════════════════════════════════════════════
        doc.add_heading('📈 Résumé Financier du Cycle', 1)
        
        trade = cycle_data.get("trade", {})
        pnl = trade.get("pnl", 0)
        capital = cycle_data.get("capital", {})
        
        # Table financière
        table = doc.add_table(rows=7, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.cell(0, 0).text = "Métrique"
        table.cell(0, 1).text = "Valeur"
        
        table.cell(1, 0).text = "💰 P&L du Cycle"
        table.cell(1, 1).text = f"${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        
        table.cell(2, 0).text = "💵 Capital Principal"
        table.cell(2, 1).text = f"${capital.get('principal', 0):,.2f}"
        
        table.cell(3, 0).text = "📊 Capital Investi"
        table.cell(3, 1).text = f"${capital.get('investment', 0):,.2f}"
        
        total_capital = capital.get('principal', 0) + capital.get('investment', 0)
        table.cell(4, 0).text = "💎 Capital Total"
        table.cell(4, 1).text = f"${total_capital:,.2f}"
        
        table.cell(5, 0).text = "📍 Asset Tradé"
        table.cell(5, 1).text = trade.get("asset", "N/A")
        
        table.cell(6, 0).text = "🎯 Résultat"
        result_text = "✅ GAIN" if pnl >= 0 else "❌ PERTE"
        table.cell(6, 1).text = result_text
        
        # ═══════════════════════════════════════════════════════
        # 🎯 DÉTAILS DU TRADE
        # ═══════════════════════════════════════════════════════
        doc.add_heading('🎯 Détails du Trade', 1)
        
        trade_table = doc.add_table(rows=5, cols=2)
        trade_table.style = 'Light Grid Accent 1'
        
        trade_table.cell(0, 0).text = "Détail"
        trade_table.cell(0, 1).text = "Valeur"
        
        trade_table.cell(1, 0).text = "Prix d'Entrée"
        trade_table.cell(1, 1).text = f"${trade.get('entry_price', 0):,.2f}"
        
        trade_table.cell(2, 0).text = "Prix de Sortie"
        trade_table.cell(2, 1).text = f"${trade.get('exit_price', 0):,.2f}"
        
        trade_table.cell(3, 0).text = "Quantité Tradée"
        trade_table.cell(3, 1).text = f"{trade.get('amount', 0):,.2f}"
        
        trade_table.cell(4, 0).text = "Fonds Retirés (Principal)"
        trade_table.cell(4, 1).text = f"${trade.get('withdrawn_to_principal', 0):.2f}"
        
        # ═══════════════════════════════════════════════════════
        # 📊 CONDITIONS DE MARCHÉ
        # ═══════════════════════════════════════════════════════
        doc.add_heading('📊 Conditions de Marché', 1)
        
        market = cycle_data.get("market", {})
        
        p = doc.add_paragraph()
        p.add_run("État du marché lors du trade:\n").bold = True
        
        for asset, change in sorted(market.items(), key=lambda x: x[1], reverse=True):
            color_emoji = "🟢" if change >= 0 else "🔴"
            p.add_run(f"\n{color_emoji} {asset}: {change:+.2f}%")
        
        # ═══════════════════════════════════════════════════════
        # 🧠 ANALYSE & APPRENTISSAGE
        # ═══════════════════════════════════════════════════════
        doc.add_heading('🧠 Analyse & Apprentissage', 1)
        
        learning_table = doc.add_table(rows=6, cols=2)
        learning_table.style = 'Light Grid Accent 1'
        
        learning_table.cell(0, 0).text = "Métrique d'Apprentissage"
        learning_table.cell(0, 1).text = "Valeur"
        
        learning_table.cell(1, 0).text = "📊 Taux de Réussite Global"
        learning_table.cell(1, 1).text = f"{learning_summary.get('win_rate', 0):.1%}"
        
        learning_table.cell(2, 0).text = "🎯 Total de Trades"
        learning_table.cell(2, 1).text = str(learning_summary.get('total_trades', 0))
        
        learning_table.cell(3, 0).text = "📚 Leçons Apprises"
        learning_table.cell(3, 1).text = str(learning_summary.get('lessons_learned', 0))
        
        learning_table.cell(4, 0).text = "⚠️ Patterns à Éviter"
        learning_table.cell(4, 1).text = str(learning_summary.get('patterns_identified', 0))
        
        learning_table.cell(5, 0).text = "📈 Niveau de Risque"
        risk_level = learning_summary.get('risk_level', 0.5)
        learning_table.cell(5, 1).text = f"{risk_level:.2f} ({'Conservateur' if risk_level < 0.4 else 'Modéré' if risk_level < 0.7 else 'Agressif'})"
        
        # Leçons récentes
        doc.add_heading('📚 Dernières Leçons Apprises', 2)
        recent_lessons = learning_summary.get('recent_lessons', [])
        
        if recent_lessons:
            for i, lesson in enumerate(recent_lessons[-5:], 1):
                doc.add_paragraph(f"{i}. {lesson}", style='List Bullet')
        else:
            doc.add_paragraph("Aucune leçon récente", style='List Bullet')
        
        # ═══════════════════════════════════════════════════════
        # 🎯 STRATÉGIE UTILISÉE
        # ═══════════════════════════════════════════════════════
        doc.add_heading('🎯 Stratégie de Trading Utilisée', 1)
        
        strategy_name = strategy_info.get("name", "Stratégie par défaut")
        strategy_type = strategy_info.get("type", "N/A")
        confidence = strategy_info.get("confidence", 0)
        
        doc.add_paragraph(f"Nom: {strategy_name}")
        doc.add_paragraph(f"Type: {strategy_type}")
        doc.add_paragraph(f"Confiance: {confidence:.1%}")
        
        # Règles appliquées
        rules = strategy_info.get("rules", [])
        if rules:
            doc.add_heading('Règles Appliquées:', 2)
            for rule in rules[:5]:  # Top 5 règles
                doc.add_paragraph(
                    f"• {rule.get('description', 'N/A')}",
                    style='List Bullet'
                )
        
        # ═══════════════════════════════════════════════════════
        # ✅ JUSTIFICATIONS DES DÉCISIONS
        # ═══════════════════════════════════════════════════════
        doc.add_heading('✅ Justifications des Décisions', 1)
        
        decision = cycle_data.get("decision", "HOLD")
        doc.add_paragraph(f"Décision prise: {decision}")
        
        # Justifications
        justifications = cycle_data.get("justifications", [])
        if justifications:
            for justif in justifications:
                doc.add_paragraph(f"• {justif}", style='List Bullet')
        else:
            # Générer des justifications basiques
            if decision == "OPEN_LONG":
                doc.add_paragraph(
                    f"• Asset {trade.get('asset')} montrait un mouvement positif de {market.get(trade.get('asset'), 0):.2f}%",
                    style='List Bullet'
                )
                doc.add_paragraph(
                    f"• Conditions de marché favorables selon l'analyse",
                    style='List Bullet'
                )
                doc.add_paragraph(
                    f"• Stratégie recommandée avec confiance de {confidence:.1%}",
                    style='List Bullet'
                )
        
        # ═══════════════════════════════════════════════════════
        # 📈 PROCHAIN CYCLE
        # ═══════════════════════════════════════════════════════
        doc.add_heading('📈 Planification du Prochain Cycle', 1)
        
        next_cycle_time = timestamp + timedelta(hours=4)
        doc.add_paragraph(f"Prochain cycle prévu: {next_cycle_time.strftime('%d/%m/%Y à %H:%M UTC')}")
        doc.add_paragraph(f"Stratégie: Adaptation continue selon performance")
        doc.add_paragraph(f"Objectif: Maintenir/améliorer le taux de réussite actuel de {learning_summary.get('win_rate', 0):.1%}")
        
        # Pied de page
        doc.add_paragraph("\n" + "_" * 80)
        footer = doc.add_paragraph(
            f"Rapport généré automatiquement par Agent Trading AI v2.0 | {timestamp.strftime('%d/%m/%Y %H:%M:%S UTC')}"
        )
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Sauvegarder
        try:
            doc.save(filepath)
            print(f"📄 Rapport 4h généré: {filepath}")
            
            # Enregistrer le cycle
            self._record_cycle(cycle_data, learning_summary, strategy_info)
            
            return str(filepath)
        except Exception as e:
            print(f"❌ Erreur génération rapport: {e}")
            return None
    
    def generate_daily_report(self) -> str:
        """
        Génère un rapport quotidien récapitulatif
        
        Returns:
            Chemin du rapport généré
        """
        timestamp = datetime.utcnow()
        filename = f"Rapport_Quotidien_{timestamp.strftime('%Y%m%d')}.docx"
        filepath = self.desktop_path / filename
        
        # Vérifier si on a des données pour aujourd'hui
        today = timestamp.date().isoformat()
        if self.daily_summary.get("date") != today:
            print("⚠️ Pas de données pour aujourd'hui")
            return None
        
        doc = Document()
        self._setup_document_style(doc)
        
        # ═══════════════════════════════════════════════════════
        # 📊 EN-TÊTE
        # ═══════════════════════════════════════════════════════
        title = doc.add_heading('📊 RAPPORT QUOTIDIEN - AGENT TRADING AI', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        subtitle = doc.add_paragraph(f"Journée du {timestamp.strftime('%d/%m/%Y')}")
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph("_" * 80)
        
        # ═══════════════════════════════════════════════════════
        # 💰 PERFORMANCE GLOBALE
        # ═══════════════════════════════════════════════════════
        doc.add_heading('💰 Performance Globale de la Journée', 1)
        
        total_pnl = self.daily_summary.get("total_pnl", 0)
        total_trades = len(self.daily_summary.get("trades", []))
        winning = self.daily_summary.get("winning_trades", 0)
        losing = self.daily_summary.get("losing_trades", 0)
        
        win_rate = winning / total_trades if total_trades > 0 else 0
        
        # Table performance
        perf_table = doc.add_table(rows=6, cols=2)
        perf_table.style = 'Light Grid Accent 1'
        
        perf_table.cell(0, 0).text = "Métrique"
        perf_table.cell(0, 1).text = "Valeur"
        
        perf_table.cell(1, 0).text = "💵 P&L Total Journalier"
        pnl_text = f"${total_pnl:.2f}" if total_pnl >= 0 else f"-${abs(total_pnl):.2f}"
        perf_table.cell(1, 1).text = pnl_text
        
        perf_table.cell(2, 0).text = "🎯 Nombre de Trades"
        perf_table.cell(2, 1).text = str(total_trades)
        
        perf_table.cell(3, 0).text = "✅ Trades Gagnants"
        perf_table.cell(3, 1).text = str(winning)
        
        perf_table.cell(4, 0).text = "❌ Trades Perdants"
        perf_table.cell(4, 1).text = str(losing)
        
        perf_table.cell(5, 0).text = "📊 Taux de Réussite"
        perf_table.cell(5, 1).text = f"{win_rate:.1%}"
        
        # ═══════════════════════════════════════════════════════
        # 🏆 MEILLEURS & PIRES TRADES
        # ═══════════════════════════════════════════════════════
        doc.add_heading('🏆 Meilleurs & Pires Trades', 1)
        
        best_trade = self.daily_summary.get("best_trade")
        worst_trade = self.daily_summary.get("worst_trade")
        
        if best_trade:
            doc.add_heading('✨ Meilleur Trade:', 2)
            doc.add_paragraph(f"Asset: {best_trade.get('asset')}")
            doc.add_paragraph(f"P&L: ${best_trade.get('pnl', 0):.2f}")
            doc.add_paragraph(f"Performance: {best_trade.get('performance_pct', 0):.2f}%")
        
        if worst_trade:
            doc.add_heading('⚠️ Pire Trade:', 2)
            doc.add_paragraph(f"Asset: {worst_trade.get('asset')}")
            doc.add_paragraph(f"P&L: ${worst_trade.get('pnl', 0):.2f}")
            doc.add_paragraph(f"Performance: {worst_trade.get('performance_pct', 0):.2f}%")
        
        # ═══════════════════════════════════════════════════════
        # 📈 STRATÉGIES UTILISÉES
        # ═══════════════════════════════════════════════════════
        doc.add_heading('📈 Stratégies Utilisées', 1)
        
        strategies = self.daily_summary.get("strategies_used", {})
        
        if strategies:
            strat_table = doc.add_table(rows=len(strategies) + 1, cols=3)
            strat_table.style = 'Light Grid Accent 1'
            
            strat_table.cell(0, 0).text = "Stratégie"
            strat_table.cell(0, 1).text = "Utilisations"
            strat_table.cell(0, 2).text = "Performance"
            
            for i, (name, stats) in enumerate(strategies.items(), 1):
                strat_table.cell(i, 0).text = name
                strat_table.cell(i, 1).text = str(stats.get("count", 0))
                strat_table.cell(i, 2).text = f"{stats.get('win_rate', 0):.1%}"
        else:
            doc.add_paragraph("Aucune stratégie spécifique utilisée")
        
        # ═══════════════════════════════════════════════════════
        # 🔧 OPTIMISATIONS & ADAPTATIONS
        # ═══════════════════════════════════════════════════════
        doc.add_heading('🔧 Optimisations & Adaptations de la Journée', 1)
        
        adaptations = self.daily_summary.get("adaptations_made", [])
        
        if adaptations:
            for adapt in adaptations:
                doc.add_paragraph(f"• {adapt}", style='List Bullet')
        else:
            doc.add_paragraph("Aucune adaptation majeure effectuée aujourd'hui")
        
        # ═══════════════════════════════════════════════════════
        # 📋 RECOMMANDATIONS POUR DEMAIN
        # ═══════════════════════════════════════════════════════
        doc.add_heading('📋 Recommandations pour le Prochain Cycle', 1)
        
        recommendations = self._generate_daily_recommendations()
        
        for rec in recommendations:
            doc.add_paragraph(f"• {rec}", style='List Bullet')
        
        # Pied de page
        doc.add_paragraph("\n" + "_" * 80)
        footer = doc.add_paragraph(
            f"Rapport quotidien généré automatiquement | {timestamp.strftime('%d/%m/%Y %H:%M:%S UTC')}"
        )
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Sauvegarder
        try:
            doc.save(filepath)
            print(f"📄 Rapport quotidien généré: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Erreur génération rapport quotidien: {e}")
            return None
    
    def _setup_document_style(self, doc: Document):
        """Configure le style du document"""
        # Style par défaut
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
    
    def _record_cycle(self, cycle_data: Dict, learning_summary: Dict, strategy_info: Dict):
        """Enregistre un cycle dans l'historique"""
        cycle_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "trade": cycle_data.get("trade"),
            "market": cycle_data.get("market"),
            "decision": cycle_data.get("decision"),
            "pnl": cycle_data.get("trade", {}).get("pnl", 0),
            "win_rate": learning_summary.get("win_rate", 0),
            "strategy": strategy_info.get("name"),
            "capital": cycle_data.get("capital")
        }
        
        self.cycle_history.append(cycle_record)
        self._save_cycle_history()
        
        # Mettre à jour le résumé quotidien
        today = datetime.utcnow().date().isoformat()
        
        if self.daily_summary.get("date") != today:
            # Nouveau jour
            self.daily_summary = {
                "date": today,
                "trades": [],
                "total_pnl": 0.0,
                "winning_trades": 0,
                "losing_trades": 0,
                "best_trade": None,
                "worst_trade": None,
                "strategies_used": {},
                "adaptations_made": []
            }
        
        # Ajouter le trade
        trade = cycle_data.get("trade", {})
        pnl = trade.get("pnl", 0)
        
        self.daily_summary["trades"].append(trade)
        self.daily_summary["total_pnl"] += pnl
        
        if pnl >= 0:
            self.daily_summary["winning_trades"] += 1
        else:
            self.daily_summary["losing_trades"] += 1
        
        # Mettre à jour meilleur/pire trade
        if not self.daily_summary["best_trade"] or pnl > self.daily_summary["best_trade"].get("pnl", 0):
            self.daily_summary["best_trade"] = trade.copy()
            self.daily_summary["best_trade"]["performance_pct"] = (pnl / (trade.get("entry_price", 1) * trade.get("amount", 1))) * 100
        
        if not self.daily_summary["worst_trade"] or pnl < self.daily_summary["worst_trade"].get("pnl", 0):
            self.daily_summary["worst_trade"] = trade.copy()
            self.daily_summary["worst_trade"]["performance_pct"] = (pnl / (trade.get("entry_price", 1) * trade.get("amount", 1))) * 100
        
        # Stratégies
        strategy_name = strategy_info.get("name", "default")
        if strategy_name not in self.daily_summary["strategies_used"]:
            self.daily_summary["strategies_used"][strategy_name] = {"count": 0, "wins": 0}
        
        self.daily_summary["strategies_used"][strategy_name]["count"] += 1
        if pnl >= 0:
            self.daily_summary["strategies_used"][strategy_name]["wins"] += 1
        
        # Calculer win rate de la stratégie
        strat_stats = self.daily_summary["strategies_used"][strategy_name]
        strat_stats["win_rate"] = strat_stats["wins"] / strat_stats["count"] if strat_stats["count"] > 0 else 0
        
        self._save_daily_summary()
    
    def _generate_daily_recommendations(self) -> List[str]:
        """Génère des recommandations pour le lendemain"""
        recommendations = []
        
        total_trades = len(self.daily_summary.get("trades", []))
        win_rate = 0
        if total_trades > 0:
            win_rate = self.daily_summary.get("winning_trades", 0) / total_trades
        
        total_pnl = self.daily_summary.get("total_pnl", 0)
        
        # Recommandations basées sur performance
        if win_rate >= 0.70:
            recommendations.append("✅ Excellente performance - Envisager d'augmenter légèrement le niveau de risque")
        elif win_rate >= 0.50:
            recommendations.append("✅ Performance satisfaisante - Maintenir la stratégie actuelle")
        else:
            recommendations.append("⚠️ Performance à améliorer - Réduire le risque et analyser les erreurs récurrentes")
        
        if total_pnl < 0:
            recommendations.append("📉 P&L négatif aujourd'hui - Réviser les critères d'entrée et stop-loss")
        
        if total_trades < 2:
            recommendations.append("📊 Peu de trades aujourd'hui - Vérifier les seuils d'entrée")
        elif total_trades > 8:
            recommendations.append("⚡ Volume de trading élevé - S'assurer de la qualité des signaux")
        
        # Recommandations stratégiques
        strategies = self.daily_summary.get("strategies_used", {})
        if strategies:
            best_strategy = max(strategies.items(), key=lambda x: x[1].get("win_rate", 0))
            recommendations.append(f"🎯 Stratégie la plus performante: {best_strategy[0]} ({best_strategy[1].get('win_rate', 0):.1%})")
        
        return recommendations
    
    def should_generate_daily_report(self) -> bool:
        """Détermine s'il faut générer un rapport quotidien"""
        now = datetime.utcnow()
        
        # Générer le rapport à minuit ou si on a au moins 1 trade dans la journée
        if now.hour == 0 or (now.hour == 23 and len(self.daily_summary.get("trades", [])) > 0):
            return True
        
        return False
    
    def get_cycle_statistics(self) -> Dict:
        """Retourne des statistiques sur les cycles"""
        recent_cycles = self.cycle_history[-20:] if self.cycle_history else []
        
        if not recent_cycles:
            return {"cycles": 0}
        
        total_pnl = sum(c.get("pnl", 0) for c in recent_cycles)
        avg_pnl = total_pnl / len(recent_cycles)
        
        winning_cycles = sum(1 for c in recent_cycles if c.get("pnl", 0) >= 0)
        win_rate = winning_cycles / len(recent_cycles)
        
        return {
            "cycles": len(recent_cycles),
            "total_pnl": round(total_pnl, 2),
            "avg_pnl": round(avg_pnl, 2),
            "win_rate": round(win_rate, 3),
            "winning_cycles": winning_cycles,
            "losing_cycles": len(recent_cycles) - winning_cycles
        }
