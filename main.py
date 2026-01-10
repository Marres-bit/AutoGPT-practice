"""
Premium AI Agent Application - Main Entry Point
Orchestrates advanced backend with immersive frontend + Autonomous Crypto Analyzer
"""
import tkinter as tk
import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent import AIAgent
from gui_premium import PremiumGUI
from autonomous_scheduler import AutonomousScheduler


def main():
    """Launch the Premium AI Agent application"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Premium AI Agent with Autonomous Crypto Analyzer")
    parser.add_argument("--autonomous", action="store_true", help="Run in autonomous mode (background)")
    parser.add_argument("--interval", type=int, default=4, help="Analysis interval in hours (default: 4)")
    parser.add_argument("--no-gui", action="store_true", help="Run without GUI (daemon mode)")
    parser.add_argument("--one-shot", action="store_true", help="Run a simulated one-shot analysis in foreground and exit (unless --auto-start)")
    parser.add_argument("--auto-start", action="store_true", help="After successful one-shot, start continuous SP loop (TestNet)")
    args = parser.parse_args()
    
    try:
        # Initialize the AI Agent backend with advanced features
        print("🔄 Initializing Premium AI Agent...")
        agent = AIAgent()
        print(f"✅ AI Agent ready!")
        print(f"   Model: {agent.get_model()}")
        print(f"   Features: Streaming • Advanced Settings • Smart Responses")
        
        # Initialize Autonomous Scheduler for Crypto Analysis
        print("\n🚀 Initializing Autonomous Crypto Analyzer...")
        
        # Callback function for GUI updates
        gui = None
        def scheduler_callback(status, message, data=None):
            """Callback from scheduler to update GUI"""
            nonlocal gui
            if gui:
                try:
                    gui.root.after(0, lambda: gui._update_status(message))
                except:
                    pass
            
            # Aussi afficher dans la console
            if status == "success":
                print(f"✅ {message}")
            elif status == "error":
                print(f"❌ {message}")
        
        scheduler = AutonomousScheduler(
            interval_hours=args.interval,
            gui_callback=scheduler_callback
        )
        scheduler.start()
        print(f"✅ Scheduler démarré (analyse toutes les {args.interval}h)")
        
        # One-shot simulated analysis requested -> run immediately in foreground and optionally start continuous SP loop.
        if args.one_shot:
            print("\n🔬 Lancement d'un one-shot simulé en foreground...")
            try:
                summary_result = scheduler.run_one_shot(simulate=True)
                # Affichage structuré du résumé
                if isinstance(summary_result, dict):
                    summary = summary_result.get("summary") or summary_result
                    summary_text = summary_result.get("summary_text") or None
                else:
                    summary = {"raw": str(summary_result)}
                    summary_text = str(summary_result)
                
                print("\n📋 Résumé du one-shot (structuré) :")
                print(f"  Timestamp: {summary.get('timestamp')}")
                print(f"  Top hausses: {summary.get('top_up')}")
                print(f"  Top baisses: {summary.get('top_down')}")
                print(f"  Décision: {summary.get('decision')}")
                if summary.get("trade"):
                    print(f"  Trade simulé: {summary.get('trade')}")
                print(f"  Capital (post-cycle): {summary.get('capital')}")
                if summary_text:
                    print("\n--- last_cycle_summary.txt ---")
                    print(summary_text)
                
                # Vérification des fichiers produits
                from pathlib import Path
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
            
            # Si demandé, démarrer la boucle continue SP en TestNet
            if args.auto_start:
                print("\n▶️ Validation OK — démarrage automatique de la boucle continue (SP mode, TestNet)...")
                scheduler.start_continuous(sp_mode=True)
                # En mode sans GUI, rester actif pour laisser la boucle tourner
                if args.no_gui:
                    print("🔁 Mode daemon actif — appuie Ctrl+C pour interrompre.")
                    try:
                        import time
                        while True:
                            time.sleep(60)
                    except KeyboardInterrupt:
                        print("\n⏸️ Arrêt demandé — arrêt de la boucle continue...")
                        scheduler.stop()
                        return
            else:
                scheduler.stop()
                print("\n✅ One-shot terminé. Les fichiers ont été écrits et vérifiés.")
                return
        
        # Skip GUI if --no-gui flag is set
        if args.no_gui:
            print("\n🔄 Mode daemon (sans interface GUI)")
            print("⏳ L'analyseur fonctionne en arrière-plan...")
            print("💾 Rapports générés sur: Desktop\\Crypto_Compte_rendu_*.docx")
            
            # Keep the scheduler running
            import time
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n⏸️ Arrêt du scheduler...")
                scheduler.stop()
            return
        
        # Create the Tkinter root window
        root = tk.Tk()
        
        # Initialize the premium GUI
        print("\n🎨 Initializing premium interface...")
        gui = PremiumGUI(root, agent)
        print("✅ Interface ready!")
        print("   Features: Animations • Streaming • Focus Mode • Quick Commands • Audio")
        
        # Display welcome message with crypto analyzer info
        welcome_msg = (
            "Bienvenue dans l'experience premium avec analyseur crypto autonome! 🚀\n\n"
            "✨ Nouvelles fonctionnalités:\n"
            f"  • Analyseur Crypto Autonome (toutes les {args.interval}h)\n"
            "  • Rapports automatiques générés sur le Bureau\n"
            "  • Reconnaissance vocale et lecture audio\n\n"
            f"📊 Prochaine analyse: {scheduler.get_next_analysis_time().strftime('%H:%M')}\n"
            "Explorez les paramètres avancés pour personnaliser notre conversation."
        )
        gui._display_message("🤖 Agent IA", welcome_msg, "agent_text")
        gui._update_status("✅ Connecté • Prêt • Scheduler autonome actif")
        
        # Start the application
        print("\n📱 Launching premium application...")
        print("💡 Tips: Ctrl+K = Focus mode | Ctrl+L = Clear | /summarize = Quick command\n")
        print("🔄 Scheduler autonome s'exécute en arrière-plan...\n")
        
        root.mainloop()
        
        # Stop scheduler when GUI closes
        scheduler.stop()
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
