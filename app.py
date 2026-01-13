from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        priority TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------
@app.route("/")
def home():
    return "Incident Management System is running"

# ---------- CREATE INCIDENT ----------
@app.route("/create", methods=["POST"])
def create_incident():
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO incidents (title, description, priority, status, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["priority"],
        "Open",
        datetime.datetime.now()
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Incident created successfully"})

# ---------- VIEW INCIDENTS ----------
@app.route("/incidents", methods=["GET"])
def view_incidents():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# ---------- UPDATE STATUS ----------
@app.route("/update/<int:id>", methods=["PUT"])
def update_status(id):
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status=? WHERE id=?", (data["status"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated"})

# ---------- ANALYTICS ----------
@app.route("/analytics", methods=["GET"])
def analytics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT priority, COUNT(*) FROM incidents GROUP BY priority")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

