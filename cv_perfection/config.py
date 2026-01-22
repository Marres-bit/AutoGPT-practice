"""
CV Perfection Module - Configuration
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class CVConfig:
    """Configuration pour le module CV Perfection"""
    
    # Dossiers
    desktop_path: Path = field(default_factory=lambda: Path.home() / "Desktop")
    input_folder: str = "CV"
    output_folder: str = "CV parfait"
    
    # Paramètres de surveillance
    scan_interval_minutes: int = 5  # Vérifier nouveaux CV toutes les 5 min
    supported_formats: List[str] = field(default_factory=lambda: ['.pdf', '.docx'])
    
    # Cache pour fichiers déjà traités
    processed_cache_file: str = "cv_processed_cache.json"
    
    # Design Settings
    available_styles: List[str] = field(default_factory=lambda: [
        'Classique',
        'Moderne', 
        'Corporate',
        'Minimaliste',
        'Creative'
    ])
    
    default_style: str = 'Moderne'
    generate_multiple_styles: bool = False  # Si True, génère tous les styles
    
    # Typography
    professional_fonts: dict = field(default_factory=lambda: {
        'Classique': ('Times New Roman', 'Georgia'),
        'Moderne': ('Calibri', 'Arial'),
        'Corporate': ('Arial', 'Helvetica'),
        'Minimaliste': ('Helvetica', 'Arial'),
        'Creative': ('Montserrat', 'Open Sans')
    })
    
    # Color Schemes (RGB)
    color_schemes: dict = field(default_factory=lambda: {
        'Classique': {'primary': (0, 0, 0), 'accent': (70, 70, 70)},
        'Moderne': {'primary': (41, 128, 185), 'accent': (52, 73, 94)},
        'Corporate': {'primary': (44, 62, 80), 'accent': (41, 128, 185)},
        'Minimaliste': {'primary': (0, 0, 0), 'accent': (100, 100, 100)},
        'Creative': {'primary': (231, 76, 60), 'accent': (52, 73, 94)}
    })
    
    # ATS Optimization
    ats_keywords_weight: float = 0.3  # Importance des mots-clés ATS
    max_pages: int = 2  # CV idéal = 1-2 pages
    
    # AI Settings
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Content Optimization
    optimize_content: bool = True  # Améliorer textes
    rewrite_bullet_points: bool = True
    enhance_descriptions: bool = True
    professional_tone: bool = True
    
    # Safety
    never_invent_data: bool = True  # CRITIQUE: Ne jamais inventer expériences/diplômes
    preserve_original: bool = True  # Toujours garder le fichier original
    
    # Reports
    generate_improvement_report: bool = True
    report_language: str = "fr"  # français
    
    def __post_init__(self):
        """Initialise les chemins complets"""
        self.input_path = self.desktop_path / self.input_folder
        self.output_path = self.desktop_path / self.output_folder
        self.cache_path = self.output_path / self.processed_cache_file
        
        # Créer les dossiers s'ils n'existent pas
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def get_font_for_style(self, style: str) -> tuple:
        """Retourne les polices recommandées pour un style"""
        return self.professional_fonts.get(style, ('Arial', 'Helvetica'))
    
    def get_colors_for_style(self, style: str) -> dict:
        """Retourne le schéma de couleurs pour un style"""
        return self.color_schemes.get(style, {'primary': (0, 0, 0), 'accent': (70, 70, 70)})


# Instance globale
_config = CVConfig()

def get_config() -> CVConfig:
    """Retourne l'instance de configuration"""
    return _config
