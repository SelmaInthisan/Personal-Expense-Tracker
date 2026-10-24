
from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT user_id, username, role FROM Users")

users = cursor.fetchall()

for user in users:
    print("ID:", user[0], "| Username:", user[1], "| Role:", user[2])

conn.close()
