# -*- coding: cp1252 -*-
import tkinter
import bar

class Controls:
    """eine Steuerungstoolbar für die Simulation"""
    def __init__(self, Parent, PlanetManager):
        self.Parent = Parent

        self.CreateWidgets()
        self.State = "pause"
        self.PlanetManager = PlanetManager
        self.PlanetManager.RegisterControl(self)

    def CreateWidgets(self):
        """erstellt die Toolbarwidgets"""
        self.HiddenBar = bar.Bar(self.Parent.Window, 25)

        bar.Separator(self.HiddenBar)
        bar.ImageButton(self.HiddenBar, "img/show.xbm", self.Show)

        self.Bar = bar.Bar(self.Parent.Window)

        bar.Separator(self.Bar)
        bar.ImageButton(self.Bar, "img/hide.xbm", self.Hide)
        bar.Separator(self.Bar)
        self.BackwardButton = bar.ImageButton(self.Bar, "img/backward.xbm", self.Backward, True)
        self.StopButton = bar.ImageButton(self.Bar, "img/stop.xbm", self.Stop)
        self.ForwardButton = bar.ImageButton(self.Bar, "img/forward.xbm", self.Forward, True)
        bar.Separator(self.Bar)
        bar.Label(self.Bar, "Speed", 40)
        self.Scale = bar.Scale(self.Bar, 100, 1, 130, self.Speed)
        self.Time = bar.Label(self.Bar, "")

        self.Show()

    def Hide(self):
        """versteckt die Toolbar"""
        self.HiddenBar.grid(row=0, column=2, sticky=tkinter.N + tkinter.W)
        self.Bar.grid_forget()

    def Show(self):
        """zeigt die Toolbar an"""
        self.HiddenBar.grid_forget()
        self.Bar.grid(row=0, column=2,
                        sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

# Methoden um Benutzereingaben an den Planetenmanager weiterzureichen

    def Pause(self):
        self.PlanetManager.SetState("pause")

    def Forward(self):
        self.PlanetManager.SetState("forward")

    def Backward(self):
        self.PlanetManager.SetState("backward")

    def Stop(self):
        self.PlanetManager.SetState("stop")

    def Speed(self, Value):
        self.PlanetManager.SetSpeed(int(Value))

# Methoden um Änderungen des Planetenmanager zu erhalten

    def SetTime(self, Value):
        """formatiert den Sekundenwert Value und zeigt ihn an"""
        TimeString = "{:0>4}:{:0>2}:{:0>2}:{:0>2}"
        self.Time.Set(TimeString.format(Value // 86400, (Value // 3600) % 24, (Value // 60) % 60,
                                        Value % 60))

    def SetSpeed(self, Value):
        """passt die Position des Schiebereglers
entsprechend des Geschwindigkeitswertes Value an"""
        self.Scale.Set(Value)

    def SetState(self, State):
        """passt die Kontrollen entsprechend des Simulationsstatuses State an"""
        if self.State == "forward":
            self.ForwardButton.Command = self.Forward
            self.ForwardButton.Deactivate()
        elif self.State == "backward":
            self.BackwardButton.Command = self.Backward
            self.BackwardButton.Deactivate()
        elif self.State == "stop":
            self.StopButton.Enable()

        self.State = State
        if State == "forward":
            self.ForwardButton.Command = self.Pause
            self.ForwardButton.Activate()
        elif State == "backward":
            self.BackwardButton.Command = self.Pause
            self.BackwardButton.Activate()
        elif State == "stop":
            self.StopButton.Disable()
