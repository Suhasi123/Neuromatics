# chatbot_tkinter.py (Tkinter GUI using rule-based backend)

import tkinter as tk
from tkinter import ttk
from chatbot import get_chatbot_response

def chatbot_gui():
    win = tk.Tk()
    win.title("Mental Health Chatbot")

    chat_display = tk.Text(win, height=20, width=60, state='disabled', wrap='word')
    chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    user_input = tk.Entry(win, width=50)
    user_input.grid(row=1, column=0, padx=10, pady=10)

    def send_message():
        message = user_input.get()
        user_input.delete(0, tk.END)

        chat_display.config(state='normal')
        chat_display.insert(tk.END, "You: " + message + "\n")

        response = get_chatbot_response(message, session_id="tk_user")
        chat_display.insert(tk.END, "Bot: " + response + "\n")
        chat_display.config(state='disabled')
        chat_display.see(tk.END)

    send_button = tk.Button(win, text="Send", command=send_message)
    send_button.grid(row=1, column=1, padx=10, pady=10)

    chat_display.config(state='normal')
    chat_display.insert(tk.END, "Bot: Hi! Let's check in on your mood. " + get_chatbot_response("start", session_id="tk_user") + "\n")
    chat_display.config(state='disabled')

    win.mainloop()

if __name__ == "__main__":
    chatbot_gui()
