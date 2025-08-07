# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from textblob import TextBlob
# # import random

# # # Initialize Flask App
# # app = Flask(__name__)
# # CORS(app)  # Enables CORS for frontend-backend connection

# # # Mood-wise motivational suggestions
# # suggestions = {
# #     "positive": [
# #         "Keep smiling, you're doing great!",
# #         "Celebrate your wins, no matter how small!",
# #         "Happiness looks good on you!"
# #     ],
# #     "negative": [
# #         "Take a deep breath. Tomorrow is a new day.",
# #         "It's okay to feel down. Talk to someone you trust.",
# #         "You’re stronger than you think. Don’t give up!"
# #     ],
# #     "neutral": [
# #         "Stay steady and grounded.",
# #         "Maybe go for a walk or listen to music.",
# #         "Let today be calm. Small steps matter."
# #     ]
# # }

# # # API Route to analyze mood
# # @app.route('/analyze', methods=['POST'])
# # def analyze():
# #     try:
# #         data = request.get_json()
# #         text = data.get("text", "")

# #         if not text.strip():
# #             return jsonify({"error": "No text provided"}), 400

# #         # Analyze mood using TextBlob
# #         blob = TextBlob(text)
# #         polarity = blob.sentiment.polarity

# #         if polarity > 0.2:
# #             mood = "Positive"
# #             suggestion = random.choice(suggestions["positive"])
# #         elif polarity < -0.2:
# #             mood = "Negative"
# #             suggestion = random.choice(suggestions["negative"])
# #         else:
# #             mood = "Neutral"
# #             suggestion = random.choice(suggestions["neutral"])

# #         # Return mood, suggestion, and polarity
# #         return jsonify({
# #             "mood": mood,
# #             "suggestion": suggestion,
# #             "polarity": polarity
# #         })

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Run the Flask app
# # if __name__ == '__main__':
# #     app.run(debug=True)

# # ---------------------------
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from textblob import TextBlob
# import sqlite3
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # Initialize database
# def init_db():
#     conn = sqlite3.connect('diary.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS diary_entries (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             entry TEXT,
#             mood TEXT,
#             polarity REAL,
#             timestamp TEXT
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS notes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             content TEXT,
#             timestamp TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# init_db()

# @app.route('/analyze', methods=['POST'])
# def analyze_mood():
#     data = request.get_json()
#     entry = data['entry']
#     blob = TextBlob(entry)
#     polarity = blob.sentiment.polarity
#     mood = "Happy" if polarity > 0.1 else "Sad" if polarity < -0.1 else "Neutral"
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     conn = sqlite3.connect('diary.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO diary_entries (entry, mood, polarity, timestamp) VALUES (?, ?, ?, ?)",
#                    (entry, mood, polarity, timestamp))
#     conn.commit()
#     conn.close()

#     return jsonify({"mood": mood, "timestamp": timestamp})

# @app.route('/history', methods=['GET'])
# def get_history():
#     conn = sqlite3.connect('diary.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT entry, mood, timestamp FROM diary_entries ORDER BY id DESC")
#     rows = cursor.fetchall()
#     conn.close()
#     return jsonify(rows)

# @app.route('/notes', methods=['POST'])
# def save_notes():
#     data = request.get_json()
#     content = data['content']
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     conn = sqlite3.connect('diary.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO notes (content, timestamp) VALUES (?, ?)", (content, timestamp))
#     conn.commit()
#     conn.close()

#     return jsonify({"message": "Note saved!"})

# @app.route('/notes', methods=['GET'])
# def get_notes():
#     conn = sqlite3.connect('diary.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT content, timestamp FROM notes ORDER BY id DESC")
#     rows = cursor.fetchall()
#     conn.close()
#     return jsonify(rows)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database Setup
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

# Mood Analysis Route
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

# Save Note
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

# View History
@app.route('/history', methods=['GET'])
def view_history():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute("SELECT entry, mood, timestamp FROM diary_entries ORDER BY timestamp DESC")
    entries = c.fetchall()
    conn.close()
    return jsonify(entries)

# View Notes
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
