# 📎 Fonctionnalité Pièces Jointes - Guide d'Utilisation

## ✨ Quoi de Neuf?

Votre agent IA peut maintenant analyser des **fichiers multimédia**: images, vidéos, et audio!

### 🎯 Types de Fichiers Supportés

**Images:**
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`
- Idéal pour: analyser des diagrammes, graphiques, photos, captures d'écran

**Vidéos:**
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`
- Idéal pour: décrire le contenu vidéo, analyser des scènes

**Audio:**
- `.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac`, `.aac`
- Idéal pour: transcrire, analyser des discours

**Documents:**
- `.pdf`, `.txt`, `.docx`, `.xlsx`, `.pptx`
- Idéal pour: résumer, extraire informations

## 🚀 Mode d'Emploi

### Étape 1: Cliquer sur "📎 FICHIER"
Le bouton **"📎 FICHIER"** apparaît à côté du bouton d'envoi.

### Étape 2: Sélectionner un Fichier
Une fenêtre s'ouvre pour choisir le fichier depuis votre ordinateur.

### Étape 3: Fichier Ajouté
Le fichier s'affiche dans la zone de chat avec:
- 🖼️ pour les images
- 🎥 pour les vidéos  
- 🎵 pour l'audio
- 📄 pour les documents

### Étape 4: Ajouter un Message (Optionnel)
Tapez une question ou instruction dans la zone de texte, par ex:
- "Qu'est-ce que tu vois sur cette image?"
- "Résume cette vidéo"
- "Transcris cet audio"

### Étape 5: Cliquer "✉️ ENVOYER"
L'agent analysera le fichier et répondra.

### Étape 6: Automatique
Les fichiers joints sont **automatiquement supprimés** après l'envoi.

## 📊 Exemples d'Utilisation

### Exemple 1: Analyser une Image
```
1. Cliquer 📎 FICHIER
2. Sélectionner: screenshot.png
3. Écrire: "Expliquer ce qu'il y a sur cet écran"
4. Cliquer ENVOYER
5. L'agent décrit l'image en détail
```

### Exemple 2: Analyser un Graphique
```
1. Cliquer 📎 FICHIER
2. Sélectionner: chart.png
3. Écrire: "Interpréter ce graphique"
4. Cliquer ENVOYER
5. L'agent analyse les données
```

### Exemple 3: Plusieurs Fichiers
Vous pouvez ajouter plusieurs fichiers:
```
1. 📎 FICHIER → image1.jpg
2. 📎 FICHIER → image2.jpg
3. Écrire: "Comparer ces deux images"
4. ENVOYER
```

## 🔒 Limitations Techniques

| Aspect | Limite |
|--------|--------|
| **Taille fichier** | 100 MB maximum |
| **Images** | Analysées avec Vision API (GPT-4V) |
| **Vidéos** | Première frame analysée |
| **Audio** | Transcription via Whisper API |
| **Documents** | Texte extrait et analysé |

## 🎓 Cas d'Usage Courants

✅ **OCR & Reconnaissance Texte**
- Extraire texte d'images
- Lire documents numériques

✅ **Analyse Visuelle**
- Identifier objets sur photos
- Analyser graphiques/diagrammes
- Lire tableaux/données visuelles

✅ **Résumé & Extraction**
- Résumer vidéos/audios
- Extraire informations clés
- Générer transcriptions

✅ **Conseils & Recommandations**
- Analyser code source (screenshot)
- Évaluer designs
- Valider documents

## ⚙️ Internals Techniques

### Architecture

```
GUI (gui_premium.py)
  ↓ [Sélection fichier]
FileHandler (file_handler.py)
  ↓ [Validation + Encoding]
AIAgent (agent.py)
  ↓ [OpenAI Vision/Whisper API]
Réponse avec analyse
```

### Fichiers Modifiés

1. **`file_handler.py`** (NEW)
   - Gère uploads, validation, encodage
   - Support 4 types multimédia
   - Max 100 MB par fichier

2. **`gui_premium.py`** (MODIFIÉ)
   - Bouton "📎 FICHIER" ajouté
   - Affichage fichiers sélectionnés
   - Nettoyage après envoi

3. **`agent.py`** (MODIFIÉ)
   - Paramètre `files_data` dans `send_message()`
   - Méthode `_build_message_content()`
   - Support images pour Vision API

## 🐛 Dépannage

### "Fichier introuvable"
→ Vérifier chemin complet du fichier

### "Type de fichier non supporté"
→ Utiliser formats listés ci-dessus

### "Fichier trop volumineux"
→ Réduire taille (max 100 MB)

### "L'agent n'analyse pas le fichier"
→ Ajouter un message texte avec le fichier
→ Ex: "Analyse cette image"

## 🚀 Prochaines Améliorations (Roadmap)

- [ ] Aperçu des images avant envoi
- [ ] Modification des fichiers sélectionnés
- [ ] Historique des fichiers uploadés
- [ ] Analyse par batch (plusieurs fichiers)
- [ ] Support des URL externes
- [ ] Transcription complète audio

## 📝 Notes

- Les fichiers **ne sont pas stockés** sur le serveur
- Les analysés sont **supprimés après utilisation**
- Les données sont traitées par **OpenAI API** (se référer à leur politique)
- Assurez vous d'avoir **les bonnes permissions** pour les fichiers

---

**Prêt à analyser des fichiers?** 🎉 Cliquez sur **📎 FICHIER** pour commencer!
