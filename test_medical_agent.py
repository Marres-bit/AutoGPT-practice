"""
Script de test pour l'Agent Médical Dr. Bob
Démontre les principales fonctionnalités
"""

from medical_agent import MedicalDatabase, MedicalAIAgent, MedicalScheduler
import sys

def test_database():
    """Test de la base de données"""
    print("=" * 60)
    print("🗄️ TEST DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    db = MedicalDatabase()
    
    # Ajouter une leçon test
    print("\n📝 Ajout d'une leçon test...")
    lesson_id = db.add_lesson(
        title="Test: Physiopathologie de l'Insuffisance Cardiaque",
        content="""
        L'insuffisance cardiaque est l'incapacité du cœur à assurer un débit 
        suffisant pour répondre aux besoins métaboliques de l'organisme.
        
        MÉCANISMES:
        - Dysfonction systolique (↓ fraction d'éjection)
        - Dysfonction diastolique (↓ compliance)
        
        PHYSIOPATHOLOGIE:
        1. Activation neuro-hormonale (SRAA, SNS)
        2. Remodelage ventriculaire
        3. Hypertrophie myocardique
        
        CONSÉQUENCES:
        - Congestion pulmonaire
        - Hypoperfusion périphérique
        - Œdèmes
        """,
        category="Cardiologie",
        difficulty="intermediate",
        auto_generated=False
    )
    
    print(f"✅ Leçon créée avec ID: {lesson_id}")
    
    # Récupérer les statistiques
    print("\n📊 Statistiques actuelles:")
    stats = db.get_statistics()
    print(f"   - Total leçons: {stats['total_lessons']}")
    print(f"   - Auto-générées: {stats['auto_generated_lessons']}")
    print(f"   - Manuelles: {stats['manual_lessons']}")
    print(f"   - Quiz: {stats['total_quizzes']}")
    print(f"   - Recherches: {stats['total_searches']}")
    
    # Rechercher
    print("\n🔍 Recherche du mot 'cardiaque':")
    results = db.search_lessons("cardiaque")
    for lesson in results:
        print(f"   • {lesson['title']}")
        print(f"     Catégorie: {lesson.get('category', 'N/A')}")
        print(f"     Vues: {lesson.get('views', 0)}")
    
    print("\n✅ Test base de données OK!")
    return True


def test_ai_agent():
    """Test de l'agent IA (sans appel réel à OpenAI)"""
    print("\n" + "=" * 60)
    print("🤖 TEST DE L'AGENT IA")
    print("=" * 60)
    
    agent = MedicalAIAgent()
    print(f"\n✅ Agent initialisé avec modèle: {agent.model}")
    print(f"✅ Température: {agent.temperature}")
    
    # Note: Ne fait pas d'appel réel pour éviter de consommer des crédits
    print("\n💡 Pour tester la génération réelle:")
    print("   python main_medical.py")
    print("   Puis taper: /lesson Pneumonie")
    
    return True


def test_scheduler():
    """Test du scheduler"""
    print("\n" + "=" * 60)
    print("⏰ TEST DU SCHEDULER")
    print("=" * 60)
    
    from medical_agent.config import (
        LESSONS_PER_WEEK, 
        LESSON_GENERATION_DAYS, 
        LESSON_GENERATION_TIME
    )
    
    print(f"\n📅 Configuration actuelle:")
    print(f"   - Leçons par semaine: {LESSONS_PER_WEEK}")
    print(f"   - Jours de génération: {LESSON_GENERATION_DAYS}")
    print(f"     (0=Lun, 1=Mar, 2=Mer, 3=Jeu, 4=Ven, 5=Sam, 6=Dim)")
    print(f"   - Heure: {LESSON_GENERATION_TIME}")
    
    agent = MedicalAIAgent()
    db = MedicalDatabase()
    scheduler = MedicalScheduler(agent, db)
    
    status = scheduler.get_status()
    print(f"\n📊 État du scheduler:")
    print(f"   - Actif: {status.get('running', False)}")
    print(f"   - Prochaine génération: {status.get('next_generation', 'N/A')}")
    
    print("\n✅ Test scheduler OK!")
    return True


def test_commands():
    """Test du système de commandes"""
    print("\n" + "=" * 60)
    print("💬 TEST DES COMMANDES")
    print("=" * 60)
    
    from medical_agent.commands import CommandHandler
    from medical_agent.config import COMMANDS
    
    print(f"\n📝 {len(COMMANDS)} commandes disponibles:\n")
    
    # COMMANDS est un dict de strings, pas un dict de dicts
    for cmd in sorted(COMMANDS.keys()):
        print(f"   {cmd}")
    
    print("\n✅ Test commandes OK!")
    return True


def run_all_tests():
    """Lance tous les tests"""
    print("\n" + "=" * 70)
    print("🧪 LANCEMENT DES TESTS - DR. BOB MEDICAL AI AGENT")
    print("=" * 70)
    
    tests = [
        ("Base de données", test_database),
        ("Agent IA", test_ai_agent),
        ("Scheduler", test_scheduler),
        ("Commandes", test_commands),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Erreur dans {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n🎯 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS! L'agent médical est prêt!")
        print("\n💡 Pour lancer l'interface:")
        print("   python main_medical.py")
        print("   ou double-clic sur: lancer_medical_agent.bat")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifier les erreurs ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
