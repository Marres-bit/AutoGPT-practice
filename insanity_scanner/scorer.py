"""
Algorithme de scoring d'insolite
Calcule un score 1-10 basé sur plusieurs critères
"""
import logging
from typing import Dict
import re
from datetime import datetime

from .config import GEISConfig


class InsanityScorer:
    """Calculateur de score d'insolite"""
    
    def __init__(self, config: GEISConfig):
        self.config = config
        self.logger = logging.getLogger("GEIS.Scorer")
    
    def calculate_score(self, item: Dict) -> float:
        """
        Calcule le score d'insolite (1.0 à 10.0)
        
        Critères:
        - Engagement (likes, comments, shares)
        - Mots-clés choc dans titre/description
        - Viralité (ratio engagement/temps)
        - Source (certaines sources plus fiables)
        - Fraîcheur (contenu récent privilégié)
        """
        score = 0.0
        
        # 1. Engagement (0-3 points)
        engagement_score = self._score_engagement(item)
        score += engagement_score
        
        # 2. Mots-clés choc (0-3 points)
        keyword_score = self._score_keywords(item)
        score += keyword_score
        
        # 3. Viralité (0-2 points)
        viral_score = self._score_virality(item)
        score += viral_score
        
        # 4. Qualité source (0-1 point)
        source_score = self._score_source(item)
        score += source_score
        
        # 5. Fraîcheur (0-1 point)
        freshness_score = self._score_freshness(item)
        score += freshness_score
        
        # Normaliser sur 10
        final_score = min(10.0, max(1.0, score))
        
        self.logger.debug(
            f"Score {final_score:.1f} pour '{item.get('title', 'N/A')[:50]}' "
            f"(eng:{engagement_score:.1f} kw:{keyword_score:.1f} viral:{viral_score:.1f})"
        )
        
        return round(final_score, 1)
    
    def _score_engagement(self, item: Dict) -> float:
        """Score basé sur l'engagement (likes, comments, shares)"""
        source = item.get('source', '')
        
        if source == 'reddit':
            score = item.get('score', 0)
            comments = item.get('num_comments', 0)
            ratio = item.get('upvote_ratio', 0.5)
            
            # Score basé sur upvotes + comments
            engagement = score + (comments * 2)
            
            # Bonus si ratio élevé (controversé)
            if ratio > 0.9:
                engagement *= 1.2
            
            # Normaliser sur 3
            if engagement > 10000:
                return 3.0
            elif engagement > 5000:
                return 2.5
            elif engagement > 1000:
                return 2.0
            elif engagement > 500:
                return 1.5
            elif engagement > 100:
                return 1.0
            else:
                return 0.5
        
        elif source == 'twitter':
            likes = item.get('likes', 0)
            retweets = item.get('retweets', 0)
            replies = item.get('replies', 0)
            
            engagement = likes + (retweets * 3) + (replies * 2)
            
            if engagement > 50000:
                return 3.0
            elif engagement > 10000:
                return 2.5
            elif engagement > 5000:
                return 2.0
            elif engagement > 1000:
                return 1.5
            else:
                return 1.0
        
        return 1.0
    
    def _score_keywords(self, item: Dict) -> float:
        """Score basé sur les mots-clés choc"""
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        
        # Compter occurrences de mots-clés
        keyword_count = 0
        for keyword in self.config.shock_keywords:
            if keyword.lower() in text:
                keyword_count += 1
        
        # Score progressif
        if keyword_count >= 5:
            return 3.0
        elif keyword_count >= 3:
            return 2.5
        elif keyword_count >= 2:
            return 2.0
        elif keyword_count >= 1:
            return 1.5
        else:
            # Patterns alternatifs
            if re.search(r'(!!!|⚠️|🔥|😱|WTF|OMG)', text, re.IGNORECASE):
                return 1.0
            return 0.5
    
    def _score_virality(self, item: Dict) -> float:
        """Score basé sur la vitesse de propagation"""
        source = item.get('source', '')
        
        # Calculer âge du contenu
        try:
            if source == 'reddit':
                created_utc = item.get('created_utc', 0)
                age_hours = (datetime.now().timestamp() - created_utc) / 3600
            elif source == 'youtube':
                published = datetime.fromisoformat(item.get('published_at', '').replace('Z', '+00:00'))
                age_hours = (datetime.now() - published.replace(tzinfo=None)).total_seconds() / 3600
            else:
                age_hours = 24  # Par défaut
            
            # Ratio engagement/temps
            if source == 'reddit':
                engagement = item.get('score', 0)
                viral_rate = engagement / max(age_hours, 1)
                
                if viral_rate > 1000:
                    return 2.0
                elif viral_rate > 500:
                    return 1.5
                elif viral_rate > 100:
                    return 1.0
                else:
                    return 0.5
        except Exception as e:
            self.logger.debug(f"Erreur calcul viralité: {e}")
        
        return 1.0
    
    def _score_source(self, item: Dict) -> float:
        """Score basé sur la qualité de la source"""
        source = item.get('source', '')
        
        # Certaines sources plus fiables
        source_scores = {
            'reddit': 1.0,
            'youtube': 0.8,
            'twitter': 0.7,
            'faits_divers': 0.9
        }
        
        return source_scores.get(source, 0.5)
    
    def _score_freshness(self, item: Dict) -> float:
        """Score basé sur la fraîcheur du contenu"""
        source = item.get('source', '')
        
        try:
            if source == 'reddit':
                created_utc = item.get('created_utc', 0)
                age_days = (datetime.now().timestamp() - created_utc) / 86400
            else:
                age_days = 7  # Par défaut
            
            # Plus récent = meilleur score
            if age_days < 1:
                return 1.0
            elif age_days < 3:
                return 0.8
            elif age_days < 7:
                return 0.6
            elif age_days < 14:
                return 0.4
            else:
                return 0.2
        except Exception:
            return 0.5
    
    def get_viral_potential(self, score: float) -> str:
        """Détermine le potentiel viral basé sur le score"""
        if score >= 8.5:
            return "explosif"
        elif score >= 7.0:
            return "fort"
        elif score >= 5.5:
            return "moyen"
        else:
            return "faible"
