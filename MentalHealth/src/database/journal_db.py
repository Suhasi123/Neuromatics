import sqlite3
from datetime import datetime

DATABASE_NAME = 'journal.db'

def get_db_connection():
    """Creates and returns a new database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    # This allows accessing columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

def init_journal_db():
    """
    Initializes the database and creates the gratitude_entry table.
    Note: A 'user' table is also created to satisfy the foreign key,
    assuming it would be managed elsewhere in a full application.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # A user table is required for the foreign key constraint to work.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    )
    """)
    
    # The table for storing journal entries.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_entry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT NOT NULL,
        date DATETIME NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    """)
    
    conn.commit()
    conn.close()

def add_journal_entry(entry_text, user_id):
    """Saves a new gratitude entry to the database."""
    if not entry_text or not user_id:
        return
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO gratitude_entry (entry, user_id, date) VALUES (?, ?, ?)',
        (entry_text, user_id, datetime.utcnow())
    )
    conn.commit()
    conn.close()

def get_journal_entries(user_id):
    """Retrieves all gratitude entries for a specific user."""
    conn = get_db_connection()
    entries = conn.execute(
        'SELECT entry, date FROM gratitude_entry WHERE user_id = ? ORDER BY date DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return entries