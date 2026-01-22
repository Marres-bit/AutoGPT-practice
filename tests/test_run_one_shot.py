# ...existing code...
from pathlib import Path
from datetime import datetime, timedelta
import json
import random
import threading
import time

class AutonomousScheduler:
    def __init__(self, interval_hours: int = 4, gui_callback=None, project_root: Path | str | None = None):
        self.interval_hours = interval_hours
        self.gui_callback = gui_callback
        self._running = False
        self._continuous_thread = None
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        self.project_root = Path(project_root) if project_root else Path(__file__).parent

    def start(self):
        self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
        if self._continuous_thread and self._continuous_thread.is_alive():
            print("⚠️ Scheduler déjà actif")
            return
        self._running = True
        self._continuous_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._continuous_thread.start()
        print(f"🚀 Scheduler autonome démarré (analyse toutes les {self.interval_hours}h)")

    def start_continuous(self, sp_mode: bool = False):
        return self.start()

    def stop(self):
        self._running = False
        if self._continuous_thread and self._continuous_thread.is_alive():
            self._continuous_thread.join(timeout=2)
        print("⏸️ Scheduler arrêté")

    def _run_scheduler(self):
        while self._running:
            try:
                self.run_one_shot(simulate=True)
            except Exception:
                pass
            # Update next analysis time and sleep interval_hours
            self._next_analysis = datetime.utcnow() + timedelta(hours=self.interval_hours)
            time.sleep(self.interval_hours * 3600)

    def get_next_analysis_time(self):
        return self._next_analysis

    def run_one_shot(self, simulate: bool = True):
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
            if float(capital.get("investment", 0.0)) == 0.0:
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

            # Decision & simulated trade (SP rules)
            decision = "HOLD"
            trade = None
            if top_up[1] > 0.5 and capital["investment"] > 0:
                decision = "OPEN_LONG"
                amount = round(capital["investment"] * 0.5, 2)
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
                    "withdrawn_to_principal": withdrawn
                }
                _log(f"TRADE: {trade}")
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
                "capital": capital
            }

            text_lines = [
                f"Résumé cycle - {summary['timestamp']}",
                f"Top hausses: {summary['top_up']}",
                f"Top baisses: {summary['top_down']}",
                f"Décision: {decision}"
            ]
            if trade:
                text_lines.append(f"Trade simulé: {json.dumps(trade)}")
            text_lines.append(f"Capital: {json.dumps(capital)}")

            with open(summary_path, "w", encoding="utf-8") as f:
                f.write("\n".join(text_lines))

            with open(capital_path, "w", encoding="utf-8") as f:
                json.dump(capital, f, indent=2)

            _log(f"SUMMARY_WRITTEN -> {summary_path.name}")
            if self.gui_callback:
                try:
                    self.gui_callback("success", "One-shot: analyse simulée terminée", data=summary)
                except Exception:
                    pass

            return {"summary": summary, "summary_text": "\n".join(text_lines)}
        except Exception as ex:
            _log(f"ERROR: {ex}")
            if self.gui_callback:
                try:
                    self.gui_callback("error", f"One-shot error: {ex}")
                except Exception:
                    pass
            raise
# ...existing code...