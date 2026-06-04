from flask import Flask, render_template, request
import mysql.connector
import os
from urllib.parse import urlparse, unquote

app = Flask(__name__)

# Parse a MySQL database URL if Render provides one
def parse_database_url(database_url):
    parsed = urlparse(database_url)
    if parsed.scheme not in ("mysql", "mysql+mysqlconnector", "mysql+pymysql"):
        raise ValueError("Unsupported database URL scheme: " + parsed.scheme)

    return {
        "host": parsed.hostname or "localhost",
        "user": unquote(parsed.username or "root"),
        "password": unquote(parsed.password or ""),
        "database": parsed.path.lstrip("/") or "studentdb",
        "port": parsed.port or 3306,
    }

def get_db_config():
    database_url = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_DATABASE_URL")
    if database_url:
        return parse_database_url(database_url)

    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", "Root@123"),
        "database": os.environ.get("DB_NAME", "studentdb"),
        "port": int(os.environ.get("DB_PORT", "3306")),
    }

def ensure_user_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
        """
    )

def connect_db():
    config = get_db_config()
    db_name = config.pop("database")

    try:
        db = mysql.connector.connect(**config, database=db_name)
    except mysql.connector.errors.ProgrammingError as exc:
        # Handle missing database by creating it first
        if exc.errno == 1049:
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            cursor.execute(f"USE `{db_name}`")
            ensure_user_table(cursor)
            db.commit()
            return db, cursor
        raise

    cursor = db.cursor()
    ensure_user_table(cursor)
    db.commit()
    return db, cursor

(db, cursor) = connect_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    sql = "INSERT INTO users(name, email) VALUES(%s, %s)"
    cursor.execute(sql, (name, email))
    db.commit()

    return "✓ Data Stored Successfully!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
