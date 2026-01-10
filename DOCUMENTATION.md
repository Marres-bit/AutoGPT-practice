# 🤖 Agent IA Conversationnel - Guide Complet

Une application moderne d'agent IA avec interface graphique élégante, sophistiquée et entièrement personnalisable.

## 📋 Vue d'ensemble

Cette application offre une **expérience utilisateur fluide et esthétique** tout en garantissant un **agent IA puissant, fiable et optimisé**. L'architecture sépare clairement le frontend (interface) du backend (logique IA) pour assurer **stabilité, rapidité et évolutivité**.

---

## 🏗️ Architecture Modulaire

### Séparation Frontend / Backend

```
┌──────────────────────────────────────┐
│      INTERFACE (GUI)                 │
│  gui.py - ModernGUI                  │
│  • Affichage du chat                 │
│  • Thèmes personnalisables           │
│  • Panneau de paramètres             │
│  • Sauvegarde des préférences        │
└─────────────┬────────────────────────┘
              │ (Communication claire)
┌─────────────▼────────────────────────┐
│     AGENT IA (BACKEND)               │
│  agent.py - AIAgent                  │
│  • Gestion API OpenAI                │
│  • Historique de conversation        │
│  • Paramètres du modèle              │
│  • Gestion des erreurs               │
└─────────────┬────────────────────────┘
              │
┌─────────────▼────────────────────────┐
│    CONFIGURATION GLOBALE             │
│  config.py                           │
│  • Thèmes & couleurs                 │
│  • Modèles disponibles               │
│  • Paramètres par défaut             │
└──────────────────────────────────────┘
```

### Fichiers de l'Application

| Fichier | Responsabilité |
|---------|----------------|
| **main.py** | Point d'entrée - Lance le GUI et l'Agent |
| **gui.py** | Interface Tkinter moderne avec thèmes |
| **agent.py** | Backend IA - Communication OpenAI |
| **config.py** | Configuration globale et thèmes |
| **.env** | Variables d'environnement (clé API) |
| **settings.json** | Préférences utilisateur (créé automatiquement) |

---

## 🚀 Installation Rapide

### 1️⃣ Prérequis
```bash
# Vérifier Python 3.8+
python --version

# Installer les dépendances
pip install openai python-dotenv
```

### 2️⃣ Configurer la clé API
Créez ou éditez `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxx...
```

Obtenez votre clé sur: https://platform.openai.com/account/api-keys

### 3️⃣ Lancer l'application
```bash
cd C:\Users\sanim\git-practice\AutoGPT
python main.py
```

---

## 🎨 Fonctionnalités Principales

### 🌙 Thèmes Personnalisables
- **Mode Clair** ☀️: Interface lumineuse et épurée
- **Mode Sombre** 🌙: Interface confortable pour les yeux
- Les thèmes se sauvegardent automatiquement

### 📝 Taille de Police Ajustable
- Contrôle de 9 à 16 pixels
- Adaptation fluide de toute l'interface
- Sauvegarde des préférences

### 🤖 Choix du Modèle IA
- **gpt-4o-mini** (Recommandé - Rapide et puissant)
- **gpt-4** (Plus puissant, réponses détaillées)
- **gpt-3.5-turbo** (Très rapide)

### 📊 Panneau de Paramètres Avancés
- **Température**: Contrôle la créativité (0 = rigide, 2 = créatif)
- **Max Tokens**: Longueur maximale des réponses
- **Historique**: Gérer et effacer la conversation

### ✨ Interface Élégante
- Bouton "Envoyer" charismatique avec icône
- Barre de statut en temps réel
- Chat scrollable avec distinction user/agent
- Feedback visuel pendant le traitement

---

## 💻 Utilisation de l'Application

### Envoyer un Message
1. Tapez votre question dans le champ de saisie
2. Appuyez sur **Entrée** ou cliquez **✉️ ENVOYER**
3. L'agent IA traite et répond automatiquement

### Utiliser les Raccourcis
| Raccourci | Action |
|-----------|--------|
| `Entrée` | Envoyer le message |
| `Shift + Entrée` | Nouvelle ligne dans le message |
| `Ctrl + L` | Effacer le chat (via paramètres) |

### Accéder aux Paramètres
1. Cliquez le bouton **⚙️ Paramètres** en haut à droite
2. Modifiez:
   - 🌙 Thème (clair/sombre)
   - 📝 Taille de police (9-16px)
   - 🤖 Modèle IA
3. Cliquez **✓ Fermer** pour appliquer

### Effacer l'Historique
1. Ouvrez **⚙️ Paramètres**
2. Cliquez **🗑️ Effacer historique**
3. Confirmez l'action

---

## 🔧 Configuration Avancée

### Changer les Modèles Disponibles
Éditez `config.py`:
```python
AVAILABLE_MODELS = [
    "gpt-4o-mini",   # Défaut recommandé
    "gpt-4",         # Plus puissant
    "gpt-3.5-turbo", # Plus rapide
    "gpt-4-turbo",   # Ajoutez d'autres modèles au besoin
]
```

