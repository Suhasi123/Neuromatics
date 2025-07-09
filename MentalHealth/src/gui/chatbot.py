# chatbot_tkinter.py - Tkinter GUI for rule-based chatbot with quiz flow

import tkinter as tk
from chatbot import get_chatbot_response

def chatbot_gui():
    win = tk.Tk()
    win.title("Mental Health Chatbot")

    chat_display = tk.Text(win, height=25, width=70, state='disabled', wrap='word')
    chat_display.pack(padx=10, pady=10)

    user_input = tk.Entry(win, width=60)
    user_input.pack(side='left', padx=(10,0), pady=(0,10))

    def send_message():
        message = user_input.get()
        if not message.strip():
            return
        user_input.delete(0, tk.END)
        chat_display.config(state='normal')
        chat_display.insert(tk.END, "You: " + message + "\n")

        response = get_chatbot_response(message, session_id="tk_user")
        chat_display.insert(tk.END, "Bot: " + response + "\n")
        chat_display.config(state='disabled')
        chat_display.see(tk.END)

        if "Thank you for checking in" in response or "We have completed" in response:
            user_input.config(state='disabled')
            send_button.config(state='disabled')

    send_button = tk.Button(win, text="Send", command=send_message)
    send_button.pack(side='left', padx=(5,10), pady=(0,10))

    chat_display.config(state='normal')
    chat_display.insert(tk.END, "Bot: Hi! Let's start your mental health check-in.\n")
    chat_display.insert(tk.END, "Bot: " + get_chatbot_response("start", session_id="tk_user") + "\n")
    chat_display.config(state='disabled')

    win.mainloop()

if __name__ == "__main__":
    chatbot_gui()

