"""
CV Scanner - Surveillance automatique du dossier CV
Détecte et envoie les nouveaux CV pour traitement
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

from .config import CVConfig


class CVScanner:
    """Scanner de CV - Détecte les nouveaux fichiers CV"""
    
    def __init__(self, config: Optional[CVConfig] = None):
        self.config = config or CVConfig()
        self.logger = self._setup_logger()
        self.processed_cache = self._load_cache()
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('CVScanner')
        logger.setLevel(logging.INFO)
        
        # Handler fichier
        log_path = self.config.output_path / 'cv_scanner.log'
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger
    
    def _load_cache(self) -> Dict:
        """Charge le cache des fichiers déjà traités"""
        if self.config.cache_path.exists():
            try:
                with open(self.config.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Impossible de charger le cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Sauvegarde le cache"""
        try:
            with open(self.config.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.processed_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde cache: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calcule le hash MD5 d'un fichier"""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Erreur calcul hash {file_path.name}: {e}")
            return ""
    
    def _is_cv_file(self, file_path: Path) -> bool:
        """Vérifie si le fichier est un CV valide"""
        # Vérifier extension
        if file_path.suffix.lower() not in self.config.supported_formats:
            return False
        
        # Ignorer les fichiers temporaires
        if file_path.name.startswith('~') or file_path.name.startswith('.'):
            return False
        
        # Ignorer fichiers trop petits (< 10 KB)
        try:
            if file_path.stat().st_size < 10240:
                return False
        except:
            return False
        
        return True
    
    def scan_for_new_cvs(self) -> List[Path]:
        """
        Scanne le dossier CV et retourne la liste des nouveaux CV à traiter
        
        Returns:
            Liste des chemins vers les nouveaux CV
        """
        new_cvs = []
        
        if not self.config.input_path.exists():
            self.logger.warning(f"Dossier d'entrée introuvable: {self.config.input_path}")
            return new_cvs
        
        self.logger.info(f"🔍 Scan du dossier: {self.config.input_path}")
        
        # Scanner tous les fichiers
        file_count = 0
        for file_path in self.config.input_path.iterdir():
            if not file_path.is_file():
                continue
            
            file_count += 1
            
            # Vérifier si c'est un CV valide
            if not self._is_cv_file(file_path):
                continue
            
            # Calculer hash
            file_hash = self._get_file_hash(file_path)
            if not file_hash:
                continue
            
            # Vérifier si déjà traité
            file_key = str(file_path.name)
            if file_key in self.processed_cache:
                cached_hash = self.processed_cache[file_key].get('hash', '')
                if cached_hash == file_hash:
                    # Déjà traité, skip
                    continue
                else:
                    self.logger.info(f"📝 CV modifié détecté: {file_path.name}")
            else:
                self.logger.info(f"✨ Nouveau CV détecté: {file_path.name}")
            
            new_cvs.append(file_path)
        
        self.logger.info(f"📊 Scan terminé: {file_count} fichiers scannés, {len(new_cvs)} nouveaux CV")
        
        return new_cvs
    
    def mark_as_processed(self, file_path: Path, success: bool = True, error: str = ""):
        """
        Marque un CV comme traité dans le cache
        
        Args:
            file_path: Chemin du fichier
            success: True si traitement réussi
            error: Message d'erreur si échec
        """
        file_hash = self._get_file_hash(file_path)
        file_key = str(file_path.name)
        
        self.processed_cache[file_key] = {
            'hash': file_hash,
            'processed_at': datetime.now().isoformat(),
            'success': success,
            'error': error,
            'file_size': file_path.stat().st_size,
            'file_extension': file_path.suffix
        }
        
        self._save_cache()
        
        if success:
            self.logger.info(f"✅ {file_path.name} marqué comme traité")
        else:
            self.logger.error(f"❌ {file_path.name} échec: {error}")
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur les CV traités"""
        total = len(self.processed_cache)
        successful = sum(1 for v in self.processed_cache.values() if v.get('success', False))
        failed = total - successful
        
        return {
            'total_processed': total,
            'successful': successful,
            'failed': failed,
            'cache_file': str(self.config.cache_path)
        }
