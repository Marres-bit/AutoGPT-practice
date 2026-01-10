# 🚀 DÉMARRAGE RAPIDE - Analyseur Crypto Ultra Autonome

**INSTALLATION ET LANCEMENT EN 3 MINUTES** ⏱️

---

## 1️⃣ INSTALLER LES DÉPENDANCES (30 secondes)

```bash
pip install -r requirements.txt
```

✅ Installe: requests, python-docx, schedule, pyttsx3, SpeechRecognition, openai, python-dotenv

---

## 2️⃣ LANCER L'APPLICATION (3 commandes au choix)

### Option A: MODE COMPLET (Recommandé) 🎯
```bash
python main.py
```
**Inclut:**
- ✅ Interface GUI premium interactive
- ✅ Analyseur crypto autonome
- ✅ Rapports Word auto sur Bureau
- ✅ Reads audio des réponses
- ✅ Chat avec IA en temps réel

**Résultat:** Interface GUI + Scheduler en arrière-plan

---

### Option B: MODE DAEMON (Arrière-plan pur)
```bash
python main.py --no-gui --interval 2
```
**Inclut:**
- ✅ Pas d'interface GUI
- ✅ Analyseur crypto en loop continue
- ✅ Rapports Word auto toutes les 2 heures
- ✅ Peut tourner en service Windows

**Résultat:** Analyseur continu sans GUI

---

### Option C: MODE PERSONNALISÉ
```bash
python main.py --interval 6
```
**Options:**
- `--interval 4` - Analyser toutes les 4 heures (défaut)
- `--interval 2` - Analyser toutes les 2 heures
- `--no-gui` - Sans interface (daemon)
- `--autonomous` - Mode autonome au démarrage Windows

---

## 3️⃣ RÉSULTATS GÉNÉRÉS 📊

### Sur votre Bureau (Desktop):
```
📄 Crypto_Compte_rendu_2026-01-09.docx
📄 Crypto_Compte_rendu_2026-01-10.docx
📄 Crypto_Compte_rendu_2026-01-11.docx
```

**Contenu:**
- 📈 Cryptos avec meilleure hausse 24h
- 📉 Cryptos avec plus forte baisse 24h
- 💹 Analyse détaillée pour chacune
- 📊 Tableau complet avec métriques
- ⏰ Timestamp de l'analyse

---

## 🎯 CE QUI SE PASSE

### Timeline d'exécution:

```
T+0:00  ► Lancement de main.py
T+0:01  ► GUI se lance
T+0:01  ► Scheduler autonome démarre en thread
T+0:05  ► Première analyse crypto (parallèle)
T+0:10  ► Rapport Word créé sur Bureau
T+0:10  ► GUI reste 100% responsive
T+4:00  ► Analyse suivante (intervalle par défaut)
T+8:00  ► Analyse suivante
...
T+∞    ► Continue jusqu'à fermeture
```

**Important:** Toutes les analyses se font en **arrière-plan** sans bloquer la GUI!

---

## 🔧 DÉMARRAGE AUTOMATIQUE WINDOWS (Optionnel)

### Activer le lancement au boot:

```python
from windows_startup import WindowsAutoStartup

WindowsAutoStartup.enable_startup()
```

✅ Au prochain redémarrage, l'app se lance automatiquement!

**Ou manuellement:**
1. Appuyez sur `WIN + R`
2. Tapez: `shell:startup`
3. Copiez `run_autonomous.bat` dans ce dossier

---

## 📊 EXEMPLE DE RAPPORT GÉNÉRÉ

```
═══════════════════════════════════════════════════════════
📊 RAPPORTS D'ANALYSES CRYPTO AUTONOMES
═══════════════════════════════════════════════════════════

📅 Analyse du 09/01/2026 à 14:32:15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Cryptos en hausse: 12 | 📉 Cryptos en baisse: 8

┌──────────┬──────────┬────────────┬──────────────┐
│ Crypto   │ Prix     │ Variation  │ Analyse      │
├──────────┼──────────┼────────────┼──────────────┤
│ BTC      │ $45,000  │ +5.50%     │ 📈 FORT      │
│ ETH      │ $2,500   │ -3.20%     │ 📉 MODÉRÉ    │
│ SOL      │ $125.00  │ +12.35%    │ ⚡ TRÈS FORT │
│ ADA      │ $1.25    │ +2.10%     │ 📊 Hausse    │
└──────────┴──────────┴────────────┴──────────────┘

Rapport généré automatiquement le 09/01/2026 à 14:32:15
```

