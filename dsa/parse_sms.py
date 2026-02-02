
import xml.etree.ElementTree as ET
from datetime import datetime
import uuid
import re

def parse_sms(file_path="modified_sms_v2.xml"):
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall("sms"):
        body = sms.get("body", "")
        amount = 0.0
        receiver = ""
        transaction_type = sms.get("type", "1")

        # Extract amount using regex (RWF amounts)
        amount_match = re.search(r"([\d,]+) RWF", body)
        if amount_match:
            amount = float(amount_match.group(1).replace(",", ""))

        # Extract receiver name (after "to" or "transferred to")
        receiver_match = re.search(r"(?:to|transferred to) ([A-Za-z ]+)", body)
        if receiver_match:
            receiver = receiver_match.group(1).strip()

        # Convert timestamp
        timestamp = datetime.fromtimestamp(int(sms.get("date", "0")) / 1000)

        transactions.append({
            "id": str(uuid.uuid4())[:6],  # short UUID for convenience
            "_full_id": str(uuid.uuid4()),  # full UUID for internal use
            "transactionType": transaction_type,
            "amount": amount,
            "sender": sms.get("address", ""),
            "receiver": receiver,
            "timestamp": timestamp.isoformat(),
            "body": body
        })

    return transactions

if __name__ == "__main__":
    txs = parse_sms()
    print(f"Parsed {len(txs)} transactions")
    for t in txs[:5]:  # print first 5 as example
        print(t)
