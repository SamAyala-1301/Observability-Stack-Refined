-- transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    user_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO transactions (amount, status, user_id) VALUES
    (99.99, 'completed', 'user_001'),
    (149.50, 'completed', 'user_002'),
    (25.00, 'pending', 'user_003'),
    (599.99, 'completed', 'user_004'),
    (12.50, 'failed', 'user_005');

-- Index for better performance
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);