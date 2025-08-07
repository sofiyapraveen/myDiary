from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)


def init_db():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT,
            mood TEXT,
            polarity REAL,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/analyze', methods=['POST'])
def analyze_mood():
    data = request.get_json()
    entry = data.get('entry', '')
    blob = TextBlob(entry)
    polarity = blob.sentiment.polarity
    mood = "Happy" if polarity > 0.1 else "Sad" if polarity < -0.1 else "Neutral"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute("INSERT INTO diary_entries (entry, mood, polarity, timestamp) VALUES (?, ?, ?, ?)",
              (entry, mood, polarity, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"mood": mood, "timestamp": timestamp})

@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    note = data.get('note', '')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (note, timestamp) VALUES (?, ?)", (note, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved successfully!"})

@app.route('/history', methods=['GET'])
def view_history():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute("SELECT entry, mood, timestamp FROM diary_entries ORDER BY timestamp DESC")
    entries = c.fetchall()
    conn.close()
    return jsonify(entries)

@app.route('/notes', methods=['GET'])
def view_notes():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute("SELECT note, timestamp FROM notes ORDER BY timestamp DESC")
    notes = c.fetchall()
    conn.close()
    return jsonify(notes)

if __name__ == '__main__':
    app.run(debug=True)
