from abstractObject import *
from attribute import *
from languageType import languageType
from helpFunctions import str2

class _focus(abstractObject):
    """Represents cursor in the code"""

    def __init__(self, _attributes = {}):
        super().__init__(languageType.FOCUS)

        self.attributes.update(_attributes)

        # add fake name to avoid printing id for focus object
        name = "name"
        self.attributes[name] = stringAttribute(name, ["имя", "название"], "")

    def __repr__(self):
        string = "@"
        return self.reprCommon(string)