import sys
sys.path.append('internal_representations')

from enum import Enum, auto
from helpFunctions import soundDiff

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

    def getClass(id, attributes):
        from Class import Class
        from Method import Method
        if id == languageType.NODEF:
            return None
        if id == languageType.CODE:
            return None
        if id == languageType.CLASS:
            return Class(attributes)
        if id == languageType.METHOD:
            return Method(attributes)
        if id == languageType.EXPRESSION:
            return None
        if id == languageType.VARIABLE:
            return None
        if id == languageType.CYCLE:
            return None
        if id == languageType.CONDITION:
            return None
        if id == languageType.PARAMETER:
            return None

    def getType(word):
        print('[getType]+')
        for type in languageType:
            for typeSound in languageType.getSounds(type):
                if soundDiff(typeSound, word):
                    print('[getType] type founded:', type)
                    return type
        print('[getType] type did not found')
        return languageType.NODEF
