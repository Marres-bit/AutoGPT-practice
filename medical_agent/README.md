# 🧽 Dr. Bob - Agent Médical Autonome

Un assistant médical intelligent qui génère automatiquement du contenu éducatif médical.

## 🌟 Fonctionnalités

### 🤖 Génération Automatique
- **3 leçons par semaine** générées automatiquement (Lundi, Mercredi, Vendredi à 9h00)
- **20 catégories médicales** : Cardiologie, Neurologie, Pneumologie, etc.
- **Contenu personnalisé** par IA (GPT-4o-mini)
- **Base de données SQLite** pour stocker tout le contenu

### 💬 Commandes Disponibles

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/lesson <sujet>` | Génère une leçon complète | `/lesson Infarctus du myocarde` |
| `/disease <maladie>` | Recherche détaillée maladie | `/disease Asthme` |
| `/quiz <sujet>` | Crée un quiz médical | `/quiz Antibiotiques` |
| `/summary` | Résume conversation | `/summary` |
| `/differential <symptômes>` | Diagnostic différentiel | `/differential fièvre toux` |
| `/treatment <maladie>` | Protocole traitement | `/treatment Pneumonie` |
| `/symptoms <maladie>` | Liste symptômes | `/symptoms Diabète type 2` |
| `/pharmacology <médicament>` | Info pharmacologique | `/pharmacology Amoxicilline` |
| `/emergency <situation>` | Protocole urgence | `/emergency Arrêt cardiaque` |
| `/statistics` | Stats application | `/statistics` |
| `/export` | Exporte leçons JSON | `/export` |
| `/list` | Liste toutes leçons | `/list` |
| `/search <terme>` | Recherche dans leçons | `/search cardiovasculaire` |
| `/generate` | Génère leçon maintenant | `/generate` |
| `/status` | État scheduler | `/status` |
| `/help` | Aide complète | `/help` |

### 🏥 Catégories Médicales

1. Cardiologie
2. Neurologie
3. Pneumologie
4. Gastro-entérologie
5. Néphrologie
6. Endocrinologie
7. Rhumatologie
8. Hématologie
9. Oncologie
10. Infectiologie
11. Dermatologie
12. Ophtalmologie
13. ORL
14. Psychiatrie
15. Pédiatrie
16. Gynécologie-Obstétrique
17. Urologie
18. Chirurgie générale
19. Médecine d'urgence
20. Médecine générale

## 🚀 Installation

### Prérequis
- Python 3.8+
- Clé API OpenAI

### Installation rapide
```bash
# 1. Cloner le projet
cd C:\Users\sanim\git-practice\AutoGPT

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'API OpenAI
# Créer un fichier .env avec:
OPENAI_API_KEY=votre_clé_api_ici
```

## 💻 Utilisation

### 1. Interface Graphique (Recommandé)
```bash
# Windows
lancer_medical_agent.bat

# Ou directement avec Python
python main_medical.py
```

### 2. Mode Daemon (Background)
```bash
# Lance seulement le scheduler automatique
python main_medical.py --no-gui
```

### 3. Génération Batch
```bash
# Générer 5 leçons immédiatement
python main_medical.py --generate 5
```

### 4. Afficher les Statistiques
```bash
python main_medical.py --stats
```

### 5. Tester le Scheduler
```bash
python main_medical.py --test-scheduler
```

## 🏗️ Architecture

```
medical_agent/
├── __init__.py          # Package initialization
├── config.py            # Configuration (catégories, commandes, prompts)
├── database.py          # Gestion SQLite (leçons, quiz, stats)
├── agent.py             # Moteur IA (OpenAI GPT-4o-mini)
├── scheduler.py         # Planification automatique (schedule)
├── commands.py          # Système de commandes
├── gui.py               # Interface Tkinter avec Bob l'éponge 🧽
└── README.md            # Cette documentation

main_medical.py          # Point d'entrée principal
lancer_medical_agent.bat # Launcher Windows
medical_lessons.db       # Base de données (auto-créée)
```

## 🗄️ Base de Données

### Tables
1. **lessons** : Leçons médicales (titre, contenu, catégorie, vues)
2. **quizzes** : Quiz avec questions/réponses
3. **disease_searches** : Cache des recherches de maladies
4. **statistics** : Statistiques d'utilisation
5. **user_sessions** : Sessions utilisateur

### Schéma Lessons
```sql
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT DEFAULT 'intermediate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_auto_generated BOOLEAN DEFAULT FALSE,
    views INTEGER DEFAULT 0
)
```

## ⚙️ Configuration

### Modifier la Fréquence de Génération
Fichier: `medical_agent/config.py`
```python
# Nombre de leçons par semaine
LESSONS_PER_WEEK = 3

# Jours de génération (0=Lundi, 6=Dimanche)
LESSON_GENERATION_DAYS = [0, 2, 4]  # Lun, Mer, Ven

# Heure de génération
LESSON_GENERATION_TIME = "09:00"
```

### Changer le Modèle IA
```python
# Dans config.py
OPENAI_MODEL = "gpt-4o-mini"  # ou "gpt-4", "gpt-3.5-turbo"
```

### Personnaliser les Catégories
```python
# Ajouter dans MEDICAL_CATEGORIES (config.py)
MEDICAL_CATEGORIES = [
    "Cardiologie",
    # ... categories existantes ...
    "Votre Nouvelle Catégorie"
]
```

## 📊 Exemples d'Utilisation

### 1. Générer une Leçon sur un Sujet Précis
```
Dans l'interface, taper:
/lesson Insuffisance cardiaque aiguë

