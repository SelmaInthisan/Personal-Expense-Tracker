
from database import get_connection


def add_category(user_id):
    name = input("Enter category name: ").strip()
    category_type = input(
        "Enter type (income/expense): "
    ).strip().lower()

    if not name:
        print("Category name cannot be empty.")
        return

    if category_type not in ("income", "expense"):
        print("Invalid category type.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Categories
            (user_id, category_name, category_type)
            VALUES (?, ?, ?)
            """,
            (user_id, name, category_type)
        )
        conn.commit()
        print("Category added successfully!")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def view_categories(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category_id, category_name, category_type
        FROM Categories
        WHERE user_id = ?
        ORDER BY category_id
        """,
        (user_id,)
    )

    categories = cursor.fetchall()

    if categories:
        print("\n--- Your Categories ---")
        for category in categories:
            print(
                category[0],
                category[1],
                "-",
                category[2]
            )
    else:
        print("No categories found.")

    conn.close()


def update_category(user_id):
    view_categories(user_id)

    try:
        category_id = int(input("Enter category ID to update: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    name = input("Enter new category name: ").strip()

    if not name:
        print("Category name cannot be empty.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Categories
        SET category_name = ?
        WHERE category_id = ? AND user_id = ?
        """,
        (name, category_id, user_id)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Category updated successfully!")
    else:
        print("Category not found.")

    conn.close()


def delete_category(user_id):
    view_categories(user_id)

    try:
        category_id = int(input("Enter category ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM Categories
        WHERE category_id = ? AND user_id = ?
        """,
        (category_id, user_id)
    )

    try:
        conn.commit()

        if cursor.rowcount > 0:
            print("Category deleted successfully!")
        else:
            print("Category not found.")

    except Exception as error:
        conn.rollback()
        print("Could not delete category:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    user_id = int(input("Enter your logged-in user ID: "))

    while True:
        print("\n--- Category Management ---")
        print("1. Add category")
        print("2. View categories")
        print("3. Update category")
        print("4. Delete category")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

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
            print("Invalid choice.")
