-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    balance DECIMAL(12, 2) DEFAULT 0.00 CHECK (balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table (Ledger)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('deposit', 'transfer_in', 'transfer_out')),
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    related_user VARCHAR(50), -- Name of the other party in transfers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes to optimize frequent searches
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);