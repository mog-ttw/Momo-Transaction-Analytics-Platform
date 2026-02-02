<<<<<<< HEAD
# MoMo Transaction Analytics Platform - API Documentation

## Overview

The MoMo Transaction Analytics API is a RESTful service for managing Mobile Money transaction data. It provides endpoints to create, read, update, and delete transaction records with built-in authentication and soft-delete functionality.

**Base URL:** `http://localhost:5000`

**API Version:** 1.0

## Authentication

All endpoints require **HTTP Basic Authentication**.

### Credentials
- **Username:** `admin`
- **Password:** `admin@123`

### Authentication Headers
```
Authorization: Basic YWRtaW46YWRtaW5AMTIz
```

### Response on Invalid Credentials
```json
{
  "error": "401 Unauthorized",
  "message": "Invalid or missing credentials. Access denied."
}
```

---

## Endpoints

### 1. List All Transactions

**GET** `/transactions`

Retrieve all active (non-deleted) transactions from the database.

#### Request
```bash
curl -u admin:admin@123 http://localhost:5000/transactions
```

#### Response
**Status Code:** 200 OK

```json
[
  {
    "transaction_id": 1,
    "transaction_ref": "TRX001",
    "category_id": 1,
    "amount": 50000.00,
    "fee": 500.00,
    "transaction_date": "2026-02-02 10:30:45",
    "raw_sms": "You have received 50000 XAF from +237...",
    "is_deleted": false,
    "deleted_at": null,
    "created_at": "2026-02-02 10:30:45"
  },
  {
    "transaction_id": 2,
    "transaction_ref": "TRX002",
    "category_id": 2,
    "amount": 25000.00,
    "fee": 250.00,
    "transaction_date": "2026-02-02 11:15:30",
    "raw_sms": "You have sent 25000 XAF to +237...",
    "is_deleted": false,
    "deleted_at": null,
    "created_at": "2026-02-02 11:15:30"
  }
]
```

#### Error Response
**Status Code:** 401 Unauthorized

```json
{
  "error": "401 Unauthorized",
  "message": "Invalid or missing credentials. Access denied."
}
```

---

### 2. Get Transaction by ID

**GET** `/transactions/<id>`

Retrieve a specific transaction by its ID.

#### Request Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Transaction ID (required, in URL path) |

#### Request Example
```bash
curl -u admin:admin@123 http://localhost:5000/transactions/1
```

#### Response
**Status Code:** 200 OK

```json
{
  "transaction_id": 1,
  "transaction_ref": "TRX001",
  "category_id": 1,
  "amount": 50000.00,
  "fee": 500.00,
  "transaction_date": "2026-02-02 10:30:45",
  "raw_sms": "You have received 50000 XAF from +237...",
  "is_deleted": false,
  "deleted_at": null,
  "created_at": "2026-02-02 10:30:45"
}
```

#### Error Response
**Status Code:** 404 Not Found

```json
{
  "error": "Transaction not found"
}
```

---

### 3. Create a New Transaction

**POST** `/transactions`

Add a new transaction to the database.

#### Request Headers
```
Authorization: Basic YWRtaW46YWRtaW5AMTIz
Content-Type: application/json
```

#### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transaction_ref` | string | Yes | Unique transaction reference |
| `category_id` | integer | Yes | Category ID for classification |
| `amount` | number | Yes | Transaction amount |
| `fee` | number | No | Transaction fee (default: 0.0) |
| `transaction_date` | string | No | Date/time in format YYYY-MM-DD HH:MM:SS (default: current timestamp) |
| `raw_sms` | string | Yes | Original SMS message content |

#### Request Example
```bash
curl -u admin:admin@123 -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_ref": "TRX003",
    "category_id": 1,
    "amount": 75000.00,
    "fee": 750.00,
    "transaction_date": "2026-02-02 12:00:00",
    "raw_sms": "You have received 75000 XAF from John Doe"
  }'
```

#### Response
**Status Code:** 201 Created

```json
{
  "message": "Transaction created",
  "id": 3
}
```

#### Error Response
**Status Code:** 400 Bad Request

```json
{
  "error": "Column 'column_name' cannot be null"
}
```

---

### 4. Update a Transaction

**PUT** `/transactions/<id>`

Update an existing transaction record. Only provided fields will be updated.

#### Request Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Transaction ID (required, in URL path) |

#### Request Headers
```
Authorization: Basic YWRtaW46YWRtaW5AMTIz
Content-Type: application/json
```

