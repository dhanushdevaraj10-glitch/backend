from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",  # Change this to your MySQL password
    database="studentdb"
)

cursor = db.cursor()

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
    app.run(debug=True)
