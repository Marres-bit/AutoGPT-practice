"""
Générateur de rapports Word structurés
Crée un document .docx avec images numérotées et liens vidéos
"""
import logging
from pathlib import Path
from typing import Dict, List
import requests
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from .config import GEISConfig
from .scorer import InsanityScorer


class ReportGenerator:
    """Générateur de rapports Word pour chaque insolite"""
    
    def __init__(self, config: GEISConfig):
        self.config = config
        self.scorer = InsanityScorer(config)
        self.logger = logging.getLogger("GEIS.ReportGenerator")
    
    def generate(self, item: Dict, insanity_number: int) -> Path:
        """
        Génère un dossier complet pour un insolite
        
        Args:
            item: Données de l'insolite
            insanity_number: Numéro séquentiel
        
        Returns:
            Chemin du document Word généré
        """
        # Créer dossier dédié
        folder_name = f"Insanity_{insanity_number:03d}"
        folder_path = self.config.output_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        
        # Télécharger images
        image_paths = self._download_images(item, folder_path)
        
        # Créer document Word
        doc_path = folder_path / f"{folder_name}.docx"
        self._create_document(item, image_paths, doc_path, insanity_number)
        
        return doc_path
    
    def _download_images(self, item: Dict, folder: Path) -> List[Path]:
        """Télécharge toutes les images associées"""
        image_paths = []
        
        # Liste des URLs d'images possibles
        image_urls = []
        
        # Reddit
        if item.get('source') == 'reddit' and item.get('media_url'):
            image_urls.append(item['media_url'])
        
        # YouTube thumbnail
        if item.get('source') == 'youtube' and item.get('thumbnail_url'):
            image_urls.append(item['thumbnail_url'])
        
        # Twitter media (si disponible)
        # À implémenter selon structure API
        
        # Télécharger chaque image
        for idx, url in enumerate(image_urls, 1):
            try:
                # Déterminer extension
                ext = url.split('.')[-1].split('?')[0]
                if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                    ext = 'jpg'
                
                # Nom de fichier numéroté
                filename = f"Image_{idx:03d}.{ext}"
                filepath = folder / filename
                
                # Télécharger
                response = requests.get(url, timeout=10, headers=self._get_headers())
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    image_paths.append(filepath)
                    self.logger.info(f"✅ Image téléchargée: {filename}")
            except Exception as e:
                self.logger.error(f"❌ Erreur téléchargement image {url}: {e}")
        
        return image_paths
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers HTTP pour téléchargement"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _create_document(self, item: Dict, image_paths: List[Path], doc_path: Path, number: int):
        """Crée le document Word structuré"""
        doc = Document()
        
        # Style du document
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
        
        # === EN-TÊTE ===
        header = doc.add_heading(f"INSANITY #{number:03d}", level=0)
        header.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header.runs[0].font.color.rgb = RGBColor(255, 0, 0)
        
        doc.add_paragraph()
        
        # === TITRE CHOC ===
        title = item.get('title', 'Titre non disponible')
        title_para = doc.add_heading(title, level=1)
        title_para.runs[0].font.color.rgb = RGBColor(0, 0, 0)
        
        doc.add_paragraph()
        
        # === DESCRIPTION ===
        doc.add_heading('📋 Description', level=2)
        description = item.get('description', 'Description non disponible')
        if description:
            doc.add_paragraph(description)
        
        doc.add_paragraph()
        
        # === POURQUOI C'EST EXCEPTIONNEL ===
        doc.add_heading('🔥 Pourquoi c\'est exceptionnel ?', level=2)
        exceptional_reasons = self._generate_exceptional_reasons(item)
        for reason in exceptional_reasons:
            doc.add_paragraph(f"• {reason}", style='List Bullet')
        
        doc.add_paragraph()
        
        # === IMAGES ===
        if image_paths:
            doc.add_heading(f'🖼️ Images ({len(image_paths)})', level=2)
            for idx, img_path in enumerate(image_paths, 1):
                doc.add_paragraph(f"Image_{idx:03d}:", style='List Bullet')
                try:
                    # Insérer image (largeur max 6 pouces)
                    doc.add_picture(str(img_path), width=Inches(6))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                except Exception as e:
                    self.logger.error(f"Erreur insertion image {img_path}: {e}")
                    doc.add_paragraph(f"[Erreur chargement image {img_path.name}]")
            doc.add_paragraph()
        
        # === VIDÉOS ===
        video_url = item.get('url')
        if video_url:
            doc.add_heading('🎥 Liens Vidéos', level=2)
            doc.add_paragraph(f"Vidéo 001: {video_url}", style='List Bullet')
            doc.add_paragraph()
        
        # === MÉTADONNÉES ===
        doc.add_heading('📊 Informations', level=2)
        
        # Source
        source = item.get('source', 'N/A').upper()
        doc.add_paragraph(f"Source: {source}")
        
        # Pays/Origine
        origin = self._extract_origin(item)
        doc.add_paragraph(f"Origine: {origin}")
        
        # Date
        date_str = self._format_date(item)
        doc.add_paragraph(f"Date: {date_str}")
        
        # Score de choc
        score = item.get('insanity_score', 5.0)
        doc.add_paragraph(f"Score de choc: {score}/10 {'🔥' * int(score/2)}")
        
        # Potentiel viral
        viral_potential = self.scorer.get_viral_potential(score)
        doc.add_paragraph(f"Potentiel viral: {viral_potential.upper()}")
        
        doc.add_paragraph()
        
        # === SOURCES ORIGINALES ===
        doc.add_heading('🔗 Sources', level=2)
        doc.add_paragraph(f"Lien principal: {video_url or 'N/A'}")
        if item.get('source') == 'reddit':
            subreddit = item.get('subreddit', 'N/A')
            doc.add_paragraph(f"Subreddit: r/{subreddit}")
        
        # Sauvegarder
        doc.save(str(doc_path))
        self.logger.info(f"📄 Document Word créé: {doc_path}")
    
    def _generate_exceptional_reasons(self, item: Dict) -> List[str]:
        """Génère les raisons pour lesquelles c'est exceptionnel"""
        reasons = []
        
        score = item.get('insanity_score', 5.0)
        source = item.get('source', '')
        
        # Engagement élevé
        if source == 'reddit':
            upvotes = item.get('score', 0)
            if upvotes > 10000:
                reasons.append(f"Engagement massif: {upvotes:,} upvotes sur Reddit")
            comments = item.get('num_comments', 0)
            if comments > 1000:
                reasons.append(f"Discussion intense: {comments:,} commentaires")
        
        # Viralité
        if score >= 8.0:
            reasons.append("Contenu à très fort potentiel viral")
        
        # Mots-clés
        title = item.get('title', '').lower()
        if any(kw in title for kw in ['shocking', 'unbelievable', 'insane', 'wtf']):
            reasons.append("Titre accrocheur avec mots-clés choc")
        
        # Fraîcheur
        if source == 'reddit':
            created_utc = item.get('created_utc', 0)
            age_hours = (datetime.now().timestamp() - created_utc) / 3600
            if age_hours < 24:
                reasons.append("Contenu très récent (moins de 24h)")
        
        # Par défaut
        if not reasons:
            reasons.append("Contenu insolite et inhabituel")
            reasons.append("Réaction émotionnelle forte probable")
        
        return reasons
    
    def _extract_origin(self, item: Dict) -> str:
        """Extrait l'origine géographique si possible"""
        # Tentative d'extraction depuis titre/description
        title = item.get('title', '')
        description = item.get('description', '')
        
        # Patterns de pays communs
        countries = [
            'USA', 'UK', 'France', 'Germany', 'China', 'Japan', 'India',
            'Russia', 'Brazil', 'Australia', 'Canada', 'Mexico', 'Spain'
        ]
        
        text = f"{title} {description}"
        for country in countries:
            if country.lower() in text.lower():
                return country
        
        # Par défaut
        return "Monde"
    
    def _format_date(self, item: Dict) -> str:
        """Formate la date du contenu"""
        source = item.get('source', '')
        
        try:
            if source == 'reddit':
                created_utc = item.get('created_utc', 0)
                dt = datetime.fromtimestamp(created_utc)
                return dt.strftime('%d/%m/%Y %H:%M')
            elif source == 'youtube':
                published = item.get('published_at', '')
                dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                return dt.strftime('%d/%m/%Y')
        except Exception:
            pass
        
        return datetime.now().strftime('%d/%m/%Y')
