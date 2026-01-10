# 🧠 Système d'Apprentissage Permanent

## Vue d'ensemble

Votre agent AI dispose maintenant d'un **moteur d'apprentissage permanent** qui analyse automatiquement ses performances, identifie ses erreurs et ajuste sa stratégie pour éviter de les répéter.

## Fonctionnalités Principales

### 1. 📊 Analyse Continue des Performances
- **Suivi en temps réel** de tous les trades
- **Calcul du Win Rate** (taux de réussite)
- **Identification des patterns** de pertes
- **Mémorisation** des leçons apprises

### 2. 🎯 Ajustements Adaptatifs

Le système ajuste automatiquement :

#### a) **Seuil d'entrée** (`min_gain_to_open`)
- Augmente après 3 pertes consécutives (+0.3%)
- Évite de trader trop tôt en marché incertain
- Maximum: 3% pour rester réactif

#### b) **Niveau de risque** (`risk_level`)
- Réduit si win rate < 40% (après 10 trades)
- Augmente si win rate > 60%
- Plage: 0.2 - 0.8

#### c) **Stop-loss adaptatif** (`max_loss_threshold`)
- Se resserre après une grosse perte
- Protège le capital plus efficacement
- Minimum: -30 (max -$30 par trade)

#### d) **Seuils de profit** (`min_win_threshold`)
- S'ajuste selon les conditions de marché
- Optimise les sorties de position

### 3. 🚫 Patterns à Éviter

Le système détecte et évite automatiquement :

#### Pattern 1: Assets Problématiques
```
Si un asset (BTC, ETH, SOL) perd > 60% du temps (sur 5+ trades)
→ Pattern: AVOID_{ASSET}_HIGH_LOSS_RATE
→ Action: Réduction drastique de l'exposition
```

#### Pattern 2: Marché Négatif Global
```
Si pertes > -$20 quand marché global < 0%
→ Pattern: NEGATIVE_MARKET_LARGE_LOSS
→ Action: Pas de nouveau trade en marché baissier
```

#### Pattern 3: Volatilité Excessive
```
Si écart marché > 5%
→ Augmentation de la prudence
→ Seuils d'entrée relevés
```

### 4. 📝 Génération de Leçons

Chaque trade perdant génère une leçon automatique :

```python
Exemples de leçons:
- "Éviter SOL quand le marché est négatif (-2.1%)"
- "Perte trop importante sur BTC - réduire l'exposition"
- "Stop-loss déclenché sur ETH - revoir le seuil d'entrée"
- "Marché très volatile - augmenter la prudence"
```

### 5. 🎲 Système de Recommandation

Avant chaque trade, le système évalue :

```python
Recommandation = {
    "asset": "BTC",
    "gain": 2.5,
    "should_trade": True,
    "reason": "Conditions favorables selon l'apprentissage",
    "confidence": 0.75  # Score 0-1
}
```

**Facteurs de confiance :**
- Gain actuel de l'asset (+0.1 à +0.2)
- Historique de l'asset (-0.3 si mauvais)
- Win rate global (+0.15 si > 60%)
- Niveau de risque actuel (multiplicateur)

## Fichiers Générés

Le système crée et maintient automatiquement :

### 1. `learning_state.json`
État principal de l'apprentissage
```json
{
  "min_gain_to_open": 0.8,
  "consecutive_losses": 0,
  "total_trades": 47,
  "winning_trades": 29,
  "losing_trades": 18,
  "win_rate": 0.617,
  "risk_level": 0.65,
  "avoid_patterns": [
    "AVOID_SOL_HIGH_LOSS_RATE",
    "NEGATIVE_MARKET_LARGE_LOSS"
  ],
  "lessons_learned": [
    "Asset SOL a un taux de perte élevé - réduire exposition",
    "Ne pas ouvrir de position quand le marché global est négatif"
  ]
}
```

### 2. `mistakes_log.json`
Historique complet des erreurs (1000 dernières)
```json
[
  {
    "timestamp": "2026-01-10T10:53:04.663015Z",
    "asset": "SOL",
    "pnl": -23.5,
    "entry_price": 991.97,
    "exit_price": 968.34,
    "market_conditions": {"BTC": -0.9, "ETH": 2.34, "SOL": 2.44},
    "lesson": "Stop-loss déclenché sur SOL - revoir le seuil d'entrée"
  }
]
```

