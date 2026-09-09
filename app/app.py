import os
import time
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}

def wait_for_db(retries=30, delay=2):
    """Ждём, пока MySQL поднимется — контейнер стартует раньше, чем БД готова принимать соединения."""
    for _ in range(retries):
        try:
            conn = pymysql.connect(**DB_CONFIG)
            conn.close()
            return
        except pymysql.MySQLError:
            time.sleep(delay)
    raise RuntimeError("DB is not available")

def init_db():
    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        cur.execute("INSERT IGNORE INTO users (id, name) VALUES (1, 'alice'), (2, 'bob')")
    conn.commit()
    conn.close()

@app.route("/health")
def health():
    """Health check endpoint — его опрашивают Docker и Nginx."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        conn.close()
        return jsonify(status="ok", db="up"), 200
    except pymysql.MySQLError:
        return jsonify(status="degraded", db="down"), 503

@app.route("/api/users")
def users():
    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM users")
        rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000)