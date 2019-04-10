from helpFunctions import soundDiff
from constants import MIN_SOUND_DIFF
from languageType import languageType

class attribute(object):
    """Abstract attribute object"""
    name = ""
    sounds = []
    value = None

    def __init__(self, _name, _sounds, _value):
        self.name = _name
        self.sounds = [_sounds] if isinstance(_sounds, str) else list(_sounds)
        self.value = _value

    def isWordThisAttribute(self, word):
        for sound in self.sounds:
            if soundDiff(sound, word):
                return True
        return False

    def searchObject(self, attribute_name, object):
        return None

    def getParent(self, id):
        return None

    def getFocusParent(self):
        return None

    def hasID(self, current_type, first_free_id):
        return False

class binaryAttribute(attribute):
    """value type is binary"""
    def __init__(self, _name, _sounds, _value):
        assert isinstance(_value, bool), "Value type is not bool!"
        return super().__init__(_name, _sounds, _value)

class intAttribute(attribute):
    """value type is integer"""
    def __init__(self, _name, _sounds, _value):
        assert isinstance(_value, int), "Value type is not int!"
        return super().__init__(_name, _sounds, _value)

class stringAttribute(attribute):
    """value type is string"""
    def __init__(self, _name, _sounds, _value):
        assert isinstance(_value, str), "Value type is not string!"
        return super().__init__(_name, _sounds, _value)

class multiAttribute(attribute):
    """value type is list"""
    def __init__(self, _name, _sounds, _value):
        assert isinstance(_value, list), "Value type is not list!"
        return super().__init__(_name, _sounds, _value)

    def searchObject(self, attribute_name, object):
        for value_object in self.value:
            res = value_object.searchObject(attribute_name, object)
            if res is not None: return res
        return None

    def getParent(self, child_id):
        for object in self.value:
            if id(object) == child_id:
                return self.value
            res = object.getParent(child_id)
            if res is not None: return res
        return None

    def getFocusParent(self):
        for object in self.value:
            if object.type == languageType.FOCUS:
                return self.value
            res = object.getFocusParent()
            if res is not None: return res
        return None

    def hasID(self, current_type, first_free_id):
        for object in self.value:
            if object.hasID(current_type, first_free_id):
                return True
        return False
