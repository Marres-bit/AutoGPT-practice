# 🎉 CV PERFECTION MODULE - GUIDE DE DÉMARRAGE RAPIDE

## ⚡ Installation en 3 minutes

### 1. Installer les dépendances

```bash
cd c:\Users\sanim\git-practice\AutoGPT
pip install -r requirements_cv_module.txt
```

### 2. Configurer l'API OpenAI (optionnel)

Créer/éditer `.env` à la racine :
```
OPENAI_API_KEY=sk-votre-cle-ici
```

### 3. Tester l'installation

```bash
python test_cv_module.py
```

---

## 🚀 Utilisation immédiate

### Option A : Traitement manuel (recommandé)

```bash
# 1. Déposer un CV dans Bureau/CV/
# 2. Lancer
python main_medical.py --cv-scan
# 3. Récupérer dans Bureau/CV parfait/
```

### Option B : Surveillance automatique

```bash
python main_medical.py --cv-daemon
# Le système surveille Bureau/CV/ automatiquement
# Ctrl+C pour arrêter
```

---

## 📋 Commandes disponibles

```bash
python main_medical.py --cv-scan        # Traiter CV en attente
python main_medical.py --cv-daemon      # Mode surveillance (5 min)
python main_medical.py --cv-config      # Afficher configuration
python main_medical.py --cv-stats       # Statistiques
```

---

## 📁 Structure des dossiers

```
Bureau/
├── CV/              # ⬅️ DÉPOSEZ VOS CV ICI
└── CV parfait/      # ➡️ RÉCUPÉREZ VOS CV ICI
```

---

## ✅ Vérifications

### Le module fonctionne si :

✓ `Bureau/CV/` existe  
✓ `Bureau/CV parfait/` créé automatiquement  
✓ Packages installés (PyPDF2, reportlab, etc.)  
✓ CV format PDF ou DOCX  
✓ Taille fichier > 10 KB  

### Formats supportés :

✅ PDF  
✅ DOCX  
❌ TXT (non supporté)  
❌ Images (non supporté)  

---

## 🎨 Résultat attendu

Pour chaque CV traité, vous obtenez :

1. **CV_Parfait_NomPrenom_Moderne.pdf** - CV redesigné
2. **Rapport_Amelioration_NomPrenom.txt** - Explications détaillées

---

## 🆘 Problèmes fréquents

### "Module cv_perfection not found"
```bash
# Vérifier que vous êtes dans le bon dossier
cd c:\Users\sanim\git-practice\AutoGPT
python main_medical.py --cv-config
```

### "ReportLab non installé"
```bash
pip install reportlab
```

### "Aucun CV détecté"
- Vérifier que fichier est .pdf ou .docx
- Vérifier taille > 10 KB
- Vérifier emplacement : Bureau/CV/

---

## 📖 Documentation complète

Voir [README_CV_MODULE.md](README_CV_MODULE.md) pour guide détaillé.

---

## ✨ Premier test

```bash
# 1. Installer
pip install -r requirements_cv_module.txt

# 2. Tester
python test_cv_module.py

# 3. Vérifier config
python main_medical.py --cv-config

# 4. Déposer un CV dans Bureau/CV/

# 5. Traiter
python main_medical.py --cv-scan

# 6. ✅ Profiter de votre CV parfait !
```

---

**Module créé avec ❤️ pour Medical Genius AI**  
Version 1.0.0 - Janvier 2026
