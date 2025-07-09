import sqlite3
from datetime import datetime

DATABASE_NAME = 'db.sqlite'

def get_db_connection():
    """Creates and returns a new database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_journal_db():
    """Initializes the database and creates necessary tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT)")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_entry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT NOT NULL,
        date DATETIME NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )""")
    conn.commit()
    conn.close()

def add_journal_entry(entry_text, user_id):
    """Saves a new gratitude entry to the database."""
    if not entry_text or not user_id:
        return
    conn = get_db_connection()
    conn.execute('INSERT INTO gratitude_entry (entry, user_id, date) VALUES (?, ?, ?)',
                 (entry_text, user_id, datetime.utcnow()))
    conn.commit()
    conn.close()

def get_journal_entries(user_id):
    """Retrieves all gratitude entries for a user, including their IDs."""
    conn = get_db_connection()
    # Select the 'id' as well, which is needed for the delete button.
    entries = conn.execute('SELECT id, entry, date FROM gratitude_entry WHERE user_id = ? ORDER BY date DESC',
                           (user_id,)).fetchall()
    conn.close()
    return entries

def delete_journal_entry(entry_id, user_id):
    """Deletes a specific journal entry belonging to a user."""
    conn = get_db_connection()
    # The WHERE clause ensures a user can only delete their own entries.
    conn.execute('DELETE FROM gratitude_entry WHERE id = ? AND user_id = ?',
                 (entry_id, user_id))
    conn.commit()
    conn.close()