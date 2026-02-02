from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import base64
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET
import re
import os

# ---------- USERS ----------
USERS = {
    'MomoUser1': '$Momo123',
    'MomoUser2': '$Momo456',
    'admin': 'password123'
}


# ---------- API CLASS ----------
class TransactionAPI(BaseHTTPRequestHandler):
    transactions = []  # List for linear search
    tx_map = {}        # Dict for fast lookup

    # ---------- Helpers ----------
    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def unauthorized(self):
        self.respond({"error": "Unauthorized"}, 401)

    def authenticate(self):
        auth = self.headers.get("Authorization")
        if not auth:
            return False
        try:
            _, token = auth.split()
            user, pwd = base64.b64decode(token).decode().split(":", 1)
            return USERS.get(user) == pwd
        except:
            return False

    def parse_path(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts[0] != "transactions":
            return None, None
        return "transactions", parts[1] if len(parts) > 1 else None

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    # ---------- CRUD ----------
    def do_GET(self):
        if not self.authenticate():
            return self.unauthorized()

        endpoint, tx_id = self.parse_path()
        if endpoint is None:
            return self.respond({"error": "Not Found"}, 404)

        if not tx_id:
            return self.respond(self.transactions)

        tx = self.tx_map.get(tx_id)
        if not tx:
            return self.respond({"error": "Transaction not found"}, 404)

        self.respond(tx)

    def do_POST(self):
        if not self.authenticate():
            return self.unauthorized()

        body = self.read_body()
        if "transactionType" not in body or "amount" not in body:
            return self.respond({"error": "Missing fields"}, 400)

        # Auto-generate IDs
        full_uuid = str(uuid.uuid4())
        short_id = full_uuid[:6]  # extremely short and easy to remember

        transaction = {
            "id": short_id,            # short API ID
            "_full_id": full_uuid,     # internal full UUID (optional)
            "transactionType": body["transactionType"],
            "amount": body["amount"],
            "sender": body.get("sender", ""),
            "receiver": body.get("receiver", ""),
            "createdAt": datetime.now().isoformat(),
            "body": body.get("body", "")
        }

        self.transactions.append(transaction)
        self.tx_map[short_id] = transaction

        self.respond(transaction, 201)

    def do_PUT(self):
        if not self.authenticate():
            return self.unauthorized()

        endpoint, tx_id = self.parse_path()
        if not tx_id or tx_id not in self.tx_map:
            return self.respond({"error": "Transaction not found"}, 404)

        updates = self.read_body()
        updates["updatedAt"] = datetime.now().isoformat()

        self.tx_map[tx_id].update(updates)

        for i, tx in enumerate(self.transactions):
            if tx["id"] == tx_id:
                self.transactions[i] = self.tx_map[tx_id]
                break

        self.respond(self.tx_map[tx_id])

    def do_DELETE(self):
        if not self.authenticate():
            return self.unauthorized()

        endpoint, tx_id = self.parse_path()
        if not tx_id or tx_id not in self.tx_map:
            return self.respond({"error": "Transaction not found"}, 404)

        deleted = self.tx_map.pop(tx_id)
        self.transactions = [tx for tx in self.transactions if tx["id"] != tx_id]

        self.respond({"deleted": deleted})

    def log_message(self, format, *args):
        pass  # disable default logging

# ---------- XML PARSER ----------
def parse_sms_xml(file_name="modified_sms_v2.xml"):
    if not os.path.exists(file_name):
        print(f"File {file_name} not found. Starting empty.")
        return []

    tree = ET.parse(file_name)
    root = tree.getroot()
    transactions = []

    for sms in root.findall("sms"):
        body = sms.get("body", "")

        # Extract transaction id, amount, receiver from body
        tx_id_match = re.search(r"TxId[:\s]*(\d+)", body)
        amount_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+) RWF", body)
        receiver_match = re.search(r"to ([A-Za-z ]+)", body)

        full_uuid = str(uuid.uuid4())
        short_id = tx_id_match.group(1)[:6] if tx_id_match else full_uuid[:6]

        amount = float(amount_match.group(1).replace(",", "")) if amount_match else 0.0
        receiver = receiver_match.group(1) if receiver_match else ""
        timestamp = datetime.fromtimestamp(int(sms.get("date", 0)) / 1000).isoformat()
        sender = sms.get("address", "")

        transactions.append({
            "id": short_id,
            "_full_id": full_uuid,
            "transactionType": sms.get("type"),
            "amount": amount,
            "sender": sender,
            "receiver": receiver,
            "timestamp": timestamp,
            "body": body
        })

    print(f"Loaded {len(transactions)} transactions from {file_name}")
    return transactions

# ---------- RUN SERVER ----------
def run():
    TransactionAPI.transactions = parse_sms_xml()
    TransactionAPI.tx_map = {tx["id"]: tx for tx in TransactionAPI.transactions}
    server = HTTPServer(("", 8500), TransactionAPI)
    print("API running on http://localhost:8500")
    server.serve_forever()

if __name__ == "__main__":
    run()

