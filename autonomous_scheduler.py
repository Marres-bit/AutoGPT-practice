"""
Module Scheduler Autonome Ultra
Gère les tâches périodiques en arrière-plan sans bloquer l'interface GUI
Avec système d'apprentissage permanent intégré
"""

from pathlib import Path
from datetime import datetime, timedelta
import json
import random
import threading
import time
from docx import Document   # add to top (require python-docx)
from learning_engine import LearningEngine

class AutonomousScheduler:
    def __init__(self, interval_hours: int = 4, gui_callback=None, project_root: Path | str | None = None):
        """
        Initialise le scheduler avec apprentissage permanent
        
        Args:
            interval_hours: Intervalle d'analyse en heures (défaut: 4h)
            gui_callback: Fonction de callback pour mettre à jour la GUI
            project_root: dossier où seront écrits les fichiers (logs, résumé, capital)
        """
        self.interval_hours = interval_hours
        self.gui_callback = gui_callback
        self._running = False
        self._continuous_thread = None
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        # Allow tests / scripts to control where files are written
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        
        # 🧠 Moteur d'apprentissage permanent
        self.learning_engine = LearningEngine(self.project_root)
        print("🧠 Moteur d'apprentissage permanent activé")

    def start(self):
        """Démarre le scheduler en arrière-plan (boucle continue)."""
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        if self._continuous_thread and self._continuous_thread.is_alive():
            print("⚠️ Scheduler déjà actif")
            return
        self._running = True
        self._continuous_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._continuous_thread.start()
        print(f"🚀 Scheduler autonome démarré (analyse toutes les {self.interval_hours}h)")

    def start_continuous(self, sp_mode: bool = False):
        """Alias explicite pour démarrer la boucle continue (compatibilité API)."""
        return self.start()

    def stop(self):
        """Arrête le scheduler et attend la fin du thread (si possible)."""
        self._running = False
        if self._continuous_thread and self._continuous_thread.is_alive():
            self._continuous_thread.join(timeout=2)
        print("⏸️ Scheduler arrêté")
    
    def _run_scheduler(self):
        """Boucle principale du scheduler (run en thread séparé)"""
        while self._running:
            try:
                self.run_one_shot(simulate=True)
            except Exception:
                pass
            time.sleep(self.interval_hours * 3600)

    def get_next_analysis_time(self):
        return self._next_analysis
    
    def run_one_shot(self, simulate: bool = True):
        """
        Run one full simulated cycle:
          - load/init capital_state.json
          - enforce initial 70% investment rule if needed
          - simulate market analysis
          - make SP decision
          - simulate TestNet trade execution (no real funds)
          - update capital_state.json, last_cycle_summary.txt and sp_agent.log
          - return a summary dict and optional text
        """
        # use self.project_root rather than Path(__file__).parent
        project_root = self.project_root
        log_path = project_root / "sp_agent.log"
        summary_path = project_root / "last_cycle_summary.txt"
        capital_path = project_root / "capital_state.json"

        def _log(msg: str):
            ts = datetime.utcnow().isoformat() + "Z"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{ts} {msg}\n")

        try:
            # Load or init capital
            if capital_path.exists():
                with open(capital_path, "r", encoding="utf-8") as f:
                    capital = json.load(f)
            else:
                capital = {"principal": 10000.0, "investment": 0.0}
                with open(capital_path, "w", encoding="utf-8") as f:
                    json.dump(capital, f, indent=2)

            # Apply initial 70% investment rule if needed
            if capital.get("investment", 0.0) == 0.0:
                invest_amount = round(capital["principal"] * 0.7, 2)
                capital["principal"] = round(capital["principal"] - invest_amount, 2)
                capital["investment"] = round(invest_amount, 2)
                _log(f"INIT INVEST: moved {invest_amount} to investment per SP rule.")

            # Simulate market analysis
            assets = ["BTC", "ETH", "SOL"]
            market = {a: round(random.uniform(-2.0, 3.0), 2) for a in assets}
            top_up = max(market.items(), key=lambda x: x[1])
            top_down = min(market.items(), key=lambda x: x[1])
            _log(f"MARKET: {market}")

            # 🧠 Obtenir la recommandation du moteur d'apprentissage
            recommendation = self.learning_engine.get_trading_recommendation(market)
            _log(f"LEARNING_RECOMMENDATION: {recommendation.get('best_choice')}")

            # Decision & simulated trade avec apprentissage
            decision = "HOLD"
            trade = None
            
            best_asset = recommendation.get("best_choice")
            if best_asset and best_asset["should_trade"] and capital["investment"] > 0:
                # Vérifier si le moteur d'apprentissage approuve
                should_trade, reason = self.learning_engine.should_trade(
                    best_asset["asset"], 
                    market
                )
                
                if should_trade:
                    decision = "OPEN_LONG"
                    # Ajuster le montant selon le niveau de risque appris
                    risk_level = self.learning_engine.state.get("risk_level", 0.5)
                    amount = round(capital["investment"] * 0.5 * risk_level, 2)
                    
                    entry_price = round(1000 * (1 + random.uniform(-0.01, 0.01)), 2)
                    exit_move = random.uniform(-1.0, 4.0)
                    exit_price = round(entry_price * (1 + exit_move / 100), 2)
                    pnl = round(amount * (exit_price - entry_price) / entry_price, 2)
                    capital["investment"] = round(capital["investment"] + pnl, 2)
                    withdrawn = 0.0
                    if pnl > 0:
                        withdrawn = round(pnl * 0.2, 2)
                        capital["investment"] = round(capital["investment"] - withdrawn, 2)
                        capital["principal"] = round(capital["principal"] + withdrawn, 2)
                    trade = {
                        "asset": best_asset["asset"],
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "amount": amount,
                        "pnl": pnl,
                        "withdrawn_to_principal": withdrawn,
                        "confidence": best_asset.get("confidence", 0.5),
                        "learning_approved": True
                    }
                    _log(f"TRADE: {trade}")
                else:
                    _log(f"TRADE_BLOCKED: {reason}")
                    decision = f"HOLD ({reason})"
            elif top_up[1] > 0.5 and capital["investment"] > 0:
                # Fallback vers l'ancienne logique si pas de recommandation
                should_trade, reason = self.learning_engine.should_trade(top_up[0], market)
                if should_trade:
                    decision = "OPEN_LONG"
                    risk_level = self.learning_engine.state.get("risk_level", 0.5)
                    amount = round(capital["investment"] * 0.5 * risk_level, 2)
                    entry_price = round(1000 * (1 + random.uniform(-0.01, 0.01)), 2)
                    exit_move = random.uniform(-1.0, 4.0)
                    exit_price = round(entry_price * (1 + exit_move / 100), 2)
                    pnl = round(amount * (exit_price - entry_price) / entry_price, 2)
                    capital["investment"] = round(capital["investment"] + pnl, 2)
                    withdrawn = 0.0
                    if pnl > 0:
                        withdrawn = round(pnl * 0.2, 2)
                        capital["investment"] = round(capital["investment"] - withdrawn, 2)
                        capital["principal"] = round(capital["principal"] + withdrawn, 2)
                    trade = {
                        "asset": top_up[0],
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "amount": amount,
                        "pnl": pnl,
                        "withdrawn_to_principal": withdrawn,
                        "learning_approved": True
                    }
                    _log(f"TRADE: {trade}")
                else:
                    _log(f"TRADE_BLOCKED: {reason}")
                    decision = f"HOLD ({reason})"
            else:
                _log("DECISION: HOLD (no trade)")

            # Build summary and persist files
            summary = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "market": market,
                "top_up": {top_up[0]: top_up[1]},
                "top_down": {top_down[0]: top_down[1]},
                "decision": decision,
                "trade": trade,
                "capital": capital,
                "learning_recommendation": recommendation
            }

            # 🧠 Analyser le trade et apprendre
            if trade:
                adjustments = self.learning_engine.analyze_trade(summary)
                _log(f"LEARNING_ADJUSTMENTS: {adjustments}")
                summary["learning_adjustments"] = adjustments
                
                # Afficher les leçons apprises
                if adjustments.get("changes"):
                    for change in adjustments["changes"]:
                        _log(f"LEARNING: {change}")

            # Write human-readable summary with learning info
            text = []
            text.append(f"Résumé cycle - {summary['timestamp']}")
            text.append(f"Top hausses: {summary['top_up']}")
            text.append(f"Top baisses: {summary['top_down']}")
            text.append(f"Décision: {decision}")
            if trade:
                text.append(f"Trade simulé: {json.dumps(trade)}")
            text.append(f"Capital: {json.dumps(capital)}")
            
            # Ajouter info d'apprentissage
            learning_summary = self.learning_engine.get_summary()
            text.append(f"\n📊 Apprentissage:")
            text.append(f"  - Win Rate: {learning_summary['win_rate']:.1%}")
            text.append(f"  - Trades totaux: {learning_summary['total_trades']}")
            text.append(f"  - Leçons apprises: {learning_summary['lessons_learned']}")
            text.append(f"  - Niveau de risque: {learning_summary['risk_level']:.2f}")
            if learning_summary.get('recent_lessons'):
                text.append(f"  - Dernières leçons:")
                for lesson in learning_summary['recent_lessons']:
                    text.append(f"    • {lesson}")
            
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write("\n".join(text))

            # Persist capital
            with open(capital_path, "w", encoding="utf-8") as f:
                json.dump(capital, f, indent=2)

            _log(f"SUMMARY_WRITTEN -> {summary_path.name}")
            
            # 📄 Générer automatiquement le rapport Word
            try:
                docx_path = self.generate_cycle_docx(summary)
                _log(f"REPORT_GENERATED -> {docx_path}")
                print(f"📄 Rapport Word généré: {docx_path}")
            except Exception as e:
                _log(f"REPORT_ERROR: {e}")
                print(f"⚠️ Erreur génération rapport: {e}")
            
            if self.gui_callback:
                try:
                    self.gui_callback("success", "One-shot: analyse simulée terminée", data=summary)
                except Exception:
                    pass

            return {"summary": summary, "summary_text": "\n".join(text)}
        except Exception as ex:
            _log(f"ERROR: {ex}")
            if self.gui_callback:
                try:
                    self.gui_callback("error", f"One-shot error: {ex}")
                except Exception:
                    pass
            raise

    def _atomic_write_json(self, path: Path, data):
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(path)

    def generate_cycle_docx(self, summary: dict, target_dir: Path | None = None):
        """
        Write a Word (.docx) report for a single cycle summarizing market, decision, trade, capital and lessons.
        Returns path to the written file.
        """
        try:
            target_dir = Path(target_dir) if target_dir else Path.home() / "Desktop"
            target_dir.mkdir(parents=True, exist_ok=True)
            timestamp = summary.get("timestamp", datetime.utcnow().isoformat())
            safe_ts = timestamp.replace(":", "-")
            filename = f"TestNet_Report_{safe_ts}.docx"
            doc = Document()
            doc.add_heading(f"TestNet Cycle Report — {timestamp}", level=1)
            doc.add_paragraph("Analyse du marché:")
            for k, v in summary.get("market", {}).items():
                doc.add_paragraph(f" - {k}: {v} %")
            doc.add_paragraph(f"Décision: {summary.get('decision')}")
            if summary.get("trade"):
                doc.add_heading("Trade simulé", level=2)
                for kk, vv in summary["trade"].items():
                    doc.add_paragraph(f"{kk}: {vv}")
            doc.add_heading("Capital", level=2)
            doc.add_paragraph(json.dumps(summary.get("capital", {}), indent=2))
            # simple lessons: pnl and suggestion
            pnl = summary.get("trade", {}).get("pnl") if summary.get("trade") else None
            doc.add_heading("Analyse & Leçons", level=2)
            if pnl is not None:
                doc.add_paragraph(f"PNL du cycle: {pnl}")
                if pnl < 0:
                    doc.add_paragraph("Perte constatée — suggestion: réduire la fraction d'investissement ou augmenter seuil d'entrée.")
                else:
                    doc.add_paragraph("Profit constaté — conserver stratégie ou envisager léger réinvestissement.")
            else:
                doc.add_paragraph("Aucun trade ouvert durant ce cycle.")
            path = target_dir / filename
            doc.save(path)
            return path
        except Exception as e:
            # fallback: write plain text summary
            txt = (target_dir or Path.home() / "Desktop") / f"TestNet_Report_{safe_ts}.txt"
            with open(txt, "w", encoding="utf-8") as f:
                f.write("Failed to create docx: " + str(e) + "\n")
            return txt

    def _load_learning_state(self):
        p = self.project_root / "learning_state.json"
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # defaults
        state = {"min_gain_to_open": 0.5, "consecutive_losses": 0}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        return state

    def _save_learning_state(self, state: dict):
        p = self.project_root / "learning_state.json"
        tmp = p.with_suffix(p.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        tmp.replace(p)

    def adjust_strategy(self, summary: dict):
        """
        Ajustement de stratégie délégué au moteur d'apprentissage permanent
        (Maintenu pour compatibilité avec l'API existante)
        """
        try:
            # Utiliser le nouveau moteur d'apprentissage
            if hasattr(self, 'learning_engine'):
                adjustments = self.learning_engine.analyze_trade(summary)
                return adjustments.get("new_parameters", {})
            
            # Fallback vers l'ancienne méthode si moteur non disponible
            state = self._load_learning_state()
            trade = summary.get("trade")
            if trade and isinstance(trade.get("pnl"), (int, float)):
                pnl = trade["pnl"]
                if pnl < 0:
                    state["consecutive_losses"] = state.get("consecutive_losses", 0) + 1
                else:
                    state["consecutive_losses"] = 0
            # if 3 losses in a row -> increase entry threshold by 0.2%
            if state.get("consecutive_losses", 0) >= 3:
                state["min_gain_to_open"] = round(state.get("min_gain_to_open", 0.5) + 0.2, 2)
                state["consecutive_losses"] = 0
            # persist
            self._save_learning_state(state)
            return state
        except Exception:
            return {}

def main():
    """Test du scheduler"""
    print("🧪 Test du Scheduler Autonome\n")
    
    def callback(status, message, data=None):
        print(f"[CALLBACK] {status.upper()}: {message}")
    
    scheduler = AutonomousScheduler(interval_hours=2, gui_callback=callback)
    scheduler.start()
    
    # Garder le thread actif pour les tests
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nArrêt du scheduler...")
        scheduler.stop()


if __name__ == "__main__":
    main()
