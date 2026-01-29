CREATE DATABASE IF NOT EXISTS momo_sms_db;
USE momo_sms_db;

DROP TABLE IF EXISTS System_Logs;
DROP TABLE IF EXISTS Transaction_Merchant;
DROP TABLE IF EXISTS Merchants;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Transaction_Categories;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL COMMENT 'User phone number in international format',
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    account_status ENUM('active', 'suspended', 'closed') DEFAULT 'active',

    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^250[0-9]{9}$')
);

    CREATE INDEX idx_users_phone ON users(phone_number);
    CREATE INDEX idx_users_status ON users(account_status);
    CREATE INDEX idx_users_email ON users(email);


CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB ;

CREATE TABLE Merchants (
    merchant_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_name VARCHAR(100) NOT NULL,
    merchant_code VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_code (merchant_code),
    INDEX idx_phone (phone_number)
) ENGINE=InnoDB;

CREATE TABLE Transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT,
    category_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'RWF',
    transaction_fee DECIMAL(10,2) DEFAULT 0.00,
    transaction_date DATETIME NOT NULL,
    description TEXT,

    CONSTRAINT fk_sender
        FOREIGN KEY (sender_id)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_receiver
        FOREIGN KEY (receiver_id)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES Transaction_Categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_category (category_id),
    INDEX idx_date (transaction_date),
    INDEX idx_amount (amount)
) ENGINE=InnoDB;

CREATE TABLE Transaction_Merchant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    merchant_id INT NOT NULL,
    merchant_fee DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tm_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_tm_merchant
        FOREIGN KEY (merchant_id)
        REFERENCES Merchants(merchant_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_transaction_merchant UNIQUE (transaction_id, merchant_id),

    INDEX idx_transaction (transaction_id),
    INDEX idx_merchant (merchant_id)
) ENGINE=InnoDB;

CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_type ENUM('info', 'warning', 'error', 'debug') NOT NULL,
    message TEXT NOT NULL,
    transaction_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSON COMMENT 'Extra context data in JSON format',

    CONSTRAINT fk_log_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_type (log_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_transaction (transaction_id)
) ENGINE=InnoDB;


INSERT INTO Users (phone_number, full_name, email, registration_date, account_status) VALUES
 ('250788000001','Dianah Gasasira','d.gasasira@example.com','2025-01-10 08:15:00','active'),
 ('250788000002','Bior Majok','b.aguer@example.com','2025-01-11 09:30:00','active'),
 ('250788000003','Ayobamidele','ayobamidele@example.com','2025-01-12 10:45:00','active'),
 ('250788000004','Jesse','jesse@example.com','2025-01-13 11:20:00','suspended'),
 ('250788000005','James','james@example.com','2025-01-14 12:05:00','active');

 INSERT INTO Transaction_Categories (category_name, description) VALUES
('Groceries','Purchases at supermarkets and local shops'),
('Utilities','Electricity, water, internet bills'),
('Transport','Public transport, taxi and ride-share payments'),
('Entertainment','Movies, events, subscriptions'),
('Savings','Transfers to savings account or wallet');

INSERT INTO Merchants (merchant_name, merchant_code, phone_number) VALUES
('Kigali Supermarket','M001','250788111001'),
('City Electricity','M002','250788222002'),
('FastTaxis','M003','250788333003'),
('CinemaPlus','M004','250788444004'),
('SafeBank','M005','250788555005');

INSERT INTO Transactions (transaction_id, sender_id, receiver_id, category_id, amount, currency, transaction_fee, transaction_date, description) VALUES
('txn-0001',1,NULL,1,45250.00,'RWF',250.00,'2025-01-15 09:00:00','Grocery purchase at Kigali Supermarket'),
('txn-0002',2,NULL,2,125000.00,'RWF',500.00,'2025-01-16 10:30:00','Electricity bill payment to City Electricity'),
('txn-0003',3,NULL,3,3000.00,'RWF',20.00,'2025-01-16 14:05:00','Taxi payment via FastTaxis'),
('txn-0004',4,NULL,4,15000.00,'RWF',100.00,'2025-01-17 18:20:00','Movie tickets at CinemaPlus'),
('txn-0005',5,NULL,5,20000.00,'RWF',0.00,'2025-01-18 08:45:00','Transfer to savings at SafeBank');

INSERT INTO Transaction_Merchant (transaction_id, merchant_id, merchant_fee) VALUES
('txn-0001',1,200.00),
('txn-0002',2,300.00),
('txn-0003',3,10.00),
('txn-0004',4,50.00),
('txn-0005',5,0.00);

INSERT INTO System_Logs (log_type, message, transaction_id, additional_data) VALUES
('info','Transaction processed successfully','txn-0001','{"method":"USSD","attempts":1}'),
('warning','Delayed confirmation from merchant','txn-0002','{"merchant_response":"slow"}'),
('info','External provider callback received','txn-0003','{"provider":"FastTaxis"}'),
('debug','Seat reservation logged for cinema purchase','txn-0004','{"screen":"Screen 2","seats":["A5","A6"]}'),
('error','Failed to credit savings account','txn-0005','{"error_code":502,"reason":"bank_timeout"}'); 