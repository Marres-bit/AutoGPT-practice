"""
Medical AI Agent - Point d'entrée principal
Lance l'application complète d'assistant médical autonome
AVEC MODULE GEIS (Global Extreme Insanity Scanner)
"""

import sys
import argparse
from pathlib import Path

# Add medical_agent to path
sys.path.insert(0, str(Path(__file__).parent))

from medical_agent.gui import main as gui_main
from medical_agent.scheduler import test_scheduler


def main():
    parser = argparse.ArgumentParser(description="🧠 MediGenius AI + 🔥 GEIS + 💼 CV-PDI - Triple Mode Agent")
    parser.add_argument("--test-scheduler", action="store_true", 
                       help="Tester le scheduler (génère une leçon test)")
    parser.add_argument("--generate", type=int, metavar="N",
                       help="Générer N leçons immédiatement")
    parser.add_argument("--stats", action="store_true",
                       help="Afficher les statistiques")
    parser.add_argument("--no-gui", action="store_true",
                       help="Mode daemon sans interface (scheduler seulement)")
    
    # === NOUVEAUX ARGUMENTS GEIS ===
    parser.add_argument("--geis-scan", action="store_true",
                       help="🔥 Lancer un scan GEIS immédiat")
    parser.add_argument("--geis-daemon", action="store_true",
                       help="🔥 Activer GEIS en mode daemon (scan toutes les 5h)")
    parser.add_argument("--geis-config", action="store_true",
                       help="🔥 Afficher la configuration GEIS")
    
    # === NOUVEAUX ARGUMENTS CV-PDI ===
    parser.add_argument("--cv-scan", action="store_true",
                       help="💼 Traiter tous les CV en attente dans le dossier Bureau/CV")
    parser.add_argument("--cv-daemon", action="store_true",
                       help="💼 Activer CV-PDI en mode daemon (scan toutes les 5 min)")
    parser.add_argument("--cv-config", action="store_true",
                       help="💼 Afficher la configuration CV Perfection")
    parser.add_argument("--cv-stats", action="store_true",
                       help="💼 Afficher les statistiques de traitement CV")
    
    args = parser.parse_args()
    
    try:
        print("="*70)
        print("🧠 MEDIGENIUS AI + 🔥 GEIS + 💼 CV-PDI - TRIPLE MODE AGENT")
        print("   Medical Intelligence + Insanity Scanner + CV Perfection")
        print("="*70)
        print()
        
        # === CV-PDI COMMANDS ===
        if args.cv_config:
            print("💼 CONFIGURATION CV PERFECTION MODULE\n")
            from cv_perfection import CVConfig
            config = CVConfig()
            print(f"📁 Dossier d'entrée: {config.input_path}")
            print(f"📁 Dossier de sortie: {config.output_path}")
            print(f"📄 Formats supportés: {', '.join(config.supported_formats)}")
            print(f"⏰ Intervalle scan: {config.scan_interval_minutes} min")
            print(f"🎨 Styles disponibles: {', '.join(config.available_styles)}")
            print(f"🎨 Style par défaut: {config.default_style}")
            print(f"🤖 Modèle IA: {config.openai_model}")
            print(f"🔒 Ne jamais inventer données: {config.never_invent_data}")
            return
        
        if args.cv_stats:
            print("💼 STATISTIQUES CV PERFECTION\n")
            from cv_perfection import CVScanner, CVConfig
            config = CVConfig()
            scanner = CVScanner(config)
            stats = scanner.get_statistics()
            
            print(f"📊 Total traités: {stats['total_processed']}")
            print(f"  ✅ Succès: {stats['successful']}")
            print(f"  ❌ Échecs: {stats['failed']}")
            print(f"\n📁 Cache: {stats['cache_file']}")
            return
        
        if args.cv_scan:
            print("💼 TRAITEMENT CV EN ATTENTE\n")
            from cv_perfection import CVProcessor
            processor = CVProcessor()
            stats = processor.process_all_pending()
            
            print("\n📊 RÉSUMÉ:")
            print(f"  Total: {stats['processed']}")
            print(f"  Succès: ✅ {stats['successful']}")
            print(f"  Échecs: ❌ {stats['failed']}")
            return
        
        if args.cv_daemon:
            print("💼 MODE DAEMON CV PERFECTION ACTIVÉ\n")
            from cv_perfection import CVProcessor, CVConfig
            import time
            import schedule
            
            processor = CVProcessor()
            config = CVConfig()
            
            def run_cv_scan():
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 💼 Scan CV...")
                stats = processor.process_all_pending()
                if stats['processed'] > 0:
                    print(f"✅ {stats['successful']} CV traités avec succès\n")
                else:
                    print("✅ Aucun nouveau CV\n")
            
            # Planifier scan toutes les 5 minutes
            schedule.every(config.scan_interval_minutes).minutes.do(run_cv_scan)
            
            # Premier scan immédiat
            run_cv_scan()
            
            print(f"⏰ Scan automatique toutes les {config.scan_interval_minutes} minutes")
            print(f"📁 Dossier surveillé: {config.input_path}")
            print("💡 Déposez vos CV dans le dossier Bureau/CV")
            print("💡 Appuyez sur Ctrl+C pour arrêter\n")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(30)  # Vérifier toutes les 30s
            except KeyboardInterrupt:
                print("\n⏸️ Arrêt CV-PDI daemon")
            return
        
        # === GEIS COMMANDS ===
        if args.geis_config:
            print("🔥 CONFIGURATION GEIS\n")
            from insanity_scanner import GEISConfig
            config = GEISConfig()
            print(f"📁 Dossier de sortie: {config.output_dir}")
            print(f"🎯 Score minimal: {config.min_insanity_score}/10")
            print(f"📊 Max résultats/scan: {config.max_results_per_scan}")
            print(f"⏰ Intervalle: {config.scan_interval_hours}h")
            print(f"📡 Sources: {', '.join(config.enabled_sources)}")
            print(f"📅 Age max contenu: {config.max_content_age_days} jours")
            return
        
        if args.geis_scan:
            print("🔥 LANCEMENT SCAN GEIS\n")
            from insanity_scanner import InsanityScanner
            scanner = InsanityScanner()
            stats = scanner.scan()
            
            print("\n📊 RÉSULTATS:")
            print(f"  Sources scannées: {stats['sources_scanned']}")
            print(f"  Items trouvés: {stats['raw_items_found']}")
            print(f"  Rapports générés: {stats['reports_generated']}")
            print(f"  Durée: {stats['duration_seconds']:.1f}s")
            
            if stats['errors']:
                print(f"\n⚠️ Erreurs: {len(stats['errors'])}")
            return
        
        if args.geis_daemon:
            print("🔥 MODE DAEMON GEIS ACTIVÉ\n")
            from insanity_scanner import InsanityScanner
            import time
            import schedule
            
            scanner = InsanityScanner()
            
            def run_scan():
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔥 Scan GEIS...")
                stats = scanner.scan()
                print(f"✅ {stats['reports_generated']} rapports générés\n")
            
            # Planifier scan toutes les 5h
            schedule.every(5).hours.do(run_scan)
            
            # Premier scan immédiat
            run_scan()
            
            print("⏰ Scan toutes les 5 heures activé")
            print("💡 Appuyez sur Ctrl+C pour arrêter\n")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n⏸️ Arrêt GEIS daemon")
            return
        
        # === MEDICAL COMMANDS (EXISTANTS) ===
        if args.test_scheduler:
            # Test du scheduler
            print("🧪 Mode test du scheduler\n")
            test_scheduler()
            return
        
        if args.generate:
            # Génération batch
            print(f"📚 Génération de {args.generate} leçons...\n")
            from medical_agent.agent import MedicalAIAgent
            from medical_agent.database import MedicalDatabase
            from medical_agent.scheduler import MedicalScheduler
            
            agent = MedicalAIAgent()
            database = MedicalDatabase()
            scheduler = MedicalScheduler(agent, database)
            
            scheduler.generate_batch(args.generate)
            print("\n✅ Génération terminée!")
            return
        
        if args.stats:
            # Afficher les statistiques
            print("📊 Statistiques de l'application\n")
            from medical_agent.database import MedicalDatabase
            db = MedicalDatabase()
            stats = db.get_statistics()
            
            print(f"📚 Total de leçons: {stats['total_lessons']}")
            print(f"   • Auto-générées: {stats['auto_generated_lessons']}")
            print(f"   • Manuelles: {stats['manual_lessons']}")
            print(f"\n📝 Total de quiz: {stats['total_quizzes']}")
            print(f"🔍 Total de recherches: {stats['total_searches']}")
            
            print("\n🏆 Top 5 leçons les plus consultées:")
            for i, (title, views) in enumerate(stats['top_lessons'], 1):
                print(f"   {i}. {title} ({views} vues)")
            
            print("\n🔍 Top 5 maladies les plus recherchées:")
            for i, (disease, count) in enumerate(stats['top_diseases'], 1):
                print(f"   {i}. {disease} ({count} fois)")
            
            return
        
        if args.no_gui:
            # Mode daemon - Scheduler seulement
            print("🔄 Mode daemon activé - Scheduler automatique uniquement\n")
            from medical_agent.agent import MedicalAIAgent
            from medical_agent.database import MedicalDatabase
            from medical_agent.scheduler import MedicalScheduler
            
            agent = MedicalAIAgent()
            database = MedicalDatabase()
            scheduler = MedicalScheduler(agent, database)
            scheduler.start()
            
            print("✅ Scheduler démarré!")
            print("⏰ 3 leçons seront générées automatiquement chaque semaine")
            print("📅 Lundi, Mercredi, Vendredi à 9h00")
            print("\n💡 Appuyez sur Ctrl+C pour arrêter\n")
            
            try:
                import time
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n⏸️ Arrêt du scheduler...")
                scheduler.stop()
                print("✅ Arrêté")
            
            return
        
        # Mode normal - Interface GUI
        print("🖥️ Lancement de l'interface graphique...\n")
        print("📚 Fonctionnalités:")
        print("  ✅ Génération automatique de 3 leçons/semaine")
        print("  ✅ Recherche de maladies et pathologies")
        print("  ✅ Création de quiz médicaux")
        print("  ✅ Protocoles de traitement")
        print("  ✅ Informations pharmacologiques")
        print("  ✅ Protocoles d'urgence")
        print()
        print("💬 Utilisez /help dans l'interface pour voir toutes les commandes")
        print()
        print("🚀 Démarrage...\n")
        
        gui_main()
        
    except KeyboardInterrupt:
        print("\n⏸️ Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
