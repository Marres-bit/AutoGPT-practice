"""
Medical AI Agent - Automatic Scheduler
Génère automatiquement 3 leçons par semaine (Lundi, Mercredi, Vendredi à 9h)
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
import random

from medical_agent.agent import MedicalAIAgent
from medical_agent.database import MedicalDatabase
from medical_agent.config import *


class MedicalScheduler:
    """Scheduler automatique pour génération de leçons"""
    
    def __init__(self, agent: MedicalAIAgent, database: MedicalDatabase):
        self.agent = agent
        self.database = database
        self.running = False
        self.thread = None
        
        print("⏰ Scheduler médical initialisé")
        print(f"📅 Configuration: {LESSONS_PER_WEEK} leçons/semaine")
        print(f"🕐 Heures de génération: {LESSON_GENERATION_DAYS} à {LESSON_GENERATION_TIME}")
    
    def start(self):
        """Démarre le scheduler en arrière-plan"""
        if self.running:
            print("⚠️ Scheduler déjà actif")
            return
        
        self.running = True
        
        # Configurer les tâches planifiées
        self._setup_schedule()
        
        # Lancer le thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        print("🚀 Scheduler automatique démarré!")
        print(f"📚 Prochaine génération: {self._get_next_generation_time()}")
    
    def stop(self):
        """Arrête le scheduler"""
        self.running = False
        schedule.clear()
        print("⏸️ Scheduler arrêté")
    
    def _setup_schedule(self):
        """Configure les tâches planifiées"""
        # Nettoyer les tâches existantes
        schedule.clear()
        
        # Mapper les jours
        days_map = {
            0: schedule.every().monday,
            1: schedule.every().tuesday,
            2: schedule.every().wednesday,
            3: schedule.every().thursday,
            4: schedule.every().friday,
            5: schedule.every().saturday,
            6: schedule.every().sunday
        }
        
        # Planifier pour chaque jour configuré
        for day in LESSON_GENERATION_DAYS:
            if day in days_map:
                days_map[day].at(LESSON_GENERATION_TIME).do(self._generate_weekly_lesson)
                print(f"📅 Planifié: {list(days_map.keys())[list(days_map.values()).index(days_map[day])]} à {LESSON_GENERATION_TIME}")
    
    def _run_scheduler(self):
        """Boucle principale du scheduler"""
        print("🔄 Boucle du scheduler active...")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Vérifier toutes les minutes
    
    def _generate_weekly_lesson(self):
        """Génère une leçon automatiquement"""
        print("\n" + "="*60)
        print(f"🤖 GÉNÉRATION AUTOMATIQUE - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*60)
        
        try:
            # Choisir une catégorie aléatoire
            category = random.choice(MEDICAL_CATEGORIES)
            difficulty = random.choice(DIFFICULTY_LEVELS)
            
            print(f"📂 Catégorie: {category}")
            print(f"🎯 Difficulté: {difficulty}")
            
            # Générer la leçon
            lesson = self.agent.generate_lesson(
                category=category,
                difficulty=difficulty
            )
            
            if lesson:
                # Sauvegarder dans la base
                lesson_id = self.database.add_lesson(
                    title=lesson['title'],
                    category=lesson['category'],
                    difficulty=lesson['difficulty'],
                    content=lesson['content'],
                    auto_generated=True
                )
                
                print(f"✅ Leçon générée et sauvegardée (ID: {lesson_id})")
                print(f"📖 Titre: {lesson['title']}")
                print("="*60 + "\n")
                
                return lesson_id
            else:
                print("❌ Échec de la génération")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération automatique: {e}")
            return None
    
    def generate_now(self):
        """Force la génération immédiate d'une leçon"""
        print("🚀 Génération manuelle forcée...")
        return self._generate_weekly_lesson()
    
    def generate_batch(self, count: int = 5):
        """Génère plusieurs leçons d'un coup"""
        print(f"📚 Génération de {count} leçons...")
        
        generated = []
        for i in range(count):
            print(f"\n📖 Leçon {i+1}/{count}")
            lesson_id = self._generate_weekly_lesson()
            if lesson_id:
                generated.append(lesson_id)
            time.sleep(2)  # Pause entre les générations
        
        print(f"\n✅ {len(generated)}/{count} leçons générées avec succès")
        return generated
    
    def _get_next_generation_time(self) -> str:
        """Calcule la prochaine heure de génération"""
        now = datetime.now()
        current_weekday = now.weekday()
        
        # Trouver le prochain jour de génération
        next_days = [d for d in LESSON_GENERATION_DAYS if d >= current_weekday]
        
        if next_days:
            next_day = next_days[0]
            days_until = next_day - current_weekday
        else:
            # Semaine prochaine
            next_day = LESSON_GENERATION_DAYS[0]
            days_until = 7 - current_weekday + next_day
        
        next_time = now + timedelta(days=days_until)
        next_time = next_time.replace(
            hour=int(LESSON_GENERATION_TIME.split(':')[0]),
            minute=int(LESSON_GENERATION_TIME.split(':')[1]),
            second=0
        )
        
        return next_time.strftime("%A %d/%m/%Y à %H:%M")
    
    def get_status(self) -> dict:
        """Retourne le statut du scheduler"""
        return {
            "running": self.running,
            "next_generation": self._get_next_generation_time(),
            "lessons_per_week": LESSONS_PER_WEEK,
            "generation_days": LESSON_GENERATION_DAYS,
            "generation_time": LESSON_GENERATION_TIME
        }
    
    def get_weekly_stats(self) -> dict:
        """Statistiques de génération de la semaine"""
        # Calcul basique - peut être amélioré
        stats = self.database.get_statistics()
        
        return {
            "this_week": stats.get('auto_generated_lessons', 0) % LESSONS_PER_WEEK,
            "total_auto": stats.get('auto_generated_lessons', 0),
            "target_per_week": LESSONS_PER_WEEK
        }


def test_scheduler():
    """Test du scheduler"""
    print("🧪 Test du scheduler médical\n")
    
    # Créer les composants
    agent = MedicalAIAgent()
    database = MedicalDatabase()
    scheduler = MedicalScheduler(agent, database)
    
    # Démarrer
    scheduler.start()
    
    # Afficher le statut
    status = scheduler.get_status()
    print("\n📊 Statut du scheduler:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Générer une leçon test
    print("\n🧪 Test de génération manuelle...")
    lesson_id = scheduler.generate_now()
    
    if lesson_id:
        print(f"\n✅ Test réussi! Leçon ID: {lesson_id}")
    else:
        print("\n❌ Test échoué")
    
    # Arrêter
    scheduler.stop()


if __name__ == "__main__":
    test_scheduler()
