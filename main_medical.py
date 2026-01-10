"""
Medical AI Agent - Point d'entrée principal
Lance l'application complète d'assistant médical autonome
"""

import sys
import argparse
from pathlib import Path

# Add medical_agent to path
sys.path.insert(0, str(Path(__file__).parent))

from medical_agent.gui import main as gui_main
from medical_agent.scheduler import test_scheduler


def main():
    parser = argparse.ArgumentParser(description="🧽 Dr. Bob - Medical AI Agent")
    parser.add_argument("--test-scheduler", action="store_true", 
                       help="Tester le scheduler (génère une leçon test)")
    parser.add_argument("--generate", type=int, metavar="N",
                       help="Générer N leçons immédiatement")
    parser.add_argument("--stats", action="store_true",
                       help="Afficher les statistiques")
    parser.add_argument("--no-gui", action="store_true",
                       help="Mode daemon sans interface (scheduler seulement)")
    
    args = parser.parse_args()
    
    try:
        print("="*60)
        print("🧽 DR. BOB - MEDICAL AI AGENT")
        print("="*60)
        print()
        
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
