# GUI for mood analysis and visualization
# src/gui/visualization.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.db_helper import DBHelper

class Visualization:
    def __init__(self, root):
        self.root = root
        self.db_helper = DBHelper()
        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Mood Visualization")

        data = self.db_helper.get_mood_data()
        moods = [entry['mood'] for entry in data]
        dates = [entry['date'] for entry in data]

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, moods, marker='o')
        ax.set_title("Mood Trends Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood")

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack()