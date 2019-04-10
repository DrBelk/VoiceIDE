from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _return(abstractObject):
    """Represents C++ return statement"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.RETURN)

        self.attributes.update(_attributes)
        
        name = "val"
        self.attributes[name] = multiAttribute(name, ["значение"], [])

    def __repr__(self):
        string =  "return "
        for val in self.attributes["val"].value:
            string += str2(val)
        string += ";"
        return self.reprCommon(string)