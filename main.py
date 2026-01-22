# ...existing code...
import sys
import argparse
import tkinter as tk
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent import AIAgent
from gui_premium import PremiumGUI
from autonomous_scheduler import AutonomousScheduler

def main():
    parser = argparse.ArgumentParser(description="Premium AI Agent with Autonomous Crypto Analyzer")
    parser.add_argument("--autonomous", action="store_true", help="Run in autonomous mode (background)")
    parser.add_argument("--interval", type=int, default=4, help="Analysis interval in hours (default: 4)")
    parser.add_argument("--no-gui", action="store_true", help="Run without GUI (daemon mode)")
    parser.add_argument("--one-shot", action="store_true", help="Run a simulated one-shot analysis in foreground and exit (unless --auto-start)")
    parser.add_argument("--auto-start", action="store_true", help="After successful one-shot, start continuous SP loop (TestNet)")
    args = parser.parse_args()

    try:
        print("🔄 Initializing Premium AI Agent...")
        agent = AIAgent()
        print(f"✅ AI Agent ready!  Model: {agent.get_model()}")

        print("\n🚀 Initializing Autonomous Crypto Analyzer...")
        gui = None

        def scheduler_callback(status, message, data=None):
            nonlocal gui
            if gui:
                try:
                    gui._update_status(message)
                    gui._display_message("Scheduler", message, "scheduler")
                except Exception:
                    pass
            if status == "success":
                print(f"✅ {message}")
            elif status == "error":
                print(f"❌ {message}")

        scheduler = AutonomousScheduler(interval_hours=args.interval, gui_callback=scheduler_callback)
        scheduler.start()

        if args.one_shot:
            print("\n🔬 Lancement d'un one-shot simulé en foreground...")
            try:
                res = scheduler.run_one_shot(simulate=True)
                summary = res.get("summary") if isinstance(res, dict) else {"raw": str(res)}
                print("\n📋 Résumé du one-shot:")
                print(f" Timestamp: {summary.get('timestamp')}")
                print(f" Top hausses: {summary.get('top_up')}")
                print(f" Top baisses: {summary.get('top_down')}")
                print(f" Décision: {summary.get('decision')}")
                if summary.get("trade"):
                    print(f" Trade simulé: {summary.get('trade')}")
                print(f" Capital (post-cycle): {summary.get('capital')}")

                project_root = Path(__file__).parent
                files = {
                    "sp_agent.log": project_root / "sp_agent.log",
                    "last_cycle_summary.txt": project_root / "last_cycle_summary.txt",
                    "capital_state.json": project_root / "capital_state.json",
                }
                print("\n🔎 Vérification fichiers générés:")
                for name, p in files.items():
                    print(f" - {name}: {'EXISTE' if p.exists() else 'MANQUANT'} (chemin: {p})")
            except Exception as ex:
                print(f"❌ Erreur durant le one-shot: {ex}")
                scheduler.stop()
                sys.exit(1)

            if args.auto_start:
                print("\n▶️ Démarrage automatique de la boucle continue (SP mode, TestNet)...")
                scheduler.start_continuous(sp_mode=True)
                if args.no_gui:
                    print("🔁 Mode daemon actif — appuie Ctrl+C pour interrompre.")
                    try:
                        import time
                        while True:
                            time.sleep(60)
                    except KeyboardInterrupt:
                        print("\n⏸️ Arrêt demandé — arrêt du scheduler...")
                        scheduler.stop()
                        return
            else:
                scheduler.stop()
                print("\n✅ One-shot terminé. Les fichiers ont été écrits et vérifiés.")
                return

        if args.no_gui:
            print("🔁 Démarrage en mode daemon sans GUI.")
            try:
                import time
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                scheduler.stop()
                return

        # GUI path
        root = tk.Tk()
        gui = PremiumGUI(root, agent)
        gui._display_message("🤖 Agent IA", "Bienvenue ...", "agent_text")
        gui._update_status("✅ Connecté • Prêt • Scheduler autonome actif")
        root.mainloop()

    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        try:
            scheduler.stop()
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
# ...existing code...
