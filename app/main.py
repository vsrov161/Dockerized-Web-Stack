from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'secret'),
        database=os.getenv('DB_NAME', 'mydb'),
        connection_timeout=5
    )

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"Hello! Database connection successful. Result: {result[0]}"
    except Exception as e:
        return f"Error connecting to database: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)