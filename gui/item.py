# -*- coding: cp1252 -*-
import tkinter
import vector

class Drawing:
    """Die Basisklasse für ein Widget eines Listeneintrages"""
    ActiveColor = "#3388FF"
    def __init__(self, Parent):
        self.Parent = Parent
        # Event-Bindings für Weitergabe an die Item-Klasse
        Parent.Parent.Canvas.tag_bind(self.Drawing, "<Button-1>", self.Click)
        Parent.Parent.Canvas.tag_bind(self.Drawing, "<B1-Motion>", self.Parent.Motion)
        Parent.Parent.Canvas.tag_bind(self.Drawing, "<ButtonRelease-1>", self.Parent.Release)
        Parent.Parent.Canvas.tag_bind(self.Drawing, "<Button-3>", self.RightClick)

# folgende Methoden können überschrieben werden
    def Click(self, e):
        self.Parent.Click(e)

    def RightClick(self, e):
        self.Parent.RightClick(e)

    def Raise(self):
        """setzt das Widget in den Vordergrund"""
        self.Parent.Parent.Canvas.tag_raise(self.Drawing)

    def Delete(self):
        """löscht das Widget"""
        self.Parent.Parent.Canvas.delete(self.Drawing)

    def Activate(self):
        pass
    def Deactivate(self):
        pass
    def Update(self):
        pass

class EntryLabel(Drawing):
    """ein Label für einen Listeneintrag,
dessen Text man bearbeiten kann, wenn man auf ihn klickt"""
    def __init__(self, Parent, X, Y, Tag, Width = 10, Highlight = False):
        self.Parent = Parent
        self.Text = self.Parent.Get(Tag)
        self.X = X
        self.Y = Y
        self.Tag = Tag
        self.Width = Width
        if Highlight:
            self.ActiveColor = "white"
            self.Color = "black"
        else:
            self.ActiveColor = "lightgrey"
            self.Color = "darkgrey"

        self.Drawing = Parent.Parent.Canvas.create_text(0, 0, anchor = tkinter.NW, fill = self.Color,
                                                        text = self.Text)

        Drawing.__init__(self, Parent)
        self.PlaceLabel()

        self.Entry = tkinter.Entry(self.Parent.Parent.Canvas, width = Width)
        self.EntryWindow = self.Parent.Parent.Canvas.create_window(self.X + 1,
                self.Y + 1 + self.Parent.Position, window = self.Entry, anchor = tkinter.NW,
                state = tkinter.HIDDEN)
        self.Entry.bind("<Return>", self.StopEdit)

        self.IsEdited = False

    def SetText(self, Text):
        """setzt den Text des Widgets"""
        self.Text = Text
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, text = Text)


    def PlaceLabel(self):
        """zeigt das Label"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, state = tkinter.NORMAL)
        self.Parent.Parent.Canvas.coords(self.Drawing, self.X + 3,
                                         self.Parent.Position + self.Y + 3)

    def PlaceEntry(self):
        """zeigt das Eingabefeld"""
        self.Parent.Parent.Canvas.itemconfig(self.EntryWindow, state = tkinter.NORMAL)
        self.Parent.Parent.Canvas.coords(self.EntryWindow, self.X + 1,
                                         self.Parent.Position + self.Y + 1)

    def ForgetLabel(self):
        """versteckt das Label"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, state = tkinter.HIDDEN)

    def ForgetEntry(self):
        """versteckt das Eingabefeld"""
        self.Parent.Parent.Canvas.itemconfig(self.EntryWindow, state = tkinter.HIDDEN)

    def Click(self, e = None):
        """bei Klick wird mit der Bearbeitung begonnen bzw. der Listeneintrag aktiviert"""
        # DragOK: Item kann nur verschoben werden, wenn nicht das Entry-Feld geöffnet wird
        IsActive = self.Parent.Active()
        self.Parent.Click(e, DragOK = not IsActive)
        if IsActive and not self.Parent.Simulation():
            self.Edit()

    def Edit(self):
        """erlaubt Bearbeitung des Widget-Textes"""
        self.IsEdited = True

        self.Entry.insert(0,self.Text)
        self.Entry.icursor(tkinter.END)
        self.Entry.selection_range(0, tkinter.END)

        self.ForgetLabel()
        self.PlaceEntry()
        self.Entry.focus_set()

    def StopEdit(self, e = None):
        """stoppt Bearbeitung des Widget-Textes und gibt diesen an den Planeten weiter"""
        self.IsEdited = False
        self.Parent.Edit(self.Tag, self.Entry.get())

        self.ForgetEntry()
        self.PlaceLabel()

        self.Entry.delete(0, tkinter.END)

    def Activate(self):
        """farbliche Hervorhebung"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, fill = self.ActiveColor)
        if self.IsEdited:
            self.StopEdit()

    def Deactivate(self):
        """Rückkehr zur normalen Farbe"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, fill = self.Color)
        if self.IsEdited:
            self.StopEdit()

    def Delete(self):
        """löscht das Widget"""
        self.Parent.Parent.Canvas.delete(self.Drawing)
        self.Parent.Parent.Canvas.delete(self.EntryWindow)

    def Update(self):
        """Neuzeichnung des Objekts"""
        if self.IsEdited:
            self.PlaceEntry()
        else:
            self.PlaceLabel()

