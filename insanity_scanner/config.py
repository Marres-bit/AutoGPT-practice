"""
Configuration du module GEIS
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class GEISConfig:
    """Configuration globale du scanner"""
    
    # Dossier de sortie
    output_dir: Path = Path.home() / "Desktop" / "MedicalGeniusAI_Insanities"
    
    # Seuil de score minimal (1-10)
    min_insanity_score: float = 6.0
    
    # Nombre max de résultats par scan
    max_results_per_scan: int = 10
    
    # Intervalle entre scans (heures)
    scan_interval_hours: int = 5
    
    # Sources activées
    enabled_sources: List[str] = None
    
    # Limite d'âge du contenu (jours)
    max_content_age_days: int = 30
    
    # APIs et clés
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "GEIS_Scanner/1.0"
    
    twitter_bearer_token: str = ""
    
    youtube_api_key: str = ""
    
    # Mots-clés choc (scoring)
    shock_keywords: List[str] = None
    
    # User agents pour scraping
    user_agents: List[str] = None
    
    # Logging
    log_file: Path = None
    
    def __post_init__(self):
        """Initialisation des valeurs par défaut"""
        if self.enabled_sources is None:
            self.enabled_sources = [
                "reddit",
                "youtube", 
                "twitter",
                "faits_divers"
            ]
        
        if self.shock_keywords is None:
            self.shock_keywords = [
                "shocking", "unbelievable", "wtf", "insane", "crazy",
                "bizarre", "weird", "strange", "incroyable", "choquant",
                "insolite", "fou", "dingue", "impossible", "viral",
                "accident", "disaster", "extreme", "rare", "unprecedented"
            ]
        
        if self.user_agents is None:
            self.user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            ]
        
        if self.log_file is None:
            self.log_file = Path("geis_scanner.log")
        
        # Créer dossier de sortie
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Charger variables d'environnement
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID", self.reddit_client_id)
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", self.reddit_client_secret)
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", self.twitter_bearer_token)
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", self.youtube_api_key)


# Configuration globale par défaut
DEFAULT_CONFIG = GEISConfig()
