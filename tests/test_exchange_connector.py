"""
Tests unitaires pour Exchange Connector
pytest tests/test_exchange_connector.py -v
"""

import pytest
from exchange_connector import ExchangeConnector


@pytest.fixture
def exchange():
    """Crée instance Exchange en mode testnet"""
    return ExchangeConnector(testnet=True)


class TestExchangeConnection:
    """Tests de connexion"""
    
    def test_connection_status(self, exchange):
        """Vérifie status de connexion"""
        status = exchange.get_connection_status()
        
        assert 'connected' in status
        assert 'testnet' in status
        assert status['testnet'] is True
    
    def test_exchange_initialized(self, exchange):
        """Exchange ccxt initialisé"""
        assert exchange.exchange is not None
        assert hasattr(exchange.exchange, 'fetch_ticker')


class TestPriceFetching:
    """Tests de récupération des prix"""
    
    def test_get_real_prices(self, exchange):
        """Récupère prix réels"""
        prices = exchange.get_real_prices()
        
        assert isinstance(prices, dict)
        assert len(prices) > 0
        
        # Vérifier assets communs
        expected_assets = ["BTC", "ETH", "BNB"]
        for asset in expected_assets:
            if asset in prices:
                assert prices[asset] > 0
    
    def test_price_format(self, exchange):
        """Format des prix correct"""
        prices = exchange.get_real_prices()
        
        for asset, price in prices.items():
            assert isinstance(price, (int, float))
            assert price > 0
    
    def test_calculate_market_changes(self, exchange):
        """Calcul des variations de prix"""
        changes = exchange.calculate_market_changes()
        
        assert isinstance(changes, dict)
        
        for asset, change in changes.items():
            assert isinstance(change, (int, float))
            assert -100 <= change <= 100  # % change raisonnable


class TestMarketData:
    """Tests des données de marché"""
    
    def test_get_market_data(self, exchange):
        """Récupère données de marché complètes"""
        data = exchange.get_market_data()
        
        assert 'prices' in data
        assert 'changes' in data
        assert 'timestamp' in data
        
        assert isinstance(data['prices'], dict)
        assert isinstance(data['changes'], dict)
    
    def test_market_data_consistency(self, exchange):
        """Cohérence entre prix et changes"""
        data = exchange.get_market_data()
        
        # Mêmes assets dans prices et changes
        price_assets = set(data['prices'].keys())
        change_assets = set(data['changes'].keys())
        
        common_assets = price_assets.intersection(change_assets)
        assert len(common_assets) > 0


class TestErrorHandling:
    """Tests de gestion d'erreurs"""
    
    def test_handles_network_errors_gracefully(self, exchange):
        """Gère erreurs réseau"""
        # Même avec erreur réseau, ne doit pas crash
        try:
            prices = exchange.get_real_prices()
            assert isinstance(prices, dict)
        except Exception as e:
            pytest.fail(f"Exchange crashed: {e}")
    
    def test_returns_empty_on_failure(self, exchange):
        """Retourne dict vide si échec"""
        # Forcer symbole invalide
        exchange.symbols = ["INVALID/USDT"]
        
        prices = exchange.get_real_prices()
        # Ne doit pas crash, retourner {} ou données valides
        assert isinstance(prices, dict)


class TestSymbolHandling:
    """Tests de gestion des symboles"""
    
    def test_default_symbols_loaded(self, exchange):
        """Symboles par défaut chargés"""
        assert len(exchange.symbols) > 0
        assert "BTC/USDT" in exchange.symbols
    
    def test_symbol_format_correct(self, exchange):
        """Format des symboles correct"""
        for symbol in exchange.symbols:
            assert "/" in symbol
            assert "USDT" in symbol


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
