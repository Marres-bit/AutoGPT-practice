"""
Script de migration: Base de données locale SQLite vers Cloud
Migre toutes les leçons existantes vers le stockage cloud
"""

from medical_agent.database import MedicalDatabase
from medical_agent.cloud_database import CloudDatabase
import sys


def migrate_to_cloud():
    """Migre les données de SQLite vers le cloud"""
    print("=" * 60)
    print("🔄 MIGRATION VERS LE CLOUD")
    print("=" * 60)
    print()
    
    # Charger la base locale
    print("📂 Chargement de la base de données locale...")
    try:
        local_db = MedicalDatabase()
    except Exception as e:
        print(f"⚠️ Pas de base locale trouvée: {e}")
        print("✅ Rien à migrer, vous pouvez utiliser directement le cloud!")
        return
    
    # Charger la base cloud
    print("☁️ Initialisation du stockage cloud...")
    cloud_db = CloudDatabase()
    
    # Récupérer toutes les leçons locales
    print("\n📚 Récupération des leçons locales...")
    lessons = local_db.get_all_lessons()
    print(f"   Trouvé: {len(lessons)} leçons")
    
    if len(lessons) == 0:
        print("✅ Aucune leçon à migrer!")
        return
    
    # Migrer chaque leçon
    print("\n📤 Migration vers le cloud...")
    migrated = 0
    for lesson in lessons:
        try:
            cloud_db.add_lesson(
                title=lesson['title'],
                content=lesson['content'],
                category=lesson.get('category', 'Général'),
                difficulty=lesson.get('difficulty', 'Intermédiaire'),
                auto_generated=lesson.get('auto_generated', False)
            )
            migrated += 1
            print(f"   ✅ {lesson['title'][:50]}...")
        except Exception as e:
            print(f"   ❌ Erreur: {lesson['title'][:50]}... - {e}")
    
    print(f"\n✅ Migration terminée: {migrated}/{len(lessons)} leçons migrées")
    
    # Statistiques
    stats = cloud_db.get_statistics()
    print(f"\n📊 Statistiques cloud:")
    print(f"   - Total leçons: {stats['total_lessons']}")
    print(f"   - Auto-générées: {stats['auto_generated_lessons']}")
    print(f"   - Manuelles: {stats['manual_lessons']}")
    
    print("\n☁️ Données maintenant disponibles dans le cloud!")
    print("💡 Vous pouvez supprimer medical_lessons.db si vous voulez")


if __name__ == "__main__":
    try:
        migrate_to_cloud()
    except KeyboardInterrupt:
        print("\n⏸️ Migration annulée")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
