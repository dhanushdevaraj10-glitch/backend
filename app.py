from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Database connection using environment variables for Render deployment
def connect_db():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "Root@123")
    db_name = os.environ.get("DB_NAME", "studentdb")

    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()
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
