from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    todos = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")

    if task:
        conn = get_db()
        conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = get_db()

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (task, id))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("update.html", task=task)

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
