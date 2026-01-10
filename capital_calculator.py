"""
Calculateur de Capital pour Objectif de Profit
Aide à déterminer le capital nécessaire selon vos objectifs
"""

def calculate_required_capital():
    """Calcule le capital nécessaire selon différents scénarios"""
    
    print("=" * 80)
    print(" 💰 CALCULATEUR DE CAPITAL TRADING BOT")
    print("=" * 80)
    print()
    
    # Demander l'objectif
    print("🎯 Quel est votre objectif de profit hebdomadaire ?")
    target_weekly = float(input("   Montant en € : "))
    print()
    
    # Scénarios de rendement
    scenarios = {
        "Très Optimiste": {
            "weekly_return": 0.10,  # 10%/semaine
            "description": "Excellent marché + robot performant (rare)",
            "risk": "ÉLEVÉ"
        },
        "Optimiste": {
            "weekly_return": 0.07,  # 7%/semaine
            "description": "Bon marché + robot bien calibré",
            "risk": "MOYEN-ÉLEVÉ"
        },
        "Réaliste": {
            "weekly_return": 0.05,  # 5%/semaine
            "description": "Conditions normales + performance stable",
            "risk": "MOYEN"
        },
        "Conservateur": {
            "weekly_return": 0.03,  # 3%/semaine
            "description": "Approche prudente + marché variable",
            "risk": "FAIBLE-MOYEN"
        },
        "Prudent": {
            "weekly_return": 0.02,  # 2%/semaine
            "description": "Très sécurisé + objectif atteignable",
            "risk": "FAIBLE"
        }
    }
    
    print("📊 CAPITAL REQUIS SELON LES SCÉNARIOS :")
    print()
    print("-" * 80)
    
    recommendations = []
    
    for scenario_name, scenario in scenarios.items():
        required = target_weekly / scenario["weekly_return"]
        weekly_trades = 42  # 6 trades/jour × 7 jours
        avg_position = required * 0.05  # 5% du capital
        
        print(f"\n🔹 Scénario {scenario_name}")
        print(f"   Rendement/semaine : {scenario['weekly_return']*100:.1f}%")
        print(f"   Description : {scenario['description']}")
        print(f"   Niveau de risque : {scenario['risk']}")
        print(f"   ")
        print(f"   💰 CAPITAL NÉCESSAIRE : {required:,.0f}€".replace(',', ' '))
        print(f"   📊 Position moyenne : {avg_position:.0f}€")
        print(f"   🎯 Objectif atteint si {scenario['weekly_return']*100:.1f}% par semaine")
        
        recommendations.append({
            "scenario": scenario_name,
            "capital": required,
            "return": scenario["weekly_return"],
            "risk": scenario["risk"]
        })
    
    print()
    print("-" * 80)
    print()
    
    # Recommandation personnalisée
    print("💡 RECOMMANDATION PERSONNALISÉE :")
    print()
    
    realistic_capital = target_weekly / 0.05  # 5% rendement
    conservative_capital = target_weekly / 0.03  # 3% rendement
    
    print(f"   Pour un objectif de {target_weekly:.0f}€/semaine :")
    print()
    print(f"   ✅ MINIMUM RECOMMANDÉ : {realistic_capital:,.0f}€".replace(',', ' '))
    print(f"      → Rendement requis : 5%/semaine (réaliste)")
    print(f"      → Position max : {realistic_capital * 0.05:.0f}€ par trade")
    print()
    print(f"   🏆 CAPITAL IDÉAL : {conservative_capital:,.0f}€".replace(',', ' '))
    print(f"      → Rendement requis : 3%/semaine (conservateur)")
    print(f"      → Confort + marge de sécurité")
    print()
    
    # Approche progressive
    print()
    print("🎯 APPROCHE PROGRESSIVE RECOMMANDÉE :")
    print()
    
    phase1_capital = min(5000, realistic_capital * 0.5)
    phase1_target = phase1_capital * 0.05
    
    phase2_capital = min(realistic_capital * 0.75, phase1_capital * 1.5)
    phase2_target = phase2_capital * 0.05
    
    phase3_capital = realistic_capital
    phase3_target = target_weekly
    
    print(f"   📅 PHASE 1 (Mois 1) - Validation")
    print(f"      Capital : {phase1_capital:,.0f}€".replace(',', ' '))
    print(f"      Objectif : {phase1_target:.0f}€/semaine")
    print(f"      But : Valider le robot en conditions réelles")
    print()
    print(f"   📅 PHASE 2 (Mois 2-3) - Croissance")
    print(f"      Capital : {phase2_capital:,.0f}€".replace(',', ' '))
    print(f"      Objectif : {phase2_target:.0f}€/semaine")
    print(f"      But : Optimiser et réinvestir progressivement")
    print()
    print(f"   📅 PHASE 3 (Mois 4+) - Production")
    print(f"      Capital : {phase3_capital:,.0f}€".replace(',', ' '))
    print(f"      Objectif : {phase3_target:.0f}€/semaine")
    print(f"      But : Atteindre objectif avec stabilité")
    print()
    
    # Calcul des risques
    print()
    print("⚠️  ANALYSE DES RISQUES :")
    print()
    
    # Scénarios négatifs
    bad_week_loss = realistic_capital * -0.05  # Mauvaise semaine
    very_bad_week_loss = realistic_capital * -0.10  # Très mauvaise semaine
    
    print(f"   📉 Mauvaise semaine (Win Rate 45%) : {bad_week_loss:.0f}€")
    print(f"   📉 Très mauvaise semaine (Win Rate 35%) : {very_bad_week_loss:.0f}€")
    print()
    print(f"   💡 Réserve de sécurité recommandée : {realistic_capital * 0.2:,.0f}€".replace(',', ' '))
    print(f"      (20% du capital pour absorber les pertes)")
    print()
    
    # Temps pour atteindre objectif
    print()
    print("⏱️  TEMPS ESTIMÉ POUR ATTEINDRE L'OBJECTIF :")
    print()
    
    if phase1_capital < realistic_capital:
        weeks_to_target = (realistic_capital - phase1_capital) / target_weekly
        print(f"   En partant de {phase1_capital:,.0f}€ :".replace(',', ' '))
        print(f"   → {weeks_to_target:.0f} semaines (~{weeks_to_target/4:.1f} mois)")
        print(f"   → En réinvestissant 100% des bénéfices")
        print()
        print(f"   ⚡ Démarrage immédiat avec {realistic_capital:,.0f}€ :".replace(',', ' '))
        print(f"   → Objectif atteignable dès la 1ère semaine")
        print(f"   → Risque et capital plus élevés")
    print()
    
    # Frais à considérer
    print()
    print("💸 COÛTS À CONSIDÉRER :")
    print()
    
    weekly_trades_count = 42
    avg_trade_size = realistic_capital * 0.05
    binance_fee = 0.001  # 0.1%
    weekly_fees = weekly_trades_count * avg_trade_size * binance_fee * 2  # Aller-retour
    monthly_fees = weekly_fees * 4
    
    print(f"   Frais Binance (0.1% par trade) :")
    print(f"   → Par semaine : ~{weekly_fees:.2f}€")
    print(f"   → Par mois : ~{monthly_fees:.2f}€")
    print(f"   ")
    print(f"   💡 Astuce : Utiliser BNB pour réduire les frais à 0.075%")
    print()
    
    # Résumé final
    print()
    print("=" * 80)
    print(" 📋 RÉSUMÉ DE LA RECOMMANDATION")
    print("=" * 80)
    print()
    print(f"   🎯 Objectif : {target_weekly:.0f}€/semaine")
    print()
    print(f"   💰 Capital minimum : {realistic_capital:,.0f}€".replace(',', ' '))
    print(f"   💰 Capital recommandé : {conservative_capital:,.0f}€".replace(',', ' '))
    print(f"   💰 Démarrage progressif : {phase1_capital:,.0f}€".replace(',', ' '))
    print()
    print(f"   📊 Rendement requis : 3-5% par semaine")
    print(f"   🛡️  Protection recommandée : {realistic_capital * 0.2:,.0f}€ de réserve".replace(',', ' '))
    print(f"   💸 Frais mensuels estimés : {monthly_fees:.2f}€")
    print()
    
    # Avertissement final
    print()
    print("⚠️  " + "=" * 76)
    print("   AVERTISSEMENT IMPORTANT")
    print("=" * 80)
    print()
    print("   Ces calculs sont basés sur des hypothèses optimistes.")
    print("   Le trading comporte des risques importants de perte en capital.")
    print()
    print("   ✅ Ne tradez QUE l'argent que vous pouvez vous permettre de perdre")
    print("   ✅ Commencez TOUJOURS par un petit capital pour valider")
    print("   ✅ Surveillez activement les performances")
    print("   ✅ Définissez des limites de perte strictes")
    print()
    print("=" * 80)
    print()
    
    # Sauvegarder le résultat
    save = input("💾 Sauvegarder ce calcul dans un fichier ? (o/n) : ").lower()
    if save == 'o':
        filename = f"capital_calculation_{target_weekly:.0f}eur_week.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"CALCUL DE CAPITAL - Objectif {target_weekly:.0f}€/semaine\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Capital minimum : {realistic_capital:,.0f}€\n".replace(',', ' '))
            f.write(f"Capital recommandé : {conservative_capital:,.0f}€\n".replace(',', ' '))
            f.write(f"Démarrage progressif : {phase1_capital:,.0f}€\n\n".replace(',', ' '))
            f.write("Détails complets disponibles dans les scénarios ci-dessus.\n")
        print(f"\n✅ Calcul sauvegardé dans : {filename}")


if __name__ == "__main__":
    try:
        calculate_required_capital()
    except KeyboardInterrupt:
        print("\n\n❌ Calcul annulé.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
