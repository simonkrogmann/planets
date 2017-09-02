# -*- coding: cp1252 -*-
import tkinter

class ImageButton:
    """ein quadratischer Button/Schalter mit einem einfarbigen Bild für die Toolbar"""
    def __init__(self, Parent, ImagePath, Command, Switch = False):
        self.Parent = Parent

        self.X, self.Y = Parent.RequestPosition(20)
        X, Y = self.X, self.Y
        self.Command = Command
        self.Switch = Switch

        if Switch:
            self.Active = False
        self.Enabled = True

        self.SetImage(ImagePath)
        self.Drawing = self.Parent.create_image(X, Y, image = self.Image, anchor = tkinter.NW)
        self.Parent.tag_bind(self.Drawing, "<Button-1>", self.Highlight)
        self.Parent.tag_bind(self.Drawing, "<B1-Motion>", self.Motion)
        self.Parent.tag_bind(self.Drawing, "<ButtonRelease-1>", self.Click)

    def SetColor(self, Color):
        """ändert das Bild"""
        if self.Image:
            self.Image.config(foreground = Color)

    def SetImage(self, ImagePath):
        """legt das Bild fest"""
        if ImagePath.endswith(".xbm"):
            self.Image = tkinter.BitmapImage(file = ImagePath)
        else:
            self.Image = None

    def Disable(self):
        """lässt den Button nicht mehr auf Klicks reagieren"""
        self.Enabled = False
        self.SetColor("darkgrey")

    def Enable(self):
        """lässt den Button wieder auf Klicks reagieren"""
        self.Enabled = True
        self.SetColor("black")

    def Activate(self):
        """Schalter auf aktiven Status gesetzt"""
        self.Highlight()
        self.Active = True

    def Deactivate(self):
        """Schalter auf inaktiven Status gesetzt"""
        self.Active = False
        self.Unhighlight()

    def Highlight(self, e = None):
        """Farbänderung für Hervorhebung"""
        if self.Enabled and not (self.Switch and self.Active):
            self.SetColor("#3388FF")

    def Unhighlight(self):
        """Farbänderung zurück zur normalen Farbe"""
        if not (self.Switch and self.Active):
            self.SetColor("black")

    def Motion(self, e):
        """führt für Farbänderung bei Bewegung mit gedrückter Maustaste"""
        if self.Enabled:
            X = e.x - self.X
            Y = e.y - self.Y
            if X < 0 or X >= 20 or Y < 0 or Y >= 20:
                self.Unhighlight()
            else:
                self.Highlight()

    def Click(self, e):
        """führt bei einem Klick das Kommando aus"""
        if self.Enabled:
            self.Unhighlight()
            X = e.x - self.X
            Y = e.y - self.Y
            if X >= 0 and X < 20 and Y >= 0 and Y < 20:
                self.Command()

class Scale:
    """ein Schieberegler für die Toolbar"""
    SliderWidth = 30
    def __init__(self, Parent, Max, Min, Width, Command):
        self.X, self.Y = Parent.RequestPosition(Width)
        X, Y = self.X, self.Y
        self.Max = Max
        self.Min = Min
        self.Width = Width
        self.Parent = Parent
        self.Command = Command
        self.Position = 0
        self.Area = self.Parent.create_rectangle(X, Y, X + Width, Y + 20,
                                                 fill = "grey", outline = "")
        self.Slider = self.Parent.create_rectangle(X, Y, X + Width + Scale.SliderWidth, Y + 20,
                                                   fill = "#444444", outline = "")
        self.Parent.tag_bind(self.Slider, "<Button-1>", self.Click)
        self.Parent.tag_bind(self.Slider, "<B1-Motion>", self.Drag)
        self.Parent.tag_bind(self.Slider, "<ButtonRelease-1>", self.Release)

    def Set(self, Value):
        """setzt den Wert des Schiebereglers"""
        self.Position = self.X + (self.Width - Scale.SliderWidth) / (self.Max - self.Min) * (Value - self.Min)
        self.Parent.coords(self.Slider, self.Position, self.Y, self.Position + Scale.SliderWidth,
                           self.Y + 20)

    def Get(self, Position):
        """gibt den aktuellen Wert des Schiebereglers zurück"""
        return Position * (self.Max - self.Min) / float(self.Width - Scale.SliderWidth) + self.Min

    def Click(self, e):
        """speichert die Mausposition zu Beginn der Bewegung und ändert die Farbe"""
        self.Parent.itemconfig(self.Slider, fill = "#3388FF")
        self.DragWidth = e.x - self.Position

    def Drag(self, e):
        """bewegt den Schieber mit der Maus mit"""
        Position = e.x - self.X - self.DragWidth
        Value = self.Get(Position)
        if Value < self.Min:
            self.Command(self.Min)
        elif Value > self.Max:
            self.Command(self.Max)
        else:
            self.Command(Value)

    def Release(self, e):
        """ändert die Farbe beim Loslassen des Schiebers zurück"""
        self.Parent.itemconfig(self.Slider, fill = "#444444")

class Label:
    """ein Textlabel für die Toolbar"""
    def __init__(self, Parent, Text, Width = 50):
        self.Parent = Parent
        self.X, self.Y = Parent.RequestPosition(Width)
        X, Y = self.X, self.Y
        self.Drawing = self.Parent.create_text(X + 3, Y + 2, text = Text, anchor = tkinter.NW)

    def Set(self, Text):
        """ändert den Text zum Parameter Text"""
        self.Parent.itemconfig(self.Drawing, text = Text)


class Separator:
    """ein Trennstrich für die Toolbar"""
    def __init__(self, Parent):
        X, Y = Parent.RequestPosition(1)
        Parent.create_line(X, Y, X, Y + 20, fill = "darkgrey")

class Bar(tkinter.Canvas):
    """eine leere mit verschiedenen Widgets befüllbare Toolbar"""
    def __init__(self, Parent, Width = 0):
        self.Parent = Parent
        self.Canvas = tkinter.Canvas.__init__(self, Parent, takefocus = False, bd = -2,
                                         background = "#DAE4ED", highlightthickness = 0,
                                         height = 24, width = Width)
        self.FreeX = 0

    def RequestPosition(self, Width):
        """gibt die Koordinaten der nächsten freien Stelle zurück
und setzt diese Stelle als belegt"""
        self.FreeX += Width
        return self.FreeX - Width, 0
