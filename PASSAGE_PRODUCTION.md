# 🚀 Guide de Passage en Production sur Binance RÉEL

## ⚠️ ATTENTION - ARGENT RÉEL

Ce guide explique comment basculer l'agent du **Testnet** (argent fictif) vers **Binance Production** (argent réel).

---

## 📋 Prérequis

### 1. Compte Binance Vérifié
- ✅ Compte Binance avec KYC complet
- ✅ 2FA activé (Google Authenticator recommandé)
- ✅ Adresse email vérifiée

### 2. Clés API Binance
1. Se connecter sur [binance.com](https://www.binance.com)
2. Aller dans **API Management**
3. Créer une nouvelle API avec restrictions:
   - ✅ **Enable Reading** (lecture des prix)
   - ✅ **Enable Spot & Margin Trading** (trading)
   - ❌ **Enable Withdrawals** (DÉSACTIVER pour sécurité)
   - ✅ **Restrict access to trusted IPs only** (ajouter ton IP)

4. Noter:
   - `API Key`: Clé publique (exemple: `xxxxxxxxxxxxxxxxxxx`)
   - `Secret Key`: Clé secrète (NE JAMAIS PARTAGER)

### 3. Capital de Test
- **Recommandation**: Commencer avec **500-1000 $** maximum
- Ne JAMAIS risquer plus que ce que tu peux perdre
- Le Risk Manager limite à 20% de drawdown max

---

## 🔧 Configuration Production

### Étape 1: Définir les clés API (Windows)

**PowerShell (temporaire - session actuelle):**
```powershell
$env:BINANCE_API_KEY = "ta_cle_api_ici"
$env:BINANCE_API_SECRET = "ton_secret_ici"
```

**PowerShell (permanent - toutes les sessions):**
```powershell
[System.Environment]::SetEnvironmentVariable("BINANCE_API_KEY", "ta_cle_api_ici", "User")
[System.Environment]::SetEnvironmentVariable("BINANCE_API_SECRET", "ton_secret_ici", "User")
```

### Étape 2: Modifier run_autonomous.py

**Ligne à changer:**
```python
# AVANT (Testnet - argent fictif)
exchange = ExchangeConnector(testnet=True)

# APRÈS (Production - ARGENT RÉEL)
exchange = ExchangeConnector(testnet=False)
```

### Étape 3: Vérifier la connexion

```powershell
python -c "from exchange_connector import ExchangeConnector; ex = ExchangeConnector(testnet=False); print(ex.get_connection_status())"
```

**Attendu:**
```
✅ Connecté à Binance PRODUCTION (ARGENT RÉEL)
⚠️⚠️⚠️ MODE RÉEL ACTIVÉ - ARGENT RÉEL EN JEU ⚠️⚠️⚠️
{'connected': True, 'testnet': False, 'exchange': 'binance', 'mode': 'production'}
```

### Étape 4: Lancer l'agent en production

```powershell
cd c:\Users\sanim\git-practice\AutoGPT
python run_autonomous.py --service --interval 2
```

---

## 🛡️ Sécurités Actives

### Risk Manager
- ✅ Max Drawdown: **20%** (stop automatique)
- ✅ Kelly Criterion: Plafonné à **10%**
- ✅ Stop-loss: **2-3%** par trade
- ✅ Position sizing: **Max 30%** du capital

### Validations
- ✅ Prix > 100$ obligatoire (évite erreurs API)
- ✅ Emergency stop si drawdown > 20%
- ✅ Trade annulé si prix réels indisponibles

### Monitoring
- 📊 Logs: `sp_agent.log`
- 📄 Rapports 4h: `Desktop/Suivi crypto de Marres/`
- 📈 Capital tracking: `capital_state.json`

---

## ⚠️ Différences Testnet vs Production

| Aspect | Testnet (fictif) | Production (réel) |
|--------|------------------|-------------------|
| **Prix** | Vrais prix réels Binance | Vrais prix réels Binance |
| **Capital** | Virtuel (illimité) | RÉEL (ton argent) |
| **Trades** | Simulés (aucun ordre réel) | RÉELS (ordres sur Binance) |
| **Frais** | 0% | 0.1% par trade (Binance) |
| **Slippage** | Aucun | Oui (marché réel) |
| **Limites ordre** | Aucune | Minimums Binance (10-20$) |

---

## 🚨 Checklist AVANT le Lancement

- [ ] Clés API définies (`$env:BINANCE_API_KEY`, `$env:BINANCE_API_SECRET`)
- [ ] Restrictions IP configurées sur Binance
- [ ] Withdrawals DÉSACTIVÉS sur l'API
- [ ] Capital de test raisonnable (500-1000$ max)
- [ ] Testnet validé pendant 48h minimum
- [ ] Win rate > 60% sur testnet
- [ ] Risk Manager testé (emergency stop fonctionne)
- [ ] Sauvegarde GitHub à jour (`git push`)
- [ ] Monitoring actif (logs + rapports)

---

## 📊 Monitoring Production

### Commandes utiles

**Vérifier statut agent:**
```powershell
Get-Process python | Where-Object { $_.CommandLine -like '*run_autonomous*' }
```

**Voir logs en temps réel:**
```powershell
Get-Content sp_agent.log -Tail 100 -Wait
```

**Vérifier capital actuel:**
```powershell
Get-Content capital_state.json | ConvertFrom-Json | Format-List
```

**Arrêter l'agent:**
```powershell
Get-Process python | Stop-Process -Force
```

---

## 🆘 En Cas de Problème

### Emergency Stop Manuel
```powershell
# Arrêter l'agent immédiatement
Get-Process python | Stop-Process -Force

# Vérifier capital restant
Get-Content capital_state.json
```

### Rollback vers Testnet
1. Arrêter l'agent
2. Modifier `run_autonomous.py`: `testnet=True`
3. Redémarrer

### Support
- Logs complets: `sp_agent.log`
- État risk: `risk_state.json`
- Historique: `drawdown_history.json`

---

## 💡 Recommandations

1. **Phase de Test (2-4 semaines):**
   - Lancer avec 500$ uniquement
   - Surveiller quotidiennement
   - Ajuster si win rate < 60%

2. **Scaling Progressif:**
   - Semaine 1-2: 500$
   - Semaine 3-4: 1000$ si stable
   - Mois 2+: Augmenter progressivement

3. **Monitoring Quotidien:**
   - Vérifier rapports 4h
   - Consulter drawdown actuel
   - Analyser trades perdants

4. **Règle d'Or:**
   - Si drawdown > 15% → Pause et analyse
   - Si win rate < 55% sur 20 trades → Arrêt
   - JAMAIS investir plus que tu peux perdre

---

## ✅ Agent Prêt pour Production

Après les corrections d'aujourd'hui:
- ✅ Prix réels Binance (BTC=91,828$, ETH=3,156$)
- ✅ Position sizing correct pour vrais prix
- ✅ Risk Manager avec drawdown reset
- ✅ Kelly plafonné à 10%
- ✅ Stop-loss adaptatif (2-3%)
- ✅ Emergency stop testé
- ✅ Logging transparent
- ✅ Connexion production configurée

**L'agent est maintenant prêt pour le trading réel!** 🚀
