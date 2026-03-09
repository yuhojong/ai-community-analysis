# MySQL Setup Documentation

This project uses MySQL as its primary database. Below are the steps to set up and configure MySQL for this application.

## 1. Prerequisites
- MySQL Server (version 8.0+ recommended)
- A MySQL user with necessary permissions to create databases and tables.

## 2. Initial Setup via CLI

You can set up the database, create a user, and generate the environment variables entirely through the command line.

### 2.1. Create Database and User
Use the `mysql` command-line tool with the `-e` flag to execute SQL commands directly. You will be prompted for your MySQL root password.

```bash
# 1. Create the database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS community_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Create the user and grant permissions
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'insight_user'@'localhost' IDENTIFIED BY 'your_secure_password'; GRANT ALL PRIVILEGES ON community_db.* TO 'insight_user'@'localhost'; FLUSH PRIVILEGES;"
```

### 2.2. Alternatively: Interactive Setup
If you prefer to connect to MySQL interactively, you can run:

```bash
mysql -u root -p
```

Then execute the following SQL commands:

```sql
CREATE DATABASE community_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'insight_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON community_db.* TO 'insight_user'@'localhost';
FLUSH PRIVILEGES;
```

## 3. Application Configuration

### 3.1. Create Environment Variables (.env) via CLI
You can automatically create the `.env` file in the `backend/` directory and generate a secure random `SECRET_KEY` using the following command:

```bash
cat <<EOF > backend/.env
MYSQL_USER=insight_user
MYSQL_PASSWORD=your_secure_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=community_db
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

## 4. Database Migrations
The application will automatically attempt to create tables upon the first run. For manual initialization, you can run the initialization script directly. Make sure you have activated your virtual environment and set the `PYTHONPATH`.

```bash
# Initialize the database manually
PYTHONPATH=. python3 backend/scripts/trigger.py init_db
```
