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



# 2. **Server-Side Request Forgery (SSRF) - New Vulnerability**
@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.form.get("url")
    response = requests.get(url)  # No validation, allowing internal network access
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
