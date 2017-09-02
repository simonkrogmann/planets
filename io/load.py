# -*- coding: cp1252 -*-
import sys
sys.path.append("..\\bin")
import vector

def Load(String):
    """wandelt einen aus einer Datei geladenen String in das entsprechende Objekt um"""
    return LoadObj(String, Count())

def LoadObj(String, Index):
    """Methode zur Auswahl der Umwandlungsmethode"""
    Identifier = String[Index.V]
    Index.V += 1
    if Identifier in LoadMethods:
        return LoadMethods[Identifier](String, Index)

class Count:
    """Eine einfache Klasse mit einem Attribut, die als Zähler verwendet werden kann"""
    def __init__(self, V=0):
        self.V = V

# Methoden zum Umwandeln der entsprechenden Objekte
def LoadBool(String, Index):
    Index.V += 1
    return bool(int(String[Index.V - 1]))

def LoadNone(String, Index):
    return None

def LoadNumber(String, Index):
    Begin = Index.V
    while Index.V < len(String) and (String[Index.V].isdigit() or String[Index.V] in "+-e"):
        Index.V += 1
    return int(String[Begin:Index.V])

def LoadFloat(String, Index):
    Begin = Index.V
    while Index.V < len(String) and (String[Index.V].isdigit() or String[Index.V] in "+-.e"):
        Index.V += 1
    return float(String[Begin:Index.V])

def LoadStr(String, Index):
    Begin = Index.V + 2
    Index.V += LoadNumber(String, Index) + 2
    return String[Begin:Index.V]

def LoadList(String, Index):
    Length = LoadNumber(String, Index)
    return [LoadObj(String, Index) for i in range(Length)]

def LoadTuple(String, Index):
    Length = LoadNumber(String, Index)
    return tuple(LoadObj(String, Index) for i in range(Length))

def LoadDict(String, Index):
    Length = LoadNumber(String, Index)
    return dict((LoadObj(String, Index), LoadObj(String, Index)) for i in range(Length))

def LoadVector(String, Index):
    Index.V += 2
    X = LoadObj(String, Index)
    Y = LoadObj(String, Index)
    Z = LoadObj(String, Index)
    return vector.Vector(X, Y, Z)

# Zuordnung Buchstabe => Umwandlungsmethode
LoadMethods = {"b" : LoadBool,
               "n" : LoadNone,
               "i" : LoadNumber,
               "f" : LoadFloat,
               "s" : LoadStr,
               "l" : LoadList,
               "t" : LoadTuple,
               "d" : LoadDict,
               "v" : LoadVector}
