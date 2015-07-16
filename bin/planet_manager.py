# -*- coding: cp1252 -*-
import planet
import vector
import time
import threading
import tkMessageBox

class PlanetManager:
    """Objekt zur Verwaltung der Planeten und Simulation der Bewegung dieser"""
    def __init__(self, Parent):
        self.Parent = Parent

        self.Planets = []
        self.Counter = 0

        self.Observers = []
        self.Controls = []

        self.Simulating = False
        self.Play = False
        self.Forward = True
        self.Trace = False

        self.ComputedStep = 0
        self.ShownStep = 0
        self.MaximumStep = 0
        self.TimeResolution = 3600
        self.Time = 0
        self.Speed = 10
        self.Finished = True

    def StartSimulation(self):
        """startet die Simulation und benachrichtigt die Beobachter
Das Fenster kann dabei weiterhin auf Benutzeranfragen reagieren."""
        self.Play = True
        self.Finished = False
        # Vorbereitung der Simulation, falls diese nicht pausiert sondern gestoppt war
        if not self.Simulating:
            self.Simulating = True
            for n in self.Planets:
                n.PrepareSimulation()
        SimThread = threading.Thread(target = self.Simulate)
        SimThread.start()
        StepTime = time.time()
        while self.Play:
            if self.Forward:
                NextStep = self.ShownStep + self.Speed
            else:
                NextStep = self.ShownStep - self.Speed
                if NextStep < 0:
                    NextStep = 0
            # sorgt für korrekte Taktung der Ausgabe
            while self.ComputedStep <= NextStep or time.time() < StepTime + 0.04:
                time.sleep(0.005)
            StepTime += 0.04
            self.ShowStep(NextStep)
            # pausiert die Simulation, wenn beim Zurückspulen
            # der Ursprungszustand erreicht wird
            if not self.Forward and NextStep == 0:
                self.SetState("pause")
            # lässt das Fenster weiterhin auf Ereignisse antworten
            self.Parent.Window.update()

    def PauseSimulation(self):
        """pausiert die Simulation"""
        self.Play = False

    def StopSimulation(self):
        """stoppt die Simulation"""
        self.Play = False
        # wartet auf Beendung des anderen Threads
        while not self.Finished:
            time.sleep(0.005)
        self.SetTime(0)
        self.ComputedStep = 0
        self.ShownStep = 0
        self.MaximumStep = 0
        for n in self.Planets:
            n.RollbackSimulation()
        self.Trace = False
        self.Simulating = False

    def Simulate(self):
        """Thread, der die Berechnung der Planetenpositionen verwaltet"""
        while self.Play:
            # Positionsberechnung begrenzt
            while self.Play and self.ComputedStep > self.ShownStep + 100 * self.Speed:
                time.sleep(0.005)
            self.SimulateStep(self.TimeResolution)
        # zeigt Beendung an
        self.Finished = True

    def SimulateStep(self, Interval):
        """lässt die Planeten ihre Zustände nach der Zeit Interval (als Integer) berechnen"""
        # Jedes Planetenpaar wird nur einmal aufgerufen
        Begin = 0
        Length = len(self.Planets)
        for Planet in self.Planets:
            Begin += 1
            for i in xrange(Begin, Length):
                Planet.GravityOf(self.Planets[i])
            Planet.SavePosition(Interval)
        self.ComputedStep += 1

    def ShowStep(self, Step):
        """lässt die Planeten ihre Zustände beim Schritt Step (als Integer) an
die Observer weitergeben"""
        
        # verhindert Zeichnung einer Spur beim Rückwärtslaufen
        if Step > self.MaximumStep:
            self.MaximumStep = Step
            self.Trace = True
        else:
            self.Trace = False

        for Planet in self.Planets:
            P = Planet.Positions[Step]
            Planet["display_position"] = vector.Vector(P[0], P[1], P[2])
            V = Planet.Velocities[Step]
            Planet["display_velocity"] = vector.Vector(V[0], V[1], V[2])
        self.ShownStep = Step
        # setzt die Zeit für die Anzeige
        self.SetTime(self.TimeResolution * self.ShownStep)

