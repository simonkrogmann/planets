# -*- coding: cp1252 -*-
import sys
sys.path.append("bin")
sys.path.append("gui")
sys.path.append("io")
import Tkinter
import tkMessageBox
import urllib
import os
import webbrowser
import sidebar
import graphics
import planet_manager
import io_gui
import controls
import threading
import settings_editor

class PlanetsGUI:
    """Die zentrale Klasse des Programm Planets"""
    Separator = "sep"

    def __init__(self):
        self.Data()
        self.CreateWindow()
        self.BuildTopMenu()
        self.PlanetManager = planet_manager.PlanetManager(self)
        self.Graphics = graphics.Graphics(self, self.PlanetManager)
        sidebar.Sidebar(self, self.PlanetManager.Simulation, self.ShowMenu)
        controls.Controls(self, self.PlanetManager)
        self.IO = io_gui.IOGui("plts", self.Window, "Planets-Datei", "example")
        self.NewFile()

    def Data(self):
        """legt verschiedene Metadaten für das Programm fest"""
        self.Title = "Planets"
        self.Version = "1.2.1"
        self.Author = "Simon Krogmann"
        self.Website = "http://planetssoftware.funpic.de/"

# Methoden um GUI zu erstellen

    def CreateWindow(self):
        """erstellt das Fenster und legt die Grundeigenschaften fest"""
        self.Window = Tkinter.Tk()
        self.Window.geometry("900x500")
        self.Window.title(self.Title)
        self.Window.protocol("WM_DELETE_WINDOW", self.Close)

        self.Window.grid_rowconfigure(1, weight = 1, pad = 0)
        self.Window.grid_columnconfigure(2, weight = 1, pad = 0)

    def BuildTopMenu(self):
        """erstellt das Hauptmenü"""
        # Menüvorlage
        self.MenuBarTemplate = (("New File",    self.NewFile),
                                ("Load",        self.Load),
                                ("Save",        self.Save),
                                ("Save As",     self.SaveAs),
                                PlanetsGUI.Separator,
                                ("Settings",    self.Settings),
                                PlanetsGUI.Separator,
                                ("Update",      self.Update),
                                ("About",       self.About),
                                ("Help",        self.Help),
                                PlanetsGUI.Separator,
                                ("Close",       self.Close)
                                )
        self.MenuBarDict = {}

        # erstellt Menü
        self.Menu = Tkinter.Menu(None, tearoff=0, takefocus=0)
        self.BuildMenu(self.MenuBarTemplate, self.Menu, self.MenuBarDict)

    def BuildMenu(self, MenuTemplate, CurrentMenu, MenuDict):
        """rekursive Funktion um ein Menü aus einer Vorlage zu erstellen"""
        for MenuEntry in MenuTemplate:

            if MenuEntry == PlanetsGUI.Separator:
                # Neuer Trennstrich
                CurrentMenu.add_separator()

            elif type(MenuEntry[1]) == tuple:
                # Neues Untermenü
                NewMenu = Tkinter.Menu(CurrentMenu, tearoff = 0)
                CurrentMenu.add_cascade(label = MenuEntry[0], menu = NewMenu)
                self.BuildMenu(MenuEntry[1], NewMenu, MenuDict)

            else:
                # Neuer Eintrag
                CurrentMenu.add_command(label = MenuEntry[0], command = MenuEntry[1])

                # speichert Ort eines Eintrags für spätere Bearbeitung
                MenuDict[MenuEntry[0]] = CurrentMenu

# Methoden um GUI zu bearbeiten

    def ConfigMenuEntry(self, Label, MenuDict, Enabled = True):
        """aktiviert/deaktiviert einen Menüeintrag eines mit BuildMenu erstellten Menüs"""
        Menu = MenuDict[Label]
        Index = Menu.index(Label)
        if Enabled:
            Menu.entryconfig(Index, state = Tkinter.NORMAL)
        else:
            Menu.entryconfig(Index, state = Tkinter.DISABLED)

# Methoden für Nutzeraktionen

    def ShowMenu(self, X, Y):
        """zeigt das Menü an, X und Y müssen als Bildschirmkoordinaten angegeben werden"""
        self.Menu.tk_popup(X, Y)

    def NewFile(self):
        """lädt eine leere Vorlage in das Programm"""
        Obj = self.IO.LoadTemplate("io/empty.plts")
        if Obj:
            self.PlanetManager.Load(Obj[0])
            self.Graphics.Load(Obj[1])

    def Load(self):
        """lässt den Benutzer eine Datei zum Laden auswählen"""
        Obj = self.IO.Load()
        if Obj:
            self.PlanetManager.Load(Obj[0])
            self.Graphics.Load(Obj[1])

    def Save(self):
        """speichert die aktuellen Daten in der aktuellen Datei"""
        Obj = self.PlanetManager.Save(), self.Graphics.Save()
        self.IO.Save(Obj)

    def SaveAs(self):
        """speichert die aktuellen Daten an einem vom Nutzer ausgewählten Ort"""
        Obj = self.PlanetManager.Save(), self.Graphics.Save()
        self.IO.SaveAt(Obj)

    def Settings(self):
        """öffnet das EInstellungsfenster"""
        settings_editor.SettingsEditor(self, self.PlanetManager)

    def Update(self):
        """ruft die aktuelle Versionsnummer aus dem Internet ab und bietet ein Update an,
wenn eine neue Version vorhanden ist"""
        try:
            VersionData = urllib.urlopen("{0}version.data".format(self.Website)).read()
        except:
            tkMessageBox.showinfo("Update", "The update server is currently unavailable.\n\
                                  Check your internet connection or try again later.")
            return

        NewVersion = VersionData.splitlines()[0]
        if NewVersion == self.Version:
            tkMessageBox.showinfo("Update", "You are using the newest version of Planets.")
        else:
            if tkMessageBox.askyesno("Update", "You are using version {0}. \
Do you want to upgrade to version {1}?".format(self.Version, NewVersion)):
                VersionFile = file("update/version.data", "w")
                VersionFile.write(self.Version)
                VersionFile.close()

                UpdateData = urllib.urlopen(self.Website + "update/{0}.py".format(NewVersion)).read()
                UpdateFile = file("update/update.py", "w")
                UpdateFile.write(UpdateData)
                UpdateFile.close()

                os.system("py update/update.py")
                self.Close()

    def About(self):
        """zeigt Versionsnummer und Credits an"""
        tkMessageBox.showinfo("Version {0}".format(self.Version), "Created by {0}".format(self.Author))

    def Help(self):
        """öffnet die Hilfe im Webbrowser"""
        os.system("start explorer \"help\help.pdf\"")

    def Close(self):
        """schließt das Programm"""
        if self.PlanetManager.Simulating:
            self.PlanetManager.SetState("stop")
        Obj = self.PlanetManager.Save(), self.Graphics.Save()
        if self.IO.Close(Obj):
            self.Window.after(100, self.Window.destroy)

if __name__ == "__main__":
    Program = PlanetsGUI()
    Program.Window.mainloop()
