import sqlite3

db = sqlite3.connect('texnomart.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    );
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS under_catalogs(
        under_catalog_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name INTEGER REFERENCES under_categories(category_id),
        under_catalog_name TEXT UNIQUE
    );
''')
cursor.execute('''
     CREATE TABLE IF NOT EXISTS under_categories(
        under_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        under_catalog_name INTEGER REFERENCES categories(under_catalog_name),
        under_category_name TEXT UNIQUE,
        under_category_link TEXT UNIQUE
    );
''')

db.commit()
db.close()