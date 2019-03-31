import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Entry, Button

def create_inline_field(self, label):
    frame = Frame(self)
    frame.pack(fill=X)
    
    lbl = create_lbl(frame, label)         
    
    entry = create_entry(frame)

    return (frame, lbl, entry)

def create_textarea_field(self, label):
    frame = Frame(self)
    frame.pack(fill=X)
    
    lbl = create_lbl(frame, label) 

    text = create_textarea(frame)

    return (frame, lbl, text)  

def create_lbl(frame, text):
    lbl = Label(frame, text=text, width=9)
    lbl.pack(side=LEFT, padx=5, pady=5)
    return lbl   

def create_entry(frame):
    entry = Entry(frame, takefocus=True)
    entry.pack(fill=X, padx=5, expand=True)
    return entry

def create_textarea(frame):
    text = Text(frame, height=8, borderwidth=2)
    text.pack(fill=X, padx=5, expand=True)
    return text