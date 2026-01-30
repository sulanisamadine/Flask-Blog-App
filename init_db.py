import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create blog table
c.execute('''
    CREATE TABLE IF NOT EXISTS blog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')

# Insert sample user with hashed password
hashed_password = generate_password_hash('admin')
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_password))

# Insert sample blog post
c.execute("INSERT INTO blog (title, content) VALUES (?, ?)", ("My First Post", "This is a test blog post."))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ database.db initialized successfully with hashed admin password!")
