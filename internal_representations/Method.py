from abstractObject import abstractObject

class Method(abstractObject):
    """Represents C++ method"""
    name = ""
    parents = [] # list of strigns


    def __repr__(self):
        str = "method"

