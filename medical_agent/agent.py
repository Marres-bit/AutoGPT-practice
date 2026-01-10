"""
Medical AI Agent - Core AI Engine
Génération automatique de leçons, quiz, et réponses médicales
"""

import openai
import os
from pathlib import Path
from typing import Dict, List, Optional
import random
from datetime import datetime
import json

# Import local config
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from medical_agent.config import *


class MedicalAIAgent:
    """Agent IA spécialisé en médecine"""
    
    def __init__(self, api_key: str = None):
        # Load API key
        if api_key:
            self.api_key = api_key
        else:
            # Try to load from .env
            env_path = Path(__file__).parent.parent / ".env"
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY'):
                            self.api_key = line.split('=')[1].strip().strip('"\'')
                            break
            else:
                raise ValueError("❌ OPENAI_API_KEY not found. Create .env file or pass api_key parameter")
        
        openai.api_key = self.api_key
        self.model = AGENT_MODEL
        self.temperature = AGENT_TEMPERATURE
        self.max_tokens = AGENT_MAX_TOKENS
        
        print(f"✅ {AGENT_NAME} initialisé avec modèle: {self.model}")
    
    def generate_lesson(self, topic: str = None, category: str = None, 
                       difficulty: str = "Intermédiaire") -> Dict:
        """
        Génère une leçon médicale complète
        
        Args:
            topic: Sujet spécifique (si None, sera choisi aléatoirement)
            category: Catégorie médicale
            difficulty: Niveau de difficulté
            
        Returns:
            Dict contenant la leçon complète
        """
        # Si pas de topic, choisir aléatoirement
        if not topic:
            if category:
                topic = self._generate_topic_for_category(category)
            else:
                category = random.choice(MEDICAL_CATEGORIES)
                topic = self._generate_topic_for_category(category)
        
        if not category:
            category = random.choice(MEDICAL_CATEGORIES)
        
        print(f"📚 Génération de la leçon: {topic} ({category}, {difficulty})")
        
        # Créer le prompt
        prompt = LESSON_GENERATION_PROMPT.format(
            topic=topic,
            difficulty=difficulty
        )
        
        try:
            # Appel à OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un professeur de médecine expert qui crée des leçons détaillées et pédagogiques."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            content = response.choices[0].message.content
            
            # Structurer la leçon
            lesson = {
                "title": topic,
                "category": category,
                "difficulty": difficulty,
                "duration": "30 min",
                "generated_at": datetime.now().isoformat(),
                "content": self._parse_lesson_content(content)
            }
            
            print(f"✅ Leçon générée: {topic}")
            return lesson
            
        except Exception as e:
            print(f"❌ Erreur génération leçon: {e}")
            return None
    
    def generate_quiz(self, topic: str, num_questions: int = 10) -> Dict:
        """
        Génère un quiz QCM sur un sujet
        
        Args:
            topic: Sujet du quiz
            num_questions: Nombre de questions
            
        Returns:
            Dict contenant le quiz
        """
        print(f"📝 Génération d'un quiz sur: {topic}")
        
        prompt = QUIZ_GENERATION_PROMPT.format(topic=topic)
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un professeur de médecine qui crée des quiz pédagogiques."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            quiz = {
                "topic": topic,
                "num_questions": num_questions,
                "generated_at": datetime.now().isoformat(),
                "questions": self._parse_quiz_content(content)
            }
            
            print(f"✅ Quiz généré: {topic}")
            return quiz
            
        except Exception as e:
            print(f"❌ Erreur génération quiz: {e}")
            return None
    
    def search_disease(self, disease_name: str) -> str:
        """
        Recherche des informations sur une maladie
        
        Args:
            disease_name: Nom de la maladie
            
        Returns:
            Information complète sur la maladie
        """
        print(f"🔍 Recherche maladie: {disease_name}")
        
        prompt = DISEASE_SEARCH_PROMPT.format(disease=disease_name)
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un médecin expert qui fournit des informations médicales précises et complètes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            print(f"✅ Informations trouvées pour: {disease_name}")
            return content
            
        except Exception as e:
            print(f"❌ Erreur recherche maladie: {e}")
            return f"Erreur lors de la recherche: {e}"
    
    def get_differential_diagnosis(self, symptoms: str) -> str:
        """Génère un diagnostic différentiel basé sur les symptômes"""
        prompt = f"""
        Basé sur les symptômes suivants : {symptoms}
        
        Fournis un diagnostic différentiel structuré avec :
        1. Les 5 diagnostics les plus probables
        2. Les examens à réaliser pour confirmer
        3. Les signes d'alarme à surveiller
        
        Format: Liste numérotée claire et concise.
        """
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un médecin diagnosticien expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur: {e}"
    
    def get_treatment_protocol(self, disease: str) -> str:
        """Obtient le protocole de traitement d'une maladie"""
        prompt = f"""
        Fournis le protocole de traitement complet pour: {disease}
        
        Inclus:
        1. Traitement de première ligne
        2. Alternatives thérapeutiques
        3. Posologie et durée
        4. Surveillance nécessaire
        5. Contre-indications
        
        Sois précis et pratique.
        """
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un médecin expert en thérapeutique."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur: {e}"
    
    def get_emergency_protocol(self, situation: str) -> str:
        """Protocole d'urgence pour une situation"""
        prompt = f"""
        URGENCE MÉDICALE: {situation}
        
        Fournis le protocole d'urgence immédiat:
        1. Premiers gestes (ABC)
        2. Traitement d'urgence
        3. Examens prioritaires
        4. Critères d'hospitalisation
        
        Réponds de manière concise et actionnable.
        """
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un urgentiste expert. Réponds rapidement et efficacement."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur: {e}"
    
    def get_pharmacology_info(self, medication: str) -> str:
        """Information pharmacologique sur un médicament"""
        prompt = f"""
        Fournis les informations pharmacologiques sur: {medication}
        
        Inclus:
        1. Classe thérapeutique
        2. Mécanisme d'action
        3. Indications
        4. Posologie usuelle
        5. Effets secondaires principaux
        6. Interactions médicamenteuses importantes
        7. Contre-indications
        
        Format structuré et clair.
        """
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un pharmacologue clinicien expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur: {e}"
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Chat général avec l'agent médical
        
        Args:
            user_message: Message de l'utilisateur
            conversation_history: Historique de conversation
            
        Returns:
            Réponse de l'agent
        """
        if conversation_history is None:
            conversation_history = []
        
        messages = [
            {"role": "system", "content": "Tu es Dr. Bob, un assistant médical IA expert et pédagogue. Tu aides les étudiants en médecine avec des explications claires et précises."}
        ]
        
        messages.extend(conversation_history[-10:])  # Garder les 10 derniers messages
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    # Helper methods
    
    def _generate_topic_for_category(self, category: str) -> str:
        """Génère un sujet aléatoire pour une catégorie"""
        topics_by_category = {
            "Cardiologie": ["Infarctus du myocarde", "Insuffisance cardiaque", "Fibrillation auriculaire", "HTA", "Endocardite"],
            "Neurologie": ["AVC ischémique", "Épilepsie", "Sclérose en plaques", "Maladie de Parkinson", "Migraine"],
            "Pneumologie": ["Asthme", "BPCO", "Pneumonie", "Embolie pulmonaire", "Tuberculose"],
            "Gastro-entérologie": ["RGO", "Ulcère gastro-duodénal", "Cirrhose", "Pancréatite", "MICI"],
            "Endocrinologie": ["Diabète type 1", "Diabète type 2", "Hyperthyroïdie", "Hypothyroïdie", "Syndrome de Cushing"],
            "Infectiologie": ["Sepsis", "Méningite", "Endocardite infectieuse", "Infection urinaire", "Pneumonie communautaire"],
            "Urgences": ["Choc anaphylactique", "État de choc", "Détresse respiratoire", "Coma", "Arrêt cardiaque"]
        }
        
        topics = topics_by_category.get(category, ["Pathologie générale"])
        return random.choice(topics)
    
    def _parse_lesson_content(self, raw_content: str) -> str:
        """Parse et nettoie le contenu brut de la leçon"""
        # Pour l'instant, retourne tel quel
        # Peut être amélioré avec parsing structuré
        return raw_content
    
    def _parse_quiz_content(self, raw_content: str) -> List[Dict]:
        """Parse le contenu brut du quiz en structure"""
        # Parsing basique - peut être amélioré
        return [{"raw": raw_content}]
