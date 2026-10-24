
from datetime import datetime
from database import get_connection


# 1. ADD TRANSACTION
def add_transaction(user_id):

    # Get category ID
    try:
        category_id = int(input("Enter category ID: "))
    except ValueError:
        print("Invalid category ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether category belongs to this user
    cursor.execute(
        "SELECT category_id FROM Categories WHERE category_id = ? AND user_id = ?",
        (category_id, user_id)
    )

    category = cursor.fetchone()

    if category is None:
        print("Invalid category ID.")
        conn.close()
        return

    # Get amount
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Enter a number.")
        conn.close()
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        conn.close()
        return

    # Get transaction type
    transaction_type = input(
        "Enter type (income/expense): "
    ).strip().lower()

    if transaction_type != "income" and transaction_type != "expense":
        print("Invalid type. Enter income or expense.")
        conn.close()
        return

    # Check whether category type matches
    cursor.execute(
        "SELECT category_id FROM Categories WHERE category_id = ? AND user_id = ? AND category_type = ?",
        (category_id, user_id, transaction_type)
    )

    category = cursor.fetchone()

    if category is None:
        print("Category type does not match.")
        conn.close()
        return

    # Get description
    description = input("Enter description: ")

    # Get and validate date
    transaction_date = input(
        "Enter date (YYYY-MM-DD): "
    ).strip()

    try:
        datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        conn.close()
        return

    # Save transaction
    cursor.execute(
        "INSERT INTO Transactions (user_id, category_id, amount, transaction_type, description, date) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, category_id, amount, transaction_type,
         description, transaction_date)
    )

    conn.commit()
    conn.close()

    print("Transaction added successfully!")


# 2. VIEW TRANSACTIONS
def view_transactions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT transaction_id, category_id, amount, transaction_type, description, date FROM Transactions WHERE user_id = ?",
        (user_id,)
    )

    records = cursor.fetchall()
    conn.close()

    if len(records) == 0:
        print("No transactions found.")
        return

    print("\n--- Your Transactions ---")

    for record in records:
        print("Transaction ID:", record[0])
        print("Category ID:", record[1])
        print("Amount:", record[2])
        print("Type:", record[3])
        print("Description:", record[4])
        print("Date:", record[5])
        print("------------------------")


# 3. UPDATE TRANSACTION
def update_transaction(user_id):

    view_transactions(user_id)

    try:
        transaction_id = int(
            input("Enter transaction ID to update: ")
        )
    except ValueError:
        print("Invalid transaction ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether transaction belongs to this user
    cursor.execute(
        "SELECT transaction_id FROM Transactions WHERE transaction_id = ? AND user_id = ?",
        (transaction_id, user_id)
    )

    transaction = cursor.fetchone()

    if transaction is None:
        print("Transaction not found.")
        conn.close()
        return

    # Get new amount
    try:
        amount = float(input("Enter new amount: "))
    except ValueError:
        print("Invalid amount. Enter a number.")
        conn.close()
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        conn.close()
        return

    # Update amount
    cursor.execute(
        "UPDATE Transactions SET amount = ? WHERE transaction_id = ? AND user_id = ?",
        (amount, transaction_id, user_id)
    )

    conn.commit()
    conn.close()

    print("Transaction updated successfully!")


# 4. DELETE TRANSACTION
def delete_transaction(user_id):

    view_transactions(user_id)

    try:
        transaction_id = int(
            input("Enter transaction ID to delete: ")
        )
    except ValueError:
        print("Invalid transaction ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether transaction belongs to this user
    cursor.execute(
        "SELECT transaction_id FROM Transactions WHERE transaction_id = ? AND user_id = ?",
        (transaction_id, user_id)
    )

    transaction = cursor.fetchone()

    if transaction is None:
        print("Transaction not found.")
        conn.close()
        return

    # Confirm deletion
    confirm = input(
        "Are you sure you want to delete it? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        conn.close()
        return

    cursor.execute(
        "DELETE FROM Transactions WHERE transaction_id = ? AND user_id = ?",
        (transaction_id, user_id)
    )

    conn.commit()
    conn.close()

    print("Transaction deleted successfully!")


# 5. MAIN MENU
if __name__ == "__main__":

    try:
        user_id = int(input("Enter your user ID: "))
    except ValueError:
        print("Invalid user ID.")
        raise SystemExit

    while True:

        print("\n--- Transaction Management ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_transaction(user_id)

        elif choice == "2":
            view_transactions(user_id)

        elif choice == "3":
            update_transaction(user_id)

        elif choice == "4":
            delete_transaction(user_id)

        elif choice == "5":
            print("Exiting Transaction Management.")
            break

        else:
            print("Invalid choice. Try again.")
