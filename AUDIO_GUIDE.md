# 🎵 Audio Features Guide

Votre assistant AI peut désormais **parler et écouter** en français, anglais, espagnol et allemand!

## 🚀 Fonctionnalités Audio

### 1. **Text-to-Speech (TTS)** 🔊
L'assistant lit automatiquement ses réponses à haute voix.

**Comment activer:**
- Cliquez sur le bouton **🔊 Audio** en haut à droite
- Le bouton devient vert quand audio est activé
- Chaque réponse de l'assistant sera lue automatiquement

**Paramètres TTS:**
- 🎚️ **Vitesse**: 50-300 mots/min (défaut: 150)
- 📊 **Volume**: 0-100% (défaut: 90%)
- 🎤 **Langue**: Français (défaut), English, Español, Deutsch

### 2. **Speech-to-Text (STT)** 🎤 *(Prochainement)*
Parlez en français et l'assistant comprendra automatiquement.

**Prérequis:**
- Microphone connecté et activé
- Permissions d'accès microphone accordées
- Connexion internet (Google API pour reconnaissance vocale)

## ⚙️ Installation

### Dépendances:
```bash
pip install pyttsx3 SpeechRecognition
```

**Modules utilisés:**
- `pyttsx3` - Text-to-Speech local (hors-ligne)
- `speech_recognition` - Speech-to-Text (Google API)

## 🎮 Utilisation

### Activer/Désactiver Audio
```
Clic sur 🔊 Audio
```
- État activé: Bouton vert
- État désactivé: Bouton gris

### Voir le statut
La barre de status indique:
- `✅ Audio activé - Les réponses seront lues` → TTS actif
- `🔇 Audio désactivé` → TTS inactif
- `🔊 Lecture de la réponse...` → En train de lire

## 🛠️ Architecture Audio

### Classes Disponibles

**1. TextToSpeech**
```python
from audio import TextToSpeech

tts = TextToSpeech(rate=150, volume=0.9)
tts.speak("Bonjour le monde")
tts.stop()
```

**2. SpeechToText** *(Prochainement intégré)*
```python
from audio import SpeechToText

stt = SpeechToText(language='fr-FR')
text = stt.listen(timeout=10)
```

**3. AudioManager** *(Recommandé)*
```python
from audio import AudioManager

audio = AudioManager(
    tts_rate=150,
    tts_volume=0.9,
    stt_language='fr-FR'
)

# Lire une réponse
audio.speak_response("Votre réponse")

# Écouter (prochainement)
audio.listen_for_input(callback=lambda text: print(text))

# Contrôles
audio.toggle_audio()
audio.set_tts_rate(200)
audio.set_tts_volume(0.8)
```

## 🔧 Configuration Audio

### Dans le code:
```python
# gui_premium.py
self.audio_manager = AudioManager(
    tts_rate=150,      # Vitesse TTS
    tts_volume=0.9,    # Volume TTS
    stt_language='fr-FR'  # Langue STT
)
```

### Via l'interface:
*(À venir)* - Onglet "Audio" dans les Paramètres
- Slider pour vitesse TTS
- Slider pour volume TTS
- Sélecteur de langue STT

## 📋 Fonctionnalités par langue

| Langue | Code | TTS | STT |
|--------|------|-----|-----|
| 🇫🇷 Français | `fr-FR` | ✅ | ✅ |
| 🇬🇧 English | `en-US` | ✅ | ✅ |
| 🇪🇸 Español | `es-ES` | ✅ | ✅ |
| 🇩🇪 Deutsch | `de-DE` | ✅ | ✅ |

## 🐛 Dépannage

### "Audio non disponible"
**Solution:** Installez les dépendances:
```bash
pip install pyttsx3 SpeechRecognition
```

### Pas de son?
1. Vérifiez que les haut-parleurs sont activés
2. Vérifiez le volume du système
3. Cliquez 🔊 Audio pour activer
4. Vérifiez la barre de statut

### Microphone ne fonctionne pas?
1. Vérifiez que le microphone est connecté
2. Vérifiez que le système autorise l'accès
3. Testez avec Cortana ou Google Assistant d'abord

### Reconnaissance vocale lente?
- Assurez-vous que vous avez une connexion internet stable
- Parlez clairement et distinctement
- Augmentez le timeout si nécessaire

## 🚀 Prochaines étapes

### À venir:
- ✅ TTS avec commandes vocales
- 🎤 STT intégré dans l'interface
- 📊 Onglet Audio dans les Paramètres
- 🔗 Intégration OpenAI Whisper pour STT plus précis
- 🎚️ Contrôles de vitesse/volume en temps réel

## 📝 Notes techniques

- **TTS** utilise le moteur par défaut du système (Cortana sur Windows)
- **STT** utilise l'API Google (gratuit, nécessite internet)
- Les deux fonctionnent de manière **asynchrone** (non-bloquante)
- Les threads audio ne gèlent pas l'interface

## 💡 Astuces

1. **Augmentez la vitesse TTS** pour une écoute plus rapide:
   - `AudioManager(tts_rate=200)`

2. **Réduisez le volume** pour la confidentialité:
   - `AudioManager(tts_volume=0.5)`

3. **Changez de langue** en temps réel:
   - Utilisera la langue de STT dans les Paramètres

4. **Arrêtez la lecture** en cliquant à nouveau sur 🔊 Audio

---

**Profitez d'une expérience AI conversationnelle avec audio! 🎵**
