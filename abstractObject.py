from enum import Enum, auto

class binaryAttribute():
    sounds = []
    


class abstractObject(object):
    """This class represents abstract language construction"""
    type = languageType.NODEF
    attributes = {}

class languageType(Enum):
    NODEF           = auto()
    CLASS           = auto()
    METHOD          = auto()
    EXPRESSION      = auto()
    VARIABLE        = auto()
    CYCLE           = auto()
    CONDITION       = auto()
    PARAMETER       = auto()