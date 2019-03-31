import tkinter as tk
from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter.filedialog import askopenfilename
# from src.gmail.connector import GmailConnector
# import src.gmail.messageSender as messageSender

import tkinterController as tkHelper

from src.gmail.messageHandler import *
from src.gmail.connector import GmailCOnnector

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Gmail client")
        self.master.iconbitmap('src/img/mail-icon.png')
        self.master.resizable(False, False)
        
        self.windows = []

        panel_root = PanedWindow(self.master, orient=VERTICAL)
        panel_root.pack(expand=1)

        panel_menu = PanedWindow(panel_root, orient=HORIZONTAL, width=800, height=30);
        panel_root.add(panel_menu)

        btn_send = Button(panel_menu, text="Написать письмо", width=9, command= lambda: self.create_window("New mail"))
        btn_send.pack(side=LEFT, expand=1)
        btn_refresh = Button(panel_menu, text="Обновить", width=9)
        btn_refresh.pack(side=LEFT, expand=1)
        panel_menu.add(btn_send)
        panel_menu.add(btn_refresh)

        panel_content = PanedWindow(panel_root, orient=HORIZONTAL, width=800, height=400);
        panel_labels = PanedWindow(panel_content, orient=VERTICAL, width=200, height=400, bg='#000')
        panel_messages = PanedWindow(panel_content, orient=VERTICAL, width=600, height=400, bg='#f0f')

        panel_content.add(panel_labels)
        panel_content.add(panel_messages)

        panel_root.add(panel_content)

        label = Frame(panel_labels)
        for x in range(0, 5):
            lbl = Button(label, text="text", width=9)
            lbl.pack(padx=5, pady=5, expand=1)

            panel_labels.add(label)

        # self.gmailConnector = GmailConnector(messageSender=messageSender)
        # self.gmailConnector.mailFrom = 'bogdanovsi884@gmail.com'
        # self.master = master
        # self.create_ui_input_msg()

    @property
    def attachment_file_path(self):
        return self._attach_file_path

    @attachment_file_path.setter
    def attachment_file_path(self, path):
        self._attach_file_path = path
        if self._attach_file_lbl is not None:
            self._attach_file_lbl.configure(text=path)

    def create_window(self, title):
        window = Toplevel(self.master)
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

        self._attach_file_lbl = Label(frame)
        self._attach_file_lbl.pack(fill=X, padx=5, expand=True)

    def chose_file(self, handler):
        path = askopenfilename(initialdir="C:/Users/",
                           filetypes = [("All Files","*.*")],
                           title = "Choose a file."
                           )
        handler.attachment_file = path

    def send_msg(self, messageHandler):
        mail = self.create_mail(messageHandler)
        self.gmailConnector.send_message('me', mail)

    def create_mail(self, messageHandler):
        mail_to = messageHandler.mail_to.get()
        subject = messageHandler.subject.get()
        msg = messageHandler.message.get()
        if messageHandler.attach_file_path is not None:
            return messageSender.CreateMessageWithAttachment(self.gmailConnector.mailFrom, mail_to, subject, msg, '', self.attachment_file_path)
        else:
            return messageSender.CreateMessage(self.gmailConnector.mailFrom, mail_to, subject, msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
