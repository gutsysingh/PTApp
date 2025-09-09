-- Initial schema (SQLite/Postgres compatible simple tables)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    name TEXT,
    password_hash TEXT,
    start_cash NUMERIC DEFAULT 100000.00
);
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    cash NUMERIC DEFAULT 100000.00
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    instrument TEXT,
    side TEXT,
    qty INTEGER,
    filled_qty INTEGER DEFAULT 0,
    price NUMERIC,
    order_type TEXT,
    status TEXT DEFAULT 'OPEN',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
