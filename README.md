# Library Management System

## Overview
The Library Management System (LMS) is a Python-based command-line application designed to manage the operations of a library. It facilitates the management of books, users, authors, and genres. The system supports operations such as adding, borrowing, returning, and searching for books, along with managing user and author details.

## Features
- **Book Operations**: Add, borrow, return, update, delete, and search for books.
- **User Management**: Add, update, and delete users, and view user details.
- **Author Management**: Add, update, and delete authors, and view author details.
- **Genre Management**: Add, update, and delete genres, and view genre details.
- **Database Integration**: Uses MySQL to store and manage all data reliably and efficiently.

## Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- `mysql-connector-python` (A Python library for connecting to MySQL databases)

## Installation

### Step 1: Clone the Repository
```
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

### Step 2: Set Up the MySQL Database
- Start your MySQL server.
- Create a new database named `library_manager`:
  ```sql
  CREATE DATABASE library_manager;
  USE library_manager;
  ```
- Execute the SQL scripts found in `database_setup.sql` to create the necessary tables:
  ```sql
  source path/to/database_setup.sql;
  ```

### Step 3: Install Dependencies
```
pip install mysql-connector-python
```

## Configuration
Update the `db_config.py` file with your MySQL server's details:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'yourusername',
    'password': 'yourpassword',
    'database': 'library_manager'
}
```

## Running the Application
To start the application, run:
```
python main.py
```

## Contact
Kai Utterback -- ktutterback@gmail.com



