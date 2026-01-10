# � MediGenius AI - Guide de Démarrage Rapide

**Assistant Médical Intelligent avec Stockage Cloud**

## Installation en 3 étapes

### 1️⃣ Vérifier Python
```bash
python --version
# Doit afficher Python 3.8 ou supérieur
```

### 2️⃣ Installer les dépendances
```bash
cd C:\Users\sanim\git-practice\AutoGPT
pip install -r requirements.txt
```

### 3️⃣ Configurer OpenAI
Créer un fichier `.env` :
```
OPENAI_API_KEY=votre_clé_ici
```

## 🚀 Lancement

### Option 1 : Double-clic (Recommandé)
```
Double-cliquer sur: lancer_medical_agent.bat
```

### Option 2 : Ligne de commande
```bash
python main_medical.py
```

## 💬 Commandes Rapides

Dans l'interface, tapez :

| Commande | Résultat |
|----------|----------|
| `/lesson Pneumonie` | Génère leçon complète |
| `/disease Asthme` | Recherche maladie |
| `/quiz Antibiotiques` | Crée un quiz |
| `/emergency Arrêt cardiaque` | Protocole urgence |
| `/help` | Voir toutes les commandes |

## 📅 Génération Automatique

L'agent génère automatiquement **3 leçons par semaine** :
- 🗓️ Lundi à 9h00
- 🗓️ Mercredi à 9h00
- 🗓️ Vendredi à 9h00

Voir le status :
```
/status
```

## 📊 Statistiques

Afficher vos statistiques :
```bash
python main_medical.py --stats
```

Ou dans l'interface :
```
/statistics
```

## 💾 Base de Données

Toutes les leçons sont sauvegardées dans :
```
medical_lessons.db
```

Exporter en JSON :
```
/export
```

## 🔍 Recherche

Rechercher dans toutes les leçons :
```
/search cardiovasculaire
```

Lister toutes les leçons :
```
/list
```

## 🧪 Test de l'Agent

Vérifier que tout fonctionne :
```bash
python test_medical_agent.py
```

Doit afficher :
```
🎯 Score: 4/4 tests réussis
🎉 TOUS LES TESTS SONT PASSÉS!
```

## ⚡ Génération Manuelle

Générer une leçon maintenant (sans attendre le scheduler) :
```
/generate
```

Ou générer plusieurs leçons :
```bash
python main_medical.py --generate 5
```

## 🔄 Mode Daemon (Background)

Lancer en arrière-plan sans interface :
```bash
python main_medical.py --no-gui
```

Utile pour :
- Laisser tourner sur un serveur
- Génération automatique en background
- Ne pas occuper l'écran

## 🛠️ Dépannage

### Interface ne se lance pas
```bash
pip install --upgrade openai schedule tkinter
```

### Erreur "No module named 'medical_agent'"
```bash
cd C:\Users\sanim\git-practice\AutoGPT
python main_medical.py
```

### Scheduler ne génère pas
Vérifier la configuration dans `medical_agent/config.py` :
```python
LESSONS_PER_WEEK = 3
LESSON_GENERATION_DAYS = [1, 3, 5]  # Lun=0, Mar=1, ...
LESSON_GENERATION_TIME = "09:00"
```

## 📖 Documentation Complète

Pour plus de détails, voir :
```
medical_agent/README.md
```

---

**🧽 Prêt à apprendre la médecine avec Dr. Bob !**
