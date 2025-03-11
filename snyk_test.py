import os
import pickle
import sqlite3
import xml.etree.ElementTree as ET
from flask import Flask, request, send_file
import bcrypt
import secrets

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

# 2. **Insecure Deserialization**
@app.route('/unpickle', methods=['POST'])
def unpickle_data():
    data = request.form.get("data")
    return pickle.loads(bytes.fromhex(data))  # Still vulnerable to Insecure Deserialization

# 3. **Path Traversal**
@app.route('/read', methods=['GET'])
def read_file():
    filename = request.args.get("file")
    with open(f"/var/www/{filename}", "r") as f:  # Still vulnerable to Path Traversal
        return f.read()

# 4. **Cross-Site Scripting (XSS)**
@app.route('/xss', methods=['GET'])
def xss():
    name = request.args.get("name")
    return f"<h1>Welcome {name}</h1>"  # Still vulnerable to XSS

# 5. **Improper Input Validation**
@app.route('/transfer', methods=['POST'])
def transfer_money():
    amount = int(request.form.get("amount"))
    if amount > 1000:
        return "Amount too large!"
    return "Transfer successful"  # No proper authentication or authorization

# 6. **Insecure File Upload (New Vulnerability)**
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f"/uploads/{file.filename}")  # No validation, allowing malicious files
    return "File uploaded successfully"

# 7. **XML External Entity (XXE) Injection (New Vulnerability)**
@app.route('/parse-xml', methods=['POST'])
def parse_xml():
    xml_data = request.form.get("xml")
    tree = ET.ElementTree(ET.fromstring(xml_data))  # Vulnerable to XXE
    return "XML Parsed"

# 8. **Secure Hashing Algorithm (Fixed MD5 Vulnerability)**
@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form.get("password").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # Secure hashing
    return hashed.decode()

# 9. **Secure Random Password Generation (Fixed Insecure Randomness)**
@app.route('/generate-password', methods=['GET'])
def generate_password():
    return secrets.token_hex(8)  # Uses cryptographically secure randomness

if __name__ == '__main__':
    app.run(debug=True)
