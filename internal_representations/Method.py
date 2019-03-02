from abstractObject import *
from attribute import *

class Method(abstractObject):
    """Represents C++ method"""

    def __init__(self):
        self.type = languageType.METHOD
        
        name = stringAttribute("name", ["имя", "название"], "")
        self.attributes[name.name] = name

        of_class = stringAttribute("ofClass", ["класса"], "")
        self.attributes[of_class.name] = of_class
        
        ret_type = stringAttribute("retType", "возвращает", "")
        self.attributes[ret_type.name] = ret_type

        parameters = multiAttribute("params", ["принимает", "параметры"], [])
        self.attributes[parameters.name] = parameters

        body = multiAttribute("body", ["принимает", "параметры"], [])
        self.attributes[body.name] = body

    def __repr__(self):
        str =  self.attributes["retType"] if self.attributes["retType"] else "void" + " "
        str += self.attributes["ofClass"] if self.attributes["ofClass"] + "::" else ""
        str += self.attributes["name"] if self.attributes["name"] else "unnamedMethod" + "("
        for param in self.attributes["params"]:
            str += str2(param) + ", "
        str += ") {\n"
        for body_element in self.attributes["body"]:
            str += str2(body_element) + "\n"
        str += "}"