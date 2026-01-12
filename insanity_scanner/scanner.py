"""
Scanner principal du module GEIS
Orchestre la collecte, le scoring et la génération de rapports
"""
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json

from .config import GEISConfig, DEFAULT_CONFIG
from .sources import RedditSource, YouTubeSource, TwitterSource, FaitsDiversSource
from .scorer import InsanityScorer
from .report_generator import ReportGenerator


class InsanityScanner:
    """Scanner principal de contenus insolites extrêmes"""
    
    def __init__(self, config: GEISConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.scorer = InsanityScorer(self.config)
        self.report_gen = ReportGenerator(self.config)
        
        # Initialiser sources
        self.sources = {}
        if "reddit" in self.config.enabled_sources:
            self.sources["reddit"] = RedditSource(self.config)
        if "youtube" in self.config.enabled_sources:
            self.sources["youtube"] = YouTubeSource(self.config)
        if "twitter" in self.config.enabled_sources:
            self.sources["twitter"] = TwitterSource(self.config)
        if "faits_divers" in self.config.enabled_sources:
            self.sources["faits_divers"] = FaitsDiversSource(self.config)
        
        # Logging
        self._setup_logging()
        
        # Cache des contenus déjà traités
        self.cache_file = self.config.output_dir / "processed_cache.json"
        self.processed_ids = self._load_cache()
    
    def _setup_logging(self):
        """Configuration du logging séparé"""
        logging.basicConfig(
            filename=self.config.log_file,
            level=logging.INFO,
            format='%(asctime)s [GEIS] %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger("GEIS")
    
    def _load_cache(self) -> set:
        """Charge le cache des contenus déjà traités"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except Exception as e:
                self.logger.warning(f"Erreur chargement cache: {e}")
        return set()
    
    def _save_cache(self):
        """Sauvegarde le cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_update': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde cache: {e}")
    
    def scan(self) -> Dict[str, any]:
        """
        Lance un scan complet
        
        Returns:
            Statistiques du scan
        """
        self.logger.info("🔥 Démarrage scan GEIS")
        start_time = datetime.now()
        
        stats = {
            'start_time': start_time.isoformat(),
            'sources_scanned': 0,
            'raw_items_found': 0,
            'filtered_items': 0,
            'reports_generated': 0,
            'errors': []
        }
        
        all_items = []
        
        # 1. Collecte depuis toutes les sources
        for source_name, source in self.sources.items():
            try:
                self.logger.info(f"📡 Scan source: {source_name}")
                items = source.fetch()
                self.logger.info(f"✅ {source_name}: {len(items)} items trouvés")
                all_items.extend(items)
                stats['sources_scanned'] += 1
                stats['raw_items_found'] += len(items)
            except Exception as e:
                error_msg = f"Erreur scan {source_name}: {e}"
                self.logger.error(error_msg)
                stats['errors'].append(error_msg)
        
        # 2. Scoring et filtrage
        scored_items = []
        for item in all_items:
            # Vérifier cache (éviter doublons)
            item_id = item.get('id') or item.get('url')
            if item_id in self.processed_ids:
                continue
            
            # Calculer score
            score = self.scorer.calculate_score(item)
            item['insanity_score'] = score
            
            # Filtrer par score minimal
            if score >= self.config.min_insanity_score:
                scored_items.append(item)
        
        # Trier par score décroissant
        scored_items.sort(key=lambda x: x['insanity_score'], reverse=True)
        
        # Limiter au nombre max
        scored_items = scored_items[:self.config.max_results_per_scan]
        stats['filtered_items'] = len(scored_items)
        
        self.logger.info(f"🎯 {len(scored_items)} items retenus (score >= {self.config.min_insanity_score})")
        
        # 3. Génération des rapports
        for idx, item in enumerate(scored_items, 1):
            try:
                report_path = self.report_gen.generate(item, insanity_number=idx)
                self.logger.info(f"📄 Rapport généré: {report_path}")
                stats['reports_generated'] += 1
                
                # Ajouter au cache
                item_id = item.get('id') or item.get('url')
                if item_id:
                    self.processed_ids.add(item_id)
            except Exception as e:
                error_msg = f"Erreur génération rapport {idx}: {e}"
                self.logger.error(error_msg)
                stats['errors'].append(error_msg)
        
        # Sauvegarder cache
        self._save_cache()
        
        # Stats finales
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        stats['end_time'] = end_time.isoformat()
        stats['duration_seconds'] = duration
        
        self.logger.info(f"✅ Scan terminé: {stats['reports_generated']} rapports en {duration:.1f}s")
        
        return stats
    
    def get_next_insanity_number(self) -> int:
        """Récupère le prochain numéro d'insolite disponible"""
        existing = list(self.config.output_dir.glob("Insanity_*"))
        if not existing:
            return 1
        
        numbers = []
        for folder in existing:
            try:
                num = int(folder.name.split('_')[1])
                numbers.append(num)
            except (IndexError, ValueError):
                continue
        
        return max(numbers, default=0) + 1