class Rectangle(Drawing):
    """ein Rechteck für den Hintergrund eines Listeneintrags"""
    def __init__(self, Parent, Width):
        self.Width = Width
        self.Parent = Parent
        self.Drawing = Parent.Parent.Canvas.create_rectangle(0, 0, 2, 2, outline = "")
        self.Update()

        Drawing.__init__(self, Parent)

    def Activate(self):
        """farbliche Hervorhebung"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, fill = Drawing.ActiveColor)

    def Deactivate(self):
        """Rückkehr zur normalen Farbe"""
        self.Parent.Parent.Canvas.itemconfig(self.Drawing, fill = "white")

    def Update(self):
        """Neuzeichnung des Objekts"""
        self.Parent.Parent.Canvas.coords(self.Drawing, 0, self.Parent.Position, self.Width,
                                         self.Parent.Position + Item.Height - 1)

class Item:
    """ein Eintrag für die Liste in der Sidebar"""
    Height = 42
    def __init__(self, Parent, Index, Planet, SimulationMethod, Width):
        self.Parent = Parent
        self.Simulation = SimulationMethod

        self.Position = Item.Height * Index

        self.Planet = Planet
        self.Planet.Register(self)

        self.Rectangle = Rectangle(self, Width)
        self.NameLabel = EntryLabel(self, 0, 0, "name", Highlight = True)
        self.PositionLabel = EntryLabel(self, 0, 20, "position", Width = 30)

        self.Widgets = [self.Rectangle, self.NameLabel, self.PositionLabel]
        self.IsDragged = False

# Observer-Methoden

    def Update(self, Tag, Value):
        """ändert den angezeigten Namen bzw. die Position"""
        if Tag == "name":
            self.NameLabel.SetText(Value)
        elif Tag == "position":
            self.PositionLabel.SetText(Value.Display())

# Methoden für Objektbearbeitung

    def Get(self, Tag):
        """gibt den Wert des Attributs des Planeten zurück"""
        return self.Planet[Tag]

    def Edit(self, Tag, Value):
        """versucht das Attribut Tag des Planeten zu Value zu ändern,
überprüft dabei die Gültigkeit des Wertes"""
        if Tag in ("name", "color"):
            self.Planet[Tag] = Value
        elif Tag in ("mass", "diameter"):
            try:
                NewValue = float(Value)
            except:
                self.BadInput(Tag, Value)
            else:
                self.Planet[Tag] = NewValue
        elif Tag in ("position", "velocity"):
            try:
                Values = tuple(float(C) for C in Value.split(","))
            except:
                self.BadInput(Tag, Value)
            else:
                if len(Values) == 3:
                    self.Planet[Tag] = vector.Vector(Values[0], Values[1], Values[2])
                else:
                    self.BadInput(Tag, Value)
        elif Tag in ("trace", "fixed"):
            try:
                NewValue = bool(Value)
            except:
                self.BadInput(Tag, Value)
            else:
                self.Planet[Tag] = NewValue

    def BadInput(self, Tag, Value):
        """zeigt eine Fehlermeldung bei ungültigen Werten an"""
        tkinter.messagebox.showwarning("Bad Input",
                "Invalid input '{0}' for option '{1}'!".format(Value, Tag.title()))

    def Delete(self):
        """löscht den Listeneintrag"""
        if self.Active():
            self.Deactivate()
        for Widget in self.Widgets:
            Widget.Delete()

# Methoden für GUI-Ereignisse

    def Click(self, e, DragOK = True):
        """leitet Ziehen des Eintrags ein und aktiviert ihn"""
        self.DragHeight = (e.y + self.Parent.Scrollbar.Offset() + 2) % Item.Height - 2
        if self.DragHeight != 39:
            self.IsDragged = self.Parent.Activate(self, e) and DragOK
        self.Raise()

    def Motion(self, e):
        """bewegt den Planeten durch die Liste"""
        if self.IsDragged:
            self.Parent.Drag(self, e.y - self.DragHeight + self.Parent.Scrollbar.Offset())

    def Release(self, e):
        """lässt den Eintrag in der Liste wieder einrasten"""
        if self.IsDragged:
            self.IsDragged = False
            self.UpdatePosition()

    def RightClick(self, e):
        """gibt einen Rechtsklick für das Kontextmenü weiter"""
        self.Parent.RightClick(e, self)

# Methoden für GUI-Veränderung

    def UpdatePosition(self, NewIndex = None):
        """zeichnet den Listeneintrag bei NewIndex neu,
bei None wird der Index abgerufen"""
        if NewIndex != None:
            self.Position = Item.Height * NewIndex
        else:
            self.Position = Item.Height * self.Index()
        for Widget in self.Widgets:
            Widget.Update()

    def Raise(self):
        """hebt den Listeneintrag in den Vordergrund"""
        for Widget in self.Widgets:
            Widget.Raise()
        self.Parent.Scrollbar.Raise()

    def Activate(self):
        """aktiviert den Listeneintrag"""
        for Widget in self.Widgets:
            Widget.Activate()
        if not self.Active():
            self.Parent.Active.append(self)

    def Deactivate(self):
        """deaktiviert den Listeneintrag"""
        for Widget in self.Widgets:
            Widget.Deactivate()
        self.Parent.Active.remove(self)

    def Active(self):
        """gibt zurück, ob der Eintrag aktiviert ist"""
        return self in self.Parent.Active

    def Index(self):
        """gibt den Index des Eintrags zurück"""
        return self.Parent.Items.index(self)

    def ScreenPosition(self):
        """gibt die y-Koordinate des Eintrags im sichtbaren Canvas-Objekt zurück"""
        return self.Position - self.Parent.Scrollbar.Offset()
