# GUI for mood tracking
# src/gui/mood_tracker.py

# src/gui/mood_tracker.py

# src/gui/mood_tracker.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database.db_helper import DBHelper

class MoodTracker:
    def __init__(self, root):
        self.root = root
        self.db_helper = DBHelper()
        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Mood Tracker")

        tk.Label(self.window, text="Select your mood:").pack()
        self.mood_var = tk.StringVar(value="Happy")
        moods = ["Happy", "Sad", "Neutral", "Angry", "Anxious"]
        self.mood_menu = ttk.Combobox(self.window, textvariable=self.mood_var, values=moods)
        self.mood_menu.pack()

        tk.Label(self.window, text="Add a note:").pack()
        self.note_text = tk.Text(self.window, height=5, width=30)
        self.note_text.pack()

        tk.Button(self.window, text="Save Mood", command=self.save_mood).pack()

    def save_mood(self):
        mood = self.mood_var.get()
        note = self.note_text.get("1.0", tk.END).strip()
        self.db_helper.insert_mood(mood, note)
        messagebox.showinfo("Success", "Mood saved successfully!")
        self.window.destroy()