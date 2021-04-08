import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import random

MAX_MESSAGE_WIDTH = 1300


class MessagesFrame(ttk.Frame):
    def __init__(self, container, background, **kwargs):
        super().__init__(container, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -- VARIABLES --
        self.messages_frames = []

        # -- CANVAS + SCROLL FRAME --
        self.canvas = tk.Canvas(self, background=background)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky='NS')
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        # --

        # -- EVENTS --
        self.scrollable_frame.bind('<Configure>', self._configure_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind('<Configure>', self._configure_window_size)
        # --

    def add_new_message(self, new_message):
        new_message_frame = MessageFrame(self.scrollable_frame,
                                         new_message['date'],
                                         new_message['message'],
                                         style='Messages.TFrame')
        new_message_frame.grid(sticky='EW', padx=(10, 50), pady=10)
        self.messages_frames.append(new_message_frame)

    def _configure_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(event.delta*-1, 'units')

    def _configure_window_size(self, event):
        self.canvas.itemconfig(self.scrollable_window, width=self.canvas.winfo_width())


class MessageFrame(ttk.Frame):

    def __init__(self, container, date, message_text, **kwargs):
        super().__init__(container, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.avatar_image = Image.open('assets/' + random.choice(('luigi.png', 'mario.png', 'peach.jpg')))
        self.avatar_image.thumbnail((25, 25), Image.ANTIALIAS)
        self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)
        self.avatar_label = ttk.Label(self,
                                      image=self.avatar_photo,
                                      anchor='center',
                                      style='Avatar.TLabel')
        self.avatar_label.grid(row=0,
                               column=0,
                               rowspan=2,
                               sticky='NESW',
                               padx=5)

        date_string = datetime.datetime.fromtimestamp(date).strftime("%d-%m-%Y %H:%M:%S")
        date_label = ttk.Label(self,
                               text=date_string,
                               anchor='w',
                               justify='left',
                               style='Time.TLabel')
        date_label.grid(row=0, column=1, sticky='EW')
        self.message_label = ttk.Label(self,
                                       text=message_text,
                                       anchor='w',
                                       justify='left',
                                       wraplength=(container.winfo_width()-50),
                                       style='Message.TLabel')

        self.message_label.grid(row=1, column=1, sticky='EW')

        def reconfigure_message_label(event):
            self.message_label.configure(wraplength=min(container.winfo_width() - 50, MAX_MESSAGE_WIDTH))

        self.bind('<Configure>', reconfigure_message_label)

