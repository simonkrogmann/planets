# -*- coding: cp1252 -*-
import math
from constants import Str

class Vector(object):
    """stellt einen Vektor und dessen Grundoperationen bereit, kann auch als Punkt im 3-dimensionalen Raum verwendet werden"""
    Identifier = "v"
    def __init__(self, X = 0,Y = 0, Z = 0):
        self._x = float(X)
        self._y = float(Y)
        self._z = float(Z)

    def _GetX(self):
        return self._x
    def _SetX(self, X):
        self._x = float(X)
    X = property(_GetX, _SetX, doc = "X-Komponente des Vektors")

    def _GetY(self):
        return self._y
    def _SetY(self, Y):
        self._y = float(Y)
    Y = property(_GetY, _SetY, doc = "Y-Koponente des Vektors")

    def _GetZ(self):
        return self._z
    def _SetZ(self, Z):
        self._z = float(Z)
    Z = property(_GetZ, _SetZ, doc = "Z-Koponente des Vektors")

    def _GetLength(self):
        Distance = abs(self)
        return (Distance.X ** 2 + Distance.Y ** 2 + Distance.Z ** 2) ** .5
    def _SetLength(self, Length):
        if self.Length:
            Factor = Length / self.Length
            self.X *= Factor
            self.Y *= Factor
            self.Z *= Factor
    Length = property(_GetLength, _SetLength, doc = "Länge des Vektors")

# arithmetische Standardoperationen

    def __add__(self, a):
        """=> self + a
a als Vektor"""
        assert isinstance(a, Vector)
        return Vector(self.X + a.X, self.Y + a.Y, self.Z + a.Z)

    def __sub__(self, a):
        """=> self - a
a als Vektor"""
        assert isinstance(a, Vector)
        return Vector(self.X - a.X, self.Y - a.Y, self.Z - a.Z)

    def __mul__(self, a):
        """=> self * a
a als Zahl"""
        assert type(a) in [int, long, float]
        return Vector(self.X * a, self.Y * a, self.Z * a)

    def __rmul__(self, a):
        """=> a * self
a als Zahl"""
        return self * a

    def __div__(self, a):
        """=> self / a
a als Zahl"""
        assert type(a) in [int, long, float]
        return Vector(self.X / a, self.Y / a, self.Z / a)

    def __pow__(self, a):
        """nimmt die Länge des Vektors hoch der Zahl a,
verändert aber nicht die Richtung"""
        assert type(a) in [int, long, float]
        Factor = self.Length ** (a - 1)
        return self * Factor

    def __abs__(self):
        """gibt den Vektor mit positiven Koordinaten zurück"""
        return Vector(abs(self.X), abs(self.Y), abs(self.Z))

    def __neg__(self):
        """gibt den Vektor in die Gegenrichtung zurück"""
        return Vector(-self.X, -self.Y, -self.Z)

    def __pos__(self):
        """gibt den Vektor zurück"""
        return Vector(self.X, self.Y, self.Z)

    def __str__(self):
        """=> Display"""
        return self.Display()

    def __repr__(self):
        """=> __str__"""
        return str(self)

    def __eq__(self, a):
        """=> self == a
a als Vektor"""
        if self.X == a.X and self.Y == a.Y and self.Z == a.Z:
            return True

# Operationen der Vektorechnung
    def ScalarProduct(self, a):
        """berechnet das Skalarprodukt von self und dem Vektor a"""
        assert isinstance(a, Vector)
        return self.X * a.X + self.Y * a.Y + self.Z * a.Z

    def VectorProduct(self, a):
        """berechnet einen Vektor der senkrecht zu self und dem Vektor a ist"""
        assert isinstance(a, Vector)
        X = self.Y * a.Z - self.Z * a.Y
        Y = self.Z * a.X - self.X * a.Z
        Z = self.X * a.Y - self.Y * a.X
        return Vector(X, Y, Z)

    def Angle(self, a):
        """berechnet den Winkel zwischen self und dem Vektor a"""
        assert isinstance(a, Vector)
        if self.Length == 0 or a.Length == 0:
            return 0.0
        Quotient = self.ScalarProduct(a) / float(self.Length * a.Length)
        # bei Rundungsfehlern können Werte außerhalb der Grenze
        # der acos Funktion entstehen
        if Quotient > 1 or Quotient < -1:
            return 0.0
        return math.acos(Quotient)

    def DistanceTo(self, a):
        """berechnet den Abstand zwischen self und dem Vektor a"""
        assert isinstance(a, Vector)
        return (self - a).Length

    def Display(self):
        """gibt einen String zur Darstellung zurück"""
        return Str(self.X) + ", " + Str(self.Y) + ", " + Str(self.Z)

    def Tuple(self):
        """gibt die Komponenten des Vektors als Tupel zurück"""
        return(self.X, self.Y, self.Z)

    Save = Tuple
