"""
Medical AI Agent - Command Handler
Gère toutes les commandes (/lesson, /disease, /quiz, etc.)
"""

from typing import Dict, Callable
from medical_agent.agent import MedicalAIAgent
from medical_agent.database import MedicalDatabase
from medical_agent.scheduler import MedicalScheduler
from medical_agent.config import COMMANDS


class CommandHandler:
    """Gestionnaire de commandes pour l'agent médical"""
    
    def __init__(self, agent: MedicalAIAgent, database: MedicalDatabase, scheduler: MedicalScheduler):
        self.agent = agent
        self.database = database
        self.scheduler = scheduler
        
        # Mapper les commandes aux fonctions
        self.commands: Dict[str, Callable] = {
            "/lesson": self.cmd_lesson,
            "/disease": self.cmd_disease,
            "/quiz": self.cmd_quiz,
            "/summary": self.cmd_summary,
            "/differential": self.cmd_differential,
            "/treatment": self.cmd_treatment,
            "/symptoms": self.cmd_symptoms,
            "/pharmacology": self.cmd_pharmacology,
            "/emergency": self.cmd_emergency,
            "/statistics": self.cmd_statistics,
            "/export": self.cmd_export,
            "/help": self.cmd_help,
            "/list": self.cmd_list,
            "/search": self.cmd_search,
            "/generate": self.cmd_generate_now,
            "/status": self.cmd_status
        }
    
    def execute(self, command: str, args: str = "") -> str:
        """
        Exécute une commande
        
        Args:
            command: La commande (ex: /lesson)
            args: Arguments de la commande
            
        Returns:
            Résultat de la commande
        """
        command = command.lower().strip()
        
        if command not in self.commands:
            return f"❌ Commande inconnue: {command}\n\nUtilise /help pour voir toutes les commandes disponibles."
        
        try:
            return self.commands[command](args)
        except Exception as e:
            return f"❌ Erreur lors de l'exécution de {command}: {e}"
    
    def cmd_lesson(self, args: str) -> str:
        """Génère une nouvelle leçon"""
        # Parser les args (optionnel: topic, category, difficulty)
        parts = args.strip().split('|') if args.strip() else []
        
        topic = parts[0].strip() if len(parts) > 0 and parts[0].strip() else None
        category = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        difficulty = parts[2].strip() if len(parts) > 2 and parts[2].strip() else "Intermédiaire"
        
        lesson = self.agent.generate_lesson(topic=topic, category=category, difficulty=difficulty)
        
        if lesson:
            # Sauvegarder
            lesson_id = self.database.add_lesson(
                title=lesson['title'],
                category=lesson['category'],
                difficulty=lesson['difficulty'],
                content=lesson['content'],
                auto_generated=False
            )
            
            return f"""✅ Leçon générée avec succès!

📖 {lesson['title']}
📂 Catégorie: {lesson['category']}
🎯 Difficulté: {lesson['difficulty']}
⏱️ Durée: {lesson['duration']}
🆔 ID: {lesson_id}

{lesson['content']}"""
        else:
            return "❌ Échec de la génération de la leçon"
    
    def cmd_disease(self, args: str) -> str:
        """Recherche une maladie"""
        if not args.strip():
            return "❌ Usage: /disease <nom de la maladie>\nExemple: /disease diabète type 2"
        
        disease_name = args.strip()
        
        # Vérifier cache
        cached = self.database.get_cached_disease(disease_name)
        if cached:
            return f"📋 Informations sur **{disease_name}** (depuis le cache):\n\n{cached}"
        
        # Sinon, rechercher
        result = self.agent.search_disease(disease_name)
        
        # Mettre en cache
        self.database.cache_disease_search(disease_name, result)
        
        return f"🔍 Informations sur **{disease_name}**:\n\n{result}"
    
    def cmd_quiz(self, args: str) -> str:
        """Génère un quiz"""
        if not args.strip():
            return "❌ Usage: /quiz <sujet>\nExemple: /quiz infarctus du myocarde"
        
        topic = args.strip()
        quiz = self.agent.generate_quiz(topic)
        
        if quiz:
            # Sauvegarder
            quiz_id = self.database.add_quiz(
                topic=quiz['topic'],
                questions=quiz['questions']
            )
            
            questions_text = quiz['questions'][0].get('raw', '') if quiz['questions'] else ''
            
            return f"""📝 Quiz généré: {quiz['topic']}

🆔 Quiz ID: {quiz_id}

{questions_text}"""
        else:
            return "❌ Échec de la génération du quiz"
    
    def cmd_summary(self, args: str) -> str:
        """Résume une pathologie"""
        if not args.strip():
            return "❌ Usage: /summary <pathologie>\nExemple: /summary cirrhose hépatique"
        
        summary = self.agent.search_disease(args.strip())
        return f"📋 Résumé de **{args.strip()}**:\n\n{summary}"
    
    def cmd_differential(self, args: str) -> str:
        """Diagnostic différentiel"""
        if not args.strip():
            return "❌ Usage: /differential <symptômes>\nExemple: /differential douleur thoracique + dyspnée"
        
        result = self.agent.get_differential_diagnosis(args.strip())
        return f"🔬 Diagnostic différentiel pour: {args.strip()}\n\n{result}"
    
    def cmd_treatment(self, args: str) -> str:
        """Traitement d'une pathologie"""
        if not args.strip():
            return "❌ Usage: /treatment <pathologie>\nExemple: /treatment pneumonie communautaire"
        
        result = self.agent.get_treatment_protocol(args.strip())
        return f"💊 Traitement de **{args.strip()}**:\n\n{result}"
    
    def cmd_symptoms(self, args: str) -> str:
        """Symptômes d'une maladie"""
        return self.cmd_disease(args)  # Même logique
    
    def cmd_pharmacology(self, args: str) -> str:
        """Info pharmacologique"""
        if not args.strip():
            return "❌ Usage: /pharmacology <médicament>\nExemple: /pharmacology amoxicilline"
        
        result = self.agent.get_pharmacology_info(args.strip())
        return f"💊 Pharmacologie - **{args.strip()}**:\n\n{result}"
    
    def cmd_emergency(self, args: str) -> str:
        """Protocole d'urgence"""
        if not args.strip():
            return "❌ Usage: /emergency <situation>\nExemple: /emergency choc anaphylactique"
        
        result = self.agent.get_emergency_protocol(args.strip())
        return f"🚨 URGENCE - **{args.strip()}**:\n\n{result}"
    
    def cmd_statistics(self, args: str) -> str:
        """Affiche les statistiques"""
        stats = self.database.get_statistics()
        
        result = f"""📊 STATISTIQUES MÉDICALES

📚 Leçons:
  • Total: {stats['total_lessons']}
  • Auto-générées: {stats['auto_generated_lessons']}
  • Manuelles: {stats['manual_lessons']}

📝 Quiz:
  • Total: {stats['total_quizzes']}

🔍 Recherches:
  • Total: {stats['total_searches']}

🏆 TOP 5 LEÇONS (par vues):
"""
        for i, (title, views) in enumerate(stats['top_lessons'], 1):
            result += f"  {i}. {title} ({views} vues)\n"
        
        result += "\n🔍 TOP 5 MALADIES RECHERCHÉES:\n"
        for i, (disease, count) in enumerate(stats['top_diseases'], 1):
            result += f"  {i}. {disease} ({count} fois)\n"
        
        return result
    
    def cmd_export(self, args: str) -> str:
        """Exporte les leçons"""
        try:
            json_data = self.database.export_all_lessons()
            
            # Sauvegarder dans un fichier nommé "Pflege azubis"
            from pathlib import Path
            from datetime import datetime
            
            # Utiliser le nom configuré + date
            from medical_agent.config import DOCUMENT_NAME, OUTPUT_FOLDER
            
            # Créer dossier de sortie
            output_dir = Path.home() / "Desktop" / OUTPUT_FOLDER
            output_dir.mkdir(exist_ok=True)
            
            filename = f"{DOCUMENT_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            return f"✅ Leçons exportées avec succès!\n📁 Fichier: {filepath}"
            
        except Exception as e:
            return f"❌ Erreur lors de l'export: {e}"
    
    def cmd_help(self, args: str) -> str:
        """Affiche l'aide"""
        help_text = "📖 COMMANDES DISPONIBLES\n\n"
        
        for cmd, description in COMMANDS.items():
            help_text += f"{cmd}\n  → {description}\n\n"
        
        help_text += """💡 EXEMPLES D'UTILISATION:

/lesson  → Génère une leçon aléatoire
/lesson diabète type 2 | Endocrinologie | Intermédiaire  → Leçon spécifique
/disease infarctus du myocarde  → Info sur une maladie
/quiz pneumonie  → Créer un quiz
/treatment asthme  → Protocole de traitement
/emergency arrêt cardiaque  → Protocole d'urgence
/pharmacology aspirine  → Info sur un médicament
"""
        
        return help_text
    
    def cmd_list(self, args: str) -> str:
        """Liste les leçons disponibles"""
        lessons = self.database.get_all_lessons(limit=20)
        
        if not lessons:
            return "📚 Aucune leçon disponible. Utilise /lesson pour en générer une!"
        
        result = f"📚 LEÇONS DISPONIBLES ({len(lessons)} dernières):\n\n"
        
        for lesson in lessons:
            auto = "🤖" if lesson['auto_generated'] else "👤"
            result += f"{auto} {lesson['id']}. {lesson['title']}\n"
            result += f"   📂 {lesson['category']} | 🎯 {lesson['difficulty']} | 👁️ {lesson['views']} vues\n\n"
        
        return result
    
    def cmd_search(self, args: str) -> str:
        """Recherche dans les leçons"""
        if not args.strip():
            return "❌ Usage: /search <mots-clés>\nExemple: /search cardiologie"
        
        results = self.database.search_lessons(args.strip())
        
        if not results:
            return f"🔍 Aucune leçon trouvée pour: {args.strip()}"
        
        result = f"🔍 RÉSULTATS POUR '{args.strip()}' ({len(results)} leçons):\n\n"
        
        for lesson in results[:10]:
            result += f"📖 {lesson['id']}. {lesson['title']}\n"
            result += f"   📂 {lesson['category']} | 🎯 {lesson['difficulty']}\n\n"
        
        return result
    
    def cmd_generate_now(self, args: str) -> str:
        """Force la génération immédiate"""
        lesson_id = self.scheduler.generate_now()
        
        if lesson_id:
            return f"✅ Leçon générée automatiquement! ID: {lesson_id}\n\nUtilise /list pour voir toutes les leçons."
        else:
            return "❌ Échec de la génération automatique"
    
    def cmd_status(self, args: str) -> str:
        """Statut du scheduler"""
        status = self.scheduler.get_status()
        stats = self.scheduler.get_weekly_stats()
        
        return f"""⏰ STATUT DU SCHEDULER

🔄 État: {'✅ Actif' if status['running'] else '❌ Inactif'}
📅 Prochaine génération: {status['next_generation']}
📊 Configuration: {status['lessons_per_week']} leçons/semaine
🕐 Jours: {status['generation_days']} à {status['generation_time']}

📈 Cette semaine:
  • Générées: {stats['this_week']}/{stats['target_per_week']}
  • Total auto: {stats['total_auto']}
"""
