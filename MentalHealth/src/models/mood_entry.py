# Model for mood entry
# src/models/mood_entry.py

class MoodEntry:
    def __init__(self, mood, note, date):
        self.mood = mood
        self.note = note
        self.date = date