from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _variable(abstractObject):
    """Represents a variable"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.VARIABLE)

        self.attributes.update(_attributes)
        
        name = "name"
        self.attributes[name] = stringAttribute(name, ["имя", "название"], "")

    def __repr__(self):
        string = self.attributes["name"].value if self.attributes["name"].value else "unnamedVariable"
        return self.reprCommon(string)
