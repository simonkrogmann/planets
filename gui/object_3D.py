# -*- coding: cp1252 -*-
import time
import vector

class Planet3D:
    """ein 3D-Objekt für das graphics-Modul, dass mit einem Planeten verbunden ist"""
    def __init__(self, Parent, Planet):
        self.Parent = Parent
        self.Planet = Planet
        self.Planet.Register(self)
        self.Positions = [Planet["position"].Tuple()]
        self.Trace = []
        self.Color = Planet["color"]
        self.TraceState = -1
        self.Drawing = self.Parent.Canvas.create_oval(-5, -5, -6, -6, fill=Planet["color"],
                                                      outline="")
        self.Redraw()

    def ResetTrace(self):
        """löscht die bisher gezeichnete Spur des Planeten"""
        for Line in self.Trace:
            self.Parent.Canvas.delete(Line.Drawing)
            self.Parent.Drawings.remove(Line)
        self.Trace = []
        self.TraceState = -1
        self.Positions = [self.Positions[-1]]

    def Redraw(self):
        """zeichnet den Planeten neu"""
        C = self.Parent.DisplayPosition(self.Positions[-1])
        if C:
            Diameter = self.Parent.DisplayDiameter(self.Positions[-1], self.Planet["diameter"])
            Coordinates = (C[0] - Diameter, C[1] - Diameter, C[0] + Diameter, C[1] + Diameter)
            self.Parent.Canvas.coords(self.Drawing, Coordinates)
        else:
            self.Parent.Canvas.coords(self.Drawing, -5, -5, -6, -6)

    def Update(self, Tag, Value):
        """ändert die Zeichnung des Planeten entsprechend der Daten.
Mögliche Daten sind die Planetenattribute."""
        if Tag == "position":
            if type(Value) == tuple:
                Tuple = Value
            else:
                Tuple = Value.Tuple()
            if self.Planet["trace"] and self.Planet.Parent.Trace:
                # fasst jeweils 5 Linien für die Spur zusammen
                self.TraceState = (self.TraceState + 1) % 5
                if not self.TraceState:
                    self.Trace.append(Line3D(self.Parent, self.Positions[-1], Tuple, self.Color))
                    self.Parent.Drawings.append(self.Trace[-1])
                    self.Positions.append(Tuple)
                else:
                    self.Positions[-1] = Tuple
                    self.Trace[-1].End = Tuple
                    self.Trace[-1].Redraw()
            else:
                self.Positions = [Tuple]
            self.Redraw()
        elif Tag == "diameter":
            self.Redraw()
        elif Tag == "color":
            self.SetColor(Value)
        elif Tag == "trace" and not Value:
            self.ResetTrace()

    def SetColor(self, Color):
        """ändert die Planetenfarbe"""
        self.Color = Color
        self.Parent.Canvas.itemconfig(self.Drawing, fill=Color)

    def Delete(self):
        """entfernt den Planeten aus der Zeichnung"""
        for Line in self.Trace:
            self.Parent.Canvas.delete(Line.Drawing)
            self.Parent.Drawings.remove(Line)
        self.Parent.Canvas.delete(self.Drawing)
        self.Planet.Deregister(self)

    def MidPoint(self):
        """gibt den Mittelpunkt des Planeten zurück"""
        return self.Positions[-1]

class Line3D:
    """eine 3D-Linie für das graphics-Modul"""
    def __init__(self, Parent, Begin, End, Color):
        self.Parent = Parent
        self.Begin = Begin
        self.End = End
        self.OnScreen = False

        self.Drawing = self.Parent.Canvas.create_line(-5, -5, -5, -5, fill=Color)
        self.Redraw()

    def Redraw(self):
        """zeichnet die Linie neu"""
        Coordinates = self.Parent.LineDisplayCoordinates(self.Begin, self.End)
        self.OnScreen = Coordinates == (-5, -5, -5, -5)
        self.Parent.Canvas.coords(self.Drawing, Coordinates)

    def MidPoint(self):
        """gibt den Mittelpunkt der Linie zurück"""
        return ((self.Begin[0] + self.End[0])/ 2,  (self.Begin[1] + self.End[1])/ 2,
                (self.Begin[2] + self.End[2])/ 2)
