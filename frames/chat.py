from frames.MessagesFrame import MessagesFrame
import tkinter as tk
from tkinter import ttk
import requests

messages = [{"message": "Hello, world", "date": 15498487}]
messages_already_shown = []


class Chat(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.messages_frame = MessagesFrame(self)
        self.messages_frame.grid(row=0, column=0, stick='NSEW', pady=5)

        input_frame = ttk.Frame(self, padding=10)
        input_frame.grid(row=1, column=0, sticky="EW")

        message_fetch = ttk.Button(
            input_frame,
            text="Fetch",
            command=self.get_messages
        )
        message_fetch.pack()

    def get_messages(self):
        global messages
        messages = requests.get("http://167.99.63.70/messages").json()
        self.update_messages_widgets()

    def update_messages_widgets(self):
        global messages, messages_already_shown

        for message in messages:
            if (message['date'], message['message']) not in messages_already_shown:
                self.messages_frame.add_new_message(message)
                messages_already_shown.append((message['date'], message['message']))

