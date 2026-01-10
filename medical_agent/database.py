"""
Medical AI Agent - Database Manager
Gère le stockage des leçons, quiz, et statistiques
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import threading


class MedicalDatabase:
    """Gestionnaire de base de données pour les leçons médicales"""
    
    def __init__(self, db_path: str = "medical_lessons.db"):
        self.db_path = Path(db_path)
        self.lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données avec toutes les tables"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table des leçons
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    duration TEXT DEFAULT '30 min',
                    content TEXT NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    auto_generated BOOLEAN DEFAULT 0,
                    views INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0.0
                )
            """)
            
            # Table des quiz
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_id INTEGER,
                    topic TEXT NOT NULL,
                    questions TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    attempts INTEGER DEFAULT 0,
                    avg_score REAL DEFAULT 0.0,
                    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
                )
            """)
            
            # Table des recherches de maladies
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS disease_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease_name TEXT NOT NULL,
                    search_count INTEGER DEFAULT 1,
                    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cached_result TEXT
                )
            """)
            
            # Table des statistiques
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    lessons_generated INTEGER DEFAULT 0,
                    quizzes_taken INTEGER DEFAULT 0,
                    searches_performed INTEGER DEFAULT 0,
                    total_time_spent INTEGER DEFAULT 0
                )
            """)
            
            # Table des sessions utilisateur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_end TIMESTAMP,
                    commands_used TEXT,
                    lessons_viewed TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            print("✅ Base de données médicale initialisée")
    
    def add_lesson(self, title: str, category: str, difficulty: str, 
                   content: dict, auto_generated: bool = False) -> int:
        """Ajoute une nouvelle leçon"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO lessons (title, category, difficulty, content, auto_generated)
                VALUES (?, ?, ?, ?, ?)
            """, (title, category, difficulty, json.dumps(content), int(auto_generated)))
            
            lesson_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Leçon ajoutée: {title} (ID: {lesson_id})")
            return lesson_id
    
    def get_all_lessons(self, limit: int = 100) -> List[Dict]:
        """Récupère toutes les leçons"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM lessons 
            ORDER BY generated_at DESC 
            LIMIT ?
        """, (limit,))
        
        lessons = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Parse JSON content
        for lesson in lessons:
            lesson['content'] = json.loads(lesson['content'])
        
        return lessons
    
    def get_lesson_by_id(self, lesson_id: int) -> Optional[Dict]:
        """Récupère une leçon par son ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            lesson = dict(row)
            lesson['content'] = json.loads(lesson['content'])
            return lesson
        return None
    
    def search_lessons(self, query: str, category: str = None) -> List[Dict]:
        """Recherche des leçons par titre ou catégorie"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM lessons 
                WHERE (title LIKE ? OR content LIKE ?) AND category = ?
                ORDER BY generated_at DESC
            """, (f"%{query}%", f"%{query}%", category))
        else:
            cursor.execute("""
                SELECT * FROM lessons 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY generated_at DESC
            """, (f"%{query}%", f"%{query}%"))
        
        lessons = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for lesson in lessons:
            lesson['content'] = json.loads(lesson['content'])
        
        return lessons
    
    def add_quiz(self, topic: str, questions: dict, lesson_id: int = None) -> int:
        """Ajoute un nouveau quiz"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO quizzes (lesson_id, topic, questions)
                VALUES (?, ?, ?)
            """, (lesson_id, topic, json.dumps(questions)))
            
            quiz_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return quiz_id
    
    def cache_disease_search(self, disease_name: str, result: str):
        """Cache le résultat d'une recherche de maladie"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si déjà en cache
            cursor.execute("""
                SELECT id FROM disease_searches WHERE disease_name = ?
            """, (disease_name,))
            
            row = cursor.fetchone()
            
            if row:
                # Update existing
                cursor.execute("""
                    UPDATE disease_searches 
                    SET search_count = search_count + 1,
                        last_searched = CURRENT_TIMESTAMP,
                        cached_result = ?
                    WHERE disease_name = ?
                """, (result, disease_name))
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO disease_searches (disease_name, cached_result)
                    VALUES (?, ?)
                """, (disease_name, result))
            
            conn.commit()
            conn.close()
    
    def get_cached_disease(self, disease_name: str) -> Optional[str]:
        """Récupère le résultat en cache d'une recherche"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cached_result FROM disease_searches 
            WHERE disease_name = ?
        """, (disease_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_statistics(self) -> Dict:
        """Récupère les statistiques globales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total lessons
        cursor.execute("SELECT COUNT(*) FROM lessons")
        total_lessons = cursor.fetchone()[0]
        
        # Auto-generated lessons
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE auto_generated = 1")
        auto_lessons = cursor.fetchone()[0]
        
        # Total quizzes
        cursor.execute("SELECT COUNT(*) FROM quizzes")
        total_quizzes = cursor.fetchone()[0]
        
        # Total disease searches
        cursor.execute("SELECT COUNT(*) FROM disease_searches")
        total_searches = cursor.fetchone()[0]
        
        # Most viewed lessons
        cursor.execute("""
            SELECT title, views FROM lessons 
            ORDER BY views DESC LIMIT 5
        """)
        top_lessons = cursor.fetchall()
        
        # Most searched diseases
        cursor.execute("""
            SELECT disease_name, search_count FROM disease_searches 
            ORDER BY search_count DESC LIMIT 5
        """)
        top_diseases = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_lessons": total_lessons,
            "auto_generated_lessons": auto_lessons,
            "manual_lessons": total_lessons - auto_lessons,
            "total_quizzes": total_quizzes,
            "total_searches": total_searches,
            "top_lessons": top_lessons,
            "top_diseases": top_diseases
        }
    
    def increment_lesson_views(self, lesson_id: int):
        """Incrémente le compteur de vues d'une leçon"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE lessons SET views = views + 1 
                WHERE id = ?
            """, (lesson_id,))
            
            conn.commit()
            conn.close()
    
    def delete_lesson(self, lesson_id: int):
        """Supprime une leçon"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
            conn.commit()
            conn.close()
            
            print(f"🗑️ Leçon {lesson_id} supprimée")
    
    def get_lessons_by_category(self, category: str) -> List[Dict]:
        """Récupère les leçons d'une catégorie spécifique"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM lessons 
            WHERE category = ?
            ORDER BY generated_at DESC
        """, (category,))
        
        lessons = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for lesson in lessons:
            lesson['content'] = json.loads(lesson['content'])
        
        return lessons
    
    def export_all_lessons(self) -> str:
        """Exporte toutes les leçons en JSON"""
        lessons = self.get_all_lessons(limit=10000)
        return json.dumps(lessons, indent=2, ensure_ascii=False)
