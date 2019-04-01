from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button

import json
import base64

class MessageWidget:
    def __init__(self, message, context):
        msg = json.loads(message)
        self.subject = "(Без темы)"
        self.message = "(Пустое сообщение)"
        self.get_info_from_msg(msg)
        self.create_frame(context)

    def get_info_from_msg(self, message):
        self.id = message['id']
        self.tread_id = message['threadId']
        self.size_estimate = message['sizeEstimate']

        for x in message['payload']['headers']:
            name = x['name'].lower()
            if name == 'from':
                value = x['value']
                self.mailFrom = value
            elif name == 'subject':
                value = x['value']
                self.subject = value
        # try:
        #     msg_text = message['payload']['parts'][0]['body']['data']
        # except KeyError:
        #     msg_text = message['payload']['body']['data']
        # self.message = base64.b64decode(msg_text).decode('utf-8', "ignore")

        self.message = message['snippet']

    @property
    def frame(self):
        return self._frame

    def bind(self, key, command):
        self._frame.bind(key, command)

    def create_frame(self, context):
        self._frame = PanedWindow(context, orient=VERTICAL, height=60)
        self._frame.pack(fill=X, padx=2, pady=2)
        # self._frame.bind('<Button-1>', self.create_window_msg)

        try:
            lbl_subject = Label(self._frame, text=self.subject, font='bold', width=8, anchor='w')
        except TclError:
            lbl_subject = Label(self._frame, text="(Без темы)", font='bold', width=8, anchor='w')
            
        lbl_subject.pack(fill=X, padx=5, pady=5)

        try:
            lbl_msg = Label(self._frame, text=self.message)
        except TclError:
            lbl_msg = Label(self._frame, text="(Без сообщения)")

        lbl_msg.pack(side=BOTTOM, fill=X, padx=5, pady=5)


