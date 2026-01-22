# 💼 CV Perfection & Design Intelligence Module (CV-PDI)

## 🎯 Vue d'ensemble

Le **CV-PDI** est un module autonome intégré à Medical Genius AI qui transforme automatiquement vos CV en documents professionnels de niveau designer expert.

### Fonctionnalités principales

✅ **Surveillance automatique** - Détecte les nouveaux CV dans Bureau/CV  
✅ **Analyse intelligente** - Évalue structure, ATS, typographie, hiérarchie  
✅ **Optimisation IA** - Améliore textes sans falsifier (GPT-4)  
✅ **Design professionnel** - 5 styles premium (Canva/Adobe niveau)  
✅ **Rapports détaillés** - Explications des améliorations apportées  
✅ **Sécurité garantie** - Ne modifie JAMAIS le fichier original  

---

## 🚀 Installation rapide

### Prérequis

```bash
pip install PyPDF2 python-docx reportlab openai schedule
```

### Configuration

1. **Créer le dossier d'entrée** :
   ```
   Bureau/CV/
   ```

2. **Configurer l'API OpenAI** (optionnel mais recommandé) :
   ```bash
   # Dans .env à la racine du projet
   OPENAI_API_KEY=sk-...
   ```

3. **Vérifier la config** :
   ```bash
   python main_medical.py --cv-config
   ```

---

## 📖 Guide d'utilisation

### Mode 1 : Traitement manuel (recommandé pour débuter)

```bash
# 1. Déposer un CV dans Bureau/CV/
# 2. Lancer le traitement
python main_medical.py --cv-scan
```

**Résultat** : CV amélioré dans `Bureau/CV parfait/`

### Mode 2 : Surveillance automatique (daemon)

```bash
python main_medical.py --cv-daemon
```

**Comportement** :
- Scanne le dossier Bureau/CV toutes les 5 minutes
- Traite automatiquement les nouveaux CV
- Tourne en arrière-plan
- `Ctrl+C` pour arrêter

### Mode 3 : Statistiques

```bash
python main_medical.py --cv-stats
```

Affiche :
- Nombre de CV traités
- Taux de succès
- Fichiers en cache

---

## 🎨 Styles de design disponibles

Le module génère des CV dans **5 styles professionnels** :

### 1. **Classique** (Corporate traditionnel)
- Police : Times New Roman / Georgia
- Couleurs : Noir/Gris
- Idéal pour : Finance, Juridique, Administration

### 2. **Moderne** (Par défaut)
- Police : Calibri / Arial
- Couleurs : Bleu moderne
- Idéal pour : Tech, Startup, Marketing

### 3. **Corporate**
- Police : Arial / Helvetica
- Couleurs : Bleu foncé professionnel
- Idéal pour : Conseil, Management, RH

### 4. **Minimaliste**
- Police : Helvetica / Arial
- Couleurs : Noir/Gris clair
- Idéal pour : Design, Architecture, Creative

### 5. **Creative**
- Police : Montserrat / Open Sans
- Couleurs : Rouge accent
- Idéal pour : Communication, Pub, Médias

**Activer génération multiple styles** :
```python
# Dans cv_perfection/config.py
generate_multiple_styles = True  # Génère les 5 styles
```

---

## 📊 Workflow de traitement

```
CV Original (Bureau/CV/)
    ↓
┌─────────────────────────┐
│ 1. SCAN & DÉTECTION     │
│ - Nouveaux fichiers     │
│ - Vérification format   │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ 2. ANALYSE              │
│ - Structure (0-10)      │
│ - Compatibilité ATS     │
│ - Typographie           │
│ - Hiérarchie visuelle   │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ 3. OPTIMISATION         │
│ - Réécriture sections   │
│ - Verbes d'action       │
│ - Ton professionnel     │
│ - SANS falsification    │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ 4. DESIGN PROFESSIONNEL │
│ - Application style     │
│ - Mise en page          │
│ - Typographie premium   │
│ - Export PDF haute qualité
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ 5. RAPPORT              │
│ - Scores d'analyse      │
│ - Améliorations         │
│ - Recommandations       │
└─────────────────────────┘
    ↓
CV Parfait (Bureau/CV parfait/)
+ Rapport d'amélioration
```

---

## 🔒 Sécurité & Confidentialité

### Garanties

✅ **Original préservé** - Fichier source JAMAIS modifié  
✅ **Pas d'invention** - Données authentiques uniquement  
✅ **Traitement local** - Données ne quittent pas votre machine (sauf API OpenAI)  
✅ **Cache sécurisé** - Hashage MD5 pour détecter doublons  

### Données envoyées à OpenAI (si activé)

- Sections de texte uniquement (max 1000 caractères/section)
- PAS de fichier complet
- PAS de données personnelles identifiables
- Uniquement pour reformulation textuelle

---

## ⚙️ Configuration avancée

### Fichier : `cv_perfection/config.py`

