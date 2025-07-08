# Unit tests for the application
# src/tests/test_app.py

import unittest
from src.app import MentalHealthApp

class TestMentalHealthApp(unittest.TestCase):
    def test_app_initialization(self):
        self.assertIsNotNone(MentalHealthApp)

if __name__ == "__main__":
    unittest.main()