# 🚀 Démarrage Rapide - Agent IA Conversationnel

## 3 étapes pour commencer

### 1️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2️⃣ Ajouter votre clé API OpenAI
Créez un fichier `.env` dans ce dossier:
```
OPENAI_API_KEY=sk-proj-votre-clé-ici
```

Obtenez votre clé: https://platform.openai.com/account/api-keys

### 3️⃣ Lancer l'application

**Windows:**
```bash
python main.py
```
Ou double-cliquez `run.bat`

**macOS / Linux:**
```bash
python3 main.py
```
Ou exécutez:
```bash
chmod +x run.sh
./run.sh
```

---

## ✨ Fonctionnalités de base

| Action | Comment faire |
|--------|--------------|
| Envoyer un message | Tapez et appuyez `Entrée` ou cliquez "✉️ ENVOYER" |
| Nouvelle ligne | `Shift + Entrée` |
| Ouvrir paramètres | Cliquez "⚙️ Paramètres" en haut à droite |
| Changer le thème | Paramètres → Thème → Mode clair/sombre |
| Changer la police | Paramètres → Taille de police → 9-16px |
| Changer le modèle | Paramètres → Modèle IA → Sélectionner |
| Effacer l'historique | Paramètres → "🗑️ Effacer historique" |

---

## 🎨 Thèmes

- **Mode Sombre** 🌙 (Défaut) - Confortable pour les yeux
- **Mode Clair** ☀️ - Interface lumineuse et épurée

---

## 🤖 Modèles disponibles

1. **gpt-4o-mini** ⭐ (Recommandé)
   - Rapide et puissant
   - Idéal pour la plupart des usages

2. **gpt-4**
   - Plus puissant
   - Réponses plus détaillées

3. **gpt-3.5-turbo**
   - Le plus rapide
   - Bonne qualité pour les requêtes simples

---

## 🐛 Problèmes courants?

### "OPENAI_API_KEY not found"
→ Créez le fichier `.env` avec votre clé API

### "openai module not found"
```bash
pip install openai
```

### L'interface est lente
→ C'est normal pendant une requête API (attendez le statut "✅")

### Ça ne répond pas
→ Vérifiez votre clé API et votre connexion internet

---

## 📚 Pour en savoir plus

Lisez [DOCUMENTATION.md](DOCUMENTATION.md) pour une guide complet!

---

**Prêt? Lancez l'application et commencez à converser! 🎉**
