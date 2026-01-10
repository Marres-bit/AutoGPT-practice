from pathlib import Path
import argparse
import signal
import threading
import time
import logging

from autonomous_scheduler import AutonomousScheduler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-block", action="store_true", help="Start continuous loop and exit (don't block)")
    parser.add_argument("--service", action="store_true", help="Run as a service (no interactive prompts)")
    parser.add_argument("--interval", type=int, default=4, help="Interval hours for continuous mode")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    log_file = project_root / "sp_agent.log"
    logging.basicConfig(filename=str(log_file), level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    sched = AutonomousScheduler(interval_hours=args.interval, project_root=project_root)

    logging.info("🔬 One-shot start (simulate=True)")
    result = sched.run_one_shot(simulate=True)
    summary_text = result.get("summary_text") if isinstance(result, dict) else str(result)
    print("\n📋 Résumé structuré:")
    print(summary_text)
    logging.info("One-shot finished")

    files = ["sp_agent.log", "last_cycle_summary.txt", "capital_state.json"]
    print("\n🔎 Vérification fichiers générés:")
    for f in files:
        p = project_root / f
        print(f" - {f}: {'EXISTE' if p.exists() else 'MANQUANT'}")

    # Start continuous loop
    logging.info("▶️ Démarrage de la boucle continue (SP mode, TestNet)...")
    sched.start()

    if args.no_block or args.service:
        # don't block, service manager will monitor process
        print("🔁 Boucle lancée en arrière-plan (no-block/service mode).")
        return

    # Otherwise block and handle signals for graceful shutdown
    stop_event = threading.Event()

    def _handle_signal(signum, frame):
        logging.info(f"Signal received: {signum} — stopping scheduler")
        print("\n⏸️ Signal d'arrêt reçu — arrêt du scheduler...")
        sched.stop()
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    print("🔁 Boucle active — appuie Ctrl+C pour arrêter.")
    try:
        while not stop_event.wait(timeout=60):
            pass
    finally:
        sched.stop()

if __name__ == "__main__":
    main()