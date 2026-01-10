# 🎯 Guide de Démarrage - Agent IA Premium

## Installation Rapide

### 1. Prérequis
```bash
# Python 3.8+
python --version

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configurer la clé API
Créez `.env`:
```env
OPENAI_API_KEY=sk-proj-votre-clé-ici
```

### 3. Lancer l'application
```bash
python main.py
```

---

## 🎮 Premier Lancement

### L'interface se lance avec:
✅ Message de bienvenue personnalisé  
✅ Connexion à l'API OpenAI vérifiée  
✅ Paramètres premium prêts à utiliser  
✅ Streaming activé par défaut  

### Vous êtes maintenant prêt à:
1. Taper une question et appuyer sur `Entrée`
2. Regarder la réponse s'afficher progressivement
3. Explorer les paramètres avancés
4. Utiliser les commandes rapides

---

## 💡 Premiers Pas Recommandés

### 1. Testez le streaming
```
Vous: Explique-moi la relativité en 3 paragraphes
→ Regardez la réponse s'afficher mot par mot
```

### 2. Changez les paramètres
```
Ouvrez ⚙️ Paramètres
→ Onglet "📝 Style de réponse"
→ Sélectionnez "Creative"
→ Testez avec une question créative
```

### 3. Essayez une commande rapide
```
Vous: /summarize
→ L'IA résume la conversation
```

### 4. Activez le Mode Focus
```
Ctrl + K (ou bouton 🎯 Focus)
→ Interface épurée pour se concentrer
```

### 5. **NOUVEAU** - Écoutez les réponses audio 🎵
```
Cliquez sur 🔊 Audio en haut à droite
→ Le bouton devient vert
→ L'assistant lira chaque réponse à haute voix
→ Cliquez à nouveau pour désactiver
```

---

## 🎵 Fonctionnalité Audio - Nouveau!

Votre assistant peut maintenant **parler**! 🔊

### Activation
1. Cliquez **🔊 Audio** en haut à droite
2. Voyez le bouton devenir vert
3. Chaque réponse sera lue automatiquement

### Contrôles
- 🔊 **Audio on/off** - Bouton audio en haut
- 🌙 **Ajuster vitesse** - Prochainement dans Paramètres
- 📊 **Ajuster volume** - Prochainement dans Paramètres

📖 **Lire le guide complet:** [AUDIO_QUICKSTART.md](AUDIO_QUICKSTART.md)

---

## 📱 Interface Premium Expliquée

```
┌─────────────────────────────────────────┐
│  🤖 Agent IA Premium    🎯 Focus  ⚙️    │  ← Top bar
├─────────────────────────────────────────┤
│                                         │
│        ZONE DE CHAT STREAMING           │  ← Messages + timestamps
│    [14:32] 👤 Vous: Question           │
│    [14:33] 🤖 Agent: Réponse...        │  ← Affiche progressivement
│                                         │
├─────────────────────────────────────────┤
│  [Champ de saisie]          ✉️ ENVOYER  │  ← Input + bouton animé
├─────────────────────────────────────────┤
│ ✅ Prêt | Conversation: 4 messages     │  ← Status bar intelligente
└─────────────────────────────────────────┘
```

---

## ⌨️ Contrôles Essentiels

### Clavier
| Touche | Action |
|--------|--------|
| `Entrée` | Envoyer |
| `Shift + Entrée` | Nouvelle ligne |
| `Ctrl + K` | Mode Focus |
| `Ctrl + L` | Effacer |

### Souris
| Élément | Action |
|---------|--------|
| Bouton "✉️ ENVOYER" | Envoyer le message |
| "🎯 Focus" | Activer mode focus |
| "⚙️ Paramètres" | Ouvrir paramètres avancés |

### Commandes texte
```
/summarize  → Résumé de la conversation
/explain    → Explication du dernier point
/translate  → Traduction
```

---

## ⚙️ Paramètres à Explorer

### Pour démarrer rapidement:

**Conversation Générale:**
- Mode: Balanced
- Détail: Medium
- Ton: Friendly
- Température: 0.7

**Apprentissage:**
- Mode: Detailed
- Détail: Comprehensive
- Ton: Academic
- Température: 0.5

**Créativité:**
- Mode: Creative
- Détail: Medium
- Ton: Casual
- Température: 1.5

**Travail:**
- Mode: Balanced
- Détail: Brief
- Ton: Professional
- Température: 0.7

---

## 🚀 Astuces Premium

### 1. Streaming en action
Regardez comment la réponse se forme progressivement. C'est plus rapide et plus engageant qu'une réponse en bloc.

### 2. Contextualisation rapide
Avant de poser une question complexe, changez les paramètres pour le type de réponse souhaité. L'IA s'adaptera automatiquement.

### 3. Export pour postériorité
Vos conversations précieuses peuvent être exportées en `.txt` pour archivage ou partage.

### 4. Résumés intelligents
Génèrez un résumé automatique de longues conversations pour retenir les points clés.

### 5. Mode Focus pour la concentration
Quand vous êtes dans un flux de travail, activez le Mode Focus pour éviter les distractions.

---

## 🔧 Dépannage Rapide

### "L'API key ne fonctionne pas"
```
1. Vérifiez que .env existe dans le même dossier que main.py
2. Vérifiez que la clé est correctement copiée (sans espaces)
3. Testez sur https://platform.openai.com/account/api-keys
```

### "Le streaming n'affiche rien"
```
1. C'est normal - patientez 1-2 secondes
2. Les réponses longues prennent plus de temps
3. Vérifiez votre connexion internet
```

### "Les paramètres ne changent rien"
```
1. Assurez-vous d'avoir cliqué sur le paramètre
2. Testez avec des extrêmes (température 0 vs 2)
3. Relancez l'application pour les paramètres globaux
```

### "Mode Focus ne marche pas"
```
1. Appuyez sur Ctrl+K pour basculer
2. Regardez le status bar pour confirmation
3. Réappuyez pour désactiver
```

---

## 📊 Termes Clés Expliqués

### Streaming
Les mots s'affichent au fur et à mesure de leur génération, au lieu d'attendre la réponse complète.

### Token
Unité de texte utilisée par l'IA. ~4 caractères = 1 token. Max 4000 tokens par réponse.

### Température
Paramètre de créativité. 0=rigide, 1=équilibré, 2=très créatif.

### System Prompt
Instructions cachées données à l'IA pour influencer le style et le ton.

### Mode Focus
Interface épurée sans paramètres visibles, pour une concentration maximale.

---

## 🎨 Personnalisation Avancée

### Changer les couleurs
Éditez `gui_premium.py`, dictionnaire `self.colors`:
```python
self.colors = {
    "accent": "#00a8ff",  # Changez cette couleur
    ...
}
```

### Ajouter une commande rapide
Éditez `gui_premium.py`, méthode `_handle_quick_command()`:
```python
commands = {
    "/mycmd": "Ma commande",
    ...
}
```

### Personnaliser le system prompt
Éditez `agent.py`, méthode `_build_system_prompt()`:
```python
prompt = f"""Vos instructions personnalisées ici...
{style_guide.get(...)}
"""
```

---

## 📈 Cas d'Usage Typiques

### Écriture & Rédaction
```
Mode: Creative
Ton: Friendly
Température: 1.2
```

### Analyse & Travail
```
Mode: Detailed
Ton: Professional
Température: 0.5
```

### Brainstorming
```
Mode: Creative
Détail: Comprehensive
Température: 1.8
```

### Programmation
```
Mode: Concise
Température: 0.2
Détail: Brief
```

---

## 🌐 Support Multilingue

L'IA peut répondre en:
- 🇫🇷 Français (défaut)
- 🇬🇧 English
- 🇪🇸 Español
- 🇩🇪 Deutsch
- (Et beaucoup d'autres!)

Changez dans ⚙️ Paramètres → "🌐 Langue & Ton"

---

## ✅ Checklist du Démarrage

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Clé API dans `.env`
- [ ] `python main.py` fonctionne
- [ ] Interface s'affiche correctement
- [ ] Première message envoie/reçoit une réponse
- [ ] Streaming visible (réponse progressive)
- [ ] Paramètres accessibles (bouton ⚙️)
- [ ] Raccourcis testés (Ctrl+K, Ctrl+L)
- [ ] Prêt à explorer! 🚀

---

## 📞 Besoin d'aide?

1. Consultez [PREMIUM_FEATURES.md](PREMIUM_FEATURES.md) pour les détails
2. Vérifiez [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre le fonctionnement
3. Consultez [DOCUMENTATION.md](DOCUMENTATION.md) pour les bases

---

## 🎉 Bon usage!

Vous disposez maintenant d'un agent IA premium, immersif et hautement configurable.

**Profitez de cette expérience nouvelle génération!**

---

*Agent IA Premium | Streaming • Avancé • Intelligent*  
*Version 2.0 | Janvier 2026*
