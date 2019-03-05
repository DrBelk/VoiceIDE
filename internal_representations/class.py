from abstractObject import abstractObject
from attribute import *
from languageType import languageType
from helpFunctions import str2

class Class(abstractObject):
    """Represents C++ class"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.CLASS)

        self.attributes = _attributes
        
        name = stringAttribute("name", ["имя", "название"], "")
        self.attributes[name.name] = name
                
        parents = multiAttribute("parents", ["родитель"], [])
        self.attributes[parents.name] = parents

        body = multiAttribute("body", ["тело", "реализация"], [])
        self.attributes[body.name] = body

    def __repr__(self):
        str = "class "
        str += self.attributes["name"].value if self.attributes["name"].value else "unnamedClass" 
        str += " {\n"
        for body_element in self.attributes["body"].value: 
            str += "\t" + str2(body_element).replace("\n", "\n\t") + "\n"
        str += "}"
        return str.replace("\t", " " * 4)