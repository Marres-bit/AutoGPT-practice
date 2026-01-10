"""
Cloud Database Manager for MediGenius AI
Utilise JSONBin.io comme backend cloud gratuit
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import os
from pathlib import Path


class CloudDatabase:
    """
    Gestionnaire de base de données cloud pour MediGenius AI
    Utilise JSONBin.io pour le stockage cloud gratuit
    """
    
    def __init__(self):
        """Initialise la connexion cloud"""
        self.api_url = "https://api.jsonbin.io/v3/b"
        self.api_key = self._load_api_key()
        self.bin_id = self._load_bin_id()
        self.local_cache = {}
        self.cache_file = Path(__file__).parent.parent / "cloud_cache.json"
        
        # Charger le cache local
        self._load_cache()
        
        print("☁️ Base de données cloud initialisée")
        if self.bin_id:
            print(f"✅ Connecté au bin: {self.bin_id[:10]}...")
        else:
            print("⚠️ Nouveau bin sera créé au premier enregistrement")
    
    def _load_api_key(self) -> str:
        """Charge la clé API depuis .env"""
        env_path = Path(__file__).parent.parent / ".env"
        
        # Vérifier si JSONBIN_API_KEY existe
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('JSONBIN_API_KEY'):
                        return line.split('=')[1].strip().strip('"\'')
        
        # Pas de clé API - utiliser le mode gratuit limité
        print("⚠️ JSONBIN_API_KEY non trouvée - Mode gratuit limité")
        print("💡 Créez un compte sur https://jsonbin.io pour obtenir une clé")
        return ""
    
    def _load_bin_id(self) -> Optional[str]:
        """Charge l'ID du bin depuis la config"""
        config_path = Path(__file__).parent.parent / "cloud_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('bin_id')
        return None
    
    def _save_bin_id(self, bin_id: str):
        """Sauvegarde l'ID du bin"""
        config_path = Path(__file__).parent.parent / "cloud_config.json"
        config = {'bin_id': bin_id, 'created_at': datetime.now().isoformat()}
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _load_cache(self):
        """Charge le cache local"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.local_cache = json.load(f)
            print(f"📦 Cache local chargé: {len(self.local_cache.get('lessons', []))} leçons")
    
    def _save_cache(self):
        """Sauvegarde le cache local"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.local_cache, f, indent=2, ensure_ascii=False)
    
    def _create_bin(self) -> str:
        """Crée un nouveau bin sur JSONBin"""
        headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            headers['X-Master-Key'] = self.api_key
        
        initial_data = {
            'app': 'MediGenius AI',
            'version': '2.0.0',
            'created_at': datetime.now().isoformat(),
            'lessons': [],
            'quizzes': [],
            'disease_searches': [],
            'statistics': {
                'total_lessons': 0,
                'total_quizzes': 0,
                'total_searches': 0
            }
        }
        
        response = requests.post(
            self.api_url,
            json=initial_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            bin_id = data['metadata']['id']
            self._save_bin_id(bin_id)
            print(f"✅ Nouveau bin cloud créé: {bin_id}")
            return bin_id
        else:
            raise Exception(f"❌ Erreur création bin: {response.status_code}")
    
    def sync_to_cloud(self) -> bool:
        """Synchronise le cache local vers le cloud"""
        if not self.bin_id:
            self.bin_id = self._create_bin()
        
        headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            headers['X-Master-Key'] = self.api_key
        
        url = f"{self.api_url}/{self.bin_id}"
        
        try:
            response = requests.put(url, json=self.local_cache, headers=headers)
            if response.status_code == 200:
                print("☁️ Données synchronisées vers le cloud")
                return True
            else:
                print(f"⚠️ Erreur sync cloud: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur connexion cloud: {e}")
            return False
    
    def sync_from_cloud(self) -> bool:
        """Synchronise depuis le cloud vers le cache local"""
        if not self.bin_id:
            print("⚠️ Aucun bin configuré")
            return False
        
        headers = {}
        if self.api_key:
            headers['X-Master-Key'] = self.api_key
        
        url = f"{self.api_url}/{self.bin_id}/latest"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.local_cache = data['record']
                self._save_cache()
                print("☁️ Données téléchargées depuis le cloud")
                return True
            else:
                print(f"⚠️ Erreur téléchargement: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur connexion cloud: {e}")
            return False
    
    def add_lesson(self, title: str, content: str, category: str = "Général",
                   difficulty: str = "Intermédiaire", auto_generated: bool = True) -> int:
        """Ajoute une leçon à la base cloud"""
        lesson = {
            'id': len(self.local_cache.get('lessons', [])) + 1,
            'title': title,
            'content': content,
            'category': category,
            'difficulty': difficulty,
            'auto_generated': auto_generated,
            'created_at': datetime.now().isoformat(),
            'views': 0
        }
        
        if 'lessons' not in self.local_cache:
            self.local_cache['lessons'] = []
        
        self.local_cache['lessons'].append(lesson)
        
        # Mettre à jour les stats
        if 'statistics' not in self.local_cache:
            self.local_cache['statistics'] = {}
        self.local_cache['statistics']['total_lessons'] = len(self.local_cache['lessons'])
        
        # Sauvegarder
        self._save_cache()
        self.sync_to_cloud()
        
        print(f"✅ Leçon ajoutée: {title} (ID: {lesson['id']})")
        return lesson['id']
    
    def get_all_lessons(self) -> List[Dict]:
        """Récupère toutes les leçons"""
        return self.local_cache.get('lessons', [])
    
    def search_lessons(self, query: str) -> List[Dict]:
        """Recherche des leçons"""
        results = []
        query_lower = query.lower()
        
        for lesson in self.local_cache.get('lessons', []):
            if (query_lower in lesson['title'].lower() or 
                query_lower in lesson['content'].lower() or
                query_lower in lesson['category'].lower()):
                results.append(lesson)
        
        return results
    
    def add_quiz(self, topic: str, questions: List[Dict]) -> int:
        """Ajoute un quiz"""
        quiz = {
            'id': len(self.local_cache.get('quizzes', [])) + 1,
            'topic': topic,
            'questions': questions,
            'created_at': datetime.now().isoformat()
        }
        
        if 'quizzes' not in self.local_cache:
            self.local_cache['quizzes'] = []
        
        self.local_cache['quizzes'].append(quiz)
        
        # Stats
        if 'statistics' not in self.local_cache:
            self.local_cache['statistics'] = {}
        self.local_cache['statistics']['total_quizzes'] = len(self.local_cache['quizzes'])
        
        self._save_cache()
        self.sync_to_cloud()
        
        return quiz['id']
    
    def cache_disease_search(self, disease: str, info: Dict):
        """Cache une recherche de maladie"""
        if 'disease_searches' not in self.local_cache:
            self.local_cache['disease_searches'] = []
        
        search = {
            'disease': disease,
            'info': info,
            'searched_at': datetime.now().isoformat()
        }
        
        self.local_cache['disease_searches'].append(search)
        
        # Stats
        if 'statistics' not in self.local_cache:
            self.local_cache['statistics'] = {}
        self.local_cache['statistics']['total_searches'] = len(self.local_cache['disease_searches'])
        
        self._save_cache()
        # Sync asynchrone pour ne pas bloquer
    
    def get_statistics(self) -> Dict:
        """Récupère les statistiques"""
        lessons = self.local_cache.get('lessons', [])
        quizzes = self.local_cache.get('quizzes', [])
        searches = self.local_cache.get('disease_searches', [])
        
        auto_generated = sum(1 for l in lessons if l.get('auto_generated', False))
        manual = len(lessons) - auto_generated
        
        # Top leçons
        sorted_lessons = sorted(lessons, key=lambda x: x.get('views', 0), reverse=True)
        top_lessons = [(l['title'], l.get('views', 0)) for l in sorted_lessons[:5]]
        
        # Top maladies
        disease_counts = {}
        for search in searches:
            disease = search['disease']
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
        top_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_lessons': len(lessons),
            'auto_generated_lessons': auto_generated,
            'manual_lessons': manual,
            'total_quizzes': len(quizzes),
            'total_searches': len(searches),
            'top_lessons': top_lessons,
            'top_diseases': top_diseases
        }
    
    def export_all_lessons(self, filepath: str = "medical_lessons_export.json") -> str:
        """Exporte toutes les leçons"""
        export_data = {
            'app': 'MediGenius AI',
            'exported_at': datetime.now().isoformat(),
            'lessons': self.local_cache.get('lessons', []),
            'quizzes': self.local_cache.get('quizzes', []),
            'statistics': self.get_statistics()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath
