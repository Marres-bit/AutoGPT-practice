"""
Générateur de rapport final après 2 jours de test
Analyse complète des performances et recommandations pour passage en production
"""

from pathlib import Path
import json
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


class FinalReportGenerator:
    def __init__(self, project_root: Path | str | None = None):
        """Initialize report generator"""
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        
    def generate_final_report(self, output_dir: Path | str | None = None):
        """
        Génère le rapport final après 2 jours de test
        Retourne le chemin du fichier généré
        """
        output_dir = Path(output_dir) if output_dir else Path.home() / "Desktop"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Collecter les données
        data = self._collect_all_data()
        
        # Créer le document Word
        doc = Document()
        
        # =============== TITRE ===============
        title = doc.add_heading("RAPPORT FINAL - TEST AGENT AI TRADING", level=0)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        subtitle = doc.add_paragraph()
        subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        run = subtitle.add_run(f"Analyse des performances après 2 jours de test\n{datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(128, 128, 128)
        
        doc.add_paragraph()  # Espace
        
        # =============== RÉSUMÉ EXÉCUTIF ===============
        doc.add_heading("📊 RÉSUMÉ EXÉCUTIF", level=1)
        
        summary_table = doc.add_table(rows=7, cols=2)
        summary_table.style = 'Light Grid Accent 1'
        
        summary_data = [
            ["Trades totaux", str(data["total_trades"])],
            ["Trades gagnants", f"{data['winning_trades']} ({data['win_rate']:.1%})"],
            ["Trades perdants", f"{data['losing_trades']} ({data['loss_rate']:.1%})"],
            ["Capital initial", f"{data['initial_capital']:.2f} €"],
            ["Capital final", f"{data['final_capital']:.2f} €"],
            ["Profit/Perte total", f"{data['total_pnl']:.2f} € ({data['pnl_percent']:+.2f}%)"],
            ["Performance moyenne par trade", f"{data['avg_pnl_per_trade']:.2f} €"]
        ]
        
        for i, (label, value) in enumerate(summary_data):
            row = summary_table.rows[i]
            row.cells[0].text = label
            row.cells[1].text = value
        
        doc.add_paragraph()
        
        # =============== ANALYSE DÉTAILLÉE ===============
        doc.add_heading("🔍 ANALYSE DÉTAILLÉE DES PERFORMANCES", level=1)
        
        # Performance par actif
        doc.add_heading("Performance par actif:", level=2)
        if data["performance_by_asset"]:
            for asset, stats in data["performance_by_asset"].items():
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f"{asset}: ").bold = True
                p.add_run(f"{stats['trades']} trades, Win rate: {stats['win_rate']:.1%}, ")
                p.add_run(f"P&L total: {stats['total_pnl']:.2f} €")
        else:
            doc.add_paragraph("Aucune donnée disponible.")
        
        doc.add_paragraph()
        
        # Meilleurs et pires trades
        doc.add_heading("📈 Meilleur trade:", level=2)
        if data["best_trade"]:
            best = data["best_trade"]
            p = doc.add_paragraph()
            p.add_run(f"{best['asset']} - Profit: {best['pnl']:.2f} € ({best['pnl_percent']:+.2f}%)\n").bold = True
            p.add_run(f"Date: {best['date']}\n")
            p.add_run(f"Entry: {best['entry_price']:.2f} € → Exit: {best['exit_price']:.2f} €")
        else:
            doc.add_paragraph("Aucun trade profitable.")
        
        doc.add_heading("📉 Pire trade:", level=2)
        if data["worst_trade"]:
            worst = data["worst_trade"]
            p = doc.add_paragraph()
            p.add_run(f"{worst['asset']} - Perte: {worst['pnl']:.2f} € ({worst['pnl_percent']:.2f}%)\n").bold = True
            p.add_run(f"Date: {worst['date']}\n")
            p.add_run(f"Entry: {worst['entry_price']:.2f} € → Exit: {worst['exit_price']:.2f} €")
        else:
            doc.add_paragraph("Aucun trade perdant.")
        
        doc.add_paragraph()
        
        # =============== APPRENTISSAGE ===============
        doc.add_heading("🧠 SYSTÈME D'APPRENTISSAGE", level=1)
        
        doc.add_heading("Évolution du niveau de risque:", level=2)
        doc.add_paragraph(f"Niveau actuel: {data['current_risk_level']:.2f} (0 = prudent, 1 = agressif)")
        
        doc.add_heading("Seuil d'entrée adaptatif:", level=2)
        doc.add_paragraph(f"Seuil minimal actuel: {data['current_entry_threshold']:.2f}%")
        
        doc.add_heading("Leçons apprises ({} au total):".format(len(data["lessons_learned"])), level=2)
        if data["lessons_learned"]:
            for i, lesson in enumerate(data["lessons_learned"][-10:], 1):  # Dernières 10 leçons
                doc.add_paragraph(f"{i}. {lesson}", style='List Bullet')
        else:
            doc.add_paragraph("Aucune leçon enregistrée.")
        
        doc.add_heading("Erreurs détectées ({} au total):".format(len(data["mistakes"])), level=2)
        if data["mistakes"]:
            for mistake in data["mistakes"][-5:]:  # Dernières 5 erreurs
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f"[{mistake['date']}] ").italic = True
                p.add_run(f"{mistake['asset']}: {mistake['pnl']:.2f} € - {mistake['lesson']}")
        else:
            doc.add_paragraph("Aucune erreur enregistrée.")
        
        doc.add_heading("Patterns détectés:", level=2)
        if data["error_patterns"]:
            for pattern_id, pattern_data in data["error_patterns"].items():
                doc.add_paragraph(f"• {pattern_id}: {pattern_data.get('description', 'N/A')}", style='List Bullet')
        else:
            doc.add_paragraph("Aucun pattern d'erreur détecté.")
        
        doc.add_paragraph()
        
        # =============== RECOMMANDATIONS ===============
        doc.add_heading("💡 RECOMMANDATIONS & CONCLUSION", level=1)
        
        recommendations = self._generate_recommendations(data)
        
        doc.add_heading("Recommandation pour la production:", level=2)
        rec_paragraph = doc.add_paragraph()
        rec_run = rec_paragraph.add_run(recommendations["production_ready"])
        rec_run.font.size = Pt(14)
        rec_run.bold = True
        if "✅" in recommendations["production_ready"]:
            rec_run.font.color.rgb = RGBColor(0, 128, 0)
        elif "⚠️" in recommendations["production_ready"]:
            rec_run.font.color.rgb = RGBColor(255, 165, 0)
        else:
            rec_run.font.color.rgb = RGBColor(255, 0, 0)
        
        doc.add_heading("Raisons:", level=3)
        for reason in recommendations["reasons"]:
            doc.add_paragraph(reason, style='List Bullet')
        
        doc.add_heading("Actions recommandées:", level=2)
        for action in recommendations["actions"]:
            doc.add_paragraph(action, style='List Number')
        
        if recommendations["needs_more_time"]:
            doc.add_heading("⏰ Durée supplémentaire recommandée:", level=2)
            doc.add_paragraph(recommendations["additional_time_needed"])
        
        doc.add_paragraph()
        
        # =============== ANNEXES ===============
        doc.add_heading("📎 ANNEXES", level=1)
        
        doc.add_heading("Configuration actuelle:", level=2)
        config_para = doc.add_paragraph()
        config_para.add_run(json.dumps(data["current_config"], indent=2))
        config_para.style = 'Intense Quote'
        
        # Sauvegarder le document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Rapport_Final_2jours_{timestamp}.docx"
        filepath = output_dir / filename
        doc.save(filepath)
        
        print(f"✅ Rapport final généré: {filepath}")
        return filepath
    
    def _collect_all_data(self):
        """Collecte toutes les données nécessaires pour le rapport"""
        data = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "initial_capital": 10000.0,
            "final_capital": 10000.0,
            "total_pnl": 0.0,
            "pnl_percent": 0.0,
            "avg_pnl_per_trade": 0.0,
            "win_rate": 0.0,
            "loss_rate": 0.0,
            "performance_by_asset": {},
            "best_trade": None,
            "worst_trade": None,
            "lessons_learned": [],
            "mistakes": [],
            "error_patterns": {},
            "current_risk_level": 0.5,
            "current_entry_threshold": 0.5,
            "current_config": {}
        }
        
        # Charger learning_state.json
        learning_state_path = self.project_root / "learning_state.json"
        if learning_state_path.exists():
            with open(learning_state_path, "r", encoding="utf-8") as f:
                learning_state = json.load(f)
                data["total_trades"] = learning_state.get("total_trades", 0)
                data["winning_trades"] = learning_state.get("winning_trades", 0)
                data["losing_trades"] = learning_state.get("losing_trades", 0)
                data["current_risk_level"] = learning_state.get("risk_level", 0.5)
                data["current_entry_threshold"] = learning_state.get("min_gain_to_open", 0.5)
                data["lessons_learned"] = learning_state.get("lessons_learned", [])
                
                if data["total_trades"] > 0:
                    data["win_rate"] = data["winning_trades"] / data["total_trades"]
                    data["loss_rate"] = data["losing_trades"] / data["total_trades"]
        
        # Charger capital_state.json
        capital_path = self.project_root / "capital_state.json"
        if capital_path.exists():
            with open(capital_path, "r", encoding="utf-8") as f:
                capital = json.load(f)
                data["final_capital"] = capital.get("principal", 10000.0) + capital.get("investment", 0.0)
                data["total_pnl"] = data["final_capital"] - data["initial_capital"]
                if data["initial_capital"] > 0:
                    data["pnl_percent"] = (data["total_pnl"] / data["initial_capital"]) * 100
                if data["total_trades"] > 0:
                    data["avg_pnl_per_trade"] = data["total_pnl"] / data["total_trades"]
        
        # Charger mistakes_log.json
        mistakes_path = self.project_root / "mistakes_log.json"
        if mistakes_path.exists():
            with open(mistakes_path, "r", encoding="utf-8") as f:
                mistakes_data = json.load(f)
                data["mistakes"] = mistakes_data.get("mistakes", [])
                
                # Analyser performance par actif
                asset_stats = {}
                best_trade = None
                worst_trade = None
                
                for mistake in data["mistakes"]:
                    asset = mistake.get("asset")
                    pnl = mistake.get("pnl", 0)
                    
                    if asset not in asset_stats:
                        asset_stats[asset] = {
                            "trades": 0,
                            "wins": 0,
                            "losses": 0,
                            "total_pnl": 0.0,
                            "win_rate": 0.0
                        }
                    
                    asset_stats[asset]["trades"] += 1
                    asset_stats[asset]["total_pnl"] += pnl
                    if pnl > 0:
                        asset_stats[asset]["wins"] += 1
                    else:
                        asset_stats[asset]["losses"] += 1
                    
                    # Calculer win rate
                    if asset_stats[asset]["trades"] > 0:
                        asset_stats[asset]["win_rate"] = asset_stats[asset]["wins"] / asset_stats[asset]["trades"]
                    
                    # Trouver meilleur/pire trade
                    if best_trade is None or pnl > best_trade.get("pnl", float('-inf')):
                        best_trade = {
                            "asset": asset,
                            "pnl": pnl,
                            "pnl_percent": mistake.get("pnl_percent", 0),
                            "date": mistake.get("date", "N/A"),
                            "entry_price": mistake.get("entry_price", 0),
                            "exit_price": mistake.get("exit_price", 0)
                        }
                    
                    if worst_trade is None or pnl < worst_trade.get("pnl", float('inf')):
                        worst_trade = {
                            "asset": asset,
                            "pnl": pnl,
                            "pnl_percent": mistake.get("pnl_percent", 0),
                            "date": mistake.get("date", "N/A"),
                            "entry_price": mistake.get("entry_price", 0),
                            "exit_price": mistake.get("exit_price", 0)
                        }
                
                data["performance_by_asset"] = asset_stats
                data["best_trade"] = best_trade
                data["worst_trade"] = worst_trade
        
        # Charger error_patterns.json
        patterns_path = self.project_root / "error_patterns.json"
        if patterns_path.exists():
            with open(patterns_path, "r", encoding="utf-8") as f:
                data["error_patterns"] = json.load(f)
        
        # Configuration actuelle
        data["current_config"] = {
            "risk_level": data["current_risk_level"],
            "entry_threshold": data["current_entry_threshold"],
            "total_trades": data["total_trades"],
            "win_rate": f"{data['win_rate']:.1%}",
            "capital": f"{data['final_capital']:.2f} €"
        }
        
        return data
    
    def _generate_recommendations(self, data):
        """Génère les recommandations basées sur les données"""
        recommendations = {
            "production_ready": "",
            "reasons": [],
            "actions": [],
            "needs_more_time": False,
            "additional_time_needed": ""
        }
        
        win_rate = data["win_rate"]
        total_trades = data["total_trades"]
        pnl_percent = data["pnl_percent"]
        
        # Critères de décision
        is_profitable = pnl_percent > 0
        has_good_win_rate = win_rate >= 0.50  # Au moins 50% de trades gagnants
        has_enough_trades = total_trades >= 20  # Au moins 20 trades pour validation
        
        # Décision finale
        if is_profitable and has_good_win_rate and has_enough_trades:
            recommendations["production_ready"] = "✅ PRÊT POUR LA PRODUCTION"
            recommendations["reasons"] = [
                f"Win rate satisfaisant: {win_rate:.1%} (≥50%)",
                f"Performance profitable: {pnl_percent:+.2f}%",
                f"Volume de trades suffisant: {total_trades} trades (≥20)",
                "Le système d'apprentissage a démontré sa capacité d'adaptation"
            ]
            recommendations["actions"] = [
                "Démarrer avec un capital test réduit (ex: 1000€)",
                "Surveiller les performances quotidiennes pendant la première semaine",
                "Augmenter progressivement le capital si les résultats sont positifs",
                "Maintenir un stop-loss global de 10% du capital total"
            ]
            recommendations["needs_more_time"] = False
            
        elif not has_enough_trades:
            recommendations["production_ready"] = "⚠️ PROLONGER LA PÉRIODE DE TEST"
            recommendations["reasons"] = [
                f"Volume de trades insuffisant: {total_trades} trades (<20 requis)",
                "Données statistiques pas encore représentatives",
                "Besoin de plus de cycles pour valider la robustesse"
            ]
            recommendations["actions"] = [
                "Continuer le test pendant 3-5 jours supplémentaires",
                "Viser au moins 30 trades pour validation statistique",
                "Analyser la cohérence des performances sur une période plus longue"
            ]
            recommendations["needs_more_time"] = True
            recommendations["additional_time_needed"] = "3-5 jours supplémentaires recommandés"
            
        elif not is_profitable:
            recommendations["production_ready"] = "❌ NE PAS PASSER EN PRODUCTION"
            recommendations["reasons"] = [
                f"Performance négative: {pnl_percent:.2f}%",
                "Le système perd de l'argent systématiquement",
                "Besoin d'optimisation des paramètres de trading"
            ]
            recommendations["actions"] = [
                "Revoir la stratégie d'entrée/sortie de positions",
                "Ajuster les seuils de stop-loss et take-profit",
                "Analyser les erreurs récurrentes dans mistakes_log.json",
                "Tester avec des paramètres de risque plus conservateurs",
                "Prolonger le test en mode simulation avec nouveaux paramètres"
            ]
            recommendations["needs_more_time"] = True
            recommendations["additional_time_needed"] = "5-7 jours avec paramètres optimisés"
            
        elif not has_good_win_rate:
            recommendations["production_ready"] = "⚠️ OPTIMISATION NÉCESSAIRE"
            recommendations["reasons"] = [
                f"Win rate insuffisant: {win_rate:.1%} (<50%)",
                "Trop de trades perdants par rapport aux gagnants",
                f"Performance globale: {pnl_percent:+.2f}% (profitable mais fragile)"
            ]
            recommendations["actions"] = [
                "Augmenter le seuil d'entrée (min_gain_to_open) pour être plus sélectif",
                "Réduire le niveau de risque (risk_level) pour limiter l'exposition",
                "Analyser les patterns d'échec dans error_patterns.json",
                "Prolonger le test de 2-3 jours avec paramètres ajustés",
                "Viser un win rate ≥55% avant production"
            ]
            recommendations["needs_more_time"] = True
            recommendations["additional_time_needed"] = "2-3 jours avec paramètres optimisés"
        
        else:
            # Cas par défaut (conditions mixtes)
            recommendations["production_ready"] = "⚠️ ÉVALUATION MITIGÉE"
            recommendations["reasons"] = [
                f"Win rate: {win_rate:.1%}",
                f"Performance: {pnl_percent:+.2f}%",
                f"Trades: {total_trades}",
                "Résultats pas assez concluants pour une décision claire"
            ]
            recommendations["actions"] = [
                "Prolonger le test de 2-3 jours supplémentaires",
                "Observer la stabilité des performances",
                "Affiner les paramètres progressivement"
            ]
            recommendations["needs_more_time"] = True
            recommendations["additional_time_needed"] = "2-3 jours supplémentaires"
        
        return recommendations


def main():
    """Point d'entrée principal"""
    import sys
    
    # Dossier du projet (où se trouvent les fichiers JSON)
    project_root = Path(__file__).parent
    
    # Dossier de sortie (Desktop par défaut)
    output_dir = Path.home() / "Desktop"
    
    # Arguments optionnels
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    print("🚀 Génération du rapport final...")
    print(f"📁 Dossier projet: {project_root}")
    print(f"📁 Dossier sortie: {output_dir}")
    print()
    
    generator = FinalReportGenerator(project_root)
    
    try:
        report_path = generator.generate_final_report(output_dir)
        print()
        print("=" * 60)
        print(f"✅ Rapport final généré avec succès!")
        print(f"📄 Fichier: {report_path}")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
