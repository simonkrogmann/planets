# -*- coding: cp1252 -*-
import tkinter

class Scrollbar:
    """stellt eine Scrollbar für ein Canvas-Objekt bereit,
Parent muss dieses Canvas-Objekt als Attribut besitzen."""
    def __init__(self, Parent, X):
        self.Parent = Parent
        self.X = X

        self.Bar = self.Parent.Canvas.create_rectangle(0, 0, 2, 2, state = tkinter.HIDDEN,
                                                      fill = "#444444", outline = "")
        self.Parent.Canvas.bind("<Configure>", self.UpdateRegion)
        self.Parent.Canvas.bind("<MouseWheel>", self.Wheel)
        self.Parent.Canvas.tag_bind(self.Bar, "<Button-1>", self.ScrollBegin)
        self.Parent.Canvas.tag_bind(self.Bar, "<B1-Motion>", self.ScrollMotion)

        self.Scrolling = False

    def Wheel(self, e):
        """scrollt die Ansicht entsprechend der Mausradbewegung"""
        if self.Scrollable:
            self.Parent.Canvas.yview_scroll(-e.delta/120, "units")
            if self.Parent.Active:
                self.Parent.Active[0].Motion(e)
            self.UpdateBar()

    def Offset(self):
        """gibt die Höhe des Bereiches zurück, der nach oben aus der Ansicht herausgescrollt ist"""
        return self.Parent.Canvas.yview()[0] * self.Region

    def UpdateRegion(self, e = None):
        """aktualisiert den scrollbaren Bereich"""
        # Die Zahlen, die in dieser Methode addiert,
        # werden gleichen Ungenauigkeiten im Canvas-Objekt aus.

        # ein vorhandenes e weist auf Aufruf durch "configure"-event hin
        # und eine Höhenveränderung des Canvas hin
        if e:
            self.Height = e.height + 8
        # bestimmt benötigte Höhe der Liste
        self.Region = self.Parent.Height() + 1
        # prüft ob eine Scrollbar benötigt wird
        if self.Region + 3 <= self.Height:
            self.Parent.Canvas.config(scrollregion = (0, 0, 0, self.Height - 8))
            self.Scrollable = False
            self.Show(0)
            self.Parent.Canvas.itemconfig(self.Bar, state = tkinter.HIDDEN)
        else:
            self.Scrollable = True
            self.Parent.Canvas.itemconfig(self.Bar, state = tkinter.NORMAL)
            self.Parent.Canvas.config(scrollregion = (0, 0, 0, self.Region))
            self.UpdateBar()

    def UpdateBar(self):
        """zeichnet die Scrollbar neu"""
        Position = self.Parent.Canvas.yview()
        Begin = self.Height * Position[0] + self.Offset()
        End = self.Height * Position[1] + self.Offset()
        self.Parent.Canvas.coords(self.Bar, self.X - 11, Begin, self.X - 3, End)
        self.Parent.Canvas.tag_raise(self.Bar)

    def ScrollBegin(self, e):
        """speichert die Position des Mausklicks beim Beginnen des Scrollens"""
        if self.Scrollable:
            self.DragHeight = float(e.y) / self.Height - self.Parent.Canvas.yview()[0]

    def ScrollMotion(self, e):
        """zieht die neue Mausposition von der gepeicherten ab und
legt danach die Scrollrichtung und -weite fest"""
        if self.Scrollable:
            self.Parent.Canvas.yview_moveto(float(e.y) / self.Height - self.DragHeight)
            self.UpdateBar()

    def Show(self, Position):
        """scrollt zum Listenelement mit dem Index Position"""
        if self.Scrollable:
            self.Parent.Canvas.yview_moveto(Position / float(self.Region))
            self.UpdateBar()

    def Raise(self):
        """zeigt die Scrollbar im Vordergrund an"""
        self.Parent.Canvas.tag_raise(self.Bar)
