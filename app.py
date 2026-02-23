import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# DATABASE_URL = os.environ.get("DATABASE_URL")
# print("DATABASE_URL:", DATABASE_URL)
# def get_connection():
#     return psycopg2.connect(DATABASE_URL)

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="CBPSI5DAS22109",
        password="Aswathir@123",
        host="backend109.postgres.database.azure.com",
        port=5432,
        sslmode="require"
    )
    

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)
    conn.commit()

    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)