"""
🔥 GEIS - Global Extreme Insanity Scanner
Module de veille mondiale des contenus insolites extrêmes
"""

__version__ = "1.0.0"
__author__ = "MediGenius AI Team"

from .scanner import InsanityScanner
from .config import GEISConfig

__all__ = ["InsanityScanner", "GEISConfig"]
