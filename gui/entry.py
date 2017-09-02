# -*- coding: cp1252 -*-
import tkinter

class Entry:
    """ein einfaches Entryfeld für leichteren Zugriff"""
    def __init__(self, Master, X, Y, Text = "", Width = 50):
        self.Var = tkinter.StringVar()
        self.Var.set(Text)
        tkinter.Entry(Master, textvariable = self.Var, width = Width,
                      relief = tkinter.GROOVE, bd = 2).place(x = X, y = Y + 2)

    def get(self):
        """gibt den Inhalt des Feldes zurück"""
        return self.Var.get()

    def set(self, Text):
        """setzt den Inhalt des Feldes"""
        self.Var.set(Text)
