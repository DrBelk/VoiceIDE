from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _number(abstractObject):
    """Represents defeniton of a variable"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.CLASS)

        self.attributes.update(_attributes)
        
        #name = "name"
        #self.attributes[name] = stringAttribute(name, ["имя", "название"], "")

    def __repr__(self):
        string = "// Number stub;"
        #str += self.attributes["type"].value if self.attributes["type"].value else "void"
        #str += " "
        #str += self.attributes["name"].value if self.attributes["name"].value else "unnamedVariable"
        #str += "["
        #str += self.attributes["size"].value if self.attributes["type"].value else 10;
        #str += "];"
        return self.reprCommon(string)
