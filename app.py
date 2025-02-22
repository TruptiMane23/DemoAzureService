from flask import Flask, request, jsonify
import os
import pyodbc

app = Flask(__name__)


DB_CONNECTION = os.getenv("AZURE_SQL_CONNECTION")
# "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:taskdb-server.database.windows.net,1433;DATABASE=TaskDB;UID=TruptiMane23;PWD=Frankfurt@2020"


# Home route
@app.route("/")
def home():
    return "Hello from Azure Flask App..........!"

# Connect to the database
def get_db_connection():
    try:
        conn = pyodbc.connect(DB_CONNECTION)
        print("Database connection:", conn)
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None


# GET Request
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, created_at FROM Tasks")
    tasks = [{"id": row[0], "task_name": row[1], "created_at": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)


# POST request
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task_name = data.get("task_name")
    

    if not task_name:
        return jsonify({"error": "Task name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added successfully"}), 201


# Update request


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
