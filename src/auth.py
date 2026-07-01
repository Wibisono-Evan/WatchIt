import bcrypt
import sqlite3
from src.database import get_connection
from src.display import get_time_based_greeting

# Register


def register_user():
    username = str(input("Username: "))
    password = ""
    password_verify = " "
    while password != password_verify:
        password = input("Password: ")
        password_verify = input("Confirm Password: ")

    # Hash password by converting password to bytes and generating a salt
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(rounds=12))

    # Connect to DB
    conn = get_connection()
    cursor = conn.cursor()

    # Add new user to database
    try:
        cursor.execute("""INSERT INTO users(username, password) VALUES(?, ?)""",
                       (username, hashed_password))
        conn.commit()
        print(f"Welcome to WatchIt, {username}!")
        return username
    except sqlite3.IntegrityError:
        print("Username is already taken, please choose another")
        return None
    finally:
        conn.close()


def user_login():
    username = str(input("Username: "))
    password = str(input("Password: "))

    # Connect to DB
    conn = get_connection()
    cursor = conn.cursor()

    # Lookup username AND retrieve
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()

    # Check if username exists
    if user_info is None:
        print(
            f"Sorry. We can't find {username} in our list. Double-check your username or register for new account :)")
        conn.close()
        return None

    # Check if password matches
    if not bcrypt.checkpw(password.encode("utf-8"), user_info["password"]):
        print(f"Sorry, incorrect password for {username}.")
        conn.close()
        return None

    # Success!
    print(f"{get_time_based_greeting()} {username}!")
    conn.close()
    return user_info["id"]
