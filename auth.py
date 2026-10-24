
import hashlib
import sqlite3
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    if not username.strip() or not password:
        print("Username and password cannot be empty.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
            """,
            (username.strip(), hash_password(password), "user")
        )
        conn.commit()
        print("Registration successful!")

    except sqlite3.IntegrityError:
        print("Username already exists.")

    except sqlite3.Error as error:
        conn.rollback()
        print("Database error:", error)

    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id, username, password, role
            FROM Users
            WHERE username = ?
            """,
            (username.strip(),)
        )
        account = cursor.fetchone()

        if account and account[2] == hash_password(password):
            print("Login successful!")
            print("Welcome,", account[1])
            print("Role:", account[3])

            return {
                "user_id": account[0],
                "username": account[1],
                "role": account[3]
            }

        print("Invalid username or password.")
        return None

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        conn.close()


if __name__ == "__main__":
    print("1. Register")
    print("2. Login")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        username = input("Create username: ")
        password = input("Create password: ")
        register_user(username, password)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        login_user(username, password)

    else:
        print("Invalid choice.")
