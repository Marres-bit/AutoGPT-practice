# Configuration des Seuils de Trading

Ce document explique les différents seuils qui contrôlent l'agressivité de l'agent de trading.

## ⚙️ Seuils Actuels (CONFIGURATION AGRESSIVE)

### 1. Learning Engine (`learning_engine.py`)

**Seuil minimal absolu** (ligne 51 + ligne 408):
- `min_gain_to_open`: **0.4%** (défaut initial)
- Blocage absolu si gain < **0.2%** (protection micro-gains)
- Seuil opportuniste: **0.3%** (avec conditions favorables)

**Logique:**
- ✅ Gain >= 0.4% → Trade autorisé
- ⚠️ Gain 0.3-0.4% → Trade si win_rate > 80% OU meilleur asset
- ❌ Gain < 0.2% → Blocage absolu

### 2. Strategy Fusion (`strategy_fusion.py`)

**Seuil de gain stratégie** (ligne 563):
- `min_gain_threshold`: **0.5%** (défaut)

**Seuil de confiance fusion** (ligne 57):
- `confidence_threshold`: **0.45** (45%)

### 3. Autonomous Scheduler (`autonomous_scheduler.py`)

**Seuil de confiance pour exécution** (ligne 336):
- Confiance minimale: **0.4** (40%)

**Conditions de trading:**
1. `trading_signals.action == "OPEN_LONG"` ✅
2. `best_choice.should_trade == True` ✅
3. `capital.investment > 0` ✅
4. `trading_signals.confidence > 0.4` ✅ (réduit de 0.5)

## 📊 Exemples de Comportement

### Scénario 1: SOL +0.8%
- ✅ **TRADE** - Au-dessus de tous les seuils
- Confiance: ~70%
- Décision: OPEN_LONG

### Scénario 2: BTC +0.45%
- ✅ **TRADE** - Si confiance stratégie > 40%
- Entre seuil learning (0.4%) et stratégie (0.5%)
- Décision: OPEN_LONG (avec prudence)

### Scénario 3: ETH +0.35%
- ⚠️ **MAYBE** - Seulement si:
  - Win rate > 80% ET aucune perte récente
  - OU ETH est le meilleur asset disponible
- Sinon: HOLD

### Scénario 4: DOGE +0.15%
- ❌ **HOLD** - Sous seuil absolu (0.2%)
- Gain trop faible

## 🎚️ Comment Ajuster l'Agressivité

### Pour un agent PLUS AGRESSIF:
```python
# learning_engine.py ligne 51
"min_gain_to_open": 0.3,  # Réduire à 0.3%

# learning_engine.py ligne 408
if asset_gain < 0.1:  # Réduire à 0.1%

# strategy_fusion.py ligne 563
min_gain_threshold: 0.4  # Réduire à 0.4%

# autonomous_scheduler.py ligne 336
> 0.3  # Réduire à 30%
```

### Pour un agent PLUS PRUDENT:
```python
# learning_engine.py ligne 51
"min_gain_to_open": 0.8,  # Augmenter à 0.8%

# learning_engine.py ligne 408
if asset_gain < 0.5:  # Augmenter à 0.5%

# strategy_fusion.py ligne 563
min_gain_threshold: 1.0  # Augmenter à 1.0%

# autonomous_scheduler.py ligne 336
> 0.6  # Augmenter à 60%
```

## 🔒 Protections Toujours Actives

Même avec configuration agressive, l'agent respecte:
1. **Risk Manager**: Max drawdown 20%, Kelly Criterion
2. **Stop Loss dynamique**: 3-5% selon volatilité
3. **Patterns à éviter**: Assets avec historique négatif
4. **Marché négatif global**: Blocage si somme < -2%

## 📝 Modifications Récentes

**17 janvier 2026 - Configuration agressive:**
- ✅ min_gain_to_open: 0.5 → 0.4
- ✅ Blocage absolu: 0.3 → 0.2
- ✅ Opportuniste: 0.4 → 0.3
- ✅ min_gain_threshold: 0.8 → 0.5
- ✅ confidence_threshold: 0.6 → 0.45
- ✅ Confiance exec: 0.5 → 0.4

**Résultat attendu:** ~3x plus de trades exécutés
