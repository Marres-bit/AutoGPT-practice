"""
Structured Logger - Logging professionnel pour système de trading
Format JSON pour analyse automatisée et monitoring
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler
import sys


class StructuredLogger:
    """
    Logger structuré avec sortie JSON pour faciliter l'analyse
    et l'intégration avec des outils de monitoring
    """
    
    def __init__(
        self,
        name: str,
        log_dir: Path,
        log_level: int = logging.INFO,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB par fichier
        backup_count: int = 5
    ):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Créer le logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        
        # Éviter les doublons de handlers
        if self.logger.handlers:
            return
        
        # Handler pour fichier JSON (rotation)
        json_log_file = self.log_dir / f"{name}.json.log"
        json_handler = RotatingFileHandler(
            json_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        json_handler.setLevel(log_level)
        json_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(json_handler)
        
        # Handler pour fichier texte lisible (rotation)
        text_log_file = self.log_dir / f"{name}.log"
        text_handler = RotatingFileHandler(
            text_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        text_handler.setLevel(log_level)
        text_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(text_handler)
        
        # Console handler (optionnel, pour debug)
        if log_level == logging.DEBUG:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logging.Formatter(
                '%(levelname)s: %(message)s'
            ))
            self.logger.addHandler(console_handler)
    
    def _log_structured(
        self,
        level: int,
        message: str,
        extra: Optional[Dict[str, Any]] = None
    ):
        """Log structuré avec contexte enrichi"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": logging.getLevelName(level),
            "message": message,
            "logger": self.name
        }
        
        if extra:
            log_data.update(extra)
        
        self.logger.log(level, message, extra={"structured": log_data})
    
    def debug(self, message: str, **kwargs):
        """Log DEBUG avec contexte"""
        self._log_structured(logging.DEBUG, message, kwargs)
    
    def info(self, message: str, **kwargs):
        """Log INFO avec contexte"""
        self._log_structured(logging.INFO, message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log WARNING avec contexte"""
        self._log_structured(logging.WARNING, message, kwargs)
    
    def error(self, message: str, **kwargs):
        """Log ERROR avec contexte"""
        self._log_structured(logging.ERROR, message, kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log CRITICAL avec contexte"""
        self._log_structured(logging.CRITICAL, message, kwargs)
    
    # Méthodes spécifiques trading
    
    def log_trade_execution(
        self,
        asset: str,
        action: str,
        entry_price: float,
        quantity: float,
        strategy: str,
        **kwargs
    ):
        """Log exécution trade"""
        self.info(
            f"Trade {action}: {quantity:.6f} {asset} @ ${entry_price:,.2f}",
            event_type="trade_execution",
            asset=asset,
            action=action,
            entry_price=entry_price,
            quantity=quantity,
            strategy=strategy,
            **kwargs
        )
    
    def log_trade_close(
        self,
        asset: str,
        exit_price: float,
        pnl: float,
        pnl_pct: float,
        duration_seconds: int,
        **kwargs
    ):
        """Log clôture trade"""
        self.info(
            f"Trade closed: {asset} P&L=${pnl:.2f} ({pnl_pct:+.2f}%)",
            event_type="trade_close",
            asset=asset,
            exit_price=exit_price,
            pnl=pnl,
            pnl_pct=pnl_pct,
            duration_seconds=duration_seconds,
            **kwargs
        )
    
    def log_risk_event(
        self,
        event_type: str,
        severity: str,
        details: Dict[str, Any]
    ):
        """Log événement de risque"""
        level = {
            "low": logging.INFO,
            "medium": logging.WARNING,
            "high": logging.ERROR,
            "critical": logging.CRITICAL
        }.get(severity, logging.WARNING)
        
        extra_data = {
            "event_type": "risk_event",
            "risk_event_type": event_type,
            "severity": severity,
            "details": details
        }
        
        self._log_structured(
            level,
            f"Risk event: {event_type}",
            extra_data
        )
    
    def log_strategy_decision(
        self,
        strategy_name: str,
        market_condition: str,
        decision: str,
        confidence: float,
        reasons: list
    ):
        """Log décision stratégique"""
        self.info(
            f"Strategy decision: {strategy_name} -> {decision}",
            event_type="strategy_decision",
            strategy=strategy_name,
            market_condition=market_condition,
            decision=decision,
            confidence=confidence,
            reasons=reasons
        )
    
    def log_performance_metrics(
        self,
        capital: float,
        win_rate: float,
        total_trades: int,
        sharpe_ratio: Optional[float] = None,
        max_drawdown: Optional[float] = None,
        **kwargs
    ):
        """Log métriques de performance"""
        self.info(
            f"Performance: Capital=${capital:,.2f}, WinRate={win_rate:.1%}",
            event_type="performance_metrics",
            capital=capital,
            win_rate=win_rate,
            total_trades=total_trades,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            **kwargs
        )


class JsonFormatter(logging.Formatter):
    """Formatter JSON pour logs structurés"""
    
    def format(self, record):
        if hasattr(record, 'structured'):
            # Si log structuré, utiliser les données enrichies
            return json.dumps(record.structured, ensure_ascii=False)
        else:
            # Sinon, format JSON basique
            log_data = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_data, ensure_ascii=False)


# Factory pour créer des loggers facilement
_loggers_cache = {}

def get_logger(
    name: str,
    log_dir: Path = None,
    log_level: int = logging.INFO
) -> StructuredLogger:
    """
    Factory pour obtenir ou créer un logger structuré
    
    Args:
        name: Nom du logger (ex: "trading", "risk", "ml")
        log_dir: Dossier des logs (défaut: ./logs)
        log_level: Niveau de log
    
    Returns:
        Instance de StructuredLogger
    """
    if name in _loggers_cache:
        return _loggers_cache[name]
    
    if log_dir is None:
        log_dir = Path(__file__).parent / "logs"
    
    logger = StructuredLogger(name, log_dir, log_level)
    _loggers_cache[name] = logger
    return logger


if __name__ == "__main__":
    # Test du logger structuré
    print("🧪 Test du Structured Logger\n")
    
    log_dir = Path(__file__).parent / "logs"
    logger = get_logger("trading_test", log_dir, logging.DEBUG)
    
    # Tests différents types de logs
    logger.info("Système démarré")
    logger.debug("Mode debug activé", mode="test", version="1.0")
    
    # Log trade
    logger.log_trade_execution(
        asset="BTC",
        action="BUY",
        entry_price=95000.0,
        quantity=0.01,
        strategy="BullX_Momentum",
        confidence=0.85
    )
    
    # Log clôture
    logger.log_trade_close(
        asset="BTC",
        exit_price=96000.0,
        pnl=10.0,
        pnl_pct=1.05,
        duration_seconds=3600
    )
    
    # Log risque
    logger.log_risk_event(
        event_type="max_drawdown_warning",
        severity="medium",
        details={"drawdown_pct": 0.15, "limit": 0.20}
    )
    
    # Log performance
    logger.log_performance_metrics(
        capital=10500.0,
        win_rate=0.75,
        total_trades=20,
        sharpe_ratio=1.8
    )
    
    logger.warning("Test warning", test_param=123)
    logger.error("Test error", error_code="TEST_001")
    
    print(f"\n✅ Logs générés dans: {log_dir}")
    print(f"  - {log_dir}/trading_test.log (texte)")
    print(f"  - {log_dir}/trading_test.json.log (JSON)")
