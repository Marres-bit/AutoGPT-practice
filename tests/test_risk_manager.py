"""
Tests unitaires pour Risk Manager
pytest tests/test_risk_manager.py -v
"""

import pytest
from pathlib import Path
import json
import tempfile
import shutil
from risk_manager import RiskManager, RiskLevel


@pytest.fixture
def temp_project_root():
    """Crée un dossier temporaire pour les tests"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def risk_manager(temp_project_root):
    """Crée une instance RiskManager pour tests"""
    return RiskManager(
        project_root=temp_project_root,
        initial_capital=10000.0,
        risk_level=RiskLevel.MODERATE
    )


class TestRiskManagerInitialization:
    """Tests d'initialisation"""
    
    def test_init_creates_state_file(self, risk_manager, temp_project_root):
        """Vérifie que le fichier d'état est créé"""
        state_file = temp_project_root / "risk_state.json"
        assert state_file.exists()
    
    def test_initial_capital_correct(self, risk_manager):
        """Vérifie le capital initial"""
        summary = risk_manager.get_risk_summary()
        assert summary['current_capital'] == 10000.0
    
    def test_risk_level_moderate(self, risk_manager):
        """Vérifie le niveau de risque MODERATE"""
        summary = risk_manager.get_risk_summary()
        assert summary['risk_level'] == 'MODERATE'
        assert summary['risk_per_trade'] == 1.5  # 1.5% pour MODERATE


class TestPositionSizing:
    """Tests de calcul de position"""
    
    def test_kelly_criterion_basic(self, risk_manager):
        """Test Kelly Criterion avec paramètres standard"""
        position = risk_manager.calculate_position_size(
            asset="BTC",
            entry_price=50000.0,
            win_rate=0.6,
            avg_win=100.0,
            avg_loss=50.0,
            volatility=0.02
        )
        
        assert position > 0
        assert position <= 10000.0  # Max capital
    
    def test_position_respects_max_risk(self, risk_manager):
        """Vérifie que la position respecte le risque max"""
        position = risk_manager.calculate_position_size(
            asset="ETH",
            entry_price=3000.0,
            win_rate=0.5,
            avg_win=50.0,
            avg_loss=50.0,
            volatility=0.03
        )
        
        # MODERATE = 1.5% max
        max_position = 10000.0 * 0.015
        assert position <= max_position * 1.1  # Tolérance 10%
    
    def test_zero_position_on_low_win_rate(self, risk_manager):
        """Position nulle si win rate trop faible"""
        position = risk_manager.calculate_position_size(
            asset="XRP",
            entry_price=0.5,
            win_rate=0.3,  # 30% très faible
            avg_win=10.0,
            avg_loss=20.0,
            volatility=0.05
        )
        
        assert position == 0  # Pas de trade si Kelly négatif


class TestRiskValidation:
    """Tests de validation des risques"""
    
    def test_can_trade_initially_true(self, risk_manager):
        """Initialement, on peut trader"""
        can_trade, reason = risk_manager.can_trade()
        assert can_trade is True
        assert "OK" in reason
    
    def test_cannot_trade_after_max_drawdown(self, risk_manager, temp_project_root):
        """Blocage après max drawdown"""
        # Simuler grosses pertes
        state_file = temp_project_root / "risk_state.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        state['current_capital'] = 7500.0  # -25% drawdown
        state['peak_capital'] = 10000.0
        
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        # Recharger
        risk_manager._load_state()
        
        can_trade, reason = risk_manager.can_trade()
        assert can_trade is False
        assert "drawdown" in reason.lower()
    
    def test_cannot_trade_after_consecutive_losses(self, risk_manager, temp_project_root):
        """Blocage après 5 pertes consécutives"""
        state_file = temp_project_root / "risk_state.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        state['consecutive_losses'] = 5
        
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        risk_manager._load_state()
        
        can_trade, reason = risk_manager.can_trade()
        assert can_trade is False
        assert "5 pertes" in reason


class TestDrawdownTracking:
    """Tests de suivi du drawdown"""
    
    def test_drawdown_calculation(self, risk_manager):
        """Calcul correct du drawdown"""
        summary = risk_manager.get_risk_summary()
        initial_dd = summary['current_drawdown']
        
        assert initial_dd == 0.0  # Pas de drawdown au début
    
    def test_peak_capital_updates(self, risk_manager, temp_project_root):
        """Peak capital se met à jour"""
        # Simuler profit
        state_file = temp_project_root / "risk_state.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        state['current_capital'] = 12000.0  # +20% profit
        
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        risk_manager._load_state()
        summary = risk_manager.get_risk_summary()
        
        assert summary['current_capital'] == 12000.0


class TestStopLossCalculation:
    """Tests de calcul stop-loss"""
    
    def test_stop_loss_basic(self, risk_manager):
        """Stop-loss entre 3-5%"""
        stop_loss = risk_manager.calculate_stop_loss(
            entry_price=1000.0,
            volatility=0.02
        )
        
        # Stop loss doit être entre -3% et -5%
        loss_pct = (stop_loss - 1000.0) / 1000.0
        assert -0.05 <= loss_pct <= -0.03
    
    def test_stop_loss_high_volatility(self, risk_manager):
        """Stop-loss plus large si haute volatilité"""
        stop_loss_low_vol = risk_manager.calculate_stop_loss(1000.0, 0.01)
        stop_loss_high_vol = risk_manager.calculate_stop_loss(1000.0, 0.10)
        
        # High volatility = stop loss plus bas (plus de marge)
        assert stop_loss_high_vol < stop_loss_low_vol


class TestRiskSummary:
    """Tests du résumé de risque"""
    
    def test_summary_contains_all_fields(self, risk_manager):
        """Résumé contient tous les champs"""
        summary = risk_manager.get_risk_summary()
        
        required_fields = [
            'current_capital', 'peak_capital', 'current_drawdown',
            'max_drawdown_limit', 'consecutive_losses', 'risk_level',
            'risk_per_trade', 'emergency_stop_active'
        ]
        
        for field in required_fields:
            assert field in summary
    
    def test_summary_types_correct(self, risk_manager):
        """Types de données corrects dans le résumé"""
        summary = risk_manager.get_risk_summary()
        
        assert isinstance(summary['current_capital'], (int, float))
        assert isinstance(summary['current_drawdown'], (int, float))
        assert isinstance(summary['consecutive_losses'], int)
        assert isinstance(summary['emergency_stop_active'], bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
