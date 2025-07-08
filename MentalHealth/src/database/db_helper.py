# Helper functions for database operations
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class DBHelper:
    def __init__(self):
        self.db_name = 'mood_tracker.db'
        self.create_tables()

    def create_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.create_connection()
        mood_table_query = """
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            note TEXT,
            date TIMESTAMP
        )
        """
        user_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            education TEXT,
            dob DATE
        )
        """
        conn.execute(mood_table_query)
        conn.execute(user_table_query)
        conn.commit()
        conn.close()

    def insert_mood(self, mood, note):
        conn = self.create_connection()
        query = "INSERT INTO moods (mood, note, date) VALUES (?, ?, ?)"
        conn.execute(query, (mood, note, datetime.now()))
        conn.commit()
        conn.close()

    def get_mood_data(self):
        conn = self.create_connection()
        query = "SELECT mood, date FROM moods"
        cursor = conn.execute(query)
        data = [
            {'mood': row[0], 'date': row[1]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return data

    def create_user(self, username, password, name, age, gender, education, dob):
        conn = self.create_connection()
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, password, name, age, gender, education, dob) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(query, (username, hashed_password, name, age, gender, education, dob))
        conn.commit()
        conn.close()

    def get_user(self, username, password):
        conn = self.create_connection()
        query = "SELECT * FROM users WHERE username = ?"
        cursor = conn.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # Assuming password is stored in the 3rd column
            return user
        return None

    def get_user_by_id(self, user_id):
        conn = self.create_connection()
        query = "SELECT * FROM users WHERE id = ?"
        cursor = conn.execute(query, (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
