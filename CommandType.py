from helpFunctions import soundDiff
from enum import Enum, auto

class CommandType(Enum):
    """Types of natural language commands"""
    NODEF	= auto()
    CREATE	= auto()
    DELETE	= auto()
    CHANGE	= auto()
    UNDO	= auto()
    REDO	= auto()

    def getSounds(id):
        return sounds[id]

    def getAction(word):
        print('[getAction]+')
        for cmd in CommandType:
            for cmdSound in CommandType.getSounds(cmd):
                if soundDiff(cmdSound, word):
                    print('[getAction] cmd founded:', cmd)
                    return cmd
        print('[getAction] cmd did not found')
        return CommandType.NODEF

sounds = {
    CommandType.CREATE:     ['создать', 'добавить'],
    CommandType.DELETE:     ['удалить', 'вырезать'],
    CommandType.CHANGE:     ['изменить', 'поменять', 'редактировать', 'сделать'],
    CommandType.UNDO:       ['отменить', 'назад'],
    CommandType.REDO:       ['вернуть'],
    CommandType.NODEF:      [] 
}