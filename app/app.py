import os
import time
from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Настройки подключения к БД берутся из переменных окружения
# (это то, что вы будете пробрасывать через docker-compose)
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "password"),
    "database": os.environ.get("DB_NAME", "demo_db"),
}


def get_connection(retries=10, delay=3):
    """
    Пытается подключиться к MySQL с повторными попытками.
    Это важно в docker-compose: контейнер приложения может
    стартовать раньше, чем MySQL будет готов принимать соединения.
    """
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            last_error = e
            print(f"[{attempt}/{retries}] MySQL ещё не готов: {e}")
            time.sleep(delay)
    raise last_error


def init_db():
    """Создаёт таблицу и тестовую запись, если их ещё нет"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text VARCHAR(255) NOT NULL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM messages")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO messages (text) VALUES (%s)",
            ("Привет из MySQL! Контейнеры работают 🐳",)
        )
    conn.commit()
    cur.close()
    conn.close()


def get_text_from_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM messages ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else "Нет данных"


@app.route("/")
def index():
    text = get_text_from_db()
    return f"""
    <html>
        <head><title>Текст из MySQL</title></head>
        <body style="font-family: sans-serif; margin: 40px;">
            <h1>Текст из базы данных:</h1>
            <p style="font-size: 20px; color: #2c3e50;">{text}</p>
            <hr>
            <small>DB host: {DB_CONFIG['host']}</small>
        </body>
    </html>
    """


@app.route("/health")
def health():
    """Полезно для healthcheck в docker-compose"""
    return {"status": "ok"}


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)