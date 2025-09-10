DROP DATABASE IF EXISTS ctf_db;

CREATE DATABASE ctf_db;
USE ctf_db;

CREATE TABLE challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT
);

INSERT INTO challenges (title, description) VALUES
('flag', 'This is not the flag. The flag is located in a different table.');

CREATE TABLE flag_parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_order INT,
    data TEXT
);

INSERT INTO flag_parts (part_order, data) VALUES
(2, 'cyBBd2Ukb21l'),
(3, 'fQ=='),
(1, 'RmxhZ3tTcS1p');
