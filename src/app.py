
import tkinterController as tkHelper
import messageSender
from connector import GmailConnector
import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter.filedialog import askopenfilename

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.gmailConnector = GmailConnector(messageSender=messageSender)
        self.gmailConnector.mailFrom = 'bogdanovsi884@gmail.com'
        self.master = master
        self.master.title("Gmail client")
        self.master.iconbitmap('src/img/mail-icon.png')
        self.master.geometry("600x400")
        self.create_ui_input_msg()

    @property
    def attachment_file_path(self):
        return self._attach_file_path

    @attachment_file_path.setter
    def attachment_file_path(self, path):
        self._attach_file_path = path
        if self._attach_file_lbl is not None:
            self._attach_file_lbl.configure(text=path)

    def create_ui_input_msg(self):
        self.pack(fill=BOTH, expand=True)
        self.entry_mail_to = tkHelper.create_inline_field(self, "Mail to:")[2]
        self.entry_subject = tkHelper.create_inline_field(self, "Subject:")[2]
        self.entry_message = tkHelper.create_textarea_field(self, "Message:")[2]

        # create button attachment
        self.craeate_field_attachment("Выберите файл")
        self.btn_send = Button(self.master, text="Отправить", command=self.send_msg, width=9)
        self.btn_send.pack(side=LEFT, padx=5, pady=5, ipadx=3)

    
    def craeate_field_attachment(self, text_btn):
        frame = Frame(self)
        frame.pack(fill=X)

        btn = Button(frame, text=text_btn, command = self.chose_file)
        btn.pack(side=LEFT, padx=5, pady=5)

        self._attach_file_lbl = Label(frame)
        self._attach_file_lbl.pack(fill=X, padx=5, expand=True)

    def chose_file(self):
        path = askopenfilename(initialdir="C:/Users/",
                           filetypes = [("All Files","*.*")],
                           title = "Choose a file."
                           )
        self.attachment_file_path = path

    def send_msg(self):
        mail = self.create_mail()
        self.gmailConnector.send_message('me', mail)

    def create_mail(self):
        mail_to = self.entry_mail_to.get()
        subject = self.entry_subject.get()
        msg = self.entry_message.get()
        if self.attach_file_path is not None:
            return messageSender.CreateMessageWithAttachment(self.gmailConnector.mailFrom, mail_to, subject, msg, '', self.attachment_file_path)
        else:
            return messageSender.CreateMessage(self.gmailConnector.mailFrom, mail_to, subject, msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
