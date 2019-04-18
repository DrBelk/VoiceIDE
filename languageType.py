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
    RETURN          = auto()
    VARIABLE        = auto()
    VARIABLE_DEF    = auto()
    ARRAY_DEF       = auto()
    CYCLE           = auto()
    CONDITION       = auto()
    NUMBER          = auto()
    INCLUDE         = auto()
    PARAMETER       = auto()

    def getSounds(id):
        sounds = {
            # should be empty
            languageType.NODEF:         [],
            languageType.CODE:          [],
            languageType.PART:          [],
            languageType.FOCUS:         [],
            # fill that for all the objects below
            languageType.CLASS:         ['класс', 'объект'],
            languageType.METHOD:        ['метод', 'функция'],
            languageType.RETURN:        ['возврат'],
            languageType.VARIABLE:      ['переменная', 'переменный'],
            languageType.VARIABLE_DEF:  ['определение переменной'],
            languageType.ARRAY_DEF:     ['определение массива'],
            languageType.CYCLE:         ['цикл'],
            languageType.CONDITION:     ['условие языка'],
            languageType.NUMBER:        ['число'],
            languageType.INCLUDE:       ['включение библиотеки', 'библиотека'],
            languageType.PARAMETER:     ["параметр"]
                 }
        return sounds[id]

    def getClass(id, attributes = {}):
        from abstractObject import abstractObject
        from _class import _class
        from _method import _method
        from _return import _return
        from _focus import _focus
        from _variableDefenition import _variableDefenition
        from _variable import _variable
        from _arrayDefenition import _arrayDefenition
        from _number import _number
        from _cycle import _cycle
        from _include import _include
        class_type = {
            languageType.FOCUS:         _focus,
            languageType.CLASS:         _class,
            languageType.METHOD:        _method,
            languageType.RETURN:        _return,
            languageType.VARIABLE:      _variable,
            languageType.VARIABLE_DEF:  _variableDefenition,
            languageType.ARRAY_DEF:     _arrayDefenition,
            languageType.CYCLE:         _cycle,
            languageType.CONDITION:     None,
            languageType.NUMBER:        _number,
            languageType.INCLUDE:       _include,
            languageType.PARAMETER:     None
                     }      
        return class_type[id](attributes)

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
