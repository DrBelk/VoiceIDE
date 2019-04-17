from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _cycle(abstractObject):
    """Represents C++ "for" cycle"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.CYCLE)

        self.attributes.update(_attributes)

        name = "body"
        self.attributes[name] =  multiAttribute(name, ["тело", "реализация"], [])

        name = "init"
        self.attributes[name] =  multiAttribute(name, ["начало"], [])

        name = "condition"
        self.attributes[name] =  multiAttribute(name, ["условие"], [])
        
        name = "endaction"
        self.attributes[name] =  multiAttribute(name, ["действие"], [])
        
    def __repr__(self):
        string = "for ("

        for init in self.attributes["init"].value[:-1]:
            string += str(init) + ', '
        string += str(self.attributes["init"].value[-1]) if self.attributes["init"].value else ""
        string += '; '

        for cond in self.attributes["condition"].value[:-1]:
            string += str(cond) + ' '
        string += str(self.attributes["condition"].value[-1]) if self.attributes["condition"].value else ""
        string += '; '

        for end in self.attributes["endaction"].value[:-1]:
            string += str(end) + ', '
        string += str(self.attributes["endaction"].value[-1]) if self.attributes["endaction"].value else ""
        string += ') {\n'
        for body_element in self.attributes["body"].value:
            string += "\t" + str2(body_element).replace("\n", "\n\t") + "\n"
        string += "}"
        return self.reprCommon(string)