# 🏗️ Architecture de l'Application - Vue Technique

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION AI AGENT                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │            COUCHE PRÉSENTATION (GUI)               │    │
│  │                                                    │    │
│  │  main.py                                           │    │
│  │  ├─ Lance Tkinter root                            │    │
│  │  ├─ Crée instance AIAgent                         │    │
│  │  └─ Initialise ModernGUI                          │    │
│  │                                                    │    │
│  │  gui.py (ModernGUI)                               │    │
│  │  ├─ Interface Tkinter moderne                     │    │
│  │  ├─ Gestion des thèmes (light/dark)              │    │
│  │  ├─ Panneau de paramètres                        │    │
│  │  ├─ Affichage du chat                            │    │
│  │  ├─ Zone de saisie + bouton Envoyer             │    │
│  │  └─ Barre de statut                              │    │
│  │                                                    │    │
│  │  gui.py (SettingsManager)                         │    │
│  │  ├─ Chargement/sauvegarde settings.json          │    │
│  │  ├─ Persistance des préférences                  │    │
│  │  └─ Accès aux configurations                     │    │
│  └────────────────────────────────────────────────────┘    │
│                           ▲                                  │
│                           │ Communication                    │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │         COUCHE MÉTIER (AGENT IA)                   │    │
│  │                                                    │    │
│  │  agent.py (AIAgent)                               │    │
│  │  ├─ __init__(api_key)                            │    │
│  │  │  ├─ Initialise OpenAI client                  │    │
│  │  │  ├─ Charge la clé API depuis .env            │    │
│  │  │  └─ Définit paramètres par défaut            │    │
│  │  │                                                │    │
│  │  ├─ send_message(user_message)                  │    │
│  │  │  ├─ Ajoute à l'historique                    │    │
│  │  │  ├─ Appelle OpenAI API                       │    │
│  │  │  ├─ Traite la réponse                        │    │
│  │  │  └─ Met à jour l'historique                  │    │
│  │  │                                                │    │
│  │  ├─ set_model(model_name)                       │    │
│  │  ├─ set_temperature(value)                      │    │
│  │  ├─ set_max_tokens(value)                       │    │
│  │  ├─ clear_history()                             │    │
│  │  ├─ get_model()                                 │    │
│  │  └─ get_conversation_length()                   │    │
│  │                                                    │    │
│  │  Attributs:                                       │    │
│  │  ├─ client: OpenAI client                        │    │
│  │  ├─ conversation_history: [ ]                    │    │
│  │  ├─ model: str                                   │    │
│  │  ├─ temperature: float                           │    │
│  │  ├─ max_tokens: int                              │    │
│  │  └─ system_prompt: str                           │    │
│  └────────────────────────────────────────────────────┘    │
│                           ▲                                  │
│                           │ API Calls                        │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │        COUCHE CONFIGURATION                        │    │
│  │                                                    │    │
│  │  config.py                                        │    │
│  │  ├─ THEMES                                        │    │
│  │  │  ├─ light: { }                                │    │
│  │  │  └─ dark: { }                                 │    │
│  │  │                                                │    │
│  │  ├─ DEFAULT_SETTINGS                             │    │
│  │  │  ├─ theme                                     │    │
│  │  │  ├─ font_size                                 │    │
│  │  │  ├─ font_family                               │    │
│  │  │  ├─ model                                     │    │
│  │  │  ├─ temperature                               │    │
│  │  │  └─ max_tokens                                │    │
│  │  │                                                │    │
│  │  ├─ AVAILABLE_MODELS                             │    │
│  │  ├─ FONT_SIZES                                   │    │
│  │  ├─ WINDOW_WIDTH / HEIGHT                        │    │
│  │  └─ BUTTON_STYLES                                │    │
│  └────────────────────────────────────────────────────┘    │
│                           ▲                                  │
│                           │ .env                             │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │        STOCKAGE DE DONNÉES                         │    │
│  │                                                    │    │
│  │  .env                                             │    │
│  │  └─ OPENAI_API_KEY=sk-proj-...                   │    │
│  │                                                    │    │
│  │  settings.json (généré automatiquement)          │    │
│  │  ├─ theme: "dark"                               │    │
│  │  ├─ font_size: 11                               │    │
│  │  └─ ... autres paramètres                       │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ HTTP/HTTPS
                           ▼
              ┌───────────────────────────┐
              │  OpenAI API               │
              │  https://api.openai.com   │
              └───────────────────────────┘
```

---

## 📊 Flux de Données - Détail Complet

### 1. Initialisation de l'Application

```
START (main.py)
   │
   ├─ Créer Tkinter root window
   │
   ├─ Initialiser AIAgent
   │  ├─ Charger .env (path relative)
   │  ├─ Récupérer OPENAI_API_KEY
   │  ├─ Créer OpenAI client
   │  └─ Initialiser conversation_history = []
   │
   ├─ Initialiser SettingsManager
   │  ├─ Charger settings.json ou defaults
   │  └─ Récupérer préférences utilisateur
   │
   ├─ Initialiser ModernGUI
   │  ├─ Créer interface Tkinter
   │  ├─ Appliquer thème (light/dark)
   │  ├─ Configurer policess et tailles
   │  └─ Afficher message de bienvenue
   │
   └─ root.mainloop()
```

### 2. Envoi d'un Message

```
UTILISATEUR: Tape un message
   │
   ├─ GUI.send_message()
   │
   ├─ Afficher message utilisateur dans le chat
   │  └─ chat_area.insert("👤 Toi: ...")
   │
   ├─ Désactiver bouton Envoyer (GUI locked)
   │
   ├─ Afficher "⏳ Agent réfléchit..." (status bar)
   │
   ├─ Appeler agent.send_message(user_input)
   │  │
   │  ├─ Ajouter à conversation_history
   │  │  └─ {"role": "user", "content": "..."}
   │  │
   │  ├─ Appeler client.chat.completions.create()
   │  │  ├─ model: agent.model
   │  │  ├─ messages: [system_prompt, ...conversation_history]
   │  │  ├─ temperature: agent.temperature
   │  │  └─ max_tokens: agent.max_tokens
   │  │
   │  ├─ Recevoir réponse OpenAI
   │  │
   │  ├─ Extraire response.choices[0].message.content
   │  │
   │  ├─ Ajouter à conversation_history
   │  │  └─ {"role": "assistant", "content": "..."}
   │  │
   │  └─ Retourner response text
   │
   ├─ Afficher réponse de l'agent
   │  └─ chat_area.insert("🤖 Agent: ...")
   │
   ├─ Mettre à jour status bar
   │  └─ "✅ Message envoyé | Conversation: X messages"
   │
   ├─ Réactiver bouton Envoyer
   │
   └─ root.update()
```

### 3. Changement de Paramètres

```
UTILISATEUR: Ouvre les paramètres
   │
   ├─ GUI.toggle_settings()
   │  └─ Créer nouvelle fenêtre Toplevel
   │
   ├─ Options disponibles:
   │  │
   │  ├─ THEME (light/dark)
   │  │  ├─ GUI.change_theme(theme_name)
   │  │  ├─ Sauvegarder dans settings_manager
   │  │  └─ Message: "Redémarrage requis"
   │  │
   │  ├─ FONT SIZE (9-16)
   │  │  ├─ GUI.change_font_size(size)
   │  │  └─ Sauvegarder dans settings.json
   │  │
   │  ├─ MODEL (gpt-4o-mini / gpt-4 / gpt-3.5-turbo)
   │  │  ├─ agent.set_model(model_name)
   │  │  ├─ Valider le modèle
   │  │  └─ Afficher feedback immédiat
   │  │
   │  └─ CLEAR HISTORY
   │     ├─ Confirmation dialogue
   │     ├─ agent.clear_history()
   │     ├─ Vider chat_area
   │     └─ Réinitialiser conversation_history = []
   │
   └─ FERMER paramètres
      └─ settings_window.destroy()
```

---

## 🔄 Interactions entre Modules

### Agent ↔ GUI

| GUI → Agent | Agent → GUI |
|------------|------------|
| `send_message(text)` | Exception handling |
| `set_model(model)` | String response |
| `clear_history()` | Status updates |
| `get_model()` | - |
| `get_conversation_length()` | - |

### Config → GUI

```python
# GUI charge depuis config
THEMES[current_theme] → Couleurs
FONT_SIZES[size] → Police
DEFAULT_SETTINGS → Paramètres initiaux
AVAILABLE_MODELS → Liste déroulante
```

### Config → Agent

```python
# Agent charge depuis config
DEFAULT_SETTINGS["model"] → model initial
DEFAULT_SETTINGS["temperature"] → temperature initial
DEFAULT_SETTINGS["max_tokens"] → max_tokens initial
```

### SettingsManager → Config

```python
settings.json → Charger user settings
defaults → Config.DEFAULT_SETTINGS
user_preference → override defaults
```

---

## 🔐 Gestion des Erreurs

### En Frontend (GUI)
- Try/catch autour de `agent.send_message()`
- Afficher message d'erreur en rouge dans le chat
- Mettre à jour status bar avec "❌ Erreur"
- Réactiver les contrôles

### En Backend (Agent)
- Validation des messages non vides
- Vérification de la clé API au démarrage
- Gestion des exceptions OpenAIError
- Rollback de l'historique en cas d'erreur

### En Configuration
- Validation des valeurs de température (0-2)
- Validation des modèles (liste blanche)
- Validation des tailles de police (9-16)

---

## 📈 Scalabilité

### Pour ajouter une nouvelle fonctionnalité:

1. **Backend**: Ajouter méthode dans `AIAgent` (agent.py)
2. **Frontend**: Ajouter widget dans `ModernGUI` (gui.py)
3. **Configuration**: Ajouter defaults si nécessaire (config.py)
4. **Communication**: Appeler la méthode depuis le GUI

### Exemple: Ajouter support des images

```python
# 1. agent.py
class AIAgent:
    def send_message_with_image(self, text, image_path):
        # Logique d'upload d'image
        pass

# 2. gui.py
def upload_image(self):
    # Ouvrir file dialog
    # Appeler agent.send_message_with_image()

# 3. config.py (si besoin)
MAX_IMAGE_SIZE = 5242880  # 5MB
```

---

## ⚡ Optimisations Possibles

1. **Threading**: Multi-threader les appels API (ne pas bloquer GUI)
2. **Caching**: Cache les réponses similaires
3. **Compression**: Compresser l'historique après N messages
4. **Database**: Remplacer JSON par SQLite pour l'historique
5. **Async**: Utiliser asyncio pour les I/O
6. **Lazy Loading**: Charger les settings que si nécessaire

---

## 📝 Notes Techniques

- **Backend indépendant**: AIAgent peut être utilisé sans Tkinter
- **GUI modulaire**: ModernGUI peut être remplacée par PyQt5/PySide6
- **Configuration centralisée**: Tous les paramètres dans config.py
- **Séparation des responsabilités**: Chaque classe a un seul job
- **Pas de dépendances globales**: Injection de dépendances

---

**Architecture conçue pour: Maintenabilité, Extensibilité, Stabilité, Performance**
