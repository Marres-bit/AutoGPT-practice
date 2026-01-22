"""
CV Perfection & Design Intelligence Module (CV-PDI)
Module autonome d'amélioration professionnelle de CV pour Medical Genius AI
"""

from .config import CVConfig
from .cv_scanner import CVScanner
from .cv_processor import CVProcessor
from .cv_analyzer import CVAnalyzer
from .cv_optimizer import CVOptimizer
from .cv_designer import CVDesigner

__all__ = [
    'CVConfig', 
    'CVScanner', 
    'CVProcessor',
    'CVAnalyzer',
    'CVOptimizer',
    'CVDesigner'
]
__version__ = '1.0.0'
