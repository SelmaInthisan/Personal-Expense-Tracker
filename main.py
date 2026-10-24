
from auth import register_user, login_user
from database import create_tables, get_connection

from categories import (
    add_category, view_categories,
    update_category, delete_category
)

from transactions import (
    add_transaction, view_transactions,
    update_transaction, delete_transaction
)

from budgets import (
    add_budget, view_budgets,
    update_budget, delete_budget
)

from reports import (
    view_summary, monthly_report, category_report
)


# ==========================================
# USER MENU
# ==========================================
def user_menu(user):

    user_id = user["user_id"]
    username = user["username"]

    while True:
        print("\n" + "=" * 40)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 40)
        print("Welcome,", username)
        print("1. Manage Categories")
        print("2. Manage Transactions")
        print("3. Manage Budgets")
        print("4. Financial Reports")
        print("5. Logout")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            category_menu(user_id)

        elif choice == "2":
            transaction_menu(user_id)

        elif choice == "3":
            budget_menu(user_id)

        elif choice == "4":
            report_menu(user_id)

        elif choice == "5":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Choose 1-5.")


# ==========================================
# CATEGORY MENU
# ==========================================
def category_menu(user_id):

    while True:
        print("\n--- Category Management ---")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_category(user_id)

        elif choice == "2":
            view_categories(user_id)

        elif choice == "3":
            update_category(user_id)

        elif choice == "4":
            delete_category(user_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Choose 1-5.")


# ==========================================
# TRANSACTION MENU
# ==========================================
def transaction_menu(user_id):

    while True:
        print("\n--- Transaction Management ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction(user_id)

        elif choice == "2":
            view_transactions(user_id)

        elif choice == "3":
            update_transaction(user_id)

        elif choice == "4":
            delete_transaction(user_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Choose 1-5.")


# ==========================================
# BUDGET MENU
# ==========================================
def budget_menu(user_id):

    while True:
        print("\n--- Budget Management ---")
        print("1. Add Budget")
        print("2. View Budgets")
        print("3. Update Budget")
        print("4. Delete Budget")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_budget(user_id)

        elif choice == "2":
            view_budgets(user_id)

        elif choice == "3":
            update_budget(user_id)

        elif choice == "4":
            delete_budget(user_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Choose 1-5.")


# ==========================================
# REPORT MENU
# ==========================================
def report_menu(user_id):

    while True:
        print("\n--- Financial Reports ---")
        print("1. Financial Summary")
        print("2. Monthly Report")
        print("3. Category-wise Expenses")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_summary(user_id)

        elif choice == "2":
            monthly_report(user_id)

        elif choice == "3":
            category_report(user_id)

        elif choice == "4":
            break

        else:
            print("Invalid choice. Choose 1-4.")


# ==========================================
# ADMIN: VIEW REGISTERED USERS
# ==========================================
def view_registered_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, username, role FROM Users ORDER BY user_id"
    )

    users = cursor.fetchall()
    conn.close()

    print("\n--- Registered Users ---")

    if len(users) == 0:
        print("No users found.")
        return

    for user in users:
        print("User ID:", user[0])
        print("Username:", user[1])
        print("Role:", user[2])
        print("------------------------")


# ==========================================
# ADMIN: REMOVE UNAUTHORIZED USER
# ==========================================
def remove_user(admin_id):

    view_registered_users()

    try:
        user_id = int(input("Enter user ID to remove: "))
    except ValueError:
        print("Invalid user ID. Enter a number.")
        return

    # Prevent deleting the currently logged-in admin
    if user_id == admin_id:
        print("You cannot remove admin account.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check whether the account exists
        cursor.execute(
            "SELECT username, role FROM Users WHERE user_id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            print("User not found.")
            return

        # Prevent deleting another admin
        if user[1] == "admin":
            print("Admin accounts cannot be removed here.")
            return

        print("Selected username:", user[0])

        confirm = input(
            "Permanently remove this user and their financial data? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Removal cancelled.")
            return

        # Remove related records first
        cursor.execute(
            "DELETE FROM Budgets WHERE user_id = ?",
            (user_id,)
        )

        cursor.execute(
            "DELETE FROM Transactions WHERE user_id = ?",
            (user_id,)
        )

        cursor.execute(
            "DELETE FROM Categories WHERE user_id = ?",
            (user_id,)
        )

        # Remove the user account
        cursor.execute(
            "DELETE FROM Users WHERE user_id = ?",
            (user_id,)
        )

        conn.commit()
        print("User and associated records removed successfully.")

    except Exception as error:
        conn.rollback()
        print("Unable to remove user:", error)

    finally:
        conn.close()


# ==========================================
# ADMIN MENU
# ==========================================
def admin_menu(user):

    while True:
        print("\n" + "=" * 35)
        print("            ADMIN MENU")
        print("=" * 35)
        print("Welcome,", user["username"])
        print("1. View Registered Users")
        print("2. Remove Unauthorized User")
        print("3. Logout")
        print("=" * 35)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_registered_users()

        elif choice == "2":
            remove_user(user["user_id"])

        elif choice == "3":
            print("Admin logged out.")
            break

        else:
            print("Invalid choice. Choose 1-3.")


# ==========================================
# MAIN PROGRAM
# ==========================================
if __name__ == "__main__":

    create_tables()

    while True:
        print("\n" + "*" * 40)
        print("       PERSONAL EXPENSE TRACKER")
        print("*" * 40)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("*" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            username = input("Enter username: ").strip()
            password = input("Enter password: ")

            if username == "" or password == "":
                print("Username and password cannot be empty.")
            else:
                register_user(username, password)

        elif choice == "2":

            username = input("Enter username: ").strip()
            password = input("Enter password: ")

            user = login_user(username, password)

            if user is not None:
                print("Login successful!")

                if user["role"] == "admin":
                    admin_menu(user)
                else:
                    user_menu(user)

            else:
                print("Invalid username or password.")

        elif choice == "3":
            print("Thank you for using Personal Expense Tracker.")
            break

        else:
            print("Invalid choice. Choose 1-3.")
