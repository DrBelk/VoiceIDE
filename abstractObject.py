from languageType import languageType

class abstractObject(object):
    """This class represents abstract language construction"""

    def __init__(self, _type):
        self.type = _type if isinstance(_type, languageType) else languageType.NODEF
        self.attributes = {}

    def __repr__(self):
        return "Waiting for details..."

    def __str__(self):
        return self.__repr__()