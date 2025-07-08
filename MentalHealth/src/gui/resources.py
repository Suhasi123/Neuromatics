# GUI for resource section
# src/gui/resources.py

import tkinter as tk

class Resources:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Resources")

        tk.Label(self.window, text="Mental Health Resources Coming Soon!").pack()