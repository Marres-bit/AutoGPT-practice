"""
Script de test et démonstration du système d'apprentissage permanent
"""
from pathlib import Path
from learning_engine import LearningEngine
import json

def test_learning_system():
    """Teste le moteur d'apprentissage avec des scénarios"""
    
    print("=" * 70)
    print("🧠 TEST DU SYSTÈME D'APPRENTISSAGE PERMANENT")
    print("=" * 70)
    
    # Initialiser le moteur
    project_root = Path(__file__).parent
    engine = LearningEngine(project_root)
    
    print("\n📊 État initial:")
    summary = engine.get_summary()
    print(f"  - Trades totaux: {summary['total_trades']}")
    print(f"  - Win rate: {summary['win_rate']:.1%}")
    print(f"  - Niveau de risque: {summary['risk_level']:.2f}")
    print(f"  - Seuil d'entrée: {summary['min_gain_threshold']}%")
    
    # Scénario 1: Trade gagnant sur BTC
    print("\n" + "=" * 70)
    print("📈 SCÉNARIO 1: Trade gagnant sur BTC (+2.5%)")
    print("=" * 70)
    
    summary1 = {
        "timestamp": "2026-01-10T12:00:00Z",
        "market": {"BTC": 2.5, "ETH": 1.2, "SOL": 0.8},
        "trade": {
            "asset": "BTC",
            "entry_price": 1000,
            "exit_price": 1045,
            "amount": 3500,
            "pnl": 157.5
        }
    }
    
    result1 = engine.analyze_trade(summary1)
    print(f"\n✅ Résultat:")
    print(f"  - Ajusté: {result1['adjusted']}")
    if result1.get('changes'):
        print(f"  - Changements:")
        for change in result1['changes']:
            print(f"    • {change}")
    
    # Scénario 2: Trade perdant sur SOL
    print("\n" + "=" * 70)
    print("📉 SCÉNARIO 2: Trade perdant sur SOL (-1.5%)")
    print("=" * 70)
    
    summary2 = {
        "timestamp": "2026-01-10T13:00:00Z",
        "market": {"BTC": -0.5, "ETH": 0.2, "SOL": -1.5},
        "trade": {
            "asset": "SOL",
            "entry_price": 1000,
            "exit_price": 965,
            "amount": 3500,
            "pnl": -122.5
        }
    }
    
    result2 = engine.analyze_trade(summary2)
    print(f"\n❌ Résultat:")
    print(f"  - Ajusté: {result2['adjusted']}")
    if result2.get('changes'):
        print(f"  - Changements:")
        for change in result2['changes']:
            print(f"    • {change}")
    
    # Scénario 3: Plusieurs pertes consécutives sur SOL
    print("\n" + "=" * 70)
    print("📉 SCÉNARIO 3: Pertes consécutives sur SOL (simulation)")
    print("=" * 70)
    
    for i in range(3):
        summary_loss = {
            "timestamp": f"2026-01-10T{14+i}:00:00Z",
            "market": {"BTC": 0.3, "ETH": 0.5, "SOL": 1.8},
            "trade": {
                "asset": "SOL",
                "entry_price": 1000,
                "exit_price": 975 - (i * 5),
                "amount": 3500,
                "pnl": -(87.5 + i * 17.5)
            }
        }
        result = engine.analyze_trade(summary_loss)
        print(f"\n  Trade {i+1}: PNL = {summary_loss['trade']['pnl']:.2f}")
        if result.get('changes'):
            for change in result['changes']:
                print(f"    • {change}")
    
    # Test de recommandation
    print("\n" + "=" * 70)
    print("🎯 TEST DE RECOMMANDATION")
    print("=" * 70)
    
    test_market = {"BTC": 2.1, "ETH": 1.5, "SOL": 0.8}
    recommendation = engine.get_trading_recommendation(test_market)
    
    print(f"\n📊 Marché actuel: {test_market}")
    print(f"\n🏆 Meilleur choix:")
    if recommendation['best_choice']:
        best = recommendation['best_choice']
        print(f"  - Asset: {best['asset']}")
        print(f"  - Gain: {best['gain']}%")
        print(f"  - Devrait trader: {best['should_trade']}")
        print(f"  - Raison: {best['reason']}")
        print(f"  - Confiance: {best['confidence']:.1%}")
    
    print(f"\n📋 Toutes les recommandations:")
    for rec in recommendation['recommendations']:
        icon = "✅" if rec['should_trade'] else "⛔"
        print(f"  {icon} {rec['asset']}: {rec['gain']:+.1f}% | Confiance: {rec['confidence']:.1%}")
        print(f"     → {rec['reason']}")
    
    # Test de vérification should_trade
    print("\n" + "=" * 70)
    print("🔍 TEST DE FILTRAGE DES TRADES")
    print("=" * 70)
    
    test_assets = ["BTC", "ETH", "SOL"]
    for asset in test_assets:
        should_trade, reason = engine.should_trade(asset, test_market)
        icon = "✅" if should_trade else "⛔"
        print(f"\n{icon} {asset}:")
        print(f"  - Décision: {'AUTORISER' if should_trade else 'BLOQUER'}")
        print(f"  - Raison: {reason}")
    
    # État final
    print("\n" + "=" * 70)
    print("📊 ÉTAT FINAL DE L'APPRENTISSAGE")
    print("=" * 70)
    
    final_summary = engine.get_summary()
    print(f"\n📈 Statistiques:")
    print(f"  - Trades totaux: {final_summary['total_trades']}")
    print(f"  - Win rate: {final_summary['win_rate']:.1%}")
    print(f"  - Pertes consécutives: {final_summary['consecutive_losses']}")
    print(f"  - Niveau de risque: {final_summary['risk_level']:.2f}")
    print(f"  - Seuil d'entrée: {final_summary['min_gain_threshold']}%")
    
    print(f"\n🎓 Apprentissage:")
    print(f"  - Patterns identifiés: {final_summary['patterns_identified']}")
    print(f"  - Leçons apprises: {final_summary['lessons_learned']}")
    
    if final_summary.get('recent_lessons'):
        print(f"\n📚 Dernières leçons:")
        for lesson in final_summary['recent_lessons']:
            print(f"  • {lesson}")
    
    # Afficher les patterns à éviter
    if engine.state.get('avoid_patterns'):
        print(f"\n⚠️ Patterns à éviter:")
        for pattern in engine.state['avoid_patterns']:
            print(f"  • {pattern}")
    
    # Afficher les statistiques par asset
    if engine.patterns.get('asset_specific'):
        print(f"\n📊 Performance par Asset:")
        for asset, stats in engine.patterns['asset_specific'].items():
            if stats['total'] > 0:
                loss_rate = stats['losses'] / stats['total']
                print(f"  - {asset}: {stats['losses']}/{stats['total']} pertes ({loss_rate:.1%})")
    
    print("\n" + "=" * 70)
    print("✅ TEST TERMINÉ")
    print("=" * 70)
    
    print(f"\n💾 Fichiers générés:")
    print(f"  - {engine.learning_file}")
    print(f"  - {engine.mistakes_log}")
    print(f"  - {engine.patterns_file}")


if __name__ == "__main__":
    test_learning_system()
