from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class arrayDefenition(abstractObject):
    """Represents defeniton of a variable"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.ARRAY_DEF)

        self.attributes = _attributes
        
        name = "name"
        self.attributes[name] = stringAttribute(name, ["имя", "название"], "")
                
        name = "type"
        self.attributes[name] = stringAttribute(name, ["тип"], "")

        name = "size"
        self.attributes[name] = intAttribute(name, ["размер"], 0)

    def __repr__(self):
        string = ""
        string += self.attributes["type"].value if self.attributes["type"].value else "void"
        string += " "
        string += self.attributes["name"].value if self.attributes["name"].value else "unnamedVariable"
        string += "["
        string += str(self.attributes["size"].value);
        string += "];"
        return string.replace("\t", " " * 4)
