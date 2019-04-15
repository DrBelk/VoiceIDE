from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _include(abstractObject):
    """Represents C++ include"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.INCLUDE)

        self.attributes.update(_attributes)
                
        name = "val"
        self.attributes[name] = stringAttribute(name, ["значение"], "")

    def __repr__(self):
        string =  "#include <"
        string += self.attributes["val"].value if self.attributes["val"].value else "thisLibraryDoesNotExist"
        string += ">"
        return self.reprCommon(string)