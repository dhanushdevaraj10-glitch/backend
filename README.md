# Simple Flask + MySQL Student Registration System

## Setup Instructions

### 1. Install Required Packages
```bash
pip install flask mysql-connector-python
```

### 2. Create MySQL Database
Run the SQL commands in `database_setup.sql`:
```sql
CREATE DATABASE studentdb;
USE studentdb;
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

Or execute in MySQL:
```bash
mysql -u root -p < database_setup.sql
```

### 3. Update Database Password
In `app.py`, change this line to your MySQL password:
```python
password="root",  # Change this to your MySQL password
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
Go to: http://localhost:5000

## How It Works

1. **HTML Form** (index.html): User enters name and email
2. **Submit Button**: Sends data to Python backend via POST
3. **Python (app.py)**: Receives data and inserts into MySQL
4. **MySQL Database**: Stores the user information

## File Structure
```
backend/
├── app.py                 (Flask backend)
├── templates/
│   └── index.html        (HTML form)
├── database_setup.sql    (Database schema)
└── README.md
```

## Testing
1. Fill in the form with name and email
2. Click Submit
3. Check MySQL database to see the stored data:
```sql
SELECT * FROM users;
```