# Methoden zum Speichern / Laden des Objektes

    def Save(self):
        """gibt eine Liste der wichtigen Daten des Objekts als Vorbereitung
für die Speicherung zurück"""
        return ([Planet.Save() for Planet in self.Planets],
                self.TimeResolution, self.Speed)

    def Load(self, Obj):
        """übernimmt die geladenen Daten aus der Liste in die Klasse"""
        for i in range(len(self.Planets)):
            self.Delete(0)
        for Data in Obj[0]:
            self.New()
            self.Planets[-1].Load(Data)
        self.TimeResolution = Obj[1]
        self.SetSpeed(Obj[2])

# Methoden für Zugriff von Beobachter

    def Register(self, Object):
        """fügt Object als Beobachter hinzu,
dieser benötigt eine update-Methode"""
        self.Observers.append(Object)

    def Deregister(self, Object):
        """löscht Object aus den Beobachtern"""
        self.Observers.remove(Object)

    def New(self):
        """fügt einen neuen Planeten hinzu und benachrichtigt die Observer"""
        if self.Simulating:
            return 1
        Object = planet.Planet(self, "Object {0}".format(self.Counter))
        self.Counter += 1
        self.Planets.append(Object)

        for Observer in self.Observers:
            Observer.NewItem(Object)

    def Delete(self, Index):
        """löscht den Planeten an der Stelle Index und benachrichtigt die Observer"""
        if self.Simulating:
            return 1
        del self.Planets[Index]

        for Observer in self.Observers:
            Observer.DeleteItem(Index)

    def Move(self, Index, NewIndex):
        """verschiebt den Planeten an der Stelle Index nach NewIndex
und benachrichtigt die Observer"""
        if self.Simulating:
            return 1
        Object = self.Planets.pop(Index)
        self.Planets.insert(NewIndex, Object)

        for Observer in self.Observers:
            Observer.MoveItem(Index, NewIndex)

# Methoden für Zugriff von Steuerungen

    def RegisterControl(self, Object):
        """fügt Object als Steuerung hinzu,
diese benötigt die Methoden SetState, SetTime und SetState"""
        self.Controls.append(Object)
        Object.SetSpeed(self.Speed)
        Object.SetTime(self.Time)
        if self.Simulating:
            if self.Play:
                if self.Forward:
                    Object.SetState("forward")
                else:
                    Object.SetState("backward")
            else:
                Object.SetState("pause")
        else:
            Object.SetState("stop")


    def DeregisterControl(self, Object):
        """löscht Object aus den Steuerungen"""
        self.Controls.remove(Object)

    def SetTime(self, Value):
        """setzt Value (als Integer) als Zeit und gibt sie an die Steuerungen weiter"""
        self.Time = Value
        for Control in self.Controls:
            Control.SetTime(Value)

    def SetSpeed(self, Value):
        """setzt Value (als Integer) als Geschwindigkeit
und gibt sie an die Steuerungen weiter"""
        self.Speed = Value
        for Control in self.Controls:
            Control.SetSpeed(Value)

    def SetState(self, State):
        """startet, stoppt, pausiert oder ändert die Richtung der Simulation
abhängig vom String State: kann "pause", "forward", "backward" oder "stop" sein
benachrichtigt die Steuerung"""
        StartSim = False
        if State == "pause":
            self.PauseSimulation()
        elif State == "forward":
            self.Forward = True
            if not self.Play:
                StartSim = True
        elif State == "backward":
            self.Forward = False
            if not self.Play:
                StartSim = True
        elif State == "stop":
            self.StopSimulation()

        for Control in self.Controls:
            Control.SetState(State)
        if StartSim:
            self.StartSimulation()

    def Simulation(self):
        """gibt als Bool zurück, ob gerade eine Simulation läuft"""
        return self.Simulating
