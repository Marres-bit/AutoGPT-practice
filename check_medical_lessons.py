import sqlite3

conn = sqlite3.connect('medical_lessons.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('📚 Tables dans la base de données:', tables)

# Compter les leçons
cursor.execute('SELECT COUNT(*) FROM lessons')
count = cursor.fetchone()
print(f'\n✅ Nombre total de leçons: {count[0]}')

# Afficher les 10 dernières leçons
cursor.execute('SELECT id, category, title, created_at FROM lessons ORDER BY created_at DESC LIMIT 10')
lessons = cursor.fetchall()
print('\n📖 10 dernières leçons:')
for lesson in lessons:
    print(f'  {lesson[0]}. [{lesson[1]}] {lesson[2]} - {lesson[3]}')

# Statistiques par catégorie
cursor.execute('SELECT category, COUNT(*) FROM lessons GROUP BY category ORDER BY COUNT(*) DESC')
stats = cursor.fetchall()
print('\n📊 Leçons par catégorie:')
for cat, cnt in stats:
    print(f'  {cat}: {cnt}')

conn.close()
