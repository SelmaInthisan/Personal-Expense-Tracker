
from datetime import datetime
from database import get_connection


# 1. ADD BUDGET
def add_budget(user_id):

    # Get category ID
    try:
        category_id = int(input("Enter category ID: "))
    except ValueError:
        print("Invalid category ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the category belongs to this user
    cursor.execute(
        "SELECT category_id FROM Categories WHERE category_id = ? AND user_id = ?",
        (category_id, user_id)
    )

    category = cursor.fetchone()

    if category is None:
        print("Invalid category ID.")
        conn.close()
        return

    # Get monthly budget limit
    try:
        amount_limit = float(input("Enter monthly budget limit: "))
    except ValueError:
        print("Invalid amount. Enter a number.")
        conn.close()
        return

    if amount_limit <= 0:
        print("Budget must be greater than zero.")
        conn.close()
        return

    # Get month
    budget_month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(budget_month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM, for example 2026-10.")
        conn.close()
        return

    # Check whether a budget already exists
    cursor.execute(
        "SELECT budget_id FROM Budgets WHERE user_id = ? AND category_id = ? AND month = ?",
        (user_id, category_id, budget_month)
    )

    existing_budget = cursor.fetchone()

    if existing_budget is not None:
        print("A budget already exists for this category and month.")
        conn.close()
        return

    # Save budget
    cursor.execute(
        "INSERT INTO Budgets (user_id, category_id, amount_limit, month) VALUES (?, ?, ?, ?)",
        (user_id, category_id, amount_limit, budget_month)
    )

    conn.commit()
    conn.close()

    print("Budget added successfully!")



# 2. VIEW BUDGETS
def view_budgets(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Budgets.budget_id,
               Categories.category_name,
               Budgets.amount_limit,
               Budgets.month
        FROM Budgets
        JOIN Categories
        ON Budgets.category_id = Categories.category_id
        WHERE Budgets.user_id = ?
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()

    if len(records) == 0:
        print("No budgets found.")
        return

    print("\n--- Your Budgets ---")

    for record in records:
        print("Budget ID:", record[0])
        print("Category Name:", record[1])
        print("Monthly Limit:", record[2])
        print("Month:", record[3])
        print("--------------------")


# 3. UPDATE BUDGET
def update_budget(user_id):

    view_budgets(user_id)

    try:
        budget_id = int(input("Enter budget ID to update: "))
    except ValueError:
        print("Invalid budget ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the budget belongs to this user
    cursor.execute(
        "SELECT budget_id FROM Budgets WHERE budget_id = ? AND user_id = ?",
        (budget_id, user_id)
    )

    budget = cursor.fetchone()

    if budget is None:
        print("Budget not found.")
        conn.close()
        return

    # Get new limit
    try:
        new_limit = float(input("Enter new monthly budget limit: "))
    except ValueError:
        print("Invalid amount. Enter a number.")
        conn.close()
        return

    if new_limit <= 0:
        print("Budget must be greater than zero.")
        conn.close()
        return

    # Update budget
    cursor.execute(
        "UPDATE Budgets SET amount_limit = ? WHERE budget_id = ? AND user_id = ?",
        (new_limit, budget_id, user_id)
    )

    conn.commit()
    conn.close()

    print("Budget updated successfully!")


# 4. DELETE BUDGET
def delete_budget(user_id):

    view_budgets(user_id)

    try:
        budget_id = int(input("Enter budget ID to delete: "))
    except ValueError:
        print("Invalid budget ID. Enter a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the budget belongs to this user
    cursor.execute(
        "SELECT budget_id FROM Budgets WHERE budget_id = ? AND user_id = ?",
        (budget_id, user_id)
    )

    budget = cursor.fetchone()

    if budget is None:
        print("Budget not found.")
        conn.close()
        return

    confirm = input("Delete this budget? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        conn.close()
        return

    cursor.execute(
        "DELETE FROM Budgets WHERE budget_id = ? AND user_id = ?",
        (budget_id, user_id)
    )

    conn.commit()
    conn.close()

    print("Budget deleted successfully!")


# 5. MAIN MENU
if __name__ == "__main__":

    try:
        user_id = int(input("Enter your user ID: "))
    except ValueError:
        print("Invalid user ID.")
        raise SystemExit

    while True:

        print("\n--- Budget Management ---")
        print("1. Add Budget")
        print("2. View Budgets")
        print("3. Update Budget")
        print("4. Delete Budget")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_budget(user_id)

        elif choice == "2":
            view_budgets(user_id)

        elif choice == "3":
            update_budget(user_id)

        elif choice == "4":
            delete_budget(user_id)

        elif choice == "5":
            print("Exiting Budget Management.")
            break

        else:
            print("Invalid choice. Try again.")
