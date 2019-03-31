from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class Focus(abstractObject):
    """Represents cursor in the code"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.FOCUS)

        self.attributes = _attributes

    def __repr__(self):
        string = "// We are here"
        return string.replace("\t", " " * 4)