---

## ⏲️ INTERVALLES RECOMMANDÉS

| Besoin | Intervalle | Commande |
|--------|-----------|----------|
| 🚀 Trader actif | 1-2 heures | `--interval 1` |
| 📊 Investisseur | 4-6 heures | `--interval 4` |
| 👁️ Observateur | 12-24 heures | `--interval 12` |

---

## 🎮 CONTRÔLES DANS LA GUI

### Clavier:
- `Entrée` - Envoyer message
- `Ctrl+K` - Mode Focus (épuré)
- `Ctrl+L` - Effacer le chat
- `/summarize` - Résumer la conversation
- `/explain` - Expliquer un point

### Souris:
- 🎙️ **Microphone** - Parler (quand audio est activé)
- 🔊 **Audio** - Écouter les réponses
- 🎯 **Focus** - Mode concentré
- ⚙️ **Paramètres** - Options avancées

---

## 🐛 SI QUELQUE CHOSE NE FONCTIONNE PAS

### Vérifier les imports:
```bash
python -c "
from crypto_analyzer import CryptoAnalyzer
from word_reporter import WordReporter
from autonomous_scheduler import AutonomousScheduler
print('OK - All modules work!')
"
```

### Vérifier les dépendances:
```bash
pip list | findstr "requests docx schedule"
```

### Relancer avec les logs:
```bash
python main.py 2>&1 | Tee-Object -FilePath debug.log
```

### Tester chaque module séparément:
```bash
python crypto_analyzer.py       # Test analyseur
python word_reporter.py         # Test rapports
python autonomous_scheduler.py  # Test scheduler
```

---

## 📁 FICHIERS CRÉÉS/MODIFIÉS

### 🆕 NOUVEAUX:
- `crypto_analyzer.py` - Analyseur crypto
- `word_reporter.py` - Générateur Word
- `autonomous_scheduler.py` - Scheduler
- `windows_startup.py` - Démarrage auto
- `test_crypto_analyzer.py` - Tests
- `CRYPTO_ANALYZER_GUIDE.md` - Doc complète
- `QUICKSTART_CRYPTO.md` - Ce fichier

### ✏️ MODIFIÉS:
- `main.py` - Intégration scheduler
- `requirements.txt` - Nouvelles dépendances

### 📊 GÉNÉRÉS:
- `Desktop/Crypto_Compte_rendu_*.docx` - Rapports

---

## 💡 ASTUCES PRATIQUES

### Accélérer les analyses:
```bash
# Analyser toutes les 30 minutes au lieu de 4h
python main.py --interval 0.5
```

### Réduire les cryptos analysées:
```python
# Dans crypto_analyzer.py, ligne 50:
analyzer = CryptoAnalyzer(min_variation=10.0)  # Variations > 10%
analyzer = CryptoAnalyzer(max_results=20)      # Max 20 cryptos
```

### Garder seulement les rapports récents:
```bash
# Supprimer rapports > 30 jours
python -c "
from pathlib import Path
import time
desktop = Path.home() / 'Desktop'
for f in desktop.glob('Crypto_Compte_rendu_*.docx'):
    if time.time() - f.stat().st_mtime > 30*86400:
        f.unlink()
"
```

---

## ✅ CHECKLIST DE DÉMARRAGE

- [ ] `pip install -r requirements.txt` ✓
- [ ] `python main.py` fonctionne ✓
- [ ] Rapports créés sur le Bureau ✓
- [ ] GUI reste responsive ✓
- [ ] Scheduler s'exécute ✓
- [ ] (Optionnel) Démarrage auto activé ✓

---

## 🎉 VOUS ÊTES PRÊT!

Votre système est maintenant:

✅ **Ultra autonome** - Tourne 24/7  
✅ **Intelligent** - Analyse crypto complète  
✅ **Automatisé** - Rapports sans intervention  
✅ **Responsive** - GUI fluide même en analyse  
✅ **Robuste** - Gère tous les erreurs  

**C'EST PARTI!** 🚀

---

## 📞 POUR PLUS D'INFOS

Voir: `CRYPTO_ANALYZER_GUIDE.md` pour guide complet
