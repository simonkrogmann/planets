# -*- coding: cp1252 -*-
import vector
from constants import G, pi
# Rechnungen erfolgen mit Standardeinheiten

class Planet(object):
    """Objekt, das einen einzelnen Planeten, Stern etc. darstellt"""
    def __init__(self, Parent, Name, Position = vector.Vector(0, 0, 0), Velocity = vector.Vector(0, 0, 0),
                 Mass = 1, Diameter = 1e10, Trace = True, Fixed = False, Color = "yellow"):
        self.Parent = Parent
        self.Force = vector.Vector(0,0,0)
        self.Positions = []
        self.Velocities = []
        # Speicherung der Daten in einem Dictionary
        self.Data = {"position" : Position, "velocity": Velocity, "mass": Mass,
                     "diameter" : Diameter, "name" : Name, "trace" : Trace, "fixed" : Fixed,
                     "color": Color}
        self.Observers = []

    def Save(self):
        """gibt die Planetendaten als Dictionary zurück"""
        return self.Data

    def Load(self, Obj):
        """übernimmt die Daten aus dem Dictionary Obj ins Objekt"""
        for Tag in Obj:
            self[Tag] = Obj[Tag]

    def __getitem__(self, Tag):
        """gibt die zum String Tag gehörige Eigenschaft zurück"""
        return self.Data[Tag]

    def __setitem__(self, Tag, Value):
        """setzt die zum String Tag gehörige Eigenschaft auf den Wert Value
und benachrichtigt die Beobachter
Bei Voranstellung von 'display_' wird das Attribut nicht bearbeitet
und nur die Beobachter werden informiert."""
        if Tag.startswith("display_"):
            for Observer in self.Observers:
                Observer.Update(Tag[8:], Value)
        elif not self.Parent.Simulating:
            if Tag == "mass" and Value == 0:
                return
            self.Data[Tag] = Value
            for Observer in self.Observers:
                Observer.Update(Tag, Value)

    def Register(self, Object):
        """Das Objekt Object wird als Beobachter angemeldet.
Es muss eine update-Methode haben."""
        self.Observers.append(Object)

    def Deregister(self, Object):
        """Das Objekt Object wird als Beobachter abgemeldet."""
        self.Observers.remove(Object)

    def PrepareSimulation(self):
        """Macht Simulationsvorbereitungen"""
        self.SimPosition = self["position"]
        self.SimVelocity = self["velocity"]
        self.Positions = [self.SimPosition.Tuple()]
        self.Velocities = [self.SimVelocity.Tuple()]

    def RollbackSimulation(self):
        """sorgt für Rücksetzen auf die Bedingungen vor der Simulation"""
        self["display_position"] = self["position"]
        self["display_velocity"] = self["velocity"]
        # löscht die Spur
        self["display_trace"] = False
        self["display_trace"] = True
        self.Positions = []
        self.Velocities = []

    def __add__(self, a):
        """fügt zwei Planeten zusammen unter Beachtung aller physikalischen Attribute,
wird nicht genutzt und ist möglicherweise fehlerhaft"""
        if isinstance(a, Planet):
            Mass = self["mass"] + a["mass"]
            Position = (self["position"] + a["position"]) / 2
            Energy = .5 * (self["mass"] * self["velocity"] ** 2 + a["mass"] * a["velocity"] ** 2)
            Velocity = (2 * Energy / Mass) ** .5
            Diameter = (self["diameter"] ** 3 + a["diameter"] ** 3) ** (1 / 3.0)
            return Planet(self.Parent, self["name"], Position, Velocity, Mass, Diameter)
        else:
            raise TypeError("unsupported type")

    def GravityOf(self, a):
        """berechnet die Gravitationskraft zwischen zwei Planeten und fügt sie zu deren Gesamtkraft hinzu"""
        try:
            Direction = a.SimPosition - self.SimPosition
            Direction.Length = G * (self["mass"] * a["mass"]) / (self.SimPosition.DistanceTo(a.SimPosition)) ** 2
            if not self["fixed"]:
                self.Force += Direction

            if not a["fixed"]:
                a.Force -= Direction
        except:
            pass

    def CollidesWith(self, a):
        """prüft, ob zwei Planeten kollidieren,
wird nicht genutzt und ist möglicherweise fehlerhaft"""
        return self["position"].DistanceTo(a["position"]) < self["diameter"] + a["diameter"]

    def SavePosition(self, Interval):
        """berechnet aus der Gesamtkraft die Position und die Geschwindigkeit nach der Zeit Interval
und speichert diese"""
        self.SimPosition += self.Force / self["mass"] * (.5 * Interval ** 2) + self.SimVelocity * Interval
        self.Positions.append(self.SimPosition.Tuple())
        self.SimVelocity += self.Force / self["mass"] * Interval
        self.Velocities.append(self.SimVelocity.Tuple())
        self.Force = vector.Vector(0,0,0)

    def __str__(self):
        """gibt die physikalischen Daten des Planeten als String zurück"""
        return "Planet(Name = " + self["name"] + ", Position = " + str(self["position"]) + ", Velocity = \
" + str(self["velocity"]) + ", Mass = " + str(self["mass"]) + ", Diameter = " + str(self["diameter"]) + ")"

    def __repr__(self):
        """=> str"""
        return str(self)
