import tkinter as tk
import asyncio
import os

from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter.filedialog import askopenfilename
# from src.gmail.connector import GmailConnector
# import src.gmail.messageSender as messageSender

import tkinterController as tkHelper

from messageHandler import *
from connector import GmailConnector
import messageSender
from messageWidget import MessageWidget


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Gmail client")
        self.master.iconbitmap('src/img/mail-icon.png')
        self.master.resizable(False, False)

        self.master.call('encoding', 'system', 'utf-8')
        self.current_label = 'UNREAD'
        self.gmailConnector = GmailConnector(messageSender)

        self.windows = []

        panel_root = PanedWindow(self.master, orient=VERTICAL)
        panel_root.pack(expand=1)

        panel_menu = PanedWindow(panel_root, orient=HORIZONTAL, width=800, height=30, bg='#ffe7c1');
        panel_root.add(panel_menu)

        panel_content = PanedWindow(panel_root, orient=HORIZONTAL, width=800, height=400);
        panel_labels = PanedWindow(panel_content, orient=VERTICAL, width=100, height=400, bg='#c9c2b7', bd=2)
        self.panel_messages = PanedWindow(panel_content, orient=VERTICAL, width=600, height=400, bd=2, bg='#d8d6d2')

        btn_send = Button(panel_menu, text="Написать письмо", width=9, command= lambda: self.create_window("New mail"))
        btn_send.pack(side=LEFT, expand=1)
        btn_refresh = Button(panel_menu, text="Обновить", width=9, command= lambda: asyncio.run(self.update_messages(self.panel_messages, self.current_label)))
        btn_refresh.pack(side=LEFT)
        panel_menu.add(btn_send)
        panel_menu.add(btn_refresh)

        panel_content.add(panel_labels)
        panel_content.add(self.panel_messages)

        panel_root.add(panel_content)

        self.gmailConnector = GmailConnector(messageSender=messageSender)
        self.gmailConnector.mailFrom = 'bogdanovsi884@gmail.com'
        
        self.update_labels(panel_labels)

        asyncio.run(self.update_messages(self.panel_messages,'UNREAD'))

    @property
    def attachment_file_path(self):
        return self._attach_file_path

    @attachment_file_path.setter
    def attachment_file_path(self, path):
        self._attach_file_path = path
        if self._attach_file_lbl is not None:
            self._attach_file_lbl.configure(text=path)

    def update_labels(self, context):
        self.labes = ['Unread', 'Sent', 'Inbox']
        self.remove_all_children(context)
        for lbl in self.labes:
            frame = Frame(context, height=30)
            frame.pack()

            label = Label(frame, text = lbl, font='bold', anchor='w')
            label.pack(side=LEFT, fill=X, padx=5, pady=5)
            label.bind('<Button-1>', lambda e: asyncio.run(self.update_messages(self.panel_messages, label.cget("text").upper())))
            context.add(frame)

    async def update_messages(self, context, label):
        print("Message update with label: %s", label)
        self.messages = await self.gmailConnector.get_list_messages(6, label)
        self.remove_all_children(context)
        for x in self.messages:
            msg = await self.gmailConnector.get_message(x['id'])
            msg_widget = MessageWidget(msg, context)
            msg_widget.frame.bind('<Button-1>', lambda e: self.open_msg(msg_widget))
            context.add(msg_widget.frame)

    def open_msg(self, msg_widget):
        window = Toplevel(self.master)
        window.resizable(False, False)
        window.title(msg_widget.subject)

        self.create_ui_msg(msg_widget, window)

        self.windows.append(window)

    def delete_msg(self, id):
        self.gmailConnector.delete_msg(id);

    def create_ui_msg(self, msg_widget, context):
        frame_btn = Frame(context)
        frame_btn.pack()

        Button(frame_btn, text="Удалить", command= lambda: self.delete_msg(msg_widget.id)).pack()

        frame = Frame(context, width=300)
        frame.pack()

        Label(frame, text="Mail from:").pack(side=LEFT)
        Label(frame, text=msg_widget.mailFrom).pack(fill=X, padx=5, expand=True)

        frame_msg = Frame(context)
        frame_msg.pack()

        Label(frame_msg, text="Message").pack(side=LEFT)
        Message(frame_msg, text=msg_widget.message).pack(fill=X, padx=5, expand=True)

    def remove_all_children(self, panel):
        childrens = panel.panes()
        for pane in childrens:
            panel.remove(pane)

    def create_window(self, title):
        window = Toplevel(self.master)
        window.resizable(False, False)
        window.title(title)

        self.create_ui_input_msg(window)

        self.windows.append(window)

    def create_layout_new_mail(self):
        layout = PanedWindow(self, orient=VERTICAL, width=800, height=400)
        self.create_ui_input_msg(layout)

        return layout

    def create_ui_input_msg(self, context):
        # context.pack(fill=BOTH, expand=True)

        msgHandler = MessageHandler(context)

        msgHandler.mail_to = tkHelper.create_inline_field(context, "Mail to:")[2]
        msgHandler.subject = tkHelper.create_inline_field(context, "Subject:")[2]
        msgHandler.message = tkHelper.create_textarea_field(context, "Message:")[2]

        # create button attachment
        self.craeate_field_attachment(context, msgHandler, "Выберите файл")
        self.btn_send = Button(context, text="Отправить", command= lambda: self.send_msg(msgHandler), width=9)
        self.btn_send.pack(side=LEFT, padx=5, pady=5, ipadx=3)

    
    def craeate_field_attachment(self, context, handler, text_btn):
        frame = Frame(context)
        frame.pack(fill=X)

        btn = Button(frame, text=text_btn, command = lambda: self.chose_file(handler))
        btn.pack(side=LEFT, padx=5, pady=5)

        handler._attach_file_lbl = Label(frame)
        handler._attach_file_lbl.pack(fill=X, padx=5, expand=True)

    def chose_file(self, handler):
        path = askopenfilename(initialdir="C:/Users/",
                           filetypes = [("All Files","*.*")],
                           title = "Choose a file."
                           )
        handler.attachment_file = path
        name = os.path.basename(path)
        handler._attach_file_lbl.configure(text = name)

    def send_msg(self, messageHandler):
        mail = self.create_mail(messageHandler)
        self.gmailConnector.send_message('me', mail)
        self.delete_window(messageHandler)

    def create_mail(self, messageHandler):
        mail_to = messageHandler.mail_to.get()
        subject = messageHandler.subject.get()
        msg = messageHandler.message.get("1.0",'end-1c')
        if messageHandler.attachment_file is not None:
            return messageSender.CreateMessageWithAttachment(self.gmailConnector.mailFrom, mail_to, subject, msg, '', messageHandler.attachment_file)
        else:
            return messageSender.CreateMessage(self.gmailConnector.mailFrom, mail_to, subject, msg)

    def delete_window(self, messageHandler):
        messageHandler.context.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
