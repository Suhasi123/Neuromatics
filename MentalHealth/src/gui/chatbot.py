# GUI for chatbot interaction (optional)
import tkinter as tk
from tkinter import ttk

# Importing the chatbot module
from chatbot import Chatbot

def chatbot_gui():
    new_chatbot = Chatbot()
    new_chatbot.load_chatbot()
    # Create instance
    win = tk.Tk()
    ekd = ttk.Notebook(win)
    ekd.pack(fill='both', expand='yes')
    # Add a tab
    tab1 = ttk.Frame(ekd)
    ekd.add(tab1, text='Chatbot')
    

    # Adding a Label
    a_label = ttk.Label(tab1, text="Chatbot")
    a_label.grid(column=0, row=0)
    data=ttk.Label(tab1, text="Enter your message here:")
    data.grid(column=0, row=1)
    # Adding a Textbox Entry widget
    user_message = ttk.Entry(tab1, width=50)
    user_message.grid(column=1, row=1)
    # Adding a Button
    def click_me():
        user_input = user_message.get()
        user_input = user_input.lower()
        response = new_chatbot.chatbot_response(user_input)
        chatbot_response = ttk.Label(tab1, text=response)
        chatbot_response.grid(column=1, row=3)
        user_message.delete(0, 'end')
    action = ttk.Button(tab1, text="Send", command=click_me)
    action.grid(column=2, row=1)
    # Start GUI
    win.mainloop()

if __name__ == "__main__":
    chatbot_gui()
