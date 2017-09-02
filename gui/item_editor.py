# -*- coding: cp1252 -*-
import tkinter
import vector
import entry

class ItemEditor(tkinter.Toplevel):
    """eine Dialogfenster für Planeteneinstellungen"""
    def __init__(self, Parent, Item):
        self.Parent = Parent

        # Fenstereigenschaften
        tkinter.Toplevel.__init__(self, Parent.Window)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.Close)
        self.title("Edit Object")
        self.geometry("430x260")
        self.resizable(width = False, height = False)

        # Verknüpfung mit zu bearbeitendem Objekt
        self.Item = Item

        # Erzeugung der Widgets für die Optionen
        self.Options = {}

        Y = 10
        Index = 0
        Units = ["","m","m/s","kg","m"]
        for Tag in ["name", "position", "velocity", "mass", "diameter"]:
            tkinter.Label(self, text = Tag.title()).place(x = 10, y = Y)
            self.Options[Tag] = entry.Entry(self, 100, Y, Item.Planet[Tag], 45)
            tkinter.Label(self, text = Units[Index]).place(x = 390, y = Y)
            Y += 30
            Index += 1
        self.Options["color"] = tkinter.StringVar()
        self.Options["color"].set(Item.Planet["color"])

        tkinter.Label(self, text = "All values are given in standard units.").place(x = 100, y = 155)

        X = 100
        for Tag in ["trace", "fixed"]:
            self.Options[Tag] = tkinter.IntVar()
            self.Options[Tag].set(Item.Planet[Tag])
            tkinter.Checkbutton(self, text = Tag.title(), variable = self.Options[Tag],
                                onvalue = True, offvalue = False).place(x = X, y = 180)
            X += 100

        self.ColorButton = tkinter.Button(self, command = self.Color, relief = tkinter.GROOVE,
                                          width = 1, bg = self.Options["color"].get(), bd = 1)
        self.ColorButton.place(x = X, y = 183, height = 18)

        tkinter.Label(self, text = "Color").place(x = X + 20, y = 182)

        # Dialog-Buttons
        tkinter.Button(self, text = "OK", command = self.OK, relief = tkinter.GROOVE,
                       width = 10).place(x = 145, y = 220)
        tkinter.Button(self, text = "Apply", command = self.Apply, relief = tkinter.GROOVE,
                       width = 10).place(x = 235, y = 220)
        tkinter.Button(self, text = "Cancel", command = self.Close, relief = tkinter.GROOVE,
                       width = 10).place(x = 325, y = 220)

        self.wait_window(self)

    def Color(self):
        """lässt den Benutzer eine Farbe für den Planeten auswählen"""
        Color = tkinter.colorchooser.askcolor(parent = self, color = self.Item.Planet["color"])
        if Color:
            self.Options["color"].set(Color[1])
            self.ColorButton.config(bg = Color[1])

    def OK(self):
        """übernimmt die Änderungen und schließt den Dialog"""
        self.Apply()
        self.destroy()

    def Apply(self):
        """übernimmt die Änderungen"""
        for Tag in self.Options:
            self.Item.Edit(Tag, self.Options[Tag].get())
            self.Options[Tag].set(self.Item.Planet[Tag])

    def Close(self):
        """schließt den Dialog"""
        self.destroy()
