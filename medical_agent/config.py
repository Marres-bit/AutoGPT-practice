"""
Medical AI Agent - Configuration
"""

# OpenAI Configuration
OPENAI_API_KEY = ""  # Sera chargé depuis .env

# Agent Settings
AGENT_NAME = "MediGenius AI - Assistant Médical Intelligent"
AGENT_MODEL = "gpt-4o-mini"

# Cloud Database Settings
USE_CLOUD_DATABASE = True
JSONBIN_API_KEY = ""  # Optionnel - mode gratuit si vide
AGENT_TEMPERATURE = 0.7
AGENT_MAX_TOKENS = 2000

# Lesson Generation Settings
LESSONS_PER_WEEK = 3  # Nombre de leçons générées automatiquement par semaine
LESSON_GENERATION_DAYS = [1, 3, 5]  # Lundi, Mercredi, Vendredi (0=Lundi, 6=Dimanche)
LESSON_GENERATION_TIME = "09:00"  # Heure de génération automatique

# Medical Topics Categories
MEDICAL_CATEGORIES = [
    "Cardiologie",
    "Neurologie",
    "Pneumologie",
    "Gastro-entérologie",
    "Endocrinologie",
    "Néphrologie",
    "Rhumatologie",
    "Dermatologie",
    "Oncologie",
    "Hématologie",
    "Infectiologie",
    "Pédiatrie",
    "Gynécologie-Obstétrique",
    "Urologie",
    "Ophtalmologie",
    "ORL",
    "Psychiatrie",
    "Urgences",
    "Médecine Générale",
    "Pharmacologie"
]

# Lesson Difficulty Levels
DIFFICULTY_LEVELS = ["Débutant", "Intermédiaire", "Avancé", "Expert"]

# Database Settings
DATABASE_PATH = "medical_lessons.db"

# GUI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME = {
    "bg_main": "#f0f9ff",  # Light blue background
    "bg_secondary": "#e0f2fe",  # Lighter blue
    "bg_card": "#ffffff",  # White cards
    "accent": "#0284c7",  # Medical blue
    "accent_hover": "#0369a1",  # Darker blue
    "text_main": "#0c4a6e",  # Dark blue text
    "text_secondary": "#075985",  # Medium blue
    "success": "#16a34a",  # Green
    "warning": "#ea580c",  # Orange
    "error": "#dc2626",  # Red
    "border": "#bae6fd",  # Light blue border
}

# Commands Available
COMMANDS = {
    "/lesson": "Générer une nouvelle leçon médicale",
    "/disease": "Rechercher une maladie spécifique",
    "/quiz": "Générer un quiz sur un sujet",
    "/summary": "Résumer une pathologie",
    "/differential": "Diagnostic différentiel d'une maladie",
    "/treatment": "Traitement d'une pathologie",
    "/symptoms": "Symptômes d'une maladie",
    "/pharmacology": "Information sur un médicament",
    "/emergency": "Protocole d'urgence",
    "/statistics": "Statistiques des leçons générées",
    "/export": "Exporter les leçons en PDF",
    "/help": "Afficher toutes les commandes disponibles"
}

# Lesson Template Structure
LESSON_STRUCTURE = {
    "title": "",
    "category": "",
    "difficulty": "",
    "duration": "30 min",
    "content": {
        "introduction": "",
        "physiopathologie": "",
        "diagnostic": {
            "clinique": "",
            "paraclinique": ""
        },
        "diagnostic_differentiel": [],
        "traitement": {
            "medical": "",
            "chirurgical": ""
        },
        "complications": [],
        "pronostic": "",
        "points_cles": []
    }
}

# Auto-generation prompts
LESSON_GENERATION_PROMPT = """
Tu es un professeur de médecine expert. Génère une leçon complète et structurée sur le sujet suivant : {topic}

La leçon doit être de niveau {difficulty} et couvrir :
1. Introduction et définition
2. Physiopathologie détaillée
3. Diagnostic (clinique et paraclinique)
4. Diagnostic différentiel
5. Traitement (médical et chirurgical si applicable)
6. Complications possibles
7. Pronostic
8. Points clés à retenir

Format la réponse de manière claire et professionnelle pour des étudiants en médecine.
"""

QUIZ_GENERATION_PROMPT = """
Génère un quiz de 10 questions QCM sur le sujet : {topic}

Chaque question doit avoir :
- Une question claire
- 4 options de réponse (A, B, C, D)
- Une seule bonne réponse
- Une explication détaillée de la réponse correcte

Le quiz doit tester la compréhension approfondie du sujet.
"""

DISEASE_SEARCH_PROMPT = """
Fournis des informations complètes et médicalement précises sur la maladie : {disease}

Inclus :
- Définition
- Épidémiologie
- Étiologie
- Symptômes principaux
- Méthodes de diagnostic
- Options de traitement
- Pronostic

Réponds de manière professionnelle et accessible.
"""
