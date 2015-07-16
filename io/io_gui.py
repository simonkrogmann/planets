# -*- coding: cp1252 -*-
from load import Load
from save import Save
from tkFileDialog import asksaveasfilename,askopenfilename
from tkMessageBox import askyesnocancel

class IOGui:
    """Dieses Modul stellt eine Oberfl�che und Verwaltung
f�r das Speichern von Python-Standard-Objekten in Dateien bereit."""
    def __init__(self, Extension, Parent, Type, InitialDirectory = None, Autosave = False):
        self.Parent = Parent
        self.Type = Type
        self.Extension = Extension
        self.Autosave = Autosave
        self.InitialDirectory = InitialDirectory
        self.New()

    def New(self):
        """setzt die Werte der Klasse zur�ck"""
        self.Path = self.InitialDirectory
        self.File = None
        # kann ver�ndert werden, um vor dem Verlieren von �nderungen warnen zu k�nnen
        self.Saved = True

    def Save(self, obj):
        """Speichert ein Objekt.
Falls noch kein Speicherort festgelegt ist, wird SaveAt aufgerufen"""
        try:
            if self.File:
                SaveStr = Save(obj)
                f=file(self.File, "w")
                f.write(SaveStr)
                f.close()
            else:
                return self.SaveAt(obj)
        except:
            return 2
        self.Saved = True
        return 0

    def SaveAt(self, obj):
        """Fragt �ber den Windows-Dialog einen Speicherort ab, und speichert das Objekt dort"""
        try:
            if self.Path:
                Target = asksaveasfilename(filetypes = [(self.Type, "." + self.Extension)],
                                           parent = self.Parent, initialdir = self.Path)
            else:
                Target = asksaveasfilename(filetypes = [(self.Type, "." + self.Extension)],
                                           parent = self.Parent)
            if Target:
                self.Path = Target.rpartition("/")[0]
                if not Target.endswith("."  + self.Extension):
                    Target += "." + self.Extension
                self.File = Target
                SaveStr = Save(obj)
                f = file(Target, "w")
                f.write(SaveStr)
                f.close()
            else:
                return 1
        except:
            return 2
        self.Saved = True
        return 0

    def LoadTemplate(self, Target):
        """l�dt eine Vorlage am Speicherort Target in die Datei"""
        try:
            f = file(Target, "r")
            Content = f.read()
            f.close()
            obj = Load(Content)
            self.Saved = True
            return obj
        except:
            pass

    def Load(self):
        """Fragt �ber den Windows-Dialog eine zu �ffnende Datei ab
und gibt den geladenen Inhalt zur�ck"""
        try:
            if self.Path:
                Target = askopenfilename(filetypes=[(self.Type, "." + self.Extension)],
                                         parent = self.Parent, initialdir = self.Path)
            else:
                Target = askopenfilename(filetypes=[(self.Type, "." + self.Extension)],
                                         parent = self.Parent)
            if Target:
                self.Path = Target.rpartition("/")[0]
                self.File = Target
                f = file(Target, "r")
                Content = f.read()
                f.close()
                obj = Load(Content)
                self.Saved = True
                return obj
        except:
            pass

    def Close(self, obj):
        """fragt den Nutzer bei ungespeicherten �nderungen,
ob das Fenster geschlossen werden kann, gibt Antwort zur�ck"""
        Close = True
        if not self.Saved:
            if self.Autosave:
                self.Save(obj)
            else:
                tmp = askyesnocancel("Wirklich beenden?", "M�chten Sie Ihre �nderungen speichern?")
                if tmp == None:
                    Close = False
                elif tmp:
                    self.Save(obj)
        return Close
