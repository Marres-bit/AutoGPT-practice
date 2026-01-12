# 📋 CONTEXT MEMO - Agent Trading & Medical AI
**Dernière mise à jour** : 2026-01-12 17:15  
**Objectif** : Permettre à tout nouveau Copilot de reprendre le contexte complet en 5 minutes

---

## 🔄 SYSTÈME DE MISE À JOUR (IMPORTANT)

**Comment garder ce fichier à jour** :
- User dit : **"Update context"**
- Copilot met à jour en 30s (état systèmes, nouveaux bugs, commits)
- Trigger : Après bug critique, nouvelle fonctionnalité, décision architecturale majeure

**Pourquoi ce fichier existe** :
- Chaque fenêtre VS Code = session Copilot isolée (pas de mémoire partagée)
- Extensions VS Code persistent (même après fermeture/redémarrage)
- Ce fichier permet au nouveau Copilot de récupérer 95% du contexte en 5-10 min

**Note** : Les conversations ne se transfèrent PAS entre fenêtres. Ce fichier compense cette limite.

---

## 🎯 RÉSUMÉ EXÉCUTIF (Lis ça d'abord !)

Vous travaillez sur **3 agents AI autonomes indépendants** :

1. **Agent Trading Crypto** : Bot Binance avec Kelly Criterion, multi-timeframe, gestion de risque
2. **GEIS Scanner** : Détecteur de contenus viraux extrêmes (Reddit/Twitter/YouTube)
3. **Medical Agent** : Générateur de leçons infirmières en allemand (Pflegeschüler)

**État actuel** : Les 3 systèmes sont **100% opérationnels et testés**

---

## 🔥 BUGS CRITIQUES RÉSOLUS (À CONNAÎTRE ABSOLUMENT)

### 1. BUG PRIX FICTIFS (RÉSOLU - 2026-01-12 08:12)
**Symptôme** : Rapports montrant BTC à $993 au lieu de $91,828  
**Cause** : Fallback silencieux `entry_price=1000$` quand API Binance échouait  
**Impact** : Position sizing 90x trop petit, learning data corrompue  
**Solution** : 
- SUPPRIMÉ fallback ligne 413-430 de `autonomous_scheduler.py`
- Validation obligatoire `if entry_price < 100: raise ValueError`
- Agent refuse maintenant de trader sans prix réels
- Commits : f6adbefee, 7b8c75a60

### 2. BUG KELLY CRITERION (RÉSOLU - 2026-01-12 08:00)
**Symptôme** : Kelly à 23.33% (4-5x trop élevé pour standards professionnels)  
**Cause** : Plafond initial à 25%  
**Solution** : Plafond abaissé à 10% (ligne 177 `risk_manager.py`)  
**Commit** : 9520c976b

### 3. BUG STOP-LOSS INCONSISTANT (RÉSOLU)
**Symptôme** : Stop-loss à -3% mais règle déclarée à -2%  
**Cause** : Pas d'adaptation au niveau de risque  
**Solution** : Stop-loss adaptatif (lignes 155-169 `risk_manager.py`)
- CONSERVATIVE: 1.5%
- MODERATE: 2%
- AGGRESSIVE: 3%
- EXTREME: 5%

### 4. BUG EMERGENCY STOP (RÉSOLU - 2026-01-12 10:08)
**Symptôme** : Drawdown 21.9% > limite 20% (stop déclenché)  
**Cause** : Drawdown calculé sur trades avec prix fictifs  
**Solution** : Reset complet des états (voir section Fichiers Critiques)  
**Commit** : 123f2687f

### 5. BUG SIGNATURE RISK MANAGER (RÉSOLU)
**Symptôme** : `TypeError: unexpected keyword argument 'trade_info'`  
**Cause** : Appel incorrect `update_after_trade(trade_info=...)`  
**Solution** : Signature correcte `update_after_trade(current_capital, pnl, was_win)`  
**Commit** : 7b8c75a60

---

## 📁 ARCHITECTURE DES 3 AGENTS

