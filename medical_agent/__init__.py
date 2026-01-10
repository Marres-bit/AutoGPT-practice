"""
MediGenius AI - Package autonome de génération de leçons médicales avec stockage cloud
Génère automatiquement 3 leçons par semaine
"""

__version__ = "2.0.0"
__author__ = "MediGenius AI"

from medical_agent.agent import MedicalAIAgent
from medical_agent.cloud_database import CloudDatabase
from medical_agent.database import MedicalDatabase  # Garde compatibilité
from medical_agent.scheduler import MedicalScheduler
from medical_agent.commands import CommandHandler
from medical_agent.gui import MedicalGUI

__all__ = [
    'MedicalAIAgent',
    'CloudDatabase',
    'MedicalDatabase',
    'MedicalScheduler',
    'CommandHandler',
    'MedicalGUI'
]
