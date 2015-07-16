# -*- coding: cp1252 -*-
import Tkinter
import vector
import math
import object_3D
import time

# Methoden für Vektorrechnung mit Tupeln
def Add(a, b):
    """addiert 2 Vektoren"""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def Sub(a, b):
    """zieht Vektor a von Vektor b ab"""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def Mul(a, b):
    """multipliziert Vektor a mit Faktor b"""
    return (a[0] * b, a[1] * b, a[2] * b)

def ScP(a, b):
    """rechnet das Skalarprodukt von 2 Vektoren aus"""
    return a[0] * b[0] + a[1] * b[1] +a[2] * b[2]

def Length(a):
    """rechnet die Länge eines Vektors aus"""
    return (a[0] ** 2 + a[1] ** 2 + a[2] ** 2) ** .5

def VP(a, b):
    """rechnet das Vektorprodukt von 2 Vektoren aus"""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

class Graphics:
    """Dieses Modul stellt eine Anzeige für die Planeten bereit"""
    def __init__(self, Parent, PlanetManager):
        self.Parent = Parent
        PlanetManager.Register(self)
        self.Canvas = Tkinter.Canvas(self.Parent.Window, takefocus = True, borderwidth = -2,
                                     background = "black", highlightthickness = 0)
        self.Canvas.grid(row = 0, column = 1, rowspan = 2, columnspan = 2,
                         sticky = Tkinter.N + Tkinter.S + Tkinter.E + Tkinter.W)
        self.Canvas.bind("<Button-1>", self.Click)
        self.Canvas.bind("<B1-Motion>", self.Motion)
        self.Canvas.bind("<MouseWheel>", self.Wheel)
        self.Canvas.bind("<Configure>", self.ChangeSize)
        self.Canvas.bind("<Enter>", self.Focus)

        self.Camera = (0, 0, 100)
        self.ProjectionPlaneDistance = 10.0
        self.ProjectionPlaneTop = (0, 0.4, 0)
        self.ProjectionPlaneLeft = (-0.4, 0, 0)

        self.MidX = 200
        self.MidY = 200
        # Mittelpunktskennzeichnung
        self.Mid = self.Canvas.create_oval(199, 199, 201, 201, fill = "green", outline = "")

        self.Items = []
        self.Drawings = []
        self.Update()
        self.DrawGrid()

    def Save(self):
        """gibt die Daten des Objekts für die Speicherung als Tupel zurück"""
        return (self.Camera, self.ProjectionPlaneDistance,
                self.ProjectionPlaneTop, self.ProjectionPlaneLeft)

    def Load(self, Obj):
        """lädt Objektdaten aus einem Tupel"""
        self.Camera = Obj[0]
        self.ProjectionPlaneDistance = Obj[1]
        self.ProjectionPlaneTop = Obj[2]
        self.ProjectionPlaneLeft = Obj[3]
        self.Update()

    def DrawGrid(self):
        """zeichnet das Orientierungsgitter"""
        Factor = 1e+10
        for i in xrange(-5, 6):
            for j in xrange(-5, 5):
                Begin = (10 * j * Factor, 10 * i * Factor, 0)
                End = (10 * (j + 1) * Factor, 10 * i * Factor, 0)
                self.Drawings.append(object_3D.Line3D(self, Begin, End, "#222222"))

                Begin = (10 * i * Factor, 10 * j * Factor, 0)
                End = (10 * i * Factor, 10 * (j + 1) * Factor, 0)
                self.Drawings.append(object_3D.Line3D(self, Begin, End, "#222222"))

    def Focus(self, e):
        """setzt den Fokus auf das Canvas-Objekt"""
        self.Canvas.focus_set()

    def Click(self, e):
        """speichert Anfangspunkt fürs Drehen des Objektes"""
        self.Drag = vector.Vector(e.x, e.y)

    def Motion(self, e):
        """berechnet Drehungsrichtung und Weite aus der Mausbewegung
und lässt das Objekt drehen"""
        self.Rotate(e.x - self.Drag.X, e.y - self.Drag.Y)

        self.Drag = vector.Vector(e.x, e.y)

    def ChangeSize(self, e):
        """Verschiebung des Mittelpunktes bei Veränderung der Fenstergröße"""
        self.MidX = e.width / 2
        self.MidY = e.height / 2
        self.Canvas.coords(self.Mid, self.MidX - 1, self.MidY - 1, self.MidX + 1, self.MidY + 1)
        self.Update()

    def Wheel(self, e):
        """Zoom über das Mausrad"""
        Factor = 1.01 ** (- e.delta / 120)
        self.Camera = Mul(self.Camera, Factor)

        # auch Definitionsvektoren der Projektionsfläche werden verändert,
        # um Drehgeschwindigkeit beizubehalten
        self.ProjectionPlaneTop = Mul(self.ProjectionPlaneTop, Factor)
        self.ProjectionPlaneLeft = Mul(self.ProjectionPlaneLeft, Factor)

        # Maximale Zoomstufe festgelegt
        if Length(self.Camera) < 1:
            Mul(self.Camera, 1 / Length(self.Camera))
        self.Update()

    def Rotate(self, X, Y):
        """dreht die Ansicht um die angegebenen Zahlen"""
        LeftLength = Length(self.ProjectionPlaneLeft)

        # Kamera wird in Richtung Orientierungsvektoren verschoben und auf die vorherige Länge verkürzt
        # zuerst Y-, dann X-Drehung, einzeln da je ein Orientierungsvektor unverändert bleibt und zur Berechnung
        # des anderen verwendet werden kann
        # Orientierungsvektoren werden über Vektorprodukt neu berechnet

        self.Camera = Add(self.Camera, Mul(self.ProjectionPlaneTop, Y))
        self.ProjectionPlaneTop = VP(self.ProjectionPlaneLeft, self.Camera)

        self.Camera = Add(self.Camera, Mul(self.ProjectionPlaneLeft, X))
        self.ProjectionPlaneLeft = VP(self.Camera, self.ProjectionPlaneTop)

        # Längenkorrektur
        self.ProjectionPlaneTop = Mul(self.ProjectionPlaneTop, self.TopLength / Length(self.ProjectionPlaneTop))
        self.ProjectionPlaneLeft = Mul(self.ProjectionPlaneLeft, LeftLength / Length(self.ProjectionPlaneLeft))
        self.Camera = Mul(self.Camera, self.CameraLength / Length(self.Camera))

        self.Update()

    def Update(self):
        """berechnet das Bild neu"""
        self.ComputedPositions = {(0, 0, 0): (self.MidX, self.MidY)}
        self.CameraLength = Length(self.Camera)
        self.TopLength = Length(self.ProjectionPlaneTop)
        # Vektor von Kamera zu Mitte der Projektionsfläche
        self.MidProjection = Sub(self.Camera, Mul(self.Camera, (1 - self.ProjectionPlaneDistance / self.CameraLength)))
        self.Factor = self.ProjectionPlaneDistance * self.CameraLength

        map(object_3D.Line3D.Redraw, self.Drawings)
        map(object_3D.Planet3D.Redraw, self.Items)
        ObjectList = self.Drawings + self.Items
        ObjectList.sort(key = lambda x: Length(Sub(x.MidPoint(), self.Camera)), reverse = True)
        for i in ObjectList:
            self.Canvas.tag_raise(i.Drawing)

    def DisplayDiameter(self, Position, Diameter):
        """berechnet den Anzeigedurchmesser eines Kreises aus dessen Mittelpunkt Position und
dem eigentlichen Durchmesser Diameter"""
        Factor = self.ProjectionPlaneDistance * -self.CameraLength / ScP(Sub(
                 Position, self.Camera), self.Camera)
        return Diameter * Factor * 100

    def DisplayPosition(self, Position):
        """berechnet die Anzeigeposition eines Punktes,
gibt None zurück, wenn sich dieser hinter dem Betrachter befindet"""

        # bisher berechnete Positionen werden in ComputedPositions gespeichert
        # und bei erneutem Aufruf direkt zurückgegeben
        try:
            return self.ComputedPositions[Position]
        except KeyError:
            pass

        # berechnet Abstand des Punktes von der Projektionsfläche
        PlaneDistance = ScP(Sub(Position, self.Camera), self.Camera)

        # prüft, ob der Punkt hinter dem Betrachter liegt
        if PlaneDistance >= 0:
            self.ComputedPositions[Position] = None
            return None

        # berechnet Projektionspunkt relativ zum Mittelpunkt der Projektionsfläche
        ProjectionVector = Add(self.MidProjection, Mul(Sub(Position, self.Camera) , (
            self.Factor / - PlaneDistance)))

        if ProjectionVector == (0,0,0):
            self.ComputedPositions[Position] = (self.MidX, self.MidY)
            return self.MidX, self.MidY


        # berechnet Abstand vom Mittelpunkt der Projektionsfläche
        ProjectionVectorLength = Length(ProjectionVector)

        # berechnet den Winkel für die Koordinatenbestimmung mithilfe von Trigonometrie
        CosTopAngle = ScP(ProjectionVector, self.ProjectionPlaneTop) / (
        ProjectionVectorLength * self.TopLength)

        # Koordinatenbestimmung
        try:
            if ScP(ProjectionVector, self.ProjectionPlaneLeft) < 0:
                Factor = 100
            else:
                Factor = -100
            X = self.MidX + Factor * ProjectionVectorLength * (1 - CosTopAngle ** 2) ** .5
            Y = self.MidY - 100 * ProjectionVectorLength * CosTopAngle
        # falls der Winkel 0° ist
        except ValueError:
            if CosTopAngle > 0:
                Factor = 100
            else:
                Factor = -100
            X = self.MidX
            Y = self.MidY - Factor * ProjectionVectorLength
        self.ComputedPositions[Position] = (X, Y)
        return X, Y

    def LineDisplayCoordinates(self, Position1, Position2):
        """berechnet Bildschirmkoordinaten zur Zeichnung der Linie von
Position1 nach Position2"""
        C1 = self.DisplayPosition(Position1)
        C2 = self.DisplayPosition(Position2)
        # wenn ein Punkt hinter dem Betrachter liegt,
        # wird ein Punkt vor dem Betrachter auf der Linie gefunden
        if C1:
            if not C2:
                Intersection = self.CameraPlaneIntersection(Position1, Position2)
                C2 = self.DisplayPosition(Intersection)
        elif C2:
            Intersection = self.CameraPlaneIntersection(Position2, Position1)
            C1 = self.DisplayPosition(Intersection)
        else:
            return (-5, -5, -5, -5)
        return C1 + C2

    def CameraPlaneIntersection(self, Position1, Position2):
        """berechnet eien Punkt auf der Linie von C1 nach C2 vor dem Betrachter"""
        Line = Sub(Position2, Position1)
        return Mul(Add(Mul(Line, ScP(Sub(Position1, self.Camera), self.Camera) / - ScP(Line, self.Camera)), Position1), 0.999)

    def NewItem(self, Object):
        """erstellt ein 3D-Objekt für den Planeten Object"""
        self.Items.append(object_3D.Planet3D(self, Object))

    def DeleteItem(self, Index):
        """löscht das 3D-Objekt an der Stelle Index"""
        self.Items[Index].Delete()
        del self.Items[Index]

    def MoveItem(self, Index, NewIndex):
        """verschiebt ein 3D-Objekt von Index nach NewIndex"""
        Item = self.Items[Index]
        self.Items.remove(Item)
        self.Items.insert(NewIndex, Item)
