import sqlite3

conn = sqlite3.connect('medical_lessons.db')
cursor = conn.cursor()

# Vérifier la structure de la table lessons
cursor.execute('PRAGMA table_info(lessons)')
columns = cursor.fetchall()
print('📋 Structure de la table "lessons":')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

# Compter les leçons
cursor.execute('SELECT COUNT(*) FROM lessons')
count = cursor.fetchone()
print(f'\n✅ Nombre total de leçons: {count[0]}')

# Afficher toutes les leçons avec les bonnes colonnes
cursor.execute('SELECT * FROM lessons')
lessons = cursor.fetchall()
print(f'\n📖 Toutes les {len(lessons)} leçons:')
print('=' * 80)
for i, lesson in enumerate(lessons, 1):
    print(f'\n{i}. Leçon #{lesson[0]}')
    print(f'   Catégorie: {lesson[1]}')
    print(f'   Titre: {lesson[2]}')
    if len(lesson) > 3:
        print(f'   Contenu: {lesson[3][:200]}...' if len(lesson[3]) > 200 else f'   Contenu: {lesson[3]}')
    print('-' * 80)

# Statistiques par catégorie
cursor.execute('SELECT category, COUNT(*) FROM lessons GROUP BY category ORDER BY COUNT(*) DESC')
stats = cursor.fetchall()
print('\n📊 Leçons par catégorie:')
for cat, cnt in stats:
    print(f'  {cat}: {cnt}')

conn.close()
