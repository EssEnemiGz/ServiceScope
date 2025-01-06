-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Route logs table
CREATE TABLE route_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    url TEXT NOT NULL,
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    headers JSONB DEFAULT '{}',
    params JSONB DEFAULT '{}',
    data JSONB DEFAULT '{}',
    json_payload JSONB DEFAULT '{}',
    response_time FLOAT NOT NULL,
    status_code INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- System logs table
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    cpu_usage FLOAT NOT NULL,
    ram_percentage FLOAT NOT NULL,
    ram_gb FLOAT NOT NULL,
    disk_usage FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Example user
INSERT INTO users (username, password, email) VALUES
('example_user', 'hashed_password_example', 'example@example.com');

-- Example route logs
INSERT INTO route_logs (user_id, url, method, response_time, status_code) VALUES
(1, 'http://127.0.0.1:5555', 'GET', 0.123, 200),
(1, 'http://127.0.0.1:5555/dashboard', 'GET', 0.456, 404);

-- Example system logs
INSERT INTO system_logs (user_id, cpu_usage, ram_percentage, ram_gb) VALUES
(1, 15.0, 45.0, 2.5),
(1, 20.0, 50.0, 3.0);