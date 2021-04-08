from frames.MessagesFrame import MessagesFrame
import tkinter as tk
from tkinter import ttk
import requests

messages = [{"message": "Hello, world", "date": 15498487}]
messages_already_shown = []


class Chat(ttk.Frame):
    def __init__(self, container, background, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # -- MESSAGES FRAME --
        self.messages_frame = MessagesFrame(self,
                                            background,
                                            style='Messages.TFrame')
        self.messages_frame.grid(row=0, column=0, stick='NSEW', pady=10)
        # --

        # -- INPUTS AND BUTTONS --
        input_frame = ttk.Frame(self, padding=10, style='Controls.TFrame')
        input_frame.grid(row=1, column=0, sticky="EW")

        self.message_input = tk.Text(input_frame, height=3)
        self.message_input.pack(expand=True, fill='both', side='left', padx=(0, 10))
        self.message_input.focus()

        message_submit = ttk.Button(input_frame,
                                    text='Send',
                                    style='SendButton.TButton',
                                    command=self.post_message)
        message_submit.pack(expand='True')

        message_fetch = ttk.Button(input_frame,
                                   text="Fetch",
                                   style='FetchButton.TButton',
                                   command=self.get_messages)
        message_fetch.pack()
        # --

        # -- EVENTS --
        self.message_input.bind('<Return>', self.post_message)
        self.message_input.bind('<KP_Enter>', self.post_message)

    def post_message(self, *args):
        body = self.message_input.get(1.0, tk.END+"-1c")
        requests.post('http://167.99.63.70/message', json={'message': body})
        self.message_input.delete(1.0, tk.END+"-1c")
        self.after(50, lambda: self.messages_frame.canvas.yview_moveto('1.0'))
        self.get_messages()

        return 'break'

    def get_messages(self):
        global messages
        messages = requests.get("http://167.99.63.70/messages").json()
        self.update_messages_widgets()
        self.after(150, lambda: self.messages_frame.canvas.yview_moveto('1.0'))

    def update_messages_widgets(self):
        global messages, messages_already_shown

        for message in messages:
            if (message['date'], message['message']) not in messages_already_shown:
                self.messages_frame.add_new_message(message)
                messages_already_shown.append((message['date'], message['message']))