Réponse:
✅ Génération de la leçon sur 'Insuffisance cardiaque aiguë'...
[Contenu complet avec définition, étiologie, clinique, traitement]
```

### 2. Rechercher une Maladie
```
/disease Asthme

Réponse:
📚 Asthme
• Définition: Maladie inflammatoire chronique des voies aériennes
• Symptômes: Dyspnée, toux, sibilants, oppression thoracique
• Traitement: Corticoïdes inhalés + β2-agonistes
```

### 3. Créer un Quiz
```
/quiz Antibiotiques

Réponse:
📝 Quiz sur les Antibiotiques (10 questions)

1. Quel antibiotique est contre-indiqué chez l'enfant?
   A) Amoxicilline
   B) Quinolones
   C) Pénicilline
   [Réponse: B]
```

### 4. Diagnostic Différentiel
```
/differential fièvre douleur abdominale nausées

Réponse:
🔍 Diagnostic différentiel:
1. Appendicite aiguë
2. Gastro-entérite infectieuse
3. Pancréatite aiguë
4. Cholécystite
5. Pyélonéphrite
```

### 5. Protocole d'Urgence
```
/emergency Arrêt cardiaque

Réponse:
🚨 PROTOCOLE D'URGENCE - Arrêt Cardiaque

1. APPELER AIDE (15/SAMU)
2. MASSAGE CARDIAQUE (100-120/min)
3. VENTILATION (30:2)
4. DÉFIBRILLATEUR si disponible
5. ADRÉNALINE 1mg IV toutes les 3-5 min
```

## 🔧 Maintenance

### Nettoyer la Base de Données
```python
# Dans un script Python
from medical_agent.database import MedicalDatabase

db = MedicalDatabase()
# Supprimer les anciennes leçons (+ de 6 mois)
db.execute("DELETE FROM lessons WHERE created_at < date('now', '-6 months')")
```

### Exporter les Données
```bash
# Via l'interface
/export

# Ou programmatiquement
python -c "from medical_agent.database import MedicalDatabase; \
           db = MedicalDatabase(); \
           db.export_all_lessons('export.json')"
```

### Backup de la Base
```bash
# Copier simplement le fichier
copy medical_lessons.db medical_lessons_backup.db
```

## 📈 Statistiques

L'application suit automatiquement:
- ✅ Nombre total de leçons (auto-générées vs manuelles)
- ✅ Nombre de quiz créés
- ✅ Nombre de recherches de maladies
- ✅ Top 5 leçons les plus consultées
- ✅ Top 5 maladies les plus recherchées

Voir les stats:
```bash
python main_medical.py --stats
```

## 🎨 Interface Graphique

### Fonctionnalités
- **🧽 Icône Bob l'éponge** en header
- **Sidebar** avec boutons rapides pour commandes fréquentes
- **Zone de chat** avec historique complet
- **Status du scheduler** en temps réel
- **Coloration syntaxique** (commandes, système, agent)
- **Auto-scroll** vers nouveaux messages
- **Threading** pour ne pas bloquer l'interface

### Raccourcis Clavier
- `Entrée` : Envoyer message
- `Échap` : Effacer zone de saisie

## 🛠️ Dépannage

### Problème: Interface ne se lance pas
```bash
# Vérifier Python
python --version

# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall
```

### Problème: Erreur OpenAI API
```bash
# Vérifier la clé API
echo %OPENAI_API_KEY%  # Windows
echo $OPENAI_API_KEY   # Linux/Mac

# Recréer le fichier .env
echo OPENAI_API_KEY=sk-proj-xxx > .env
```

### Problème: Base de données corrompue
```bash
# Supprimer et recréer
del medical_lessons.db
python main_medical.py
```

### Problème: Scheduler ne génère pas
```bash
# Tester manuellement
python main_medical.py --test-scheduler

# Vérifier la configuration
python -c "from medical_agent.config import *; \
           print(f'Jours: {LESSON_GENERATION_DAYS}'); \
           print(f'Heure: {LESSON_GENERATION_TIME}')"
```

## 📝 Logs

Les logs sont affichés dans la console:
```
✅ Dr. Bob - Medical AI initialisé
✅ Base de données médicale initialisée
⏰ Scheduler médical initialisé
📚 Prochaine génération: Monday 12/01/2026 à 09:00
```

Pour sauvegarder les logs dans un fichier:
```bash
python main_medical.py > logs.txt 2>&1
```

## 🤝 Contribution

Pour ajouter une fonctionnalité:
1. Modifier le fichier approprié dans `medical_agent/`
2. Tester avec `python main_medical.py --test-scheduler`
3. Commiter les changements

## 📄 Licence

Ce projet est pour usage personnel éducatif.

## 👨‍⚕️ À Propos

**Dr. Bob - Medical AI Agent**
- Version: 1.0.0
- Modèle IA: OpenAI GPT-4o-mini
- Framework GUI: Tkinter
- Database: SQLite3
- Scheduler: schedule library

---

**🧽 Dr. Bob est toujours prêt à vous enseigner la médecine!**

Pour toute question, utilisez `/help` dans l'interface ou consultez cette documentation.
