import sys
sys.path.append('internal_representations')

from enum import Enum, auto
from helpFunctions import soundDiff

class languageType(Enum):
    NODEF           = auto()
    CODE            = auto()
    FOCUS           = auto()
    CLASS           = auto()
    METHOD          = auto()
    VARIABLE        = auto()
    VARIABLE_DEF    = auto()
    ARRAY_DEF       = auto()
    CYCLE           = auto()
    CONDITION       = auto()
    PARAMETER       = auto()

    def getSounds(id):
        sounds = {
            languageType.NODEF:         [],
            languageType.CODE:          [],
            languageType.FOCUS:         [],
            languageType.CLASS:         ['класс', 'объект'],
            languageType.METHOD:        ['метод', 'функция'],
            languageType.VARIABLE:      ['переменная'],
            languageType.VARIABLE_DEF:  ['определение'], # TODO: more than 1 word sound?
            languageType.ARRAY_DEF:     ['определение2'],
            languageType.CYCLE:         ['цикл'],
            languageType.CONDITION:     ['условие'],
            languageType.PARAMETER:     ["параметр"]
                 }
        return sounds[id]

    def getClass(id, attributes = {}):
        from Class import Class
        from Method import Method
        from Focus import Focus
        from variableDefenition import variableDefenition
        class_type = {
            languageType.NODEF:         None,
            languageType.CODE:          None,
            languageType.FOCUS:         Focus(attributes),
            languageType.CLASS:         Class(attributes),
            languageType.METHOD:        Method(attributes),
            languageType.VARIABLE:      None,
            languageType.VARIABLE_DEF:  variableDefenition(attributes),
            languageType.ARRAY_DEF:     None,
            languageType.CYCLE:         None,
            languageType.CONDITION:     None,
            languageType.PARAMETER:     None
                    }      
        return class_type[id]

    def getType(word):
        print('[getType]+')
        for type in languageType:
            for typeSound in languageType.getSounds(type):
                if soundDiff(typeSound, word):
                    print('[getType] type found:', type)
                    return type
        print('[getType] type did not found')
        return languageType.NODEF
