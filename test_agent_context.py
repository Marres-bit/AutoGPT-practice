"""
Test de l'agent avec contexte de trading
Vérifie que l'agent peut discuter de ses performances
"""
from agent import AIAgent
from trading_context import TradingContextProvider

def test_agent_trading_context():
    """Teste si l'agent comprend son contexte de trading"""
    
    print("=" * 80)
    print("🧪 TEST DE L'AGENT AVEC CONTEXTE DE TRADING")
    print("=" * 80)
    print()
    
    # Créer l'agent
    print("1️⃣ Création de l'agent...")
    try:
        agent = AIAgent(enable_trading_context=True)
        print("✅ Agent créé avec contexte de trading")
    except Exception as e:
        print(f"❌ Erreur création agent: {e}")
        return
    
    print()
    
    # Vérifier que le contexte est chargé
    print("2️⃣ Vérification du contexte...")
    if agent.trading_context_enabled:
        print("✅ Contexte de trading activé")
        
        # Afficher un aperçu du contexte
        try:
            context_provider = TradingContextProvider()
            stats = context_provider.get_statistics_summary()
            
            if stats["available"]:
                print(f"\n📊 Données disponibles:")
                print(f"   - Trades: {stats['total_trades']}")
                print(f"   - Win Rate: {stats['win_rate']:.1%}")
                print(f"   - Capital: {stats['current_capital']:,.2f}€".replace(',', ' '))
                print(f"   - P&L: {stats['total_pnl']:+,.2f}€".replace(',', ' '))
                print(f"   - Leçons: {stats['lessons_learned']}")
                print(f"   - Patterns: {stats['patterns_detected']}")
            else:
                print("⚠️ Pas encore de données de trading disponibles")
        except Exception as e:
            print(f"⚠️ Erreur lecture stats: {e}")
    else:
        print("❌ Contexte de trading non disponible")
        print("   Assurez-vous que les fichiers de trading existent")
        return
    
    print()
    print("=" * 80)
    print("3️⃣ TEST DE CONVERSATION")
    print("=" * 80)
    print()
    
    # Questions de test
    test_questions = [
        "Comment se passent tes trades ?",
        "Quel est ton win rate ?",
        "Quelles erreurs as-tu faites récemment ?",
        "Qu'as-tu appris ?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 80)
        
        try:
            response = agent.send_message(question)
            print(f"🤖 Réponse: {response}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print()
    
    print("=" * 80)
    print("✅ TEST TERMINÉ")
    print("=" * 80)
    print()
    print("💡 L'agent devrait maintenant pouvoir discuter de ses trades")
    print("   en utilisant ses vraies données de performance.")
    print()


if __name__ == "__main__":
    test_agent_trading_context()
