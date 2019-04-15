from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _number(abstractObject):
    """Represents defeniton of a variable"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.NUMBER)

        self.attributes.update(_attributes)
        
        name = "val"
        self.attributes[name] = intAttribute(name, ["значение"], 0)

    def __repr__(self):
        string = "/*ID:"
        string += str(self.attributes["id"].value)
        string += "*/"
        string += str(self.attributes["val"].value)
        return self.reprCommon(string, False)
