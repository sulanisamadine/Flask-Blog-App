from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_NAME = 'database.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # Create tables
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        hashed_pw = generate_password_hash('admin')
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
        c.execute('''CREATE TABLE blog (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM blog")
    blogs = c.fetchall()
    conn.close()
    return render_template('dashboard.html', blogs=blogs)

@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO blog (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_edit.html', action="Add")

@app.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    if 'username' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE blog SET title=?, content=? WHERE id=?", (title, content, blog_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        c.execute("SELECT * FROM blog WHERE id=?", (blog_id,))
        blog = c.fetchone()
        conn.close()
        return render_template('add_edit.html', action="Edit", blog=blog)

@app.route('/delete/<int:blog_id>')
def delete_blog(blog_id):
    if 'username' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM blog WHERE id=?", (blog_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
