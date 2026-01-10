"""
Medical AI Agent - Package autonome de génération de leçons médicales
Génère automatiquement 3 leçons par semaine
"""

__version__ = "1.0.0"
__author__ = "AI Medical Assistant"

from medical_agent.agent import MedicalAIAgent
from medical_agent.database import MedicalDatabase
from medical_agent.scheduler import MedicalScheduler
from medical_agent.commands import CommandHandler
from medical_agent.gui import MedicalGUI

__all__ = [
    'MedicalAIAgent',
    'MedicalDatabase',
    'MedicalScheduler',
    'CommandHandler',
    'MedicalGUI'
]
