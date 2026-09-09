CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO messages (message)
VALUES
    ('Hello from MySQL!'),
    ('Docker Compose is working!'),
    ('DevOps lab is running!');