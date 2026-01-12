"""
Script de test du module GEIS
"""
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

from insanity_scanner import InsanityScanner, GEISConfig


def main():
    """Test du scanner"""
    print("🔥 TEST MODULE GEIS - Global Extreme Insanity Scanner")
    print("=" * 60)
    
    # Configuration
    config = GEISConfig()
    print(f"\n📁 Dossier de sortie: {config.output_dir}")
    print(f"🎯 Score minimal: {config.min_insanity_score}/10")
    print(f"📊 Max résultats par scan: {config.max_results_per_scan}")
    print(f"⏰ Intervalle: {config.scan_interval_hours}h")
    
    # Créer scanner
    scanner = InsanityScanner(config)
    
    # Lancer scan
    print("\n🚀 Lancement du scan...\n")
    stats = scanner.scan()
    
    # Afficher résultats
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DU SCAN")
    print("=" * 60)
    print(f"Sources scannées: {stats['sources_scanned']}")
    print(f"Items bruts trouvés: {stats['raw_items_found']}")
    print(f"Items filtrés (score >= {config.min_insanity_score}): {stats['filtered_items']}")
    print(f"Rapports générés: {stats['reports_generated']}")
    print(f"Durée: {stats['duration_seconds']:.1f}s")
    
    if stats['errors']:
        print(f"\n⚠️ Erreurs ({len(stats['errors'])}):")
        for error in stats['errors']:
            print(f"  - {error}")
    
    print(f"\n✅ Dossiers créés dans: {config.output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
