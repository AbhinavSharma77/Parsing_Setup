import os
import pickle
import sqlite3
import requests
import time
from flask import Flask, request

app = Flask(__name__)

# 1. **SQL Injection Vulnerability**
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # Still vulnerable to SQL Injection
    result = cursor.fetchall()
    conn.close()
    return result

# 2. **Path Traversal**
@app.route('/read', methods=['GET'])
def read_file():
    filename = request.args.get("file")
    with open(f"/var/www/{filename}", "r") as f:  # Still vulnerable to Path Traversal
        return f.read()

# 3. **Race Condition (TOCTOU) - New Vulnerability**
@app.route('/race-condition', methods=['POST'])
def race_condition():
    filename = request.form.get("file")
    
    # Check if the file exists
    if os.path.exists(filename):
        time.sleep(2)  # Simulating a delay
        with open(filename, "r") as f:
            return f.read()  # TOCTOU - File can be modified before access

# 4. **Server-Side Request Forgery (SSRF) - New Vulnerability**
@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.form.get("url")
    response = requests.get(url)  # No validation, allowing internal network access
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
