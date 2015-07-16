# -*- coding: cp1252 -*-
import Tkinter

class ItemInfo:
    """Ein kleiner Infobereich für einen Planeten, der neben der Sidebar angezeigt wird"""
    def __init__(self, Parent, Item, X):
        self.Parent = Parent

        self.Planet = Item.Planet
        self.Planet.Register(self)

        Height = 110
        Width = 250
        ScreenPosition = Item.ScreenPosition() - Height + 45 + 21
        if ScreenPosition < 21:
            ScreenPosition = 21

        self.Canvas = Tkinter.Canvas(self.Parent.Window, width = Width, height = Height, bd = -2,
                                     highlightthickness = 0)
        self.Canvas.place(x = X, y = ScreenPosition)
        self.Canvas.focus_set()
        for i in range(5):
            self.Canvas.create_line(i, 0, i, Height, fill = "#3388FF")

        self.Info = {}

        Y = 5
        for Tag in ["name", "position", "velocity", "mass", "diameter"]:
            self.Canvas.create_text(10, Y, anchor = Tkinter.NW, text = Tag.title())
            self.Info[Tag] = self.Canvas.create_text(70, Y, anchor = Tkinter.NW,
                                                    text = self.Planet[Tag])
            Y += 20

    def Update(self, Tag, Value):
        """aktualisiert einen der Werte entsprechend des angegebenen Planetenattributs"""
        if Tag in self.Info:
            self.Canvas.itemconfig(self.Info[Tag], text = Value)

    def Close(self):
        """schließt den Infobereich"""
        self.Planet.Deregister(self)
        self.Canvas.place_forget()
