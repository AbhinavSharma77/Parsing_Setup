import os
import pickle
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 1. Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"

# 2. SQL Injection Vulnerability
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # Vulnerable to SQL Injection
    result = cursor.fetchall()
    conn.close()
    return result

# 3. Command Injection@app.route('/run', methods=['POST'])
def run_command():
    cmd = request.form.get("cmd")
    return subprocess.check_output(cmd, shell=True)  # Vulnerable to Command Injection

# 4. Insecure Deserialization@app.route('/unpickle', methods=['POST'])
def unpickle_data():
    data = request.form.get("data")
    return pickle.loads(bytes.fromhex(data))  # Vulnerable to Insecure Deserialization

# 5. Path Traversal@app.route('/read', methods=['GET'])
def read_file():
    filename = request.args.get("file")
    with open(f"/var/www/{filename}", "r") as f:  # Vulnerable to Path Traversal
        return f.read()

# 6. Cross-Site Scripting (XSS)@app.route('/xss', methods=['GET'])
def xss():
    name = request.args.get("name")
    return f"<h1>Welcome {name}</h1>"  # Vulnerable to XSS

# 7. Insecure Randomness@app.route('/generate-password', methods=['GET'])
def generate_password():
    import random
    password = "".join([chr(random.randint(97, 122)) for _ in range(8)])  # Predictable random passwords
    return password

# 8. Use of eval@app.route('/eval', methods=['POST'])
def eval_code():
    code = request.form.get("code")
    return str(eval(code))  # Arbitrary code execution vulnerability

# 9. Improper Input Validation@app.route('/transfer', methods=['POST'])
def transfer_money():
    amount = int(request.form.get("amount"))
    if amount > 1000:
        return "Amount too large!"
    return "Transfer successful"  # No proper authentication or authorization

# 10. Weak Hashing Algorithm@app.route('/hash', methods=['POST'])
def hash_password():
    import hashlib
    password = request.form.get("password")
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is insecure

if __name__ == '__main__':
    app.run(debug=True)
