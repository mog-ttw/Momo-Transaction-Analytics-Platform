# MoMo Transactions API


This is a simple REST API for Mobile Money (MoMo) transactions built in plain Python using `http.server`. The API allows CRUD operations on SMS-based transaction records parsed from XML.


---


## Features


- Parse SMS transaction records from `modified_sms_v2.xml`
- Perform CRUD operations:  
  - **GET** /transactions → list all transactions  
  - **GET** /transactions/{id} → get a specific transaction  
  - **POST** /transactions → add a new transaction  
  - **PUT** /transactions/{id} → update a transaction  
  - **DELETE** /transactions/{id} → delete a transaction
- Basic Authentication (username/password)
- Auto-generated short UUID for transactions
- Fast transaction lookup using dictionary
- Test script included for PowerShell


---


## Default Users (for testing)


| Username      | Password      |
|---------------|---------------|
| admin         | password123   |
| MomoUser1     | $Momo123      |
| MomoUser2     | $Momo456      |


> Use `admin:password123` for the test script.


---


## Requirements


- Python 3.8+  
- PowerShell (for running the test script)
- Standard libraries only (`http.server`, `json`, `uuid`, `base64`, `xml.etree.ElementTree`, `datetime`)


---


## Setup


1. Clone or download this repository.  
2. Ensure `modified_sms_v2.xml` is in the same folder as `server.py`.  
3. Start the API server:


```bash
python server.py

Server will start at: http://localhost:8500

Testing the API

PowerShell script is included: test_momo_api.ps1

Open PowerShell as Administrator.

Temporarily allow script execution:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Navigate to project folder:

cd "C:\Users\coach\OneDrive\Desktop\momo_api"

Run the test script:

.\test_momo_api.ps1

This script performs:

GET all transactions

POST a new transaction

GET the new transaction

PUT update the transaction

GET updated transaction

DELETE the transaction

Confirm deletion

API Usage Examples
GET all transactions
curl -u admin:password123 http://localhost:8500/transactions
GET a transaction by ID
curl -u admin:password123 http://localhost:8500/transactions/<short_id>
POST a new transaction
curl -u admin:password123 -H "Content-Type: application/json" -X POST \
-d '{"transactionType": "1", "amount": 5000, "sender": "M-Money", "receiver": "Alice Smith", "body": "Payment 5000 RWF"}' \
http://localhost:8500/transactions

PUT update transaction
curl -u admin:password123 -H "Content-Type: application/json" -X PUT \
-d '{"amount": 5500, "receiver": "Gasasira"}' \
http://localhost:8500/transactions/<short_id>
DELETE a transaction
curl -u admin:password123 -X DELETE http://localhost:8500/transactions/<short_id>
Notes

Transaction IDs are auto-generated short UUIDs (id) for easy retrieval.

Full UUID is stored internally as _full_id.

Authentication uses Basic Auth; for production, consider stronger alternatives (JWT, OAuth2).

API is in-memory; stopping the server will lose unsaved data unless exported manually.