from helpFunctions import soundDiff
from constants import MIN_SOUND_DIFF

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
            if soundDiff(sound, word) > MIN_SOUND_DIFF:
                return True
        return False

    def searchObject(self, attribute_name, object):
        return None

    def get_attr_id_name_and_id_parent(self, id):
        return None

class binaryAttribute(attribute):
    """value type is binary"""
    def __init__(self, _name, _sounds, _value):
        assert isinstance(_value, bool), "Value type is not bool!"
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

    def get_attr_id_name_and_id_parent(self, id):
        for value_object in self.value:
            res = value_object.get_attr_id_name_and_id_parent(id)
            if res is not None: return res
        return None
