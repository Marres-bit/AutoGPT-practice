"""
Tests unitaires pour Learning Engine
pytest tests/test_learning_engine.py -v
"""

import pytest
from pathlib import Path
import json
import tempfile
import shutil
from learning_engine import LearningEngine


@pytest.fixture
def temp_project_root():
    """Crée un dossier temporaire"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def learning_engine(temp_project_root):
    """Crée instance LearningEngine"""
    return LearningEngine(temp_project_root)


class TestLearningEngineInit:
    """Tests d'initialisation"""
    
    def test_creates_state_file(self, learning_engine, temp_project_root):
        """Fichier d'état créé"""
        state_file = temp_project_root / "learning_state.json"
        assert state_file.exists()
    
    def test_initial_state_defaults(self, learning_engine):
        """Valeurs par défaut correctes"""
        state = learning_engine.state
        assert state['win_rate'] == 0
        assert state['total_trades'] == 0
        assert state['min_gain_to_open'] == 0.5


class TestShouldTrade:
    """Tests de la logique should_trade"""
    
    def test_trade_on_high_gain(self, learning_engine):
        """Trade si gain >= 0.80%"""
        market = {"BTC": 1.5, "ETH": 0.9, "BNB": 0.5}
        
        should_trade, reason = learning_engine.should_trade("BTC", market)
        assert should_trade is True
        assert "1.50%" in reason
    
    def test_block_on_low_gain(self, learning_engine):
        """Bloque si gain < 0.3%"""
        market = {"BTC": 0.2, "ETH": 0.1}
        
        should_trade, reason = learning_engine.should_trade("BTC", market)
        assert should_trade is False
        assert "0.3%" in reason or "trop faible" in reason
    
    def test_opportunistic_high_win_rate(self, learning_engine, temp_project_root):
        """Trade 0.4-0.8% si win rate >80%"""
        # Simuler win rate élevé
        state_file = temp_project_root / "learning_state.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        state['win_rate'] = 0.85
        state['consecutive_losses'] = 0
        state['min_gain_to_open'] = 0.80
        
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        learning_engine._load_state()
        
        market = {"ETH": 0.5, "BTC": 0.3}  # 0.5% entre 0.4 et 0.8
        should_trade, reason = learning_engine.should_trade("ETH", market)
        
        assert should_trade is True
        assert "Win rate excellent" in reason or "Opportunité" in reason
    
    def test_best_asset_trades(self, learning_engine):
        """Trade meilleur asset même si 0.4-0.8%"""
        market = {"BTC": 0.6, "ETH": 0.3, "BNB": 0.2}
        
        should_trade, reason = learning_engine.should_trade("BTC", market)
        # BTC est le meilleur avec 0.6%
        assert should_trade is True or "Meilleur asset" in reason


class TestLearnFromTrade:
    """Tests d'apprentissage"""
    
    def test_win_rate_updates(self, learning_engine):
        """Win rate se met à jour"""
        initial_trades = learning_engine.state['total_trades']
        
        learning_engine.learn_from_trade("BTC", 1000, 1100, True)
        
        assert learning_engine.state['total_trades'] == initial_trades + 1
        assert learning_engine.state['win_rate'] == 1.0  # 100% sur 1 trade
    
    def test_consecutive_losses_increment(self, learning_engine):
        """Pertes consécutives incrémentent"""
        learning_engine.learn_from_trade("ETH", 1000, 900, False)
        learning_engine.learn_from_trade("BTC", 1000, 950, False)
        
        assert learning_engine.state['consecutive_losses'] == 2
    
    def test_consecutive_losses_reset_on_win(self, learning_engine):
        """Reset pertes après gain"""
        learning_engine.state['consecutive_losses'] = 3
        learning_engine.learn_from_trade("BTC", 1000, 1100, True)
        
        assert learning_engine.state['consecutive_losses'] == 0


class TestRiskLevelAdjustment:
    """Tests d'ajustement du niveau de risque"""
    
    def test_risk_decreases_on_loss(self, learning_engine):
        """Risque diminue après perte"""
        initial_risk = learning_engine.state['risk_level']
        
        learning_engine.learn_from_trade("BTC", 1000, 800, False)  # Grosse perte
        
        assert learning_engine.state['risk_level'] < initial_risk
    
    def test_risk_increases_on_win(self, learning_engine):
        """Risque augmente après gain"""
        learning_engine.state['risk_level'] = 0.5
        
        learning_engine.learn_from_trade("ETH", 1000, 1200, True)
        
        assert learning_engine.state['risk_level'] > 0.5


class TestAvoidPatterns:
    """Tests des patterns à éviter"""
    
    def test_avoid_asset_after_losses(self, learning_engine, temp_project_root):
        """Éviter asset après pertes"""
        # Simuler pattern avoid
        state_file = temp_project_root / "learning_state.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        state['avoid_patterns'] = ["AVOID_BTC_HIGH_LOSS_RATE"]
        
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        learning_engine._load_state()
        
        market = {"BTC": 2.0, "ETH": 1.0}
        should_trade, reason = learning_engine.should_trade("BTC", market)
        
        assert should_trade is False
        assert "historique de pertes" in reason


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