#### Request Body
All transaction fields are optional. Only include fields you want to update.

```json
{
  "amount": 80000.00,
  "fee": 800.00,
  "category_id": 2
}
```

#### Request Example
```bash
curl -u admin:admin@123 -X PUT http://localhost:5000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 80000.00,
    "fee": 800.00
  }'
```

#### Response
**Status Code:** 200 OK

```json
{
  "message": "Transaction updated"
}
```

#### Error Responses

**Status Code:** 400 Bad Request
```json
{
  "error": "No data provided"
}
```

**Status Code:** 404 Not Found
```json
{
  "error": "Transaction not found"
}
```

---

### 5. Delete a Transaction

**DELETE** `/transactions/<id>`

Soft delete a transaction record. The record is not removed from the database but marked as deleted.

#### Request Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Transaction ID (required, in URL path) |

#### Request Example
```bash
curl -u admin:admin@123 -X DELETE http://localhost:5000/transactions/1
```

#### Response
**Status Code:** 200 OK

```json
{
  "message": "Transaction deleted (soft delete)"
}
```

#### Error Response
**Status Code:** 404 Not Found

```json
{
  "error": "Transaction not found"
}
```

---

## Data Models

### Transaction Object

```json
{
  "transaction_id": "integer - Unique identifier",
  "transaction_ref": "string - Unique reference code",
  "category_id": "integer - Category classification ID",
  "amount": "number - Transaction amount",
  "fee": "number - Transaction fee",
  "transaction_date": "string - Transaction date/time (YYYY-MM-DD HH:MM:SS)",
  "raw_sms": "string - Original SMS message",
  "is_deleted": "boolean - Soft delete flag",
  "deleted_at": "string - Timestamp of deletion (YYYY-MM-DD HH:MM:SS) or null",
  "created_at": "string - Record creation timestamp (YYYY-MM-DD HH:MM:SS)"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource successfully created |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Invalid or missing credentials |
| 404 | Not Found - Resource does not exist |
| 500 | Internal Server Error - Server error |

---

## Database Configuration

The API connects to a MySQL database with the following configuration:

```
Host: localhost
User: root
Password: Philosophy@360
Database: momo_sms_db
```

---

## Soft Delete Behavior

Deleted transactions are not permanently removed from the database. Instead:
- The `is_deleted` field is set to `TRUE`
- The `deleted_at` field records the deletion timestamp
- All GET requests exclude soft-deleted records
- Soft-deleted records can be recovered by updating `is_deleted` to `FALSE`

---

## Error Handling

All errors are returned as JSON objects with an `error` field describing the issue:

```json
{
  "error": "Error description"
}
```

Common error scenarios:
- Missing required authentication credentials → 401
- Invalid transaction ID → 404
- Malformed request body → 400
- Database connection failures → 500

---

## Examples

### Complete CRUD Workflow

**1. Create a transaction:**
```bash
curl -u admin:admin@123 -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_ref":"TRX100","category_id":1,"amount":10000,"raw_sms":"SMS text"}'
```

**2. Retrieve the transaction:**
```bash
curl -u admin:admin@123 http://localhost:5000/transactions/1
```

**3. Update the transaction:**
```bash
curl -u admin:admin@123 -X PUT http://localhost:5000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount":12000}'
```

**4. Delete the transaction:**
```bash
curl -u admin:admin@123 -X DELETE http://localhost:5000/transactions/1
```

---

## Running the API Server

To start the API server, run:

```bash
python api/server.py
```

The server will start on `http://localhost:5000` in debug mode.

---

**Last Updated:** February 2, 2026
=======
# MoMo Transactions API Documentation

This document describes the REST API for Mobile Money (MoMo) transactions. It covers all endpoints, request/response formats, authentication, and error codes.

---

## Authentication

All endpoints are protected with **Basic Authentication**.  
Include the `Authorization` header in every request:

Authorization: Basic <base64(username:password)>


**Default users for testing:**

| Username   | Password      |
|-----------|---------------|
| admin     | password123   |
| MomoUser1 | $Momo123      |
| MomoUser2 | $Momo456      |

> Note: Base64 encoding of `username:password` is required.

**Example using curl:**

```bash
curl -u admin:password123 http://localhost:8500/transactions
Endpoints
1. GET /transactions
Retrieve a list of all transactions. Optional query parameter type filters by transaction type.

Request:

GET /transactions
Authorization: Basic <encoded_credentials>
Query Example:

GET /transactions?type=1
Response Example:

{
  "success": true,
  "count": 3,
  "statusCode": 200,
  "transactions": [
    {
      "id": "1f1e88",
      "_full_id": "1f1e886d-2352-4a6c-8586-40ffdee85d0f",
      "transactionType": 1,
      "amount": 5500,
      "sender": "M-Money",
      "receiver": "Gasasira",
      "createdAt": "2026-01-28T15:24:01.916912",
      "body": "TxId: custom12345. Your payment of 5500 RWF to Gasasira..."
    }
  ]
}
Error Codes:

Code	Message
401	Invalid credentials
404	Endpoint not found
2. GET /transactions/{id}
Retrieve a single transaction by its short ID.

Request:

GET /transactions/1f1e88
Authorization: Basic <encoded_credentials>
Response Example:

{
  "success": true,
  "transaction": {
    "id": "1f1e88",
    "_full_id": "1f1e886d-2352-4a6c-8586-40ffdee85d0f",
    "transactionType": 1,
    "amount": 5500,
    "sender": "M-Money",
    "receiver": "Gasasira",
    "createdAt": "2026-01-28T15:24:01.916912",
    "body": "TxId: custom12345. Your payment of 5500 RWF to Gasasira..."
  }
}
Error Codes:

Code	Message
401	Invalid credentials
404	Transaction not found
3. POST /transactions
Create a new transaction. The system auto-generates the transaction ID.

Request:

POST /transactions
Authorization: Basic <encoded_credentials>
Content-Type: application/json
Body Example:

{
  "transactionType": "1",
  "amount": 5000,
  "sender": "M-Money",
  "receiver": "Alice Smith",
  "body": "TxId: custom12345. Your payment of 5000 RWF to Alice Smith..."
}
Response Example:

{
  "success": true,
  "statusCode": 201,
  "transaction": {
    "id": "2f26bd",
    "_full_id": "2f26bd12-3f4a-4b8c-9c50-85c4c0e9a456",
    "transactionType": 1,
    "amount": 5000,
    "sender": "M-Money",
    "receiver": "Alice Smith",
    "createdAt": "2026-01-28T15:07:58.122817",
    "body": "TxId: custom12345. Your payment of 5000 RWF to Alice Smith..."
  }
}
Error Codes:

Code	Message
400	Missing required fields
401	Invalid credentials
4. PUT /transactions/{id}
Update an existing transaction.

Request:

PUT /transactions/2f26bd
Authorization: Basic <encoded_credentials>
Content-Type: application/json
Body Example:

{
  "amount": 5500,
  "receiver": "Gasasira"
}
Response Example:

{
  "success": true,
  "statusCode": 200,
  "transaction": {
    "id": "2f26bd",
    "_full_id": "2f26bd12-3f4a-4b8c-9c50-85c4c0e9a456",
    "transactionType": 1,
    "amount": 5500,
    "sender": "M-Money",
    "receiver": "Gasasira",
    "createdAt": "2026-01-28T15:07:58.122817",
    "updatedAt": "2026-01-28T15:25:43.579892",
    "body": "TxId: custom12345. Your payment of 5000 RWF to Alice Smith..."
  }
}
Error Codes:

Code	Message
401	Invalid credentials
404	Transaction not found
5. DELETE /transactions/{id}
Delete a transaction by its short ID.

Request:

DELETE /transactions/2f26bd
Authorization: Basic <encoded_credentials>
Response Example:

{
  "success": true,
  "statusCode": 200,
  "message": "Deleted",
  "transaction": {
    "id": "2f26bd",
    "_full_id": "2f26bd12-3f4a-4b8c-9c50-85c4c0e9a456",
    "transactionType": 1,
    "amount": 5500,
    "sender": "M-Money",
    "receiver": "Gasasira",
    "createdAt": "2026-01-28T15:07:58.122817",
    "body": "TxId: custom12345. Your payment of 5000 RWF to Alice Smith..."
  }
}
Error Codes:

Code	Message
401	Invalid credentials
404	Transaction not found
Notes
id → short UUID for easy retrieval

_full_id → full UUID stored internally

Basic Auth is weak; consider JWT or OAuth2 for production

All timestamps are ISO 8601 format

Query parameter type filters transactions by type
>>>>>>> 6410c4a (Initial commit: MoMo API with XML parsing, CRUD, DSA, and docs)
