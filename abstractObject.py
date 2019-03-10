from languageType import languageType

class abstractObject(object):
    """This class represents abstract language construction"""

    def __init__(self, _type):
        self.type = _type if isinstance(_type, languageType) else languageType.NODEF
        self.attributes = {}

    def __repr__(self):
        return "Waiting for details..."

    def __str__(self):
        return self.__repr__()

    def searchObject(self, attribute_sound, object):
        if attribute_sound is None:
            # link to an object is reqired
            if self.type == object.type:
                #check if the name of the self object is the same
                if "name" in self.attributes and "name" in object.attributes and \
                    self.attributes["name"].value == object.attributes["name"].value:
                    return self
        else:
            # link to an attribute is reqired
            if self.type == object.type:
                # check if there is some attribute with given sound
                does_given_sound_represent_attribute = False
                for attr in self.attributes.values():
                    if attr.isWordThisAttribute(attribute_sound):
                        does_given_sound_represent_attribute = True
                        searched_attr = attr.value
                        break
                if does_given_sound_represent_attribute:
                    #check if the name of the object is the same
                    if "name" in self.attributes and "name" in object.attributes and \
                        self.attributes["name"].value == object.attributes["name"].value:
                        return searched_attr
        for attr in self.attributes.values():
            res = attr.searchObject(attribute_sound, object)
            if res is not None: return res
        return None

    def getAttrIdAndSound(self, searched_id):
        # check if any attr has provided id
        for attr in self.attributes.values():
            if searched_id == id(attr.value):
                return (self, attr.sounds[0])
        for attr in self.attributes.values():
            res = attr.getAttrIdAndSound(searched_id)
            if res is not None: return res
        return None

    def getParent(self, child_id):
        for attr in self.attributes.values():
            res = attr.getParent(child_id)
            if res is not None: return res
        return None