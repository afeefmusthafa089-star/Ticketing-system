from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# OpenAI client
client = OpenAI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tickets.db")

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            issue TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    priority = request.form['priority']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (name, email, issue, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'Open', ?)
    """, (name, email, issue, priority, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return "Ticket submitted successfully!"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    try:
        response = client.responses.create(
            model="gpt-5.4",
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for a ticketing system. Help users describe issues clearly, choose ticket priority, and suggest simple troubleshooting steps."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return jsonify({"reply": response.output_text})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
           
   
