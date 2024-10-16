-- SQL script that creates a table users following these requirements 
-- id, email, name, country(US,CO and TN)
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    COUNTRY ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);

