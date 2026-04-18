from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Submit ticket
@app.route('/submit', methods=['POST'])
def submit_ticket():
    full_name = request.form['full_name']
    issue_description = request.form['issue_description']
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tickets (full_name, issue_description, created_at)
        VALUES (?, ?, ?)
    ''', (full_name, issue_description, created_at))

    conn.commit()
    conn.close()

    return redirect(url_for('view_tickets'))

# View all tickets
@app.route('/view')
def view_tickets():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tickets ORDER BY id DESC')
    tickets = cursor.fetchall()

    conn.close()
    return render_template('view.html', tickets=tickets)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
