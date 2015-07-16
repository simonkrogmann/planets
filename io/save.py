# -*- coding: cp1252 -*-
def Save(Obj):
    """Wandelt ein Standard-Python-Objekt in einen String um, der gespeichert werden kann"""
    return SaveObj(Obj)

def SaveObj(Obj):
    """Methode zur Auswahl der Umwandlungsmethode"""
    Type = type(Obj)
    if Type in SaveMethods:
        String = SaveMethods[Type](Obj)
    else:
        String = Obj.Identifier + SaveObj(Obj.Save())
    return String

# Methoden zum Umwandeln der entsprechenden Objekte
def SaveBool(Obj):
    return "b" + str(int(Obj))

def SaveNone(Obj):
    return "n"

def SaveNumber(Obj):
    return "i" + str(Obj)

def SaveFloat(Obj):
    return "f" + str(Obj)

def SaveStr(Obj):
    return "s" + str(len(Obj)) + "'" + Obj

def SaveList(Obj):
    return "l" + str(len(Obj)) + "".join([SaveObj(Element) for Element in Obj])

def SaveTuple(Obj):
    return "t" + str(len(Obj)) + "".join([SaveObj(Element) for Element in Obj])

def SaveDict(Obj):
    return ("d" + str(len(Obj)) +
            "".join(SaveObj(Element) + SaveObj(Obj[Element]) for Element in Obj))

# Zuordnung Objekttyp => Umwandlungsmethode
SaveMethods = {bool: SaveBool,
               type(None): SaveNone,
               int: SaveNumber,
               long: SaveNumber,
               float: SaveFloat,
               str: SaveStr,
               list: SaveList,
               tuple: SaveTuple,
               dict: SaveDict}
