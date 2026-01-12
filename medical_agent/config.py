"""
Medical AI Agent - Configuration
"""

# OpenAI Configuration
OPENAI_API_KEY = ""  # Sera chargé depuis .env

# Agent Settings
AGENT_NAME = "MediGenius AI - Pflege Ausbildung (DE)"
AGENT_MODEL = "gpt-4o-mini"
AGENT_LANGUAGE = "de"  # Langue: allemand
DOCUMENT_NAME = "Pflege azubis"  # Nom du document de sortie
OUTPUT_FOLDER = "Pflege ausbildung"  # Dossier de sortie sur Bureau

# Cloud Database Settings
USE_CLOUD_DATABASE = True
JSONBIN_API_KEY = ""  # Optionnel - mode gratuit si vide
AGENT_TEMPERATURE = 0.7
AGENT_MAX_TOKENS = 2000

# Lesson Generation Settings
LESSONS_PER_WEEK = 3  # Nombre de leçons générées automatiquement par semaine
LESSON_GENERATION_DAYS = [1, 3, 5]  # Lundi, Mercredi, Vendredi (0=Lundi, 6=Dimanche)
LESSON_GENERATION_TIME = "09:00"  # Heure de génération automatique

# Medical Topics Categories (Allemand - Pflege)
MEDICAL_CATEGORIES = [
    "Kardiologie",
    "Neurologie",
    "Pneumologie",
    "Gastroenterologie",
    "Endokrinologie",
    "Nephrologie",
    "Rheumatologie",
    "Dermatologie",
    "Onkologie",
    "Hämatologie",
    "Infektiologie",
    "Pädiatrie",
    "Gynäkologie",
    "Urologie",
    "Ophthalmologie",
    "HNO",
    "Psychiatrie",
    "Notfallmedizin",
    "Geriatrie",
    "Palliativpflege"
]

# Lesson Difficulty Levels (Allemand)
DIFFICULTY_LEVELS = ["Anfänger", "Fortgeschritten", "Experte"]

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

# Auto-generation prompts (ALLEMAND)
LESSON_GENERATION_PROMPT = """
Du bist ein Experte für Krankenpflege und Pflegeausbildung. Erstelle eine vollständige und strukturierte Lektion auf Deutsch zum folgenden Thema: {topic}

Die Lektion muss auf Niveau {difficulty} sein und folgendes abdecken:
1. Einleitung und Definition
2. Pathophysiologie
3. Klinische Merkmale und Symptome
4. Diagnostische Verfahren
5. Differentialdiagnosen
6. Behandlung (medikamentös und pflegerisch)
7. Mögliche Komplikationen
8. Prognose
9. Wichtige Punkte zum Merken

⚠️ WICHTIG: Füge am Ende einen detaillierten "PFLEGEPLANUNG" Abschnitt hinzu mit:
   - Pflegediagnosen
   - Pflegeziele (kurz- und langfristig)
   - Pflegemaßnahmen (konkret und umsetzbar)
   - Evaluation

Formatiere die Antwort klar und professionell für Pflegeschüler (Azubis).
Alle Inhalte MÜSSEN auf DEUTSCH sein.
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
