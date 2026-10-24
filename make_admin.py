
from database import get_connection

username = input("Enter username to make admin: ").strip()

if not username:
    print("Username cannot be empty.")

else:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check whether the username exists.
        cursor.execute(
            "SELECT user_id, role FROM Users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if user is None:
            print("Username not found.")

        elif user[1] == "admin":
            print("This user is already an administrator.")

        else:
            # Check whether another administrator exists.
            cursor.execute(
                "SELECT username FROM Users WHERE role = 'admin' LIMIT 1"
            )
            existing_admin = cursor.fetchone()

            if existing_admin:
                print(
                    "An administrator already exists:",
                    existing_admin[0]
                )
                print("Only one administrator is allowed.")

            else:
                cursor.execute(
                    "UPDATE Users SET role = 'admin' WHERE username = ?",
                    (username,)
                )
                conn.commit()
                print("Administrator created successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()
