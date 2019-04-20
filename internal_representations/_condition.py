from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _condition(abstractObject):
    """Represents C++ condition"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.CONDITION)

        self.attributes.update(_attributes)

        name = "if"
        self.attributes[name] =  multiAttribute(name, ["правда"], [])

        name = "else"
        self.attributes[name] =  multiAttribute(name, ["ложь"], [])

        name = "condition"
        self.attributes[name] =  multiAttribute(name, ["условие"], [])
        
        name = "endaction"
        self.attributes[name] =  multiAttribute(name, ["действие"], [])
        
    def __repr__(self):
        string = "if ("

        for cond in self.attributes["condition"].value[:-1]:
            string += str(cond) + ' '
        string += str(self.attributes["condition"].value[-1]) if self.attributes["condition"].value else ""
        string += ') {\n'

        for body_element in self.attributes["if"].value:
            string += "\t" + str2(body_element).replace("\n", "\n\t") + "\n"
        string += "}"

        if self.attributes['else'].value:
            string += ' else {\n'
            for else_element in self.attributes["else"].value:
                string += "\t" + str2(else_element).replace("\n", "\n\t") + "\n"
            string += "}"
        return self.reprCommon(string)