from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = "tickets.db"

# Create database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            issue TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Add ticket
@app.route('/add', methods=['POST'])
def add_ticket():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    priority = request.form['priority']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tickets (name, email, issue, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, issue, priority, "Open", str(datetime.now())))
    
    conn.commit()
    conn.close()
    
    return redirect('/view')

# View tickets
@app.route('/view')
def view():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    
    conn.close()
    
    return render_template('view.html', tickets=tickets)

# ✅ FIXED HERE
if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)