```python
# Intervalle de scan (minutes)
scan_interval_minutes = 5

# Styles à générer
generate_multiple_styles = False  # True = tous les styles
default_style = 'Moderne'

# Optimisation IA
optimize_content = True  # False = skip optimisation
openai_model = "gpt-4o-mini"  # ou "gpt-4"

# Sécurité
never_invent_data = True  # TOUJOURS True !
preserve_original = True  # TOUJOURS True !

# Rapports
generate_improvement_report = True
report_language = "fr"
```

---

## 📁 Structure des fichiers

```
Bureau/
├── CV/                          # ENTRÉE (déposez vos CV ici)
│   ├── CV_John_Doe.pdf
│   └── Mon_CV_2024.docx
│
└── CV parfait/                  # SORTIE (CV améliorés)
    ├── CV_Parfait_John_Doe_Moderne.pdf
    ├── Rapport_Amelioration_John_Doe.txt
    ├── cv_processed_cache.json  # Cache anti-doublons
    ├── cv_scanner.log           # Logs scanner
    └── cv_processor.log         # Logs processeur
```

---

## 🎓 Exemples d'utilisation

### Scénario 1 : Améliorer un CV pour candidature urgente

```bash
# 1. Copier CV dans Bureau/CV/
cp Mon_CV.pdf ~/Desktop/CV/

# 2. Traiter immédiatement
python main_medical.py --cv-scan

# 3. Récupérer CV parfait
# Résultat : Bureau/CV parfait/CV_Parfait_Mon_CV_Moderne.pdf
```

### Scénario 2 : Optimiser plusieurs CV d'une équipe

```bash
# 1. Activer génération multiple styles
# Éditer config.py : generate_multiple_styles = True

# 2. Déposer tous les CV dans Bureau/CV/

# 3. Traiter en lot
python main_medical.py --cv-scan

# 4. Résultat : 5 versions par CV (tous les styles)
```

### Scénario 3 : Surveillance continue (cabinet de recrutement)

```bash
# Démarrer daemon
python main_medical.py --cv-daemon

# Laisser tourner en arrière-plan
# Chaque nouveau CV dans Bureau/CV/ sera traité automatiquement
```

---

## 🛠️ Troubleshooting

### Problème : "ReportLab non installé"

```bash
pip install reportlab
```

### Problème : "PyPDF2 non installé"

```bash
pip install PyPDF2
```

### Problème : "Optimisation limitée (OpenAI non configurée)"

```bash
# Configurer dans .env
OPENAI_API_KEY=sk-your-key-here
```

### Problème : CV pas détecté

Vérifier :
- ✅ Extension : `.pdf` ou `.docx`
- ✅ Taille : > 10 KB
- ✅ Nom : Pas commencer par `~` ou `.`
- ✅ Dossier : Bien dans `Bureau/CV/`

### Problème : "Score d'analyse très bas"

Causes communes :
- CV sans sections claires (Expérience, Formation, etc.)
- Texte non extractible (PDF image)
- Format trop complexe

**Solution** : Convertir en .docx ou simplifier structure

---

## 🤝 Intégration avec Medical Genius AI

Le module CV-PDI est **100% indépendant** et ne perturbe PAS les fonctions médicales :

```bash
# Utiliser simultanément
python main_medical.py --no-gui           # Medical daemon
python main_medical.py --cv-daemon        # CV daemon
python main_medical.py --geis-daemon      # GEIS daemon

# Tous peuvent tourner en parallèle !
```

---

## 📈 Roadmap futures améliorations

### Version 2.0 (planifiée)

- [ ] Support langues multiples (EN, DE, ES)
- [ ] Templates spécifiques par industrie
- [ ] Analyse sémantique avancée (matching offre d'emploi)
- [ ] Export DOCX éditable
- [ ] Interface web de prévisualisation
- [ ] Intégration LinkedIn (import/export)
- [ ] Scoring ATS avec outils externes

---

## 💡 Conseils d'expert

### Pour candidats

1. **Utilisez le style adapté** à votre secteur
2. **Vérifiez le rapport** pour comprendre les améliorations
3. **Personnalisez** le CV généré pour chaque candidature
4. **Testez l'ATS** avec des outils comme Jobscan
5. **Conservez** plusieurs versions (par secteur)

### Pour recruteurs

1. **Activez le daemon** pour traitement automatique
2. **Générez tous les styles** pour proposer options aux candidats
3. **Utilisez les rapports** pour feedback constructif
4. **Cache automatique** évite retraitements

---

## 📞 Support

**Logs** :
- Scanner : `Bureau/CV parfait/cv_scanner.log`
- Processor : `Bureau/CV parfait/cv_processor.log`

**Commandes debug** :
```bash
python main_medical.py --cv-config  # Vérifier config
python main_medical.py --cv-stats   # Statistiques
```

---

## ✨ Créé avec excellence

**CV Perfection & Design Intelligence Module**  
Intégré à Medical Genius AI  
Version 1.0.0

Transforme vos CV en chef-d'œuvres professionnels. 🎯
