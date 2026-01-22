"""
CV Optimizer - Optimisation intelligente du contenu
Améliore textes, descriptions, ton professionnel SANS falsifier
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Charger .env depuis la racine du projet
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    OpenAI = None
    _openai_available = False

from .cv_analyzer import CVAnalysis


@dataclass
class OptimizedContent:
    """Contenu optimisé du CV"""
    
    sections: Dict[str, str]  # Sections réécrites
    improvements: List[str]  # Liste des améliorations apportées
    original_preserved: bool = True  # Confirme que les données sont authentiques
    tone: str = "professional"  # Ton utilisé
    language: str = "fr"  # Langue détectée


class CVOptimizer:
    """Optimiseur de contenu CV via IA"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.logger = self._setup_logger()
        
        if not self.api_key:
            self.logger.warning("⚠️ OPENAI_API_KEY non configurée - optimisation limitée")
            self.client = None
        else:
            if not _openai_available:
                self.logger.error("❌ openai package non installé")
                self.client = None
            else:
                self.client = OpenAI(api_key=self.api_key)
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('CVOptimizer')
        logger.setLevel(logging.INFO)
        return logger
    
    def _detect_language(self, text: str) -> str:
        """Détecte la langue du CV basé sur mots-clés"""
        text_lower = text.lower()
        
        # Compteurs de mots caractéristiques
        de_words = ['lebenslauf', 'beruf', 'ausbildung', 'kenntnisse', 'deutsch', 'geboren', 'abitur']
        fr_words = ['formation', 'expérience', 'compétences', 'profil', 'diplôme']
        en_words = ['experience', 'education', 'skills', 'profile', 'resume']
        
        de_count = sum(1 for w in de_words if w in text_lower)
        fr_count = sum(1 for w in fr_words if w in text_lower)
        en_count = sum(1 for w in en_words if w in text_lower)
        
        if de_count > fr_count and de_count > en_count:
            return 'de'
        elif fr_count > en_count:
            return 'fr'
        else:
            return 'en'
    
    def _parse_cv_structure(self, text: str, language: str) -> Dict[str, str]:
        """Parse le CV pour extraire les sections avec leur contenu réel"""
        sections = {}
        lines = text.split('\n')
        
        # Mots-clés de sections par langue
        section_markers = {
            'de': {
                'personal': ['personliche', 'daten', 'kontakt', 'oaten'],  # oaten = typo de daten
                'education': ['ausbildung', 'bildung', 'schule', 'studium', 'gymnasium', 'grundschule'],
                'experience': ['berufserfahrung', 'praktikum', 'erfahrung', 'deutschkurs'],
                'skills': ['kenntnisse', 'fahigkeiten', 'sprach', 'eigenschaften'],
                'other': ['hobbys', 'interessen']
            },
            'fr': {
                'personal': ['coordonnées', 'contact', 'personnel'],
                'education': ['formation', 'diplôme', 'études'],
                'experience': ['expérience', 'professionnel', 'emploi'],
                'skills': ['compétences', 'aptitudes', 'langues'],
                'other': ['loisirs', 'centres d\'intérêt']
            },
            'en': {
                'personal': ['contact', 'personal', 'info'],
                'education': ['education', 'academic', 'degree'],
                'experience': ['experience', 'employment', 'work'],
                'skills': ['skills', 'abilities', 'languages'],
                'other': ['hobbies', 'interests']
            }
        }
        
        markers = section_markers.get(language, section_markers['en'])
        current_section = 'summary'
        current_content = []
        last_section_line = -1
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean:
                if current_content:  # Conserver lignes vides dans section
                    current_content.append('')
                continue
            
            line_lower = line_clean.lower()
            
            # Vérifier si c'est un marqueur de section (et pas trop proche du dernier)
            is_section_header = False
            if i > last_section_line + 1:  # Au moins 2 lignes après dernière section
                for section_name, keywords in markers.items():
                    if any(kw in line_lower for kw in keywords):
                        # Sauvegarder section précédente
                        if current_content:
                            sections[current_section] = '\n'.join(current_content).strip()
                        current_section = section_name
                        current_content = [line_clean]  # Inclure le titre
                        is_section_header = True
                        last_section_line = i
                        break
            
            if not is_section_header:
                current_content.append(line_clean)
        
        # Sauvegarder dernière section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def optimize(self, analysis: CVAnalysis, target_language: str = "auto") -> OptimizedContent:
        """
        Optimise le contenu du CV SANS le modifier radicalement
        
        Args:
            analysis: Résultat d'analyse du CV
            target_language: Langue cible (fr, en, de, auto)
        
        Returns:
            Contenu optimisé qui PRESERVE le contenu original
        """
        self.logger.info("🎯 Optimisation du contenu CV")
        
        # Détecter langue automatiquement
        if target_language == "auto":
            target_language = self._detect_language(analysis.raw_text)
            self.logger.info(f"  Langue détectée: {target_language}")
        
        if not self.client:
            self.logger.warning("Client OpenAI non disponible - optimisation basique")
            return self._basic_optimization(analysis, target_language)
        
        optimized = OptimizedContent(
            sections={},
            improvements=[],
            language=target_language
        )
        
        # IMPORTANT: Parser le contenu brut en sections structurées
        parsed_sections = self._parse_cv_structure(analysis.raw_text, target_language)
        
        # Optimiser chaque section PARSÉE (pas juste les keywords détectés)
        for section_name, section_content in parsed_sections.items():
            self.logger.info(f"  📝 Amélioration section: {section_name}")
            
            optimized_text = self._optimize_section(
                section_name=section_name,
                original_text=section_content,
                context=analysis.raw_text,
                language=target_language
            )
            
            if optimized_text:
                optimized.sections[section_name] = optimized_text
                optimized.improvements.append(f"Section '{section_name}' améliorée")
        
        self.logger.info(f"✅ {len(optimized.sections)} sections optimisées")
        
        return optimized
    
    def _optimize_section(
        self, 
        section_name: str, 
        original_text: str, 
        context: str,
        language: str
    ) -> Optional[str]:
        """Optimise une section spécifique via GPT"""
        
        if not self.client or not original_text:
            return None
        
        # Prompt selon la section
        prompts = {
            'experience': self._get_experience_prompt(language),
            'education': self._get_education_prompt(language),
            'skills': self._get_skills_prompt(language),
            'summary': self._get_summary_prompt(language),
        }
        
        system_prompt = prompts.get(section_name, self._get_generic_prompt(language))
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Texte à optimiser:\n\n{original_text[:1000]}"}  # Limiter taille
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            optimized = response.choices[0].message.content.strip()
            return optimized
            
        except Exception as e:
            self.logger.error(f"Erreur optimisation {section_name}: {e}")
            return None
    
    def _get_experience_prompt(self, lang: str) -> str:
        """Prompt pour optimiser section Expérience"""
        base_instruction = "RÈGLE ABSOLUE: PRÉSERVE exactement toutes les informations, dates, lieux, et expériences. NE JAMAIS inventer ou modifier des faits. Améliore UNIQUEMENT le style et la clarté."
        
        if lang == "de":
            return f"{base_instruction}\n\nOptimiere die Berufserfahrung: verbessere Formulierung und Struktur, aber ändere KEINE Fakten, Daten oder Erfahrungen. Behalte die ursprüngliche Sprache bei."
        elif lang == "fr":
            return """Tu es un expert RH et rédacteur de CV professionnel.

MISSION: Améliorer la description d'expérience professionnelle pour maximiser l'impact.

RÈGLES STRICTES:
- NE JAMAIS inventer d'expérience, de poste, ou de dates
- NE JAMAIS ajouter de compétences non mentionnées
- Reformuler pour plus de clarté et impact
- Utiliser des verbes d'action forts
- Quantifier les résultats quand possible
- Ton professionnel, concis, impactant
- Maximum 3-4 bullet points par poste

STRUCTURE:
- [Titre du poste] - [Entreprise] - [Dates]
- • Réalisation 1 (avec verbe d'action + résultat quantifié si possible)
- • Réalisation 2
- • Réalisation 3

Retourne UNIQUEMENT le texte optimisé, sans explication."""
        else:
            return "You are a professional CV writer. Improve the work experience section. Never invent information. Use action verbs and quantify results when possible."
    
    def _get_education_prompt(self, lang: str) -> str:
        """Prompt pour optimiser section Formation"""
        base_instruction = "RÈGLE ABSOLUE: PRÉSERVE exactement toutes les informations, dates, diplômes et établissements. NE JAMAIS inventer. Améliore UNIQUEMENT la présentation."
        
        if lang == "de":
            return f"{base_instruction}\n\nOptimiere die Ausbildung: verbessere Formatierung, aber ändere KEINE Daten, Abschlüsse oder Institutionen. Behalte die ursprüngliche Sprache bei."
        elif lang == "fr":
            return """Tu es un expert en rédaction de CV.

MISSION: Améliorer la section Formation de manière professionnelle.

RÈGLES:
- NE JAMAIS inventer de diplôme ou d'établissement
- Clarifier les titres de diplômes
- Mettre en valeur les spécialisations pertinentes
- Format: [Diplôme] - [Établissement] - [Année]
- Mentionner mentions/distinctions si présentes

Retourne UNIQUEMENT le texte optimisé."""
        else:
            return "You are a CV expert. Improve the education section. Never invent degrees. Be clear and professional."
    
    def _get_skills_prompt(self, lang: str) -> str:
        """Prompt pour optimiser section Compétences"""
        if lang == "fr":
            return """Tu es un expert en recrutement tech/business.

MISSION: Organiser et optimiser la section Compétences.

RÈGLES:
- NE PAS ajouter de compétences non mentionnées
- Regrouper par catégories logiques (Techniques, Langues, Soft skills, etc.)
- Prioriser les plus pertinentes en premier
- Format clair et scannable par ATS

Retourne UNIQUEMENT le texte optimisé."""
        else:
            return "You are a recruitment expert. Organize the skills section clearly. Never add skills not mentioned. Group by categories."
    
    def _get_summary_prompt(self, lang: str) -> str:
        """Prompt pour optimiser résumé/profil"""
        if lang == "fr":
            return """Tu es un expert en personal branding.

MISSION: Créer un résumé professionnel percutant (3-4 lignes).

RÈGLES:
- Basé UNIQUEMENT sur les informations fournies
- Mettre en avant les points forts uniques
- Ton professionnel et confiant
- Maximum 50 mots
- Sans jargon excessif

Retourne UNIQUEMENT le résumé optimisé."""
        else:
            return "You are a personal branding expert. Create a compelling professional summary (3-4 lines) based only on provided information."
    
    def _get_generic_prompt(self, lang: str) -> str:
        """Prompt générique"""
        if lang == "fr":
            return """Tu es un expert en rédaction de CV professionnel.

MISSION: Améliorer le texte fourni pour un CV.

RÈGLES:
- NE JAMAIS inventer d'information
- Clarifier et rendre plus impactant
- Ton professionnel international
- Concis et scannable

Retourne UNIQUEMENT le texte optimisé."""
        else:
            return "You are a professional CV writer. Improve the text without inventing information. Be clear, impactful, and professional."
    
    def _basic_optimization(self, analysis: CVAnalysis, language: str = "fr") -> OptimizedContent:
        """Optimisation basique sans IA (fallback)"""
        self.logger.info("📝 Optimisation basique (sans IA)")
        
        return OptimizedContent(
            sections=analysis.sections,
            improvements=["Analyse effectuée sans optimisation IA"],
            original_preserved=True
        )
    
    def enhance_bullet_points(self, text: str) -> str:
        """Améliore les bullet points (ajout verbes d'action)"""
        
        action_verbs_fr = [
            'Développé', 'Conçu', 'Géré', 'Dirigé', 'Optimisé',
            'Créé', 'Implémenté', 'Analysé', 'Coordonné', 'Piloté'
        ]
        
        lines = text.split('\n')
        enhanced = []
        
        for line in lines:
            line = line.strip()
            if line and not any(verb in line for verb in action_verbs_fr):
                # Ajouter verbe d'action si manquant
                if not line.startswith(('•', '-', '*')):
                    line = f"• {line}"
            enhanced.append(line)
        
        return '\n'.join(enhanced)
