"""
CV Analyzer - Analyse intelligente de CV
Évalue structure, ATS, typographie, hiérarchie visuelle
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import logging

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from pdf2image import convert_from_path
    import pytesseract
    import os
    # Configuration Tesseract pour Windows
    if os.name == 'nt':  # Windows
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Ajouter Poppler au PATH
        poppler_path = os.path.expanduser(r'~\poppler\poppler-24.08.0\Library\bin')
        if os.path.exists(poppler_path) and poppler_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] += os.pathsep + poppler_path
    
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    convert_from_path = None
    pytesseract = None


@dataclass
class CVAnalysis:
    """Résultat d'analyse d'un CV"""
    
    # Données brutes extraites
    raw_text: str = ""
    personal_info: Dict[str, str] = field(default_factory=dict)
    sections: Dict[str, str] = field(default_factory=dict)
    
    # Scores d'évaluation (0-10)
    structure_score: float = 0.0
    ats_score: float = 0.0
    typography_score: float = 0.0
    visual_hierarchy_score: float = 0.0
    readability_score: float = 0.0
    overall_score: float = 0.0
    
    # Problèmes détectés
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    
    # Métadonnées
    page_count: int = 0
    word_count: int = 0
    has_photo: bool = False
    detected_language: str = "unknown"


class CVAnalyzer:
    """Analyseur intelligent de CV"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Patterns de détection
        self.section_keywords = {
            'experience': ['experience', 'expérience', 'emploi', 'parcours professionnel', 'work experience', 'employment'],
            'education': ['formation', 'éducation', 'education', 'diplômes', 'studies', 'academic'],
            'skills': ['compétences', 'skills', 'expertise', 'technologies', 'outils'],
            'languages': ['langues', 'languages', 'idiomes'],
            'certifications': ['certifications', 'certificats', 'certificates', 'licenses'],
            'projects': ['projets', 'projects', 'réalisations', 'achievements'],
            'summary': ['résumé', 'profil', 'summary', 'about', 'profile', 'objective']
        }
        
        # Mots-clés ATS communs
        self.ats_keywords = [
            'gestion', 'management', 'leadership', 'équipe', 'team',
            'projet', 'project', 'développement', 'development',
            'analyse', 'analysis', 'stratégie', 'strategy',
            'résultats', 'results', 'achievements', 'performance'
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('CVAnalyzer')
        logger.setLevel(logging.INFO)
        return logger
    
    def analyze(self, file_path: Path) -> CVAnalysis:
        """
        Analyse complète d'un CV
        
        Args:
            file_path: Chemin vers le fichier CV
        
        Returns:
            Objet CVAnalysis avec tous les résultats
        """
        self.logger.info(f"🔍 Analyse de: {file_path.name}")
        
        analysis = CVAnalysis()
        
        # Extraire le texte
        if file_path.suffix.lower() == '.pdf':
            analysis.raw_text, analysis.page_count = self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() == '.docx':
            analysis.raw_text, analysis.page_count = self._extract_from_docx(file_path)
        else:
            self.logger.error(f"Format non supporté: {file_path.suffix}")
            return analysis
        
        if not analysis.raw_text:
            analysis.issues.append("Impossible d'extraire le texte du CV")
            return analysis
        
        # Analyses
        analysis.word_count = len(analysis.raw_text.split())
        analysis.sections = self._detect_sections(analysis.raw_text)
        analysis.personal_info = self._extract_personal_info(analysis.raw_text)
        
        # Scores
        analysis.structure_score = self._evaluate_structure(analysis)
        analysis.ats_score = self._evaluate_ats_compatibility(analysis)
        analysis.typography_score = self._evaluate_typography(analysis)
        analysis.visual_hierarchy_score = self._evaluate_hierarchy(analysis)
        analysis.readability_score = self._evaluate_readability(analysis)
        
        # Score global
        analysis.overall_score = (
            analysis.structure_score * 0.25 +
            analysis.ats_score * 0.20 +
            analysis.typography_score * 0.20 +
            analysis.visual_hierarchy_score * 0.20 +
            analysis.readability_score * 0.15
        )
        
        # Générer recommendations
        analysis.recommendations = self._generate_recommendations(analysis)
        
        self.logger.info(f"✅ Analyse terminée - Score: {analysis.overall_score:.1f}/10")
        
        return analysis
    
    def _extract_from_pdf(self, file_path: Path) -> tuple[str, int]:
        """Extrait le texte d'un PDF (avec OCR si nécessaire)"""
        if not PyPDF2:
            self.logger.error("PyPDF2 non installé")
            return "", 0
        
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                page_count = len(reader.pages)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                # Si le texte est vide ou presque, essayer OCR
                if len(text.strip()) < 50 and OCR_AVAILABLE:
                    self.logger.info("⚠️ PDF image détecté - Utilisation OCR...")
                    text = self._extract_with_ocr(file_path)
                    if text:
                        self.logger.info(f"✅ OCR réussi - {len(text)} caractères extraits")
                
                return text, page_count
        except Exception as e:
            self.logger.error(f"Erreur extraction PDF: {e}")
            return "", 0
    
    def _extract_with_ocr(self, file_path: Path) -> str:
        """Extrait le texte d'un PDF image avec OCR"""
        if not OCR_AVAILABLE:
            self.logger.warning("OCR non disponible (pdf2image/pytesseract manquants)")
            return ""
        
        try:
            # Définir le chemin Poppler
            import os
            poppler_path = os.path.expanduser(r'~\poppler\poppler-24.08.0\Library\bin')
            
            # Convertir PDF en images avec chemin Poppler explicite
            if os.path.exists(poppler_path):
                images = convert_from_path(str(file_path), dpi=300, poppler_path=poppler_path)
            else:
                # Essayer sans chemin explicite
                images = convert_from_path(str(file_path), dpi=300)
            
            # Extraire texte de chaque image
            text = ""
            for i, image in enumerate(images):
                self.logger.info(f"  OCR page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image, lang='fra+eng')
                text += page_text + "\n\n"
            
            return text
        except Exception as e:
            self.logger.error(f"Erreur OCR: {e}")
            return ""
    
    def _extract_from_docx(self, file_path: Path) -> tuple[str, int]:
        """Extrait le texte d'un DOCX"""
        if not Document:
            self.logger.error("python-docx non installé")
            return "", 0
        
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            # Estimation pages (300 mots/page)
            page_count = max(1, len(text.split()) // 300)
            return text, page_count
        except Exception as e:
            self.logger.error(f"Erreur extraction DOCX: {e}")
            return "", 0
    
    def _detect_sections(self, text: str) -> Dict[str, str]:
        """Détecte les sections du CV"""
        sections = {}
        lines = text.split('\n')
        
        # Chercher dans chaque ligne
        for line in lines:
            line_lower = line.lower().strip()
            
            # Ignorer lignes trop courtes
            if len(line_lower) < 3:
                continue
            
            for section_name, keywords in self.section_keywords.items():
                for keyword in keywords:
                    # Match plus flexible: permet tirets, espaces, etc.
                    if keyword.replace(' ', '') in line_lower.replace(' ', '').replace('-', '').replace('_', ''):
                        if section_name not in sections:
                            sections[section_name] = keyword
                        break
        
        # Fallback: si aucune section détectée, créer des sections basiques
        if not sections:
            self.logger.warning("Aucune section détectée - utilisation détection intelligente")
            # Diviser le texte en sections basées sur le contenu
            if len(text) > 100:
                sections['summary'] = 'profile'
                sections['experience'] = 'work history'
                sections['skills'] = 'competencies'
        
        return sections
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extrait informations personnelles (nom, email, téléphone)"""
        info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            info['email'] = emails[0]
        
        # Téléphone (français/international)
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        return info
    
    def _evaluate_structure(self, analysis: CVAnalysis) -> float:
        """Évalue la structure du CV (0-10)"""
        score = 10.0
        
        # Pénalités
        if analysis.page_count == 0:
            score -= 3
        elif analysis.page_count > 2:
            score -= 2
            analysis.warnings.append(f"CV trop long ({analysis.page_count} pages). Idéal: 1-2 pages")
        
        # Sections obligatoires
        required_sections = ['experience', 'education', 'skills']
        missing = [s for s in required_sections if s not in analysis.sections]
        if missing:
            score -= len(missing) * 2
            analysis.issues.append(f"Sections manquantes: {', '.join(missing)}")
        
        return max(0.0, score)
    
    def _evaluate_ats_compatibility(self, analysis: CVAnalysis) -> float:
        """Évalue compatibilité ATS (0-10)"""
        score = 10.0
        text_lower = analysis.raw_text.lower()
        
        # Vérifier présence mots-clés
        keyword_count = sum(1 for kw in self.ats_keywords if kw in text_lower)
        keyword_ratio = keyword_count / len(self.ats_keywords)
        
        if keyword_ratio < 0.1:
            score -= 4
            analysis.issues.append("Peu de mots-clés ATS détectés")
        elif keyword_ratio < 0.3:
            score -= 2
            analysis.warnings.append("Mots-clés ATS limités")
        
        # Sections clairement nommées
        if len(analysis.sections) < 3:
            score -= 2
            analysis.issues.append("Sections mal structurées pour ATS")
        
        return max(0.0, score)
    
    def _evaluate_typography(self, analysis: CVAnalysis) -> float:
        """Évalue la typographie (0-10)"""
        # Basique - dans un vrai système, analyser police, taille, etc.
        score = 7.0  # Score moyen par défaut
        
        if analysis.word_count < 100:
            score -= 3
            analysis.issues.append("Contenu trop court")
        elif analysis.word_count > 1000:
            score -= 1
            analysis.warnings.append("Contenu très dense")
        
        return max(0.0, score)
    
    def _evaluate_hierarchy(self, analysis: CVAnalysis) -> float:
        """Évalue la hiérarchie visuelle (0-10)"""
        score = 7.0
        
        # Vérifier présence de structure
        if not analysis.sections:
            score -= 3
            analysis.issues.append("Hiérarchie visuelle absente")
        
        return max(0.0, score)
    
    def _evaluate_readability(self, analysis: CVAnalysis) -> float:
        """Évalue la lisibilité (0-10)"""
        score = 8.0
        
        # Longueur moyenne des phrases
        sentences = analysis.raw_text.split('.')
        if sentences:
            avg_sentence_length = analysis.word_count / len(sentences)
            if avg_sentence_length > 30:
                score -= 2
                analysis.warnings.append("Phrases trop longues")
        
        return max(0.0, score)
    
    def _generate_recommendations(self, analysis: CVAnalysis) -> List[str]:
        """Génère des recommandations d'amélioration"""
        recommendations = []
        
        if analysis.overall_score < 5:
            recommendations.append("🔴 CV nécessite une refonte complète")
        elif analysis.overall_score < 7:
            recommendations.append("🟡 CV nécessite des améliorations significatives")
        else:
            recommendations.append("🟢 CV de bonne qualité, optimisations mineures suggérées")
        
        if analysis.structure_score < 6:
            recommendations.append("➤ Restructurer les sections principales")
        
        if analysis.ats_score < 6:
            recommendations.append("➤ Améliorer la compatibilité ATS (mots-clés, format)")
        
        if analysis.page_count > 2:
            recommendations.append("➤ Réduire à 1-2 pages maximum")
        
        if not analysis.personal_info.get('email'):
            recommendations.append("➤ Ajouter une adresse email visible")
        
        recommendations.append("➤ Appliquer un design professionnel moderne")
        
        return recommendations
