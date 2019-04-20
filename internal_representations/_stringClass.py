from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _stringClass(abstractObject):
    """Represents string"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.STRING)

        self.attributes.update(_attributes)
        
        name = "val"
        self.attributes[name] = strAttribute(name, ["значение"], '')

    def __repr__(self):
        string = "/*ID:"
        string += str(self.attributes["id"].value)
        string += "*/"
        string += self.attributes["val"].value
        return self.reprCommon(string, False)
