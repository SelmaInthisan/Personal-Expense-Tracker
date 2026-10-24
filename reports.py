
from datetime import datetime
from database import get_connection


def view_summary(user_id):
    """Display the user's total income, expenses, and balance."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT transaction_type, COALESCE(SUM(amount), 0)
            FROM Transactions
            WHERE user_id = ?
            GROUP BY transaction_type
        """, (user_id,))

        totals = dict(cursor.fetchall())

        income = totals.get("income", 0)
        expenses = totals.get("expense", 0)
        balance = income - expenses

        print("\n========== FINANCIAL SUMMARY ==========")
        print(f"Total Income   : Rs. {income:.2f}")
        print(f"Total Expenses : Rs. {expenses:.2f}")
        print(f"Balance        : Rs. {balance:.2f}")
        print("=======================================")

    except Exception as error:
        print("Error generating financial summary:", error)

    finally:
        conn.close()


def monthly_report(user_id):
    """Display monthly income, expenses, savings, and budget status."""

    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Please use YYYY-MM, for example 2026-10.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Calculate monthly income and expenses.
        cursor.execute("""
            SELECT transaction_type, COALESCE(SUM(amount), 0)
            FROM Transactions
            WHERE user_id = ? AND date LIKE ?
            GROUP BY transaction_type
        """, (user_id, month + "%"))

        totals = dict(cursor.fetchall())

        income = totals.get("income", 0)
        expenses = totals.get("expense", 0)
        savings = income - expenses

        print("\n========== MONTHLY REPORT ==========")
        print(f"Month          : {month}")
        print(f"Total Income   : Rs. {income:.2f}")
        print(f"Total Expenses : Rs. {expenses:.2f}")
        print(f"Savings/Balance: Rs. {savings:.2f}")

        # Find the highest-spending category.
        cursor.execute("""
            SELECT c.category_name, SUM(t.amount) AS total
            FROM Transactions t
            JOIN Categories c
                ON t.category_id = c.category_id
            WHERE t.user_id = ?
              AND t.transaction_type = 'expense'
              AND t.date LIKE ?
            GROUP BY c.category_id, c.category_name
            ORDER BY total DESC
            LIMIT 1
        """, (user_id, month + "%"))

        highest = cursor.fetchone()

        if highest:
            print(
                f"Highest Spending Category: {highest[0]} "
                f"(Rs. {highest[1]:.2f})"
            )
        else:
            print("Highest Spending Category: No expenses recorded")

        # Calculate spending against each monthly budget.
        cursor.execute("""
            SELECT c.category_name,
                   b.amount_limit,
                   COALESCE(SUM(t.amount), 0) AS spent
            FROM Budgets b
            JOIN Categories c
                ON b.category_id = c.category_id
            LEFT JOIN Transactions t
                ON t.category_id = b.category_id
                AND t.user_id = b.user_id
                AND t.transaction_type = 'expense'
                AND t.date LIKE ?
            WHERE b.user_id = ?
              AND b.month = ?
            GROUP BY b.budget_id, c.category_name, b.amount_limit
        """, (month + "%", user_id, month))

        budgets = cursor.fetchall()

        print("\n---------- BUDGET STATUS ----------")

        if not budgets:
            print("No budgets set for this month.")

        for category, limit_amount, spent in budgets:
            if spent > limit_amount:
                status = "Budget Exceeded"
            elif spent == limit_amount:
                status = "Budget Reached"
            else:
                status = "Within Budget"

            print(f"\nCategory : {category}")
            print(f"Budget   : Rs. {limit_amount:.2f}")
            print(f"Spent    : Rs. {spent:.2f}")
            print(f"Status   : {status}")

        print("===================================")

    except Exception as error:
        print("Error generating monthly report:", error)

    finally:
        conn.close()


def category_report(user_id):
    """Display expense totals for each category."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT c.category_name,
                   COALESCE(SUM(t.amount), 0) AS total
            FROM Categories c
            LEFT JOIN Transactions t
                ON t.category_id = c.category_id
                AND t.user_id = c.user_id
                AND t.transaction_type = 'expense'
            WHERE c.user_id = ?
              AND c.category_type = 'expense'
            GROUP BY c.category_id, c.category_name
            ORDER BY total DESC, c.category_name
        """, (user_id,))

        categories = cursor.fetchall()

        print("\n======= CATEGORY-WISE EXPENSE REPORT =======")

        if not categories:
            print("No expense categories found.")
            return

        for category, total in categories:
            print(f"{category}: Rs. {total:.2f}")

        print("============================================")

    except Exception as error:
        print("Error generating category report:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    print("Run reports through main.py for the logged-in user's reports.")
