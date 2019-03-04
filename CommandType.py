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
        if id == CommandType.CREATE:
            return ['создать', 'добавить']
        if id == CommandType.DELETE:
            return ['удалить', 'вырезать']
        if id == CommandType.CHANGE:
            return ['изменить', 'поменять']
        if id == CommandType.UNDO:
            return ['отменить', 'назад']
        if id == CommandType.REDO:
            return ['вернуть']
        if id == CommandType.NODEF:
            return []

    def getAction(word):
        print('[getAction]+')
        for cmd in CommandType:
            for cmdSound in CommandType.getSounds(cmd):
                print('[getAction] handle sound', cmdSound)
                if soundDiff(cmdSound, word):
                    print('[getAction] cmd founded:', cmd)
                    return cmd
        print('[getAction] cmd did not found')
        return NODEF