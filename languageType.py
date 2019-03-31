import sys
sys.path.append('internal_representations')

from enum import Enum, auto
from helpFunctions import soundDiff

class languageType(Enum):
    NODEF           = auto()
    CODE            = auto()
    PART            = auto()
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
            languageType.PART:          [],
            languageType.FOCUS:         [],
            languageType.CLASS:         ['класс', 'объект'],
            languageType.METHOD:        ['метод', 'функция'],
            languageType.VARIABLE:      ['переменная'],
            languageType.VARIABLE_DEF:  ['определение переменной'],
            languageType.ARRAY_DEF:     ['определение массива'],
            languageType.CYCLE:         ['цикл'],
            languageType.CONDITION:     ['условие'],
            languageType.PARAMETER:     ["параметр"]
                 }
        return sounds[id]

    def getClass(id, attributes = {}):
        from abstractObject import abstractObject
        from Class import Class
        from Method import Method
        from Focus import Focus
        from variableDefenition import variableDefenition
        from arrayDefenition import arrayDefenition
        class_type = {
            languageType.NODEF:         abstractObject(languageType.NODEF),
            languageType.CODE:          None,
            languageType.PART:          None,
            languageType.FOCUS:         Focus(attributes),
            languageType.CLASS:         Class(attributes),
            languageType.METHOD:        Method(attributes),
            languageType.VARIABLE:      None,
            languageType.VARIABLE_DEF:  variableDefenition(attributes),
            languageType.ARRAY_DEF:     arrayDefenition(attributes),
            languageType.CYCLE:         None,
            languageType.CONDITION:     None,
            languageType.PARAMETER:     None
                     }      
        return class_type[id]

    def getType(word):
        print('[getType]+')
        for type in languageType:
            for typeSound in languageType.getSounds(type):
                if " " in typeSound:
                    should_be_equal = (len(typeSound.split(" ")) - len(word.split(" "))) == 0
                    num_equal_parts = 0
                    for sound_part, word_part in zip(typeSound.split(" "), word.split(" ")):
                        if soundDiff(sound_part, word_part):
                            num_equal_parts += 1
                        else:
                            break
                    if num_equal_parts == len(word.split(" ")):
                        if should_be_equal:
                            print('[getType] type found:', type)
                            return type
                        else:
                            print('[getType] type part found:', type)
                            return languageType.PART
                if soundDiff(typeSound, word):
                    print('[getType] type found:', type)
                    return type
        print('[getType] type did not found')
        return languageType.NODEF
