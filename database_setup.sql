-- Create Database
CREATE DATABASE studentdb;

-- Use the database
USE studentdb;

-- Create users table
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