### 🤖 Agent Trading Crypto
**Localisation** : `c:\Users\sanim\git-practice\AutoGPT\`  
**Commande** : `python run_autonomous.py --service --interval 2`  
**Fréquence** : Analyse toutes les 2h, rapports Desktop/Suivi crypto de Marres/

**Fichiers principaux** :
- `run_autonomous.py` : Point d'entrée
- `autonomous_scheduler.py` : Orchestrateur (cycles 2h)
- `strategy_fusion.py` : Multi-timeframe (15m/1h/4h confluence)
- `risk_manager.py` : Kelly Criterion, stop-loss, emergency stop
- `exchange_connector.py` : Connexion Binance (testnet/production)
- `advanced_reporting.py` : Génération rapports Word
- `learning_engine.py` : Apprentissage des patterns gagnants

**État actuel** :
- Capital : $10,000 (testnet)
- Win rate : 0% (0 trades - état clean après reset)
- Drawdown : 0%
- Seuil confiance : 50% (SOL récent à 26% → pas tradé, CORRECT)
- Prix réels validés : BTC=$91,828, ETH=$3,156, SOL=$142

**Mode production** :
- Prêt mais PAS activé (voir PASSAGE_PRODUCTION.md)
- Nécessite : API keys Binance, testnet=False
- Recommandation : 2-4 semaines testnet + win rate >60%

### 🔮 GEIS Scanner (Global Extreme Insanity Scanner)
**Localisation** : `c:\Users\sanim\git-practice\AutoGPT\insanity_scanner\`  
**Commande** : `python main_medical.py --geis-scan` (manuel) ou `--geis-daemon` (auto 5h)  
**Output** : Desktop/MedicalGeniusAI_Insanities/Insanity_XXX/

**Fichiers** :
- `scanner.py` : Orchestrateur principal
- `sources.py` : Reddit, YouTube, Twitter, FaitsDivers
- `scorer.py` : Algorithme scoring 1-10
- `report_generator.py` : Création Word docs + images
- `config.py` : GEISConfig (min_score=6.0, interval=5h)

**Algorithme scoring (5 critères)** :
- Engagement (0-3) : Upvotes, comments, likes
- Keywords (0-3) : "shocking", "wtf", "insane", etc.
- Virality (0-2) : Taux engagement/heure
- Source (0-1) : Reddit=1.0, YouTube=0.8, Twitter=0.7
- Freshness (0-1) : <1 jour=1.0

**Test validé** : 6 rapports générés en 3.8s (Insanity_001 à Insanity_006)

### 🏥 Medical Agent (MediGenius AI - Pflege Ausbildung)
**Localisation** : `c:\Users\sanim\git-practice\AutoGPT\medical_agent\`  
**Commande** : `python main_medical.py --no-gui` (daemon) ou `python test_pflege_lecon.py` (test)  
**Fréquence** : 3 leçons/semaine (Lun/Mer/Ven 9h)  
**Output** : Desktop/Pflege ausbildung/Pflege azubis_YYYYMMDD_HHMMSS.docx

**Particularités** :
- Langue : **ALLEMAND** (Deutsch)
- Cible : Pflegeschüler (apprentis infirmiers)
- Section obligatoire : **PFLEGEPLANUNG** (plan de soins)
- Document : "Pflege azubis"
- Catégories : Kardiologie, Pneumologie, Neurologie, etc. (en allemand)

**Fichiers modifiés pour allemand** :
- `config.py` : AGENT_LANGUAGE="de", catégories traduites, prompt allemand
- `agent.py` : System prompt nursing expert (ligne 82)
- `commands.py` : Export vers OUTPUT_FOLDER (lignes 213-224)

**Test validé** : Leçon "Pneumonie" avec section Pflege Plannung confirmée

---

## 📂 FICHIERS CRITIQUES & BACKUPS

### États Reset (2026-01-12 10:14)
**Raison** : Données corrompues par prix fictifs + emergency stop

**Fichiers SUPPRIMÉS** (backups créés) :
```
risk_state.json → risk_state.json.backup_20260112_101418
learning_state.json → learning_state.json.backup_20260112_101423
drawdown_history.json → (supprimé sans backup, recréé auto)
```

**Contenu backups** (pour info historique) :
- `risk_state.json.backup` : drawdown=21.9%, peak_capital=10000, trades_today=0
- `learning_state.json.backup` : win_rate=89%, 0 trades historique (fake data)

**États actuels** (propres) :
- `risk_state.json` : Recréé, drawdown=0%, peak_capital=10000
- `learning_state.json` : Recréé, win_rate=0%, 0 trades
- `drawdown_history.json` : Recréé, liste vide []

### GEIS Cache
```
Desktop/MedicalGeniusAI_Insanities/processed_cache.json
```
Anti-duplicates, contient IDs Reddit/Twitter déjà traités

---

## 🔑 DÉCISIONS ARCHITECTURALES (POURQUOI)

### Pourquoi Kelly à 10% max (pas 25%) ?
Standards professionnels : 2-5% pour fonds hedge, 10% déjà agressif pour retail. 25% = trop volatil.

### Pourquoi refuser trades sans prix réels ?
Erreur silencieuse = catastrophe production. Mieux échouer bruyamment que trader avec données fausses.

### Pourquoi stop-loss adaptatif ?
CONSERVATIVE doit être vraiment conservateur (1.5%), AGGRESSIVE peut tolérer -3%. Cohérence nom/comportement.

### Pourquoi reset complet des états ?
Drawdown 21.9% basé sur trades fictifs = métrique inutile. Learning data corrompue = faux patterns. Clean slate obligatoire.

### Pourquoi 3 agents séparés (pas 1 monolithe) ?
- Indépendance : GEIS crash ≠ trading arrêté
- Maintenance : Modifier medical ≠ risque crypto
- Scaling : Chaque agent peut tourner sur machine différente

### Pourquoi allemand pour Medical Agent ?
User travaille infirmerie en Allemagne, élèves germanophones. "Pflege Plannung" = concept légal allemand spécifique.

### Pourquoi seuil confiance 50% ?
Balance exploitation/exploration. <50% = pattern trop faible, >70% = trop peu trades. 50% = sweet spot.

---

## 🚀 COMMANDES ESSENTIELLES

### Agent Trading - Vérifier état
```powershell
# Log derniers cycles
Get-Content "c:\Users\sanim\git-practice\AutoGPT\sp_agent.log" -Tail 50

