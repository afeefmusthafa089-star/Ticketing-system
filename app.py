from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            issue TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    issue = request.form['issue']

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (name, issue, status, created_at) VALUES (?, ?, ?, ?)",
        (name, issue, 'Open', datetime.now())
    )
    conn.commit()
    conn.close()

    return redirect('/tickets')

@app.route('/tickets')
def tickets():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    data = cursor.fetchall()
    conn.close()

    return render_template('tickets.html', tickets=data)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
