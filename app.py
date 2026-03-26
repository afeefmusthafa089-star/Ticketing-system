from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            issue TEXT,
            priority TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    priority = request.form['priority']

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (name, email, issue, priority, status) VALUES (?, ?, ?, ?, ?)",
        (name, email, issue, priority, "Open")
    )
    conn.commit()
    conn.close()

    return "Ticket Submitted Successfully!"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return render_template('admin.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