### Personnaliser les Thèmes
Éditez `config.py` dans la section `THEMES`:
```python
THEMES = {
    "dark": {
        "bg_main": "#1e1e1e",        # Fond principal
        "bg_secondary": "#2d2d2d",   # Fond secondaire
        "text_main": "#ffffff",      # Texte principal
        "accent": "#00a8ff",         # Couleur d'accent (boutons)
        "user_bubble": "#0066cc",    # Couleur message utilisateur
        "agent_bubble": "#3a3a3a",   # Couleur message agent
    }
}
```

### Modifier le Système de Prompts
Éditez `agent.py`:
```python
def __init__(self, api_key=None):
    # ...
    self.system_prompt = "Tu es un assistant utile..."  # ← Modifier ici
```

### Ajuster les Paramètres par Défaut
Éditez `config.py`:
```python
DEFAULT_SETTINGS = {
    "theme": "dark",           # Thème par défaut
    "font_size": 11,          # Taille police par défaut
    "font_family": "Segoe UI", # Police par défaut
    "model": "gpt-4o-mini",   # Modèle par défaut
    "temperature": 0.7,       # Créativité par défaut
    "max_tokens": 2000,       # Longueur max par défaut
}
```

---

## 🏆 Avantages de l'Architecture

| Avantage | Description |
|----------|-------------|
| ✅ **Séparation claire** | Frontend et backend complètement indépendants |
| ✅ **Maintenance facile** | Chaque module a une responsabilité unique |
| ✅ **Extensibilité** | Ajouter des fonctionnalités sans affecter l'IA |
| ✅ **Performance** | L'interface n'impacte pas la logique IA |
| ✅ **Stabilité** | Les bugs d'interface n'affectent pas l'IA |
| ✅ **Personnalisation** | Tous les paramètres modifiables |
| ✅ **Évolutivité** | Facile d'ajouter de nouveaux modèles ou thèmes |

---

## 📊 Flux de Conversation

```
1. Utilisateur tape → message affiché dans le chat
2. GUI envoie → Backend AI
3. Backend envoie → API OpenAI
4. API répond → Backend reçoit
5. Backend traite → GUI affiche réponse
6. Status bar → mise à jour en temps réel
```

---

## 🐛 Dépannage

### ❌ "OPENAI_API_KEY not found"
**Solution:**
- Vérifiez que `.env` existe dans le même dossier que `main.py`
- Vérifiez que la clé est correctement copiée (sans espaces)
- Relancez l'application

### ❌ "openai module not found"
**Solution:**
```bash
pip install openai
```

### ❌ L'interface est lente
**Cause:** Requête API en cours (normal)
**Conseil:** Regardez "⏳ Agent réfléchit..." dans la barre de statut

### ❌ Les paramètres ne se sauvegardent pas
**Solution:**
- Vérifiez les permissions d'écriture dans le dossier
- Le fichier `settings.json` doit être créé automatiquement
- Relancez l'application

### ❌ Message d'erreur API
**Causes possibles:**
- Clé API expirée ou invalide
- Quota API dépassé
- Connexion internet interrompue
- Modèle indisponible

**Solution:** Vérifiez votre compte OpenAI: https://platform.openai.com/account/billing

---

## 📁 Structure des Fichiers

```
AutoGPT/
├── main.py              # Point d'entrée
├── gui.py               # Interface GUI
├── agent.py             # Backend IA
├── config.py            # Configuration
├── .env                 # Clé API
├── settings.json        # Paramètres utilisateur (généré)
├── DOCUMENTATION.md     # Ce fichier
└── __pycache__/         # Cache Python (auto)
```

---

## 🔐 Sécurité

### ⚠️ Important
- **Ne commitez JAMAIS votre `.env`** avec votre clé API
- Ajoutez `.env` à `.gitignore`
- Utilisez des variables d'environnement en production

### Bonnes Pratiques
```bash
# Dans .gitignore
.env
settings.json
__pycache__/
```

---

## 🚀 Améliorations Futures Possibles

- [ ] Export des conversations (PDF, TXT, JSON)
- [ ] Sauvegarde de l'historique complet
- [ ] Search dans les conversations précédentes
- [ ] Support des images dans le chat
- [ ] Support du drag & drop de fichiers
- [ ] Animations fluides entre transitions
- [ ] Multi-threading pour les requêtes
- [ ] Mode offline avec LLM local (Ollama)
- [ ] Partage de conversations
- [ ] Intégration avec d'autres APIs (Claude, Gemini)

---

## 📚 Ressources Utiles

- 📖 [OpenAI API Docs](https://platform.openai.com/docs)
- 🐍 [Python Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- 🎨 [Tkinter Themes](https://ttkbootstrap.readthedocs.io/)
- 💬 [OpenAI Community](https://community.openai.com)

---

## 📄 Informations Légales

Cette application utilise l'**OpenAI API**. Consultez:
- [Conditions d'utilisation OpenAI](https://openai.com/policies/terms-of-use)
- [Politique de confidentialité](https://openai.com/policies/privacy-policy)

---

## 💡 Support & Feedback

Pour signaler des bugs ou proposer des améliorations:
1. Vérifiez les solutions de dépannage
2. Consultez la documentation OpenAI
3. Testez avec un modèle différent
4. Vérifiez votre connexion internet

---

**Créé pour offrir une expérience utilisateur fluide, personnalisable et esthétique.**  
**Version 1.0 | Janvier 2026**
