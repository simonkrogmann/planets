# -*- coding: cp1252 -*-
import Tkinter

class Entry:
    """ein einfaches Entryfeld für leichteren Zugriff"""
    def __init__(self, Master, X, Y, Text = "", Width = 50):
        self.Var = Tkinter.StringVar()
        self.Var.set(Text)
        Tkinter.Entry(Master, textvariable = self.Var, width = Width,
                      relief = Tkinter.GROOVE, bd = 2).place(x = X, y = Y + 2)

    def get(self):
        """gibt den Inhalt des Feldes zurück"""
        return self.Var.get()

    def set(self, Text):
        """setzt den Inhalt des Feldes"""
        self.Var.set(Text)
