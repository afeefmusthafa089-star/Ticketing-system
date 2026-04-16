from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tickets.db")

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            issue TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Login details
USERNAME = "admin"
PASSWORD = "1234"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    issue = request.form['issue']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (name, issue, status, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, issue, 'Open', datetime.now().strftime("%d-%m-%Y %I:%M %p")))
    conn.commit()
    conn.close()

    return redirect('/view')

@app.route('/view', methods=['GET'])
def view():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    return render_template('view.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
