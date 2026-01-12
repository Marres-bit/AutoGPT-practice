# 🔥 GEIS - Global Extreme Insanity Scanner

## 📋 Description

Module autonome de veille mondiale intégré à **MediGenius AI** pour détecter et archiver les contenus les plus insolites, choquants et viraux du monde entier.

## 🎯 Objectif

Créer automatiquement des dossiers structurés (Word + images) pour chaque contenu extrême détecté, avec :
- Titre choc accrocheur
- Description détaillée
- Images numérotées téléchargées
- Liens vidéos référencés
- Score de choc (1-10)
- Potentiel viral
- Sources tracées

## 🌍 Sources Analysées

- **Reddit**: r/WTF, r/PublicFreakout, r/CrazyFuckingVideos, etc.
- **YouTube**: Vidéos virales récentes
- **Twitter/X**: Tweets avec fort engagement
- **Faits divers**: Sites d'actualité insolite

## 📁 Structure de Sortie

```
Desktop/MedicalGeniusAI_Insanities/
├── Insanity_001/
│   ├── Insanity_001.docx
│   ├── Image_001.jpg
│   ├── Image_002.jpg
│   └── Image_003.jpg
├── Insanity_002/
│   ├── Insanity_002.docx
│   └── Image_001.jpg
└── processed_cache.json
```

## 🚀 Utilisation

### Scan manuel immédiat
```bash
python main_medical.py --geis-scan
```

### Mode daemon (scan toutes les 5h)
```bash
python main_medical.py --geis-daemon
```

### Afficher configuration
```bash
python main_medical.py --geis-config
```

### Test indépendant
```bash
python test_geis_scanner.py
```

## ⚙️ Configuration

Le fichier `insanity_scanner/config.py` contient tous les paramètres :

```python
min_insanity_score = 6.0  # Score minimal pour inclure un contenu
max_results_per_scan = 10  # Nombre max de rapports par scan
scan_interval_hours = 5  # Intervalle entre scans
max_content_age_days = 30  # Age max du contenu
```

### Variables d'environnement (optionnelles)

Pour accès API complet, créer un fichier `.env` :

```env
# Reddit (optionnel - API publique limitée sinon)
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_secret
REDDIT_USER_AGENT=GEIS_Scanner/1.0

# Twitter (optionnel)
TWITTER_BEARER_TOKEN=votre_bearer_token

# YouTube (optionnel)
YOUTUBE_API_KEY=votre_api_key
```

**Sans clés API**, le module fonctionne avec l'API publique Reddit (limitée).

## 📊 Algorithme de Scoring

Chaque contenu reçoit un score **1.0 à 10.0** basé sur :

1. **Engagement** (0-3 pts) : Upvotes, comments, likes, retweets
2. **Mots-clés choc** (0-3 pts) : "shocking", "wtf", "insane", etc.
3. **Viralité** (0-2 pts) : Vitesse de propagation
4. **Qualité source** (0-1 pt) : Fiabilité de la source
5. **Fraîcheur** (0-1 pt) : Contenu récent prioritaire

**Seuil minimal** : 6.0/10 (configurable)

## 📄 Contenu des Documents Word

Chaque rapport `.docx` contient :

- **Titre choc** en gros caractères
- **Description** détaillée de l'événement
- **Pourquoi c'est exceptionnel** (liste à puces)
- **Images** numérotées et insérées (Image_001, Image_002...)
- **Liens vidéos** référencés
- **Métadonnées** :
  - Source (Reddit, YouTube, Twitter...)
  - Origine géographique (si détectable)
  - Date
  - Score de choc (X/10 avec emojis 🔥)
  - Potentiel viral (faible / moyen / fort / explosif)
- **Sources** originales avec liens cliquables

## 🛡️ Protection & Cache

- **Cache des contenus traités** : Évite les doublons
- **Fichier** : `processed_cache.json`
- **Validation** : Chaque contenu scanné une seule fois

## 🔗 Intégration avec MediGenius AI

Les deux modules fonctionnent **en parallèle** sans interférence :

### Mode Medical seul
```bash
python main_medical.py  # Interface GUI médicale
```

### Mode GEIS seul
```bash
python main_medical.py --geis-scan
```

### Mode daemon complet (Medical + GEIS)
```bash
# Terminal 1: Medical daemon
python main_medical.py --no-gui

# Terminal 2: GEIS daemon
python main_medical.py --geis-daemon
```

## 📦 Dépendances

```bash
pip install praw requests python-docx schedule
```

- **praw** : Reddit API (optionnel)
- **requests** : Téléchargement images/APIs
- **python-docx** : Génération documents Word
- **schedule** : Planification scans (mode daemon)

## 🧪 Test

```bash
# Test complet du pipeline
python test_geis_scanner.py

# Vérifier dossier de sortie
ls ~/Desktop/MedicalGeniusAI_Insanities/
```

## 🚫 Contraintes Respectées

✅ Pas de contenu banal (score >= 6.0)
✅ Pas de doublons (cache)
✅ Qualité > quantité (max 10 par scan)
✅ Images numérotées et tracées
✅ Liens vidéos référencés
✅ Métadonnées complètes
✅ Sources vérifiables

## 📝 Logging

Fichier de log : `geis_scanner.log`

```log
2026-01-12 14:30:00 [GEIS] INFO: 🔥 Démarrage scan GEIS
2026-01-12 14:30:05 [GEIS] INFO: 📡 Scan source: reddit
2026-01-12 14:30:10 [GEIS] INFO: ✅ reddit: 47 items trouvés
2026-01-12 14:30:15 [GEIS] INFO: 🎯 8 items retenus (score >= 6.0)
2026-01-12 14:30:20 [GEIS] INFO: 📄 Rapport généré: Insanity_001.docx
```

## 🎯 Exemples de Contenus Détectés

- Accidents improbables filmés
- Comportements humains inexplicables
- Phénomènes naturels rares
- Situations absurdes du quotidien
- Vidéos "vous ne le croirez pas"
- Images dérangeantes mais réelles
- Faits divers extrêmes

## ⚠️ Notes Importantes

1. **Respect APIs** : Rate limiting automatique
2. **Éthique** : Pas de contenu illégal/dangereux
3. **Copyright** : Images téléchargées pour archivage personnel
4. **Qualité** : Filtrage agressif pour éviter le bruit

## 🔮 Évolutions Futures

- [ ] Support TikTok API
- [ ] Détection automatique de deepfakes
- [ ] Classification par catégories (accident, nature, humain...)
- [ ] Alertes push pour contenus score > 9.0
- [ ] Export PDF en plus de Word
- [ ] Dashboard web pour visualisation

---

**🧠 MediGenius AI** : Intelligence médicale professionnelle
**🔥 GEIS** : Radar mondial de l'insolite extrême

*Deux modules. Un seul agent.*
