import os
import time
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

def wait_for_db():
    while True:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            cur.close()
            break
        except Exception as e:
            print("⏳ Waiting for MySQL...", e)
            time.sleep(3)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT message FROM messages")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=data)

@app.route('/submit', methods=['POST'])
def submit():
    msg = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", (msg,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": msg})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=5000)
