from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class Method(abstractObject):
    """Represents C++ method"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.METHOD)

        self.attributes = _attributes
        
        name = "name"
        self.attributes[name] = stringAttribute(name, ["имя", "название"], "")
        
        name = "retType"
        self.attributes[name] = stringAttribute(name, ["возврт"], "")

        name = "params"
        self.attributes[name] = multiAttribute(name, ["принимает", "параметры"], [])

        name = "body"
        self.attributes[name] =  multiAttribute(name, ["тело", "реализация"], [])

        name = "isStatic"
        self.attributes[name] =  binaryAttribute(name, ["статический"], False)

    def __repr__(self):
        string =  "static " if self.attributes["isStatic"].value else ""
        string += self.attributes["retType"].value if self.attributes["retType"].value else "void"
        string += " "
        #string += self.attributes["ofClass"].value if self.attributes["ofClass"].value + "::" else ""
        string += self.attributes["name"].value if self.attributes["name"].value else "unnamedMethod"
        string += "("
        for param in self.attributes["params"].value:
            string += str2(param) + ", "
        string += ") {\n"
        for body_element in self.attributes["body"].value:
            string += "\t" + str2(body_element).replace("\n", "\n\t") + "\n"
        string += "}"
        return string.replace("\t", " " * 4)