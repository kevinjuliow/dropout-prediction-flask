CREATE TABLE prediction_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    features TEXT,
    scaled_features TEXT,
    prediction VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
