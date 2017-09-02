# -*- coding: cp1252 -*-
import tkinter
import entry

class SettingsEditor(tkinter.Toplevel):
    """eine Dialogfenster für Simulationseinstellungen"""
    def __init__(self, Parent, PlanetManager):
        self.Parent = Parent

        # Fenstereigenschaften
        tkinter.Toplevel.__init__(self, Parent.Window)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.Close)
        self.title("Edit Settings")
        self.geometry("380x150")
        self.resizable(width = False, height = False)

        # Verknüpfung mit zu bearbeitendem Objekt
        self.PlanetManager = PlanetManager

        # Erzeugung der Widgets für die Optionen
        self.Options = {}

        tkinter.Label(self, text = "Time Resolution").place(x = 10, y = 10)
        self.Options["time_resolution"] = entry.Entry(self, 110, 10, self.PlanetManager.TimeResolution, 10)
        tkinter.Label(self, text = "Seconds/Step").place(x = 180, y = 10)

        tkinter.Label(self, text = "Sets, how much time in seconds is between the computed steps.\n\
A lower values gives better accuracy, but needs more performance,\n\
a higher value needs less time to display.", justify = tkinter.LEFT).place(x = 10, y = 35)

        # Dialog-Buttons
        tkinter.Button(self, text = "OK", command = self.OK, relief = tkinter.GROOVE,
                       width = 10).place(x = 95, y = 110)
        tkinter.Button(self, text = "Apply", command = self.Apply, relief = tkinter.GROOVE,
                       width = 10).place(x = 185, y = 110)
        tkinter.Button(self, text = "Cancel", command = self.Close, relief = tkinter.GROOVE,
                       width = 10).place(x = 275, y = 110)

        self.wait_window(self)

    def OK(self):
        """übernimmt die Änderungen und schließt den Dialog"""
        self.Apply()
        self.destroy()

    def Apply(self):
        """übernimmt die Änderungen"""
        TimeResolution = self.Options["time_resolution"].get()
        try:
            TimeResolution = int(TimeResolution)
            self.PlanetManager.TimeResolution = TimeResolution
        except:
            tkinter.messagebox.showwarning("Invalid Input", "Bad Value {0} for Attribute Time Resolution".format(TimeResolution))

    def Close(self):
        """schließt den Dialog"""
        self.destroy()