### 3. `error_patterns.json`
Patterns identifiés et statistiques
```json
{
  "loss_patterns": [
    {
      "type": "NEGATIVE_MARKET_LARGE_LOSS",
      "market_sum": -3.2,
      "loss": -28.5,
      "timestamp": "2026-01-10T08:30:00Z"
    }
  ],
  "asset_specific": {
    "BTC": {"losses": 3, "total": 15},
    "ETH": {"losses": 5, "total": 12},
    "SOL": {"losses": 8, "total": 10}
  }
}
```

## Utilisation

### Activation Automatique
Le système s'active automatiquement au démarrage :
```python
scheduler = AutonomousScheduler(interval_hours=4)
# 🧠 Moteur d'apprentissage permanent activé
```

### Consultation de l'État
Dans les logs et `last_cycle_summary.txt` :
```
📊 Apprentissage:
  - Win Rate: 61.7%
  - Trades totaux: 47
  - Leçons apprises: 12
  - Niveau de risque: 0.65
  - Dernières leçons:
    • Asset SOL a un taux de perte élevé - réduire exposition
    • Ne pas ouvrir de position quand le marché global est négatif
```

### Logs Détaillés
Consultez `sp_agent.log` pour voir l'apprentissage en action :
```
2026-01-10T11:00:00Z LEARNING_RECOMMENDATION: {"asset": "BTC", "confidence": 0.75}
2026-01-10T11:00:05Z TRADE_BLOCKED: Gain BTC (0.3%) < seuil requis (0.8%)
2026-01-10T11:00:10Z LEARNING_ADJUSTMENTS: {"changes": ["Seuil d'entrée augmenté: 0.8% → 1.1%"]}
2026-01-10T11:00:11Z LEARNING: Seuil d'entrée augmenté: 0.8% → 1.1%
```

## Avantages

✅ **Évite les erreurs répétitives** : Ne retombe pas dans les mêmes pièges  
✅ **Adaptatif** : S'ajuste aux conditions changeantes du marché  
✅ **Protecteur** : Réduit automatiquement l'exposition après pertes  
✅ **Transparent** : Toutes les décisions sont loggées et expliquées  
✅ **Autonome** : Pas d'intervention manuelle nécessaire  
✅ **Cumulatif** : L'apprentissage persiste entre les redémarrages  

## Exemple de Cycle d'Apprentissage

### Cycle 1-5 : Exploration
```
Trades: BTC ✓, ETH ✗, SOL ✗, BTC ✓, ETH ✗
Win Rate: 40%
Action: Réduction du niveau de risque 0.5 → 0.4
```

### Cycle 6-10 : Ajustement
```
Seuil d'entrée: 0.5% → 0.8%
Pattern détecté: ETH perd 66% du temps
Action: Éviter ETH temporairement
```

### Cycle 11-20 : Optimisation
```
Win Rate amélioré: 55%
Niveau de risque: 0.4 → 0.5
ETH réadmis avec surveillance
```

### Cycle 21+ : Performance Stable
```
Win Rate stabilisé: 60-65%
Niveau de risque optimal: 0.6-0.7
Stratégie affinée et performante
```

## Configuration Avancée

Pour ajuster le comportement d'apprentissage, modifiez `learning_engine.py` :

```python
# learning_rate: Vitesse d'ajustement (0-1)
self.state["learning_rate"] = 0.1  # Default

# max_loss_threshold: Perte max par trade
self.state["max_loss_threshold"] = -50.0  # Default: -$50

# min_win_threshold: Gain min recherché
self.state["min_win_threshold"] = 10.0  # Default: $10
```

## Monitoring

Surveillez l'apprentissage via :

1. **Interface GUI** : Affichage du win rate et leçons
2. **Fichier summary** : `last_cycle_summary.txt`
3. **Logs détaillés** : `sp_agent.log`
4. **État JSON** : `learning_state.json`

## Réinitialisation

Pour recommencer l'apprentissage :
```bash
# Supprimer les fichiers d'apprentissage
rm learning_state.json mistakes_log.json error_patterns.json
```

L'agent repartira avec les paramètres par défaut et réapprendra progressivement.

---

**🎯 Objectif** : Transformer chaque échec en leçon pour améliorer continuellement la performance de l'agent.
