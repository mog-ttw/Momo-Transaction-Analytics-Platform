from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic Authentication
USER_DATA = {
    "admin": generate_password_hash("admin@123")
}

@auth.verify_password
def verify_password(username, password):
    if username in USER_DATA and \
       check_password_hash(USER_DATA.get(username), password):
        return username
    return None

# Custom error handler for 401 Unauthorized
@auth.error_handler
def auth_error(status):
    return jsonify({
        "error": "401 Unauthorized",
        "message": "Invalid or missing credentials. Access denied."
    }), 401

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Philosophy@360',
    'database': 'momo_sms_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# 1. GET /transactions -> List all active transactions
@app.route('/transactions', methods=['GET'])
@auth.login_required
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # We only fetch records where is_deleted is FALSE
    cursor.execute("SELECT * FROM transactions WHERE is_deleted = FALSE")
    transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(transactions), 200

# 2. GET /transactions/{id} -> View one transaction
@app.route('/transactions/<int:t_id>', methods=['GET'])
@auth.login_required
def get_transaction(t_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = %s AND is_deleted = FALSE", (t_id,))
    transaction = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if transaction:
        return jsonify(transaction), 200
    return jsonify({"error": "Transaction not found"}), 404

# 3. POST /transactions -> Add a new transaction
@app.route('/transactions', methods=['POST'])
@auth.login_required
def add_transaction():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = """INSERT INTO transactions 
             (transaction_ref, category_id, amount, fee, transaction_date, raw_sms) 
             VALUES (%s, %s, %s, %s, %s, %s)"""
    
    values = (
        data.get('transaction_ref'),
        data.get('category_id'),
        data.get('amount'),
        data.get('fee', 0.0),
        data.get('transaction_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        data.get('raw_sms')
    )
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"message": "Transaction created", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# 4. PUT /transactions/{id} -> Update an existing record
@app.route('/transactions/<int:t_id>', methods=['PUT'])
@auth.login_required
def update_transaction(t_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dynamically build the update query based on provided fields
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)
    
    if not fields:
        return jsonify({"error": "No data provided"}), 400
        
    values.append(t_id)
    sql = f"UPDATE transactions SET {', '.join(fields)} WHERE transaction_id = %s"
    
    cursor.execute(sql, values)
    conn.commit()
    
    success = cursor.rowcount > 0
    cursor.close()
    conn.close()
    
    if success:
        return jsonify({"message": "Transaction updated"}), 200
    return jsonify({"error": "Transaction not found"}), 404

# 5. DELETE /transactions/{id} -> Soft delete a record
@app.route('/transactions/<int:t_id>', methods=['DELETE'])
@auth.login_required
def delete_transaction(t_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Following your SQL schema logic: Soft Delete
    sql = """UPDATE transactions 
             SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP 
             WHERE transaction_id = %s"""
    
    cursor.execute(sql, (t_id,))
    conn.commit()
    
    success = cursor.rowcount > 0
    cursor.close()
    conn.close()
    
    if success:
        return jsonify({"message": "Transaction deleted (soft delete)"}), 200
    return jsonify({"error": "Transaction not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)