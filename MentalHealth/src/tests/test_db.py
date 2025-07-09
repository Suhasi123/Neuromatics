# Unit tests for database operations
# src/tests/test_db.py

import unittest
from database.db_helper import DBHelper

class TestDBHelper(unittest.TestCase):
    def setUp(self):
        self.db_helper = DBHelper()

    def test_insert_mood(self):
        self.db_helper.insert_mood("Happy", "Feeling great!")
        data = self.db_helper.get_mood_data()
        self.assertGreater(len(data), 0)

if __name__ == "__main__":
    unittest.main()