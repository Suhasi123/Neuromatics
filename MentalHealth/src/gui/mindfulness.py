import tkinter as tk
import webbrowser

class Mindfulness:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Mindfulness Exercises")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Guided Mindfulness Exercises").pack(pady=10)

        # Add buttons for mindfulness exercises
        tk.Button(self.window, text="Breathing Exercise", command=lambda: self.open_exercise('breathing')).pack(pady=5)
        tk.Button(self.window, text="Body Scan Meditation", command=lambda: self.open_exercise('body_scan')).pack(pady=5)
        tk.Button(self.window, text="Mindful Walking", command=lambda: self.open_exercise('walking')).pack(pady=5)
        tk.Button(self.window, text="Mindful Eating", command=lambda: self.open_exercise('eating')).pack(pady=5)

        # Close button
        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def open_exercise(self, exercise_type):
        url = f"http://127.0.0.1:5000/mindfulness#{exercise_type}"
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main Tkinter window
    app = Mindfulness(root)
    root.mainloop()
