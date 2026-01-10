# 🎵 Audio Feature - Quick Start

## Installation Rapide

```bash
# Les dépendances sont déjà dans requirements.txt
pip install -r requirements.txt
```

**Dépendances ajoutées:**
- `pyttsx3` - Text-to-Speech (lire les réponses)
- `SpeechRecognition` - Speech-to-Text (écouter la voix)

## 🚀 Utilisation Immédiate

### 1. **Lancer l'application**
```bash
python main.py
```

### 2. **Activer le mode Audio**
- Cliquez sur le bouton **🔊 Audio** en haut à droite
- Le bouton devient vert quand activé
- Vous verrez: `✅ Audio activé - Les réponses seront lues`

### 3. **Parler à l'assistant**
- Tapez votre message dans la zone de saisie
- Appuyez sur **Entrée**
- L'assistant répondra et **lira sa réponse à haute voix** 🔊

### 4. **Contrôles Audio**
| Action | Résultat |
|--------|----------|
| Clic sur 🔊 Audio | Active/désactive la lecture audio |
| Bouton vert | Audio activé ✅ |
| Bouton gris | Audio désactivé 🔇 |

## 🔧 Configuration

### Vitesse de lecture (dans audio.py)
```python
AudioManager(tts_rate=150)  # Par défaut: 150 mots/min
# Plage: 50-300 mots/min
```

### Volume (dans audio.py)
```python
AudioManager(tts_volume=0.9)  # Par défaut: 0.9 (90%)
# Plage: 0.0-1.0
```

### Langue (pour futur STT)
```python
AudioManager(stt_language='fr-FR')  # Défaut: Français
# Options: 'fr-FR', 'en-US', 'es-ES', 'de-DE'
```

## 📊 Statut Audio dans l'interface

Regardez la barre de statut en bas pour:
- `✅ Audio activé` → TTS actif
- `🔇 Audio désactivé` → TTS inactif  
- `🔊 Lecture de la réponse...` → En train de lire

## 💡 Fonctionnalités avancées

### Code d'utilisation direct
```python
from audio import AudioManager

# Créer un gestionnaire audio
audio = AudioManager(
    tts_rate=150,        # Vitesse
    tts_volume=0.9,      # Volume
    stt_language='fr-FR' # Langue
)

# Lire une réponse
audio.speak_response("Bonjour!")

# Arrêter la lecture (à venir)
audio.stop()

# Changer la vitesse
audio.set_tts_rate(200)

# Changer le volume
audio.set_tts_volume(0.7)
```

## 🐛 Dépannage

| Problème | Solution |
|----------|----------|
| "Audio non disponible" | Installez: `pip install pyttsx3 SpeechRecognition` |
| Pas de son | Vérifiez haut-parleurs + cliquez 🔊 Audio |
| Lectur très lente/rapide | Ajustez `tts_rate` (50-300) |
| Trop fort/faible | Ajustez `tts_volume` (0.0-1.0) |

## 📋 Architecture

```
Interface GUI (gui_premium.py)
    ↓
Bouton 🔊 Audio
    ↓
toggle_audio() → active/désactive
    ↓
_on_message_complete()
    ↓
audio_manager.speak_response()
    ↓
TextToSpeech.speak() → pyttsx3
    ↓
🔊 Audio jouée
```

## 🎯 Prochaines étapes

**À venir prochainement:**
- 🎤 Mode microphone pour parler à l'assistant
- 📊 Onglet Audio dans Paramètres
- 🎚️ Sliders en temps réel
- ⚡ Whisper API pour meilleure reconnaissance vocale

---

**Profitez de votre assistant qui parle! 🎵**
