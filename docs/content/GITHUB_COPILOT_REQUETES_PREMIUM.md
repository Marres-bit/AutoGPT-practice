# Synthèse : Système de Requêtes Premium GitHub Copilot

## Résumé

Ce document explique le système de requêtes premium de GitHub Copilot, introduit le 18 juin 2025. Les requêtes premium correspondent aux interactions avancées avec Copilot (chat, révision de code, agent de codage) et consomment un crédit mensuel variable selon le modèle d'IA utilisé (multiplicateurs de 0x à 10x). Les plans gratuits offrent 50 requêtes premium par mois, tandis que les plans payants incluent des modèles de base illimités (GPT-5 mini, GPT-4.1, GPT-4o) et une allocation mensuelle pour les modèles premium. Les crédits non utilisés ne se reportent pas au mois suivant, et des budgets supplémentaires peuvent être configurés pour dépasser l'allocation de base.

## À propos de ce document

### Contexte général

Ce texte présente le système de facturation des **requêtes premium** de GitHub Copilot, une fonctionnalité de tarification différenciée mise en place pour mieux contrôler les coûts liés à l'utilisation des modèles d'IA avancés. 

### Qu'est-ce qu'une requête ?

Une **requête** représente toute interaction avec GitHub Copilot : générer du code, poser une question, ou utiliser une extension. Chaque invite envoyée dans une fenêtre de chat ou déclenchée par Copilot constitue une requête.

### Qu'est-ce qu'une requête premium ?

Certaines fonctionnalités de Copilot nécessitent une puissance de traitement plus importante et comptent comme **requêtes premium**. Le nombre de requêtes premium consommées varie selon :
- La fonctionnalité utilisée
- Le modèle d'IA sélectionné

### Fonctionnalités premium principales

1. **Copilot Chat** - Chat dans l'IDE avec multiplicateur selon le modèle
2. **Copilot CLI** - Interface en ligne de commande
3. **Copilot Code Review** - Révision automatique de code
4. **Copilot Coding Agent** - Agent de codage autonome (SKU dédié depuis nov. 2025)
5. **Copilot Spaces** - Espaces de travail collaboratifs
6. **Spark** - Génération rapide (4 requêtes par invite, SKU dédié depuis nov. 2025)

### Systèmes de facturation

#### Plans gratuits (Copilot Free)
- 2 000 suggestions inline par mois
- 50 requêtes premium par mois
- Accès limité aux modèles (toutes les interactions de chat comptent comme premium)

#### Plans payants
- Suggestions inline illimitées
- Chat illimité avec les modèles inclus (GPT-5 mini, GPT-4.1, GPT-4o)
- Allocation mensuelle de requêtes premium pour les modèles avancés
- Limitations de débit pour gérer la forte demande

### Multiplicateurs de modèles

Chaque modèle possède un **multiplicateur de requêtes premium** basé sur sa complexité :

| Modèle | Multiplicateur (plans payants) | Multiplicateur (Copilot Free) |
|--------|-------------------------------|-------------------------------|
| GPT-5 mini, GPT-4.1, GPT-4o | 0x (gratuit) | 1x |
| Claude Haiku 4.5, Gemini 3 Flash | 0.33x | 1x ou N/A |
| Claude Sonnet 4/4.5, GPT-5, Gemini 3 Pro | 1x | N/A |
| Claude Opus 4.5 | 3x | N/A |
| Claude Opus 4.1 | 10x | N/A |

**Note** : Les plans payants bénéficient d'une réduction de 10% sur les multiplicateurs lors de l'utilisation de la sélection automatique de modèle.

### Gestion des allocations

- **Réinitialisation mensuelle** : Les compteurs de requêtes premium se réinitialisent le 1er de chaque mois à 00:00:00 UTC
- **Pas de report** : Les requêtes non utilisées ne se reportent pas au mois suivant
- **Dépassement de quota** : Pour les plans payants qui épuisent leur allocation :
  - Accès maintenu aux modèles inclus pour le reste du mois
  - Possibilité de configurer un budget pour les requêtes supplémentaires
  - Pour les organisations/entreprises : s'assurer que la politique "Premium request paid usage" est activée

### Points importants

1. **Dates clés** :
   - 18 juin 2025 : Début de la facturation pour GitHub.com
   - 1er août 2025 : Début de la facturation pour GHE.com
   - 1er novembre 2025 : SKU dédiés pour Spark et l'agent de codage

2. **Budgets par défaut** : Les comptes créés avant le 22 août 2025 ont un budget par défaut de 0$ pour les requêtes premium dépassant l'allocation

3. **Surveillance** : Les utilisateurs peuvent surveiller leur utilisation via le tableau de bord dédié

### Exemples d'utilisation

- **Claude Opus 4.1 dans Copilot Chat** (plan payant) : 1 interaction = 10 requêtes premium
- **GPT-5 mini sur Copilot Free** : 1 interaction = 1 requête premium
- **GPT-5 mini sur plan payant** : 0 requête premium consommée

## Conclusion

Le système de requêtes premium GitHub Copilot offre une facturation différenciée permettant un meilleur contrôle des coûts tout en maintenant un accès illimité aux modèles de base pour les utilisateurs payants. La transparence sur les multiplicateurs et les SKU dédiés facilite la gestion budgétaire et l'optimisation de l'utilisation des ressources d'IA.
