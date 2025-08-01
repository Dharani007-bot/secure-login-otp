import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)''')
conn.commit()
conn.close()
print("Database created successfully.")
