# Configuration de l'Agent AI Crypto

## Rapport Quotidien

**Heure de génération :** 23h00 (heure locale, fin de journée)
- Configure dans `advanced_reporting.py` avec `timezone_offset=1` (Europe)
- Généré après le dernier cycle de la journée
- Contient le récapitulatif complet de tous les trades du jour

## Sauvegardes Git Automatiques

**Fréquence :** Toutes les 4 cycles (environ 8 heures)

**Fichiers sauvegardés automatiquement :**
- États d'apprentissage (learning_state.json)
- États de risque (risk_state.json, drawdown_history.json)
- Logs de trading (logs/*.log)
- Rapports générés (reports/*.docx)

**Commandes Git automatiques :**
1. `git add -A` - Ajoute tous les fichiers modifiés
2. `git commit -m "Auto-save: Cycle #X - Capital Y$"` - Commit avec info cycle
3. `git push origin update-name` - Push vers GitHub (si connexion disponible)

**Message de commit :** Inclut le numéro de cycle et le capital actuel pour traçabilité

## Fuseau Horaire

**Par défaut :** UTC+1 (Europe Centrale)
- Modifiable dans `AdvancedReportingSystem(timezone_offset=1)`
- Ajuster selon votre localisation :
  - Paris/Berlin : +1
  - Londres : +0
  - New York : -5
  - Tokyo : +9

## Intervalle de Trading

**Actuel :** 2 heures entre chaque cycle
- Modifiable avec `--interval X` (en heures)
- Exemple : `python run_autonomous.py --service --interval 4` pour 4h

## Sécurité

- Testnet Binance activé (capital virtuel)
- Risk Manager : Max drawdown 20%
- Stop-loss dynamique : 3-5% selon volatilité
- Kelly Criterion pour position sizing optimal

## Lancement Automatique

L'agent démarre automatiquement au démarrage de Windows via le Planificateur de tâches.

**Pour vérifier :** Gestionnaire des tâches → Onglet "Démarrage" → "CryptoAgentAutoGPT"
