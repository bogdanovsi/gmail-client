import tkinter as tk

import messageSender
from connector import GmailConnector

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

    def create_ui_input_msg(self):
        self.pack(fill=BOTH, expand=True)
        self.entry_mail_to = self.create_inline_field("Mail to:")
        self.entry_subject = self.create_inline_field("Subject:")
        self.entry_message = self.create_inline_field("Message:")

        # create button attachment
        self.craeate_button_attachment("Выберите файл")
        self.btn_send = self.craeate_button_attachment("Отправить")
        self.btn_send.configure(command=self.send_msg)

    def create_inline_field(self, label):
        frame = Frame(self)
        frame.pack(fill=X)
        
        lbl = Label(frame, text=label, width=10)
        lbl.pack(side=LEFT, padx=5, pady=5)           
       
        entry = Entry(frame)
        entry.pack(fill=X, padx=5, expand=True)

        return entry

    def craeate_button_attachment(self, text_btn):
        btn = Button(self.master, text=text_btn, command = self.chose_file)
        btn.pack(side=LEFT, padx=5, pady=5)
        return btn

    def chose_file(self):
        path = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
        self.attach_file_path = path
        print (path)

    def send_msg(self):
        mail = self.create_mail()
        self.gmailConnector.send_message('me', mail)

    def create_mail(self):
        mail_to = self.entry_mail_to.get()
        subject = self.entry_subject.get()
        msg = self.entry_message.get()
        if self.attach_file_path is not None:
            return messageSender.CreateMessageWithAttachment(self.gmailConnector.mailFrom, mail_to, subject, msg, '', self.attach_file_path)
        else:
            return messageSender.CreateMessage(self.gmailConnector.mailFrom, mail_to, subject, msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
