import sqlite3
from passlib.hash import bcrypt



# Authenticate a user
def authenticate_user(username, password):
    user = get_user(username)
    if user and user[2] == hash_password(password):  # Check hashed password
        return user  # Return user details (id, username, role)
    return None

# Hash a password
def hash_password(password):
    return bcrypt.hash(password)

# Verify a password
def verify_password(password, hashed):
    return bcrypt.verify(password, hashed)

# Get user from the database
def get_user(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Add a user to the database
def add_user(username, hashed_password, role):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, (username, hashed_password, role))
    conn.commit()
    conn.close()
