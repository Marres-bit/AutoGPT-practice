"""
CV Designer - Design professionnel de niveau expert
Génère des CV visuellement parfaits inspirés de Canva/Adobe
"""

import io
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass
import logging

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    _A4 = A4
    _reportlab_available = True
except ImportError:
    SimpleDocTemplate = None
    _A4 = (595.27, 841.89)  # A4 size in points as fallback
    _reportlab_available = False

from .config import CVConfig
from .cv_analyzer import CVAnalysis
from .cv_optimizer import OptimizedContent


@dataclass
class CVDesign:
    """Configuration de design pour un CV"""
    
    style_name: str
    primary_color: tuple  # RGB
    accent_color: tuple  # RGB
    font_main: str
    font_accent: str
    page_size: tuple = None
    margins: Dict[str, float] = None
    
    def __post_init__(self):
        if self.page_size is None:
            self.page_size = _A4
        if self.margins is None:
            try:
                self.margins = {'top': 2*cm, 'bottom': 2*cm, 'left': 2*cm, 'right': 2*cm}
            except:
                # Fallback si cm n'est pas disponible
                self.margins = {'top': 56.69, 'bottom': 56.69, 'left': 56.69, 'right': 56.69}


class CVDesigner:
    """Designer de CV professionnel"""
    
    def __init__(self, config: Optional[CVConfig] = None):
        self.config = config or CVConfig()
        self.logger = self._setup_logger()
        
        if not SimpleDocTemplate:
            self.logger.error("❌ reportlab non installé - design PDF impossible")
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('CVDesigner')
        logger.setLevel(logging.INFO)
        return logger
    
    def create_professional_cv(
        self,
        analysis: CVAnalysis,
        optimized_content: OptimizedContent,
        output_path: Path,
        style: str = 'Moderne'
    ) -> bool:
        """
        Crée un CV professionnel avec design premium
        
        Args:
            analysis: Analyse du CV original
            optimized_content: Contenu optimisé
            output_path: Chemin de sortie du PDF
            style: Style de design ('Classique', 'Moderne', etc.)
        
        Returns:
            True si succès
        """
        if not SimpleDocTemplate:
            self.logger.error("ReportLab requis pour générer PDF")
            return False
        
        self.logger.info(f"🎨 Création CV style '{style}'")
        
        # Obtenir config design
        design = self._get_design_config(style)
        
        try:
            # Créer document PDF
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=design.page_size,
                topMargin=design.margins['top'],
                bottomMargin=design.margins['bottom'],
                leftMargin=design.margins['left'],
                rightMargin=design.margins['right']
            )
            
            # Créer contenu
            story = []
            
            # En-tête avec infos personnelles
            story.extend(self._create_header(analysis, design))
            story.append(Spacer(1, 0.3*inch))
            
            # Si aucune section optimisée, utiliser le contenu brut
            if not optimized_content.sections:
                self.logger.warning("Aucune section optimisée - utilisation contenu brut")
                # Créer une section unique avec tout le contenu
                story.extend(self._create_raw_content_section(analysis.raw_text, design))
            else:
                # Résumé professionnel (si présent)
                if 'summary' in optimized_content.sections:
                    story.extend(self._create_summary_section(optimized_content.sections['summary'], design))
                    story.append(Spacer(1, 0.2*inch))
                
                # Expérience professionnelle
                if 'experience' in optimized_content.sections:
                    story.extend(self._create_experience_section(optimized_content.sections['experience'], design))
                    story.append(Spacer(1, 0.2*inch))
                
                # Formation
                if 'education' in optimized_content.sections:
                    story.extend(self._create_education_section(optimized_content.sections['education'], design))
                    story.append(Spacer(1, 0.2*inch))
                
                # Compétences
                if 'skills' in optimized_content.sections:
                    story.extend(self._create_skills_section(optimized_content.sections['skills'], design))
            
            # Générer PDF
            doc.build(story)
            
            self.logger.info(f"✅ CV créé: {output_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création PDF: {e}")
            return False
    
    def _get_design_config(self, style: str) -> CVDesign:
        """Retourne la configuration de design pour un style"""
        
        colors_dict = self.config.get_colors_for_style(style)
        fonts = self.config.get_font_for_style(style)
        
        return CVDesign(
            style_name=style,
            primary_color=colors_dict['primary'],
            accent_color=colors_dict['accent'],
            font_main=fonts[0],
            font_accent=fonts[1]
        )
    
    def _create_header(self, analysis: CVAnalysis, design: CVDesign) -> List:
        """Crée l'en-tête du CV avec nom et contact"""
        elements = []
        styles = getSampleStyleSheet()
        
        # Style nom (grand, gras, couleur primaire)
        name_style = ParagraphStyle(
            'CVName',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.Color(
                design.primary_color[0]/255,
                design.primary_color[1]/255,
                design.primary_color[2]/255
            ),
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        # Extraire nom (première ligne du texte généralement)
        lines = analysis.raw_text.split('\n')
        name = lines[0].strip() if lines else "Candidat Professionnel"
        
        elements.append(Paragraph(name, name_style))
        
        # Informations de contact
        contact_info = []
        if analysis.personal_info.get('email'):
            contact_info.append(analysis.personal_info['email'])
        if analysis.personal_info.get('phone'):
            contact_info.append(analysis.personal_info['phone'])
        
        if contact_info:
            contact_style = ParagraphStyle(
                'CVContact',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.grey,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            contact_text = " | ".join(contact_info)
            elements.append(Paragraph(contact_text, contact_style))
        
        # Ligne de séparation
        elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_raw_content_section(self, text: str, design: CVDesign) -> List:
        """Crée une section avec le contenu brut du CV"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(self._create_section_title("CONTENU DU CV", design))
        
        content_style = ParagraphStyle(
            'CVRawContent',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=4,
            leading=13
        )
        
        # Diviser par paragraphes et formater
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for para in paragraphs[:20]:  # Limiter à 20 premiers paragraphes
            if para:
                elements.append(Paragraph(para.replace('\n', '<br/>'), content_style))
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_section_title(self, title: str, design: CVDesign) -> Paragraph:
        """Crée un titre de section stylisé"""
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CVSectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.Color(
                design.primary_color[0]/255,
                design.primary_color[1]/255,
                design.primary_color[2]/255
            ),
            fontName='Helvetica-Bold',
            spaceBefore=12,
            spaceAfter=8,
            borderWidth=0,
            borderPadding=0,
            leftIndent=0
        )
        
        return Paragraph(title.upper(), title_style)
    
    def _create_summary_section(self, text: str, design: CVDesign) -> List:
        """Crée la section résumé/profil"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(self._create_section_title("PROFIL PROFESSIONNEL", design))
        
        summary_style = ParagraphStyle(
            'CVSummary',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            leading=14
        )
        
        elements.append(Paragraph(text, summary_style))
        
        return elements
    
    def _create_experience_section(self, text: str, design: CVDesign) -> List:
        """Crée la section expérience professionnelle"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(self._create_section_title("EXPÉRIENCE PROFESSIONNELLE", design))
        
        exp_style = ParagraphStyle(
            'CVExperience',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=4,
            leading=13,
            bulletIndent=10,
            leftIndent=15
        )
        
        # Séparer par lignes et formater
        for line in text.split('\n'):
            line = line.strip()
            if line:
                if line.startswith(('•', '-', '*')):
                    line = line[1:].strip()
                    elements.append(Paragraph(f"• {line}", exp_style))
                else:
                    # Titre de poste ou entreprise
                    job_style = ParagraphStyle(
                        'CVJobTitle',
                        parent=styles['Normal'],
                        fontSize=11,
                        textColor=colors.black,
                        fontName='Helvetica-Bold',
                        spaceAfter=2,
                        spaceBefore=6
                    )
                    elements.append(Paragraph(line, job_style))
        
        return elements
    
    def _create_education_section(self, text: str, design: CVDesign) -> List:
        """Crée la section formation"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(self._create_section_title("FORMATION", design))
        
        edu_style = ParagraphStyle(
            'CVEducation',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            leading=13
        )
        
        for line in text.split('\n'):
            line = line.strip()
            if line:
                elements.append(Paragraph(line, edu_style))
        
        return elements
    
    def _create_skills_section(self, text: str, design: CVDesign) -> List:
        """Crée la section compétences"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(self._create_section_title("COMPÉTENCES", design))
        
        skills_style = ParagraphStyle(
            'CVSkills',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=3,
            leading=13,
            bulletIndent=10,
            leftIndent=15
        )
        
        for line in text.split('\n'):
            line = line.strip()
            if line:
                if not line.startswith(('•', '-', '*')):
                    line = f"• {line}"
                elements.append(Paragraph(line, skills_style))
        
        return elements
    
    def create_multiple_styles(
        self,
        analysis: CVAnalysis,
        optimized_content: OptimizedContent,
        output_dir: Path,
        base_filename: str
    ) -> List[Path]:
        """
        Génère le CV dans plusieurs styles
        
        Returns:
            Liste des fichiers créés
        """
        created_files = []
        
        for style in self.config.available_styles:
            output_path = output_dir / f"{base_filename}_{style}.pdf"
            
            success = self.create_professional_cv(
                analysis=analysis,
                optimized_content=optimized_content,
                output_path=output_path,
                style=style
            )
            
            if success:
                created_files.append(output_path)
        
        self.logger.info(f"✅ {len(created_files)} styles générés")
        
        return created_files
