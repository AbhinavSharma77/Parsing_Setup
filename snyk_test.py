import os
import pickle
import sqlite3
import requests
import time
from flask import Flask, request
import subprocess  # Importing subprocess for command execution

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

# 2. **Server-Side Request Forgery (SSRF)**
@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.form.get("url")
    response = requests.get(url)  # No validation, allowing internal network access
    return response.text

# 3. **Remote Code Execution (RCE)**
@app.route('/execute', methods=['POST'])
def execute():
    code = request.form.get("code")
    result = eval(code)  # Dangerous! Allows execution of arbitrary code
    return str(result)

# 4. **Insecure Deserialization**
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.files['file'].read()
    obj = pickle.loads(data)  # No validation! Allows execution of malicious payloads
    return str(obj)

# 5. **Command Injection**
@app.route('/run-command', methods=['POST'])
def run_command():
    cmd = request.form.get("cmd")
    output = subprocess.check_output(cmd, shell=True)  # Vulnerable! Allows command injection
    return output.decode()

if __name__ == '__main__':
    app.run(debug=True)
