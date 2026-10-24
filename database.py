
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "expense_tracker.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK(role IN ('user', 'admin'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            category_type TEXT NOT NULL
                CHECK(category_type IN ('income', 'expense')),
            FOREIGN KEY (user_id)
                REFERENCES Users(user_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            transaction_type TEXT NOT NULL
                CHECK(transaction_type IN ('income', 'expense')),
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES Users(user_id),
            FOREIGN KEY (category_id)
                REFERENCES Categories(category_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount_limit REAL NOT NULL CHECK(amount_limit > 0),
            month TEXT NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES Users(user_id),
            FOREIGN KEY (category_id)
                REFERENCES Categories(category_id),
            UNIQUE(user_id, category_id, month)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
    print("Database location:", DB_NAME)
