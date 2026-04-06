from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    issue = request.form['issue']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (name, issue, status, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, issue, 'Open', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect('/view')

@app.route('/view', methods=['GET'])
def view():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    return render_template('view.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
