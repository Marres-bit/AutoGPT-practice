"""
Script de test de l'intégration complète
"""
from autonomous_scheduler import AutonomousScheduler
from pathlib import Path

print('🚀 Test du système complet de trading...\n')

scheduler = AutonomousScheduler(interval_hours=4, project_root=Path.cwd())
print('\n▶️ Exécution d\'un cycle de test...\n')

try:
    result = scheduler.run_one_shot(simulate=True)
    print('\n' + '='*70)
    print('✅ CYCLE TERMINÉ AVEC SUCCÈS!')
    print('='*70)
    
    summary = result["summary"]
    print(f'\n📊 Résultats:')
    print(f'  Cycle: #{summary.get("cycle", 1)}')
    print(f'  Condition marché: {summary.get("market_condition")}')
    print(f'  Stratégie: {summary.get("strategy_used")}')
    print(f'  Décision: {summary.get("decision")}')
    
    capital = summary.get("capital", {})
    print(f'\n💰 Capital:')
    print(f'  Principal: ${capital.get("principal", 0):,.2f}')
    print(f'  Investment: ${capital.get("investment", 0):,.2f}')
    print(f'  Total: ${capital.get("principal", 0) + capital.get("investment", 0):,.2f}')
    
    if summary.get('trade'):
        trade = summary['trade']
        print(f'\n📈 Trade:')
        print(f'  Asset: {trade.get("asset")}')
        print(f'  P&L: ${trade.get("pnl", 0):.2f}')
        print(f'  Stratégie: {trade.get("strategy_used")}')
        print(f'  Confiance: {trade.get("fusion_confidence", 0):.1%}')
    
    print('\n✅ Test réussi! Le système fonctionne correctement.')
    
except Exception as e:
    print(f'\n❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
