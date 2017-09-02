# -*- coding: cp1252 -*-
import tkinter
import scrollbar
import item
import item_info
import item_editor
import bar

class Sidebar:
    """Dieses Modul stellt die Seitenleiste mit der Liste bereit"""
    Width = 190
    def __init__(self, Parent, SimulationMethod, MenuMethod = None):
        self.Parent = Parent
        self.Simulation = SimulationMethod
        self.Parent.PlanetManager.Register(self)

        self.CreateToolBar(MenuMethod)

        self.Canvas = tkinter.Canvas(self.Parent.Window, takefocus = True, borderwidth = -2,
                                     width = Sidebar.Width + 4, background = "darkgrey",
                                     highlightthickness = 0)

        self.Scrollbar = scrollbar.Scrollbar(self, Sidebar.Width)
        self.Canvas.bind("<Button-1>", self.CloseInfo)
        self.Canvas.bind("<Button-3>", self.Context)
        self.Canvas.bind("<Enter>", self.Focus)

        self.Items = []
        self.Active = []
        self.RightClicked = None
        self.OpenInfo = None
        self.SelectionChanged()

        self.BuildContextMenu()
        self.Show()

    def CreateToolBar(self, MenuMethod):
        """erstellt die Toolbar über der Liste"""
        self.HiddenBar = bar.Bar(self.Parent.Window, 24)
        bar.ImageButton(self.HiddenBar, "img/right.xbm", self.Show)

        self.Bar = bar.Bar(self.Parent.Window)
        if MenuMethod:
            self.MenuMethod = MenuMethod
            self.MenuButton = bar.ImageButton(self.Bar,"img/menu.xbm", self.ShowMenu)
            bar.Separator(self.Bar)
            Space = 121
        else:
            Space = 100
        bar.ImageButton(self.Bar, "img/new.xbm", self.New)
        self.EditButton = bar.ImageButton(self.Bar, "img/edit.xbm", self.Edit)
        self.InfoButton = bar.ImageButton(self.Bar, "img/info.xbm", self.Info)
        bar.Label(self.Bar, "", Sidebar.Width - Space)
        self.DeleteButton = bar.ImageButton(self.Bar, "img/delete.xbm", self.Delete)
        bar.ImageButton(self.Bar, "img/left.xbm", self.Hide)

    def Hide(self):
        """versteckt die Seitenleiste"""
        self.CloseInfo()
        self.HiddenBar.grid(row = 0, column = 1, sticky = tkinter.N + tkinter.W)
        self.Bar.grid_forget()
        self.Canvas.grid_forget()

    def Show(self):
        """zeigt die Seitenleiste"""
        self.HiddenBar.grid_forget()
        self.Bar.grid(row = 0, column = 0,
                      sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self.Canvas.grid(row = 1, column = 0,
                         sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

    def ShowMenu(self):
        """zeigt das Hauptmenü"""
        if not self.Simulation():
            self.MenuMethod(self.Canvas.winfo_rootx(), self.Canvas.winfo_rooty())
        else:
            self.SimulationWarning()

    def SelectionChanged(self):
        """passt die Toolbar bei veränderter Auswahl an"""
        self.CloseInfo()
        if len(self.Active) == 1:
            self.EditButton.Enable()
            self.InfoButton.Enable()
        else:
            self.EditButton.Disable()
            self.InfoButton.Disable()
        if len(self.Active) == 0:
            self.DeleteButton.Disable()
        else:
            self.DeleteButton.Enable()

    def BuildContextMenu(self):
        """erstellt das Rechtsklickmenü"""
        # Menüvorlage
        self.ContextMenuTemplate = (("New",         self.New),
                                    ("Info",        self.Info),
                                    ("Edit",        self.Edit),
                                    ("Delete",      self.Delete)
                                    )
        self.ContextMenuDict = {}
        self.ContextMenu = tkinter.Menu(None, tearoff=0, takefocus=0)
        self.Parent.BuildMenu(self.ContextMenuTemplate, self.ContextMenu, self.ContextMenuDict)

# Methoden für GUI-Ereignisse

    def Activate(self, Item, e = None):
        """aktiviert und hebt ein oder mehrere Elemente hervor"""
        # return-Wert gibt an, ob Item verschoben werden kann
        # (nur bei einzelner Auswahl verschiebbar)

        if e and e.state == 1 and self.Active: # Shift, fügt mehrere Elemente zur Auswahl hinzu
            Index1 = Item.Index()
            Index2 = self.Active[-1].Index()
            MinIndex = min(Index1, Index2)
            MaxIndex = max(Index1, Index2)
            for n in self.Items[MinIndex:MaxIndex + 1]:
                n.Activate()

        elif e and e.state == 4: # Control, fügt Element zur Auswahl hinzu
            if not Item.Active():
                Item.Activate()
            else:
                Item.Deactivate()
        else:
            for n in self.Active[:]:
                n.Deactivate()
            Item.Activate()
            if e:
                self.SelectionChanged()
                return True
        self.SelectionChanged()
        return False

    def RightClick(self, e, Item):
        """speichert den geklickten Listeneintrag"""
        self.RightClicked = Item

    def Context(self, e):
        """öffnet ein Kontextmenü"""
        self.CloseInfo()
        # prüft, ob auf ein Element oder den Zwischenraum geklickt wurde
        if self.RightClicked:
            # Aktiviert geklicktes Objekt, wenn es nicht ausgewählt ist
            if not self.RightClicked in self.Active:
                self.Activate(self.RightClicked, e)
            # Deaktiviert 'Edit' bei mehreren ausgewählten Objekten
            self.Parent.ConfigMenuEntry("Edit", self.ContextMenuDict, len(self.Active) == 1)
            self.Parent.ConfigMenuEntry("Info", self.ContextMenuDict, len(self.Active) == 1)
            self.Parent.ConfigMenuEntry("Delete", self.ContextMenuDict, True)
        else:
            self.Parent.ConfigMenuEntry("Edit", self.ContextMenuDict, False)
            self.Parent.ConfigMenuEntry("Info", self.ContextMenuDict, False)
            self.Parent.ConfigMenuEntry("Delete", self.ContextMenuDict, False)
        self.ContextMenu.tk_popup(e.x_root, e.y_root)
        self.RightClicked = None

    def Focus(self, e):
        """setzt den Fokus auf das Canvas-Objekt"""
        self.Canvas.focus_set()

    def Drag(self, Item, Height):
        """bewegt ein Element Item durch die Liste und passt den Index an"""
        NewIndex = Height / float(item.Item.Height)
        Index = Item.Index()
        while NewIndex - Index > 0.5 and NewIndex < len(self.Items) - 1:
            self.Move(Index + 1, Index)
            Index += 1
        while Index - NewIndex > 0.5 and NewIndex > 0:
            self.Move(Index - 1, Index)
            Index -= 1
        Item.UpdatePosition(NewIndex)

# Observer-Methoden

    def NewItem(self, Planet):
        """legt einen neuen Listeneintrag an und verknüpft ihn mit dem Planeten"""
        Item = item.Item(self, len(self.Items), Planet, self.Simulation, Sidebar.Width)
        self.Items.append(Item)
        self.Activate(Item)
        self.Scrollbar.UpdateRegion()
        self.ShowItem(Item)

    def DeleteItem(self, Index):
        """löscht den Listeneintrag an der Stelle Index"""
        self.Items[Index].Delete()
        del self.Items[Index]

        for Item in self.Items:
            Item.UpdatePosition()
        self.Scrollbar.UpdateRegion()
        self.SelectionChanged()

    def MoveItem(self, Index, NewIndex):
        """bewegt einen Listeneintrag von Index nach NewIndex"""
        Item = self.Items[Index]
        self.Items.remove(Item)
        self.Items.insert(NewIndex, Item)

        Item.UpdatePosition()

# Methoden für Bearbeiten von Objekten

    def New(self):
        """lässt Planetenmanager neuen Planeten erstellen"""
        if not self.Simulation():
            self.Parent.PlanetManager.New()
        else:
            self.SimulationWarning()

    def Delete(self):
        """lässt Planetenmanager Planeten löschen"""
        if not self.Simulation():
            for Item in self.Active[:]:
                self.Parent.PlanetManager.Delete(self.Items.index(Item))
        else:
            self.SimulationWarning()


    def Move(self, Index, NewIndex):
        """lässt Planetenmanager die Listenposition von Planeten ändern"""
        if not self.Simulation():
            self.Parent.PlanetManager.Move(Index, NewIndex)


    def Edit(self):
        """öffnet den Planeteneditor"""
        if not self.Simulation():
            item_editor.ItemEditor(self.Parent, self.Active[0])
        else:
            self.SimulationWarning()


    def Info(self):
        """öffnet den Infobereich für einen Planeten"""
        self.CloseInfo()
        self.OpenInfo = item_info.ItemInfo(self.Parent, self.Active[0], Sidebar.Width)

    def CloseInfo(self, e = None):
        """schließt einen evtl. offenen Infobereich"""
        if self.OpenInfo:
            self.OpenInfo.Close()
            self.OpenInfo = None

    def Height(self):
        """gibt die Höhe der gesamten Liste zurück"""
        return item.Item.Height * len(self.Items)

    def ShowItem(self, Item):
        """lässt die Scrollbar einen bestimmten Planeten anzeigen"""
        self.Scrollbar.Show(Item.Position)

    def SimulationWarning(self):
        """zeigt ein Warnungsfenster, wenn für eine Aktion erst die Simulation gestoppt werden muss"""
        tkinter.messagebox.showwarning("Simulation Running",
"Stop the Simulation by clicking on the square in the toolbar to proceed with this action.")
