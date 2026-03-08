# MySQL Setup Documentation

This project uses MySQL as its primary database. Below are the steps to set up and configure MySQL for this application.

## 1. Prerequisites
- MySQL Server (version 8.0+ recommended)
- A MySQL user with necessary permissions to create databases and tables.

## 2. Initial Setup

### 2.1. Connect to MySQL
Use your preferred MySQL client (e.g., `mysql` CLI, MySQL Workbench, DBeaver) to connect to your server.

```bash
mysql -u root -p
```

### 2.2. Create Database
Create a database named `community_db`.

```sql
CREATE DATABASE community_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.3. Create User and Grant Permissions
It is recommended to create a dedicated user for the application.

```sql
CREATE USER 'insight_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON community_db.* TO 'insight_user'@'localhost';
FLUSH PRIVILEGES;
```

## 3. Application Configuration

### 3.1. Environment Variables
Create a `.env` file in the `backend/` directory with the following database connection details:

```env
MYSQL_USER=insight_user
MYSQL_PASSWORD=your_secure_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=community_db
SECRET_KEY=generate_a_random_secret_key
```

## 4. Database Migrations
The application will automatically attempt to create tables upon the first run, but for manual initialization, you can use the provided setup script.

```bash
# Example command to initialize the database (to be implemented)
python backend/scripts/init_db.py
```
