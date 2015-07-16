# -*- coding: cp1252 -*-
import Tkinter
import vector
import tkColorChooser
import entry

class ItemEditor(Tkinter.Toplevel):
    """eine Dialogfenster für Planeteneinstellungen"""
    def __init__(self, Parent, Item):
        self.Parent = Parent

        # Fenstereigenschaften
        Tkinter.Toplevel.__init__(self, Parent.Window)

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
            Tkinter.Label(self, text = Tag.title()).place(x = 10, y = Y)
            self.Options[Tag] = entry.Entry(self, 100, Y, Item.Planet[Tag], 45)
            Tkinter.Label(self, text = Units[Index]).place(x = 390, y = Y)
            Y += 30
            Index += 1
        self.Options["color"] = Tkinter.StringVar()
        self.Options["color"].set(Item.Planet["color"])

        Tkinter.Label(self, text = "All values are given in standard units.").place(x = 100, y = 155)

        X = 100
        for Tag in ["trace", "fixed"]:
            self.Options[Tag] = Tkinter.IntVar()
            self.Options[Tag].set(Item.Planet[Tag])
            Tkinter.Checkbutton(self, text = Tag.title(), variable = self.Options[Tag],
                                onvalue = True, offvalue = False).place(x = X, y = 180)
            X += 100

        self.ColorButton = Tkinter.Button(self, command = self.Color, relief = Tkinter.GROOVE,
                                          width = 1, bg = self.Options["color"].get(), bd = 1)
        self.ColorButton.place(x = X, y = 183, height = 18)

        Tkinter.Label(self, text = "Color").place(x = X + 20, y = 182)

        # Dialog-Buttons
        Tkinter.Button(self, text = "OK", command = self.OK, relief = Tkinter.GROOVE,
                       width = 10).place(x = 145, y = 220)
        Tkinter.Button(self, text = "Apply", command = self.Apply, relief = Tkinter.GROOVE,
                       width = 10).place(x = 235, y = 220)
        Tkinter.Button(self, text = "Cancel", command = self.Close, relief = Tkinter.GROOVE,
                       width = 10).place(x = 325, y = 220)

        self.wait_window(self)

    def Color(self):
        """lässt den Benutzer eine Farbe für den Planeten auswählen"""
        Color = tkColorChooser.askcolor(parent = self, color = self.Item.Planet["color"])
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
