from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _param(abstractObject):
    """Represents defeniton of a variable"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.PARAMETER)

        self.attributes.update(_attributes)
        
        name = "name"
        self.attributes[name] = stringAttribute(name, ["имя", "название"], "")
                
        name = "type"
        self.attributes[name] = stringAttribute(name, ["тип"], "")

    def __repr__(self):
        string = ""
        string += self.attributes["type"].value if self.attributes["type"].value else "void"
        string += " "
        string += self.attributes["name"].value if self.attributes["name"].value else "unnamedParameter"
        return self.reprCommon(string)
