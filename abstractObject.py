from enum import Enum, auto
from helpFunctions import soundDiff

class binaryAttribute():
    sounds = []

class abstractObject(object):
    """This class represents abstract language construction"""

    def __init__(self, _type):
        self.type = _type if isinstance(_type, languageType) else languageType.NODEF
        self.attributes = {}


class languageType(Enum):
    NODEF           = auto()
    CODE            = auto()
    CLASS           = auto()
    METHOD          = auto()
    EXPRESSION      = auto()
    VARIABLE        = auto()
    CYCLE           = auto()
    CONDITION       = auto()
    PARAMETER       = auto()

    def getSounds(id):
        if id == languageType.NODEF:
            return []
        if id == languageType.CODE:
            return []
        if id == languageType.CLASS:
            return ['класс', 'объект']
        if id == languageType.METHOD:
            return ['метод', 'функция']
        if id == languageType.EXPRESSION:
            return ['выражение']
        if id == languageType.VARIABLE:
            return ['переменная']
        if id == languageType.CYCLE:
            return ['цикл']
        if id == languageType.CONDITION:
            return ['условие']
        if id == languageType.PARAMETER:
            return ["параметр"]

    def getType(word):
        print('[getType]+')
        for type in languageType:
            for typeSound in languageType.getSounds(type):
                print('[getType] handle sound', typeSound)
                if soundDiff(typeSound, word):
                    print('[getType] type founded:', type)
                    return type
        print('[getType] type did not found')
        return NODEF