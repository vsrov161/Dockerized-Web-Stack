from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "webapp"),
        user=os.getenv("MYSQL_USER", "webapp"),
        password=os.getenv("MYSQL_PASSWORD", "webapp_password"),
    )


def wait_for_database():
    while True:
        try:
            connection = get_db_connection()
            connection.close()
            print("MySQL is ready")
            return
        except mysql.connector.Error as error:
            print(f"MySQL is not ready yet: {error}")
            time.sleep(2)


@app.get("/")
def index():
    return {
        "message": "Hello from Docker!",
        "hostname": os.uname().nodename
    }


@app.get("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return {
            "status": "UP",
            "database": "UP"
        }

    except mysql.connector.Error:
        return {
            "status": "UP",
            "database": "DOWN"
        }, 503


@app.get("/db")
def database_test():
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT VERSION()")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "mysql_version": result[0]
    }


if __name__ == "__main__":
    wait_for_database()
    app.run(host="0.0.0.0", port=8000)