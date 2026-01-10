"""
Module d'Analyse des Crypto-monnaies Ultra Autonome
Récupère les données depuis CoinGecko et analyse les variations 24h
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import time
from pathlib import Path


class CryptoAnalyzer:
    """Analyse les crypto-monnaies avec variations significatives"""
    
    def __init__(self, min_variation=5.0, max_results=50):
        """
        Initialise l'analyseur
        
        Args:
            min_variation: Variation min à considérer comme significative (%)
            max_results: Nombre max de cryptos à analyser
        """
        self.min_variation = min_variation
        self.max_results = max_results
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CryptoAnalyzer/1.0"})
        
    def get_top_cryptocurrencies(self, limit=250) -> List[Dict]:
        """
        Récupère les top cryptos avec variations 24h
        
        Returns:
            Liste des cryptos avec variations
        """
        try:
            print(f"📡 Récupération des données CoinGecko ({limit} cryptos)...")
            
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": min(limit, 250),
                "page": 1,
                "sparkline": False,
                "price_change_percentage": "24h"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ {len(data)} cryptos récupérées")
            return data
            
        except requests.RequestException as e:
            print(f"❌ Erreur API CoinGecko: {e}")
            return []
    
    def filter_significant_changes(self, cryptos: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Filtre les cryptos avec variations significatives
        
        Returns:
            Tuple (gainers, losers) avec variations > min_variation
        """
        gainers = []
        losers = []
        
        for crypto in cryptos:
            if not crypto.get("price_change_percentage_24h"):
                continue
            
            change = crypto["price_change_percentage_24h"]
            
            if abs(change) >= self.min_variation:
                crypto_info = {
                    "name": crypto.get("name", "Unknown"),
                    "symbol": crypto.get("symbol", "???").upper(),
                    "price": crypto.get("current_price", 0),
                    "market_cap": crypto.get("market_cap", 0),
                    "volume_24h": crypto.get("total_volume", 0),
                    "change_24h": change,
                    "circulating_supply": crypto.get("circulating_supply", 0),
                    "market_cap_rank": crypto.get("market_cap_rank", 0),
                    "ath": crypto.get("ath", 0),
                    "atl": crypto.get("atl", 0),
                }
                
                if change > 0:
                    gainers.append(crypto_info)
                else:
                    losers.append(crypto_info)
        
        # Trier par variation absolue
        gainers.sort(key=lambda x: x["change_24h"], reverse=True)
        losers.sort(key=lambda x: x["change_24h"])
        
        return gainers[:self.max_results], losers[:self.max_results]
    
    def analyze_crypto(self, crypto: Dict) -> Dict:
        """
        Génère une analyse complète pour une crypto
        
        Returns:
            Analyse avec métriques et commentaire
        """
        symbol = crypto["symbol"]
        change = crypto["change_24h"]
        price = crypto["price"]
        market_cap = crypto["market_cap"]
        volume = crypto["volume_24h"]
        
        # Calcul du ratio volume/market_cap
        volume_ratio = (volume / market_cap * 100) if market_cap > 0 else 0
        
        # Détermination de la force du mouvement
        change_abs = abs(change)
        if change_abs > 50:
            strength = "🔥 EXTRÊME"
        elif change_abs > 20:
            strength = "⚡ TRÈS FORT"
        elif change_abs > 10:
            strength = "📈 FORT"
        else:
            strength = "📊 MODÉRÉ"
        
        # Analyse de la liquidité
        if volume_ratio > 50:
            liquidity = "💧 Très bonne"
        elif volume_ratio > 20:
            liquidity = "💧 Bonne"
        elif volume_ratio > 5:
            liquidity = "⚠️ Modérée"
        else:
            liquidity = "🚨 Faible"
        
        # Génération du commentaire
        if change > 0:
            comment = self._generate_positive_analysis(crypto, volume_ratio)
        else:
            comment = self._generate_negative_analysis(crypto, volume_ratio)
        
        return {
            "name": crypto["name"],
            "symbol": symbol,
            "price": f"${price:.8f}" if price < 1 else f"${price:,.2f}",
            "change_24h": f"{change:+.2f}%",
            "market_cap": f"${market_cap:,.0f}" if market_cap else "N/A",
            "volume_24h": f"${volume:,.0f}" if volume else "N/A",
            "strength": strength,
            "liquidity": liquidity,
            "volume_ratio": f"{volume_ratio:.1f}%",
            "rank": crypto["market_cap_rank"],
            "analysis": comment,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_positive_analysis(self, crypto: Dict, volume_ratio: float) -> str:
        """Analyse pour une crypto en hausse"""
        change = crypto["change_24h"]
        
        if change > 100:
            trend = "🚀 Explosion exceptionnelle"
            reason = "Volume d'achat massif ou annonce positive"
        elif change > 50:
            trend = "⚡ Hausse très forte"
            reason = "Intérêt croissant des acheteurs"
        elif change > 20:
            trend = "📈 Hausse signifiante"
            reason = "Mouvement d'achat significatif"
        else:
            trend = "💚 Hausse modérée"
            reason = "Intérêt progressif"
        
        if volume_ratio > 30:
            liquidity_note = " Forte liquidité confirmée."
        elif volume_ratio > 10:
            liquidity_note = " Volume sain."
        else:
            liquidity_note = " Volume prudent - vigilance recommandée."
        
        return f"{trend}. {reason}.{liquidity_note} À surveiller pour confirmation."
    
    def _generate_negative_analysis(self, crypto: Dict, volume_ratio: float) -> str:
        """Analyse pour une crypto en baisse"""
        change = crypto["change_24h"]
        
        if change < -50:
            trend = "🔴 Crash significatif"
            reason = "Vente massive ou mauvaise nouvelle"
        elif change < -20:
            trend = "📉 Baisse forte"
            reason = "Pression de vente importante"
        elif change < -10:
            trend = "💔 Baisse modérée"
            reason = "Consolidation baissière"
        else:
            trend = "📊 Baisse mineure"
            reason = "Correction technique"
        
        if crypto["price"] > 0 and crypto["atl"] > 0:
            from_ath = ((crypto["price"] - crypto["ath"]) / crypto["ath"] * 100) if crypto["ath"] > 0 else 0
            recovery_note = f" Distance de l'ATL: {abs(from_ath):.1f}%."
        else:
            recovery_note = ""
        
        return f"{trend}. {reason}.{recovery_note} Possibilité de rebond ou consolidation."
    
    def analyze_all(self) -> Dict:
        """
        Lance une analyse complète
        
        Returns:
            Dictionnaire avec toutes les analyses
        """
        print("\n" + "="*60)
        print("🔍 ANALYSE CRYPTO AUTONOME")
        print("="*60)
        
        # Récupération des données
        cryptos = self.get_top_cryptocurrencies(limit=250)
        if not cryptos:
            print("❌ Impossible de récupérer les données")
            return {"status": "error", "cryptos": []}
        
        # Filtrage des variations significatives
        gainers, losers = self.filter_significant_changes(cryptos)
        
        print(f"✅ {len(gainers)} gagnants détectés")
        print(f"✅ {len(losers)} perdants détectés")
        
        # Analyse complète
        all_analyzed = []
        
        print("\n📈 Analyse des gagnants...")
        for crypto in gainers[:20]:  # Top 20 gagnants
            analysis = self.analyze_crypto(crypto)
            all_analyzed.append(analysis)
            print(f"  {crypto['symbol']}: {crypto['change_24h']:+.2f}%")
        
        print("\n📉 Analyse des perdants...")
        for crypto in losers[:20]:  # Top 20 perdants
            analysis = self.analyze_crypto(crypto)
            all_analyzed.append(analysis)
            print(f"  {crypto['symbol']}: {crypto['change_24h']:+.2f}%")
        
        print("\n" + "="*60)
        print(f"✅ {len(all_analyzed)} cryptos analysées")
        print("="*60 + "\n")
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "cryptos": all_analyzed,
            "gainers_count": len(gainers),
            "losers_count": len(losers)
        }


def main():
    """Test du module"""
    analyzer = CryptoAnalyzer(min_variation=5.0)
    result = analyzer.analyze_all()
    
    if result["status"] == "success":
        print(f"Analyse réussie: {len(result['cryptos'])} cryptos")
    else:
        print("Analyse échouée")


if __name__ == "__main__":
    main()