# Dernier rapport
Get-ChildItem "$env:USERPROFILE\Desktop\Suivi crypto de Marres\" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Prix réels actuels
cd "c:\Users\sanim\git-practice\AutoGPT"
python exchange_connector.py
```

### Agent Trading - Redémarrer
```powershell
# Arrêter processus en cours
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Démarrer
Push-Location "c:\Users\sanim\git-practice\AutoGPT"
python run_autonomous.py --service --interval 2
```

### GEIS - Scan manuel
```powershell
cd "c:\Users\sanim\git-practice\AutoGPT"
python main_medical.py --geis-scan
```

### Medical Agent - Test génération
```powershell
cd "c:\Users\sanim\git-practice\AutoGPT"
python test_pflege_lecon.py
```

### Git - Historique corrections
```powershell
cd "c:\Users\sanim\git-practice\AutoGPT"
git log --oneline -20
git show 123f2687f  # Nettoyage production
git show f6adbefee  # Fix prix réels
git show 9520c976b  # Fix Kelly + stop-loss
```

---

## 📊 ÉTAT ACTUEL SYSTÈMES (2026-01-12 17:15)

### ✅ Agent Trading Crypto
- Status : **OPÉRATIONNEL** (testnet)
- Dernier cycle : 2h depuis dernier rapport
- Trades : 0 (seuil confiance pas atteint)
- Drawdown : 0.00%
- Prochain rapport : +2h
- Prêt production : OUI (mais attendre validation)

### ✅ GEIS Scanner  
- Status : **OPÉRATIONNEL**
- Dernier scan : Test manuel 6 rapports
- Reddit API : Fonctionnel (mode public)
- YouTube/Twitter : Nécessitent API keys (optionnel)
- Daemon : NON activé

### ✅ Medical Agent
- Status : **OPÉRATIONNEL**
- Dernière leçon : "Pneumonie" (test validé)
- Langue : Allemand ✅
- Pflege Plannung : Validé ✅
- Scheduler : NON activé (génération manuelle)

### 📋 CONTEXT_MEMO.md
- Status : **CRÉÉ** (2026-01-12 17:00)
- Taille : ~300 lignes
- Système mise à jour : Option 1 activé ("Update context")
- Localisation : `c:\Users\sanim\git-practice\AutoGPT\CONTEXT_MEMO.md`

---

## 📋 PROCHAINES ÉTAPES (ROADMAP)

### Phase 1 : Validation Testnet (EN COURS)
- [ ] 2-4 semaines trading testnet
- [ ] Objectif : Win rate >60%, drawdown <10%
- [ ] Monitorer rapports toutes les 2h
- [ ] Valider confidence threshold 50% efficace

### Phase 2 : Production Crypto (BLOQUÉ - Décision user)
**Prérequis** :
1. Créer API keys Binance (Trading ON, Withdrawal OFF)
2. Restriction IP obligatoire
3. Variables environnement BINANCE_API_KEY/BINANCE_API_SECRET
4. Modifier `testnet=False` dans exchange_connector.py
5. Capital initial : $500-1000 recommandé

**Guide complet** : Lire `PASSAGE_PRODUCTION.md`

### Phase 3 : Features Avancées (FUTUR)
**Phase 2 Trading** :
- Sentiment Analysis (Twitter/Reddit/News API)
- ML Predictions (LightGBM sur 6 mois historique)
- Regime Detection (trending/sideways/volatile)

**Phase 3 Trading** :
- Portfolio Optimization (Markowitz)
- VaR/CVaR calculation
- Reinforcement Learning (PPO agent)

**GEIS Enhancements** :
- TikTok API support
- Deepfake detection
- Category classification
- PDF export option

**Medical Agent** :
- Activer scheduler automatique (3/semaine)
- Base de données quiz interactifs
- Export PDF option

---

## 🆘 TROUBLESHOOTING RAPIDE

### Agent Trading ne trade pas
✅ **NORMAL** si confidence <50%. Vérifier log :
```
[INFO] Analyse BTC/USDT : confidence 26% < seuil 50%
```

### Rapport affiche prix bizarres (< $100)
❌ **BUG PRIX RÉEL** réapparu ! Vérifier :
```powershell
python exchange_connector.py
```
Si échec : vérifier internet, Binance status

### Emergency stop déclenché
Vérifier `risk_state.json` :
```json
{"drawdown_pct": 21.5, "emergency_stop_active": true}
```
Si drawdown fake (pas de trades récents) : DELETE risk_state.json, restart agent

### GEIS retourne 0 résultats
- Vérifier Reddit accessible (pas down)
- Score threshold 6.0 très sélectif (normal 0-3 résultats/scan)
- Tester avec `min_score=5.0` dans config.py

### Medical Agent génère en anglais
Vérifier `config.py` :
```python
AGENT_LANGUAGE = "de"  # DOIT être "de" pas "en"
```

### Git push échoue
Branches : `update-name` (local) → `update-name` (remote)
```powershell
git pull origin update-name  # Sync first
git push origin update-name
```

---

## 📞 CONTACT & RÉFÉRENCES

**User** : sanim  
**Workspace** : `c:\Users\sanim\git-practice\AutoGPT\`  
**Desktop Output** :
- Crypto : `Desktop/Suivi crypto de Marres/`
- GEIS : `Desktop/MedicalGeniusAI_Insanities/`
- Medical : `Desktop/Pflege ausbildung/`

**Git Repos** :
- Marres-bit/AutoGPT-practice (branch: update-name)
- Fork de Significant-Gravitas/AutoGPT

**Derniers commits critiques** :
- `[PENDING]` : Ajout CONTEXT_MEMO.md (2026-01-12 17:00)
- `123f2687f` : Nettoyage production (2026-01-12 10:15)
- `7b8c75a60` : Fix signature Risk Manager
- `f6adbefee` : Suppression fallback prix fictifs
- `9520c976b` : Fix Kelly + stop-loss adaptatif

---

## 🎓 POUR UN NOUVEAU COPILOT

**1. Lis d'abord** (5 min) :
- [ ] Section "Résumé Exécutif"
- [ ] Section "Bugs Critiques Résolus"
- [ ] Section "État Actuel Systèmes"

**2. Si user demande aide crypto** :
- [ ] Lire "Agent Trading Crypto" architecture
- [ ] Checker log : `Get-Content sp_agent.log -Tail 50`
- [ ] Vérifier dernier rapport Desktop

**3. Si user demande modification** :
- [ ] Lire "Décisions Architecturales" (comprendre POURQUOI)
- [ ] Vérifier Git log pour contexte récent
- [ ] Tester avant commit

**4. Si erreur inconnue** :
- [ ] Checker "Troubleshooting Rapide"
- [ ] Lire backups (*.backup_20260112_*)
- [ ] Vérifier Git commits récents

**Tu devrais être opérationnel en 5-10 minutes !** 🚀

---

**Fin du Context Memo** - Mise à jour régulièrement après changements majeurs
