# 🎯 DÉMARRAGE RAPIDE - Pièces Jointes (File Attachments)

## ⚡ 30 Secondes pour Commencer

### Installation (si nécessaire)
```bash
pip install -r requirements.txt
```

### Lancement
```bash
python main.py
```

### Utilisation
1. **Cliquer le bouton "📎 FICHIER"** (à côté d'ENVOYER)
2. **Sélectionner une image/vidéo/audio** depuis votre PC
3. **Écrire votre question** (optionnel) ex: "Analyze this"
4. **Cliquer "✉️ ENVOYER"**
5. **Agent analyse et répond!**

---

## 🎬 Démonstration Rapide (5 min)

### Étape 1: Préparer un Fichier Test
```
Prendre une image: screenshot.png, photo.jpg, etc.
Mettre sur Desktop pour faciliter
```

### Étape 2: Lancer l'App
```bash
python main.py
```

### Étape 3: Joindre Fichier
```
Interface apparaît
  ↓
Voir bouton "📎 FICHIER" en bas à gauche
  ↓
Click
  ↓
Sélectionner image.jpg depuis Desktop
  ↓
OK
```

### Étape 4: Voir le Fichier Ajouté
```
Chat affiche:
  📎 Fichiers joints:
    🖼️ image.jpg (250 KB)
```

### Étape 5: Ajouter Question
```
Zone input: "Qu'est-ce que tu vois?"
```

### Étape 6: Envoyer
```
Click "✉️ ENVOYER"
ou
Appuyer Entrée
```

### Étape 7: Résultat
```
Agent analyse image et répond complètement
Fichier supprimé automatiquement
Prêt pour nouveau fichier
```

---

## 🎨 Ce Qu'On Peut Faire

### Avec des Images 🖼️
```
✅ "Qu'est-ce que tu vois?"          → Description complète
✅ "Lis le texte sur cet écran"     → OCR/Transcription
✅ "Compte les objets"              → Analyse détaillée
✅ "Interprète ce graphique"        → Analyse données
✅ "Décris les couleurs"            → Analyse visuelle
```

### Avec des Vidéos 🎥
```
✅ "Résume cette vidéo"             → Synthèse
✅ "Qu'est-ce qui se passe?"        → Description
✅ "Identifie les personnes"        → Détection
```

### Avec de l'Audio 🎵
```
✅ "Transcris cet audio"             → Texte complet
✅ "Résume ce discours"              → Points clés
✅ "Quel est le sujet?"              → Identification
```

### Avec des Documents 📄
```
✅ "Résume ce PDF"                   → Synthèse
✅ "Extrait les infos clés"          → Extraction
✅ "Traduis ce texte"                → Traduction
```

---

## 📋 Fichiers Supportés

### ✅ Images (6 formats)
```
.jpg, .jpeg, .png, .gif, .webp, .bmp
```

### ✅ Vidéos (6 formats)
```
.mp4, .avi, .mov, .mkv, .webm, .flv
```

### ✅ Audio (6 formats)
```
.mp3, .wav, .ogg, .m4a, .flac, .aac
```

### ✅ Documents (5 formats)
```
.pdf, .txt, .docx, .xlsx, .pptx
```

**Limite: 100 MB par fichier**

---

## 🎯 Cas d'Usage Réels

### Cas 1: Scanner de Reçus
```
1. Photographier reçu
2. 📎 FICHIER → photo_recei.jpg
3. "Extraire montants et dates"
4. Agent lit reçu
```

### Cas 2: Aide aux Devoirs
```
1. Photographier exercice math
2. 📎 FICHIER → exercice.jpg
3. "Explique la solution"
4. Agent décompose étapes
```

### Cas 3: Traduction Rapide
```
1. Screenshot texte étranger
2. 📎 FICHIER → text.png
3. "Traduis en français"
4. Agent traduit
```

### Cas 4: Analyse Code
```
1. Screenshot code source
2. 📎 FICHIER → code.png
3. "Que fait ce code?"
4. Agent explique
```

### Cas 5: Vérification Documents
```
1. Screenshot document
2. 📎 FICHIER → document.png
3. "Vérifie l'orthographe"
4. Agent corrige
```

---

## ⚙️ FAQ Rapide

### Q: Quel modèle d'IA analyse les images?
**A:** GPT-4V (Vision API) - le plus performant OpenAI

### Q: Comment joindre plusieurs fichiers?
**A:** Cliquer 📎 FICHIER plusieurs fois
- Button devient "📎 (2)" pour 2 fichiers
- Puis ENVOYER envoie tous

### Q: Et si j'oublie d'écrire un message?
**A:** Pas de souci! Agent dit: "Veuillez analyser le fichier joint"

### Q: Où sont stockés les fichiers?
**A:** Nulle part! Envoyés à OpenAI, puis supprimés automatiquement

### Q: Max 100 MB c'est gros?
**A:** Oui! Peut faire:
- 10+ images HD
- 1 vidéo courte
- Dizaines de fichiers audio

### Q: Comment supprimer un fichier jointe?
**A:** Cliquer 📎 bouton plusieurs fois, ou simplement ENVOYER

---

## 🚀 Shortcuts Clavier

| Action | Touche |
|--------|--------|
| Envoyer message | `Entrée` |
| Nouvelle ligne | `Maj + Entrée` |
| Joindre fichier | Click 📎 |
| Effacer chat | `Ctrl + L` |
| Mode Focus | `Ctrl + K` |

---

## 🔧 Dépannage Express

### Bouton 📎 n'apparaît pas
```bash
python main.py --no-gui  # Debug mode
```

### "Type de fichier non supporté"
→ Utiliser formats listés ci-dessus

### "Fichier trop volumineux"
→ Compresser ou utiliser plus petit

### Agent ne répond pas
→ Vérifier OPENAI_API_KEY dans .env

---

## 📚 Documentation Complète

Pour plus de détails, voir:
- `FILE_ATTACHMENT_GUIDE.md` - Guide complet (15 min)
- `FILE_ATTACHMENT_UPDATES.md` - Changements techniques (10 min)
- `test_file_attachment.py` - Tests integration

---

## ✅ Checklist Première Utilisation

- [ ] App lancée: `python main.py`
- [ ] Interface visible
- [ ] Bouton "📎 FICHIER" présent
- [ ] Fichier sélectionné et affiché
- [ ] Message écrit
- [ ] Message envoyé avec succès
- [ ] Agent a analysé le fichier
- [ ] Fichier disparu automatiquement

**Tous les points cochés? 🎉 Vous êtes prêt!**

---

## 🎓 Niveau Avancé

### Éditer Configuration
```python
# Dans file_handler.py
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 MB au lieu de 100
```

### Ajouter Format
```python
SUPPORTED_TYPES = {
    'image': ['.jpg', '.png', '.webp', '.tiff'],  # Ajouter .tiff
    ...
}
```

### Debug Messages
```bash
python main.py 2>&1 | grep -i "file\|attach"
```

---

## 🎉 C'est Parti!

**Vous avez maintenant un super-agent qui peut:**
- 👀 Voir et analyser images
- 📊 Interpréter graphiques
- 📄 Lire documents
- 🔊 Écouter et transcrire audio

**Lancez et essayez!**
```bash
python main.py
```

**Puis cliquez 📎 FICHIER et explorez! 🚀**

