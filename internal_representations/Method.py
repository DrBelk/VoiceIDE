from abstractObject import *
from attribute import *
from languageType import languageType

class Method(abstractObject):
    """Represents C++ method"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.METHOD)

        self.attributes = _attributes
        
        name = stringAttribute("name", ["имя", "название"], "")
        self.attributes[name.name] = name

        of_class = stringAttribute("ofClass", ["класса"], "")
        self.attributes[of_class.name] = of_class
        
        ret_type = stringAttribute("retType", "возвращает", "")
        self.attributes[ret_type.name] = ret_type

        parameters = multiAttribute("params", ["принимает", "параметры"], [])
        self.attributes[parameters.name] = parameters

        body = multiAttribute("body", ["тело", "реализация"], [])
        self.attributes[body.name] = body

    def __repr__(self):
        str =  self.attributes["retType"].value if self.attributes["retType"].value else "void" + " "
        str += self.attributes["ofClass"].value if self.attributes["ofClass"].value + "::" else ""
        str += self.attributes["name"].value if self.attributes["name"].value else "unnamedMethod"
        str += "("
        for param in self.attributes["params"].value:
            str += str2(param) + ", "
        str += ") {\n"
        for body_element in self.attributes["body"].value:
            str += str2(body_element) + "\n"
        str += "}"
        return str