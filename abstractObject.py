from languageType import languageType
from attribute import intAttribute

class abstractObject(object):
    """This class represents abstract language construction"""

    def __init__(self, _type):
        self.type = _type if isinstance(_type, languageType) else languageType.NODEF
        self.attributes = {}

        name = "id"
        self.attributes[name] = intAttribute(name, ["номер"], 0)

    def __repr__(self):
        return "// Waiting for details..."

    def __str__(self):
        return self.__repr__()

    def reprCommon(self, child_repr):
        string = ""
        if "name" not in self.attributes:
            string += "// id is "
            string += str(self.attributes["id"].value) + "\n"
        string += child_repr
        return string.replace("\t", " " * 4)


    def setBinary(self, attribute_sound, isTrue):
        for attr in self.attributes.values():
            if attr.isWordThisAttribute(attribute_sound):
                attr.value = isTrue
                return True
        return False

    def searchObject(self, attribute_sound, object):
        def isObjectHasTheSameNameOrId():
            # check if name exists for both
            if "name" in self.attributes and "name" in object.attributes:
                # check if names are the same
                if self.attributes["name"].value == object.attributes["name"].value:
                    return True
            else:
                # check if IDs are the same
                if self.attributes["id"].value == object.attributes["id"].value:
                    return True
            return False
            
        # check if the type is good
        if self.type == object.type:
            if attribute_sound is None:
                # link to an object is reqired
                if isObjectHasTheSameNameOrId():
                    return self
            else:
                # link to an attribute is reqired
                # check if there is some attribute with given sound
                does_given_sound_represent_attribute = False
                for attr in self.attributes.values():
                    if attr.isWordThisAttribute(attribute_sound):
                        does_given_sound_represent_attribute = True
                        searched_attr = attr
                        break
                if does_given_sound_represent_attribute:
                    if isObjectHasTheSameNameOrId():
                        return searched_attr
        else:
            for attr in self.attributes.values():
                res = attr.searchObject(attribute_sound, object)
                if res is not None: return res
        return None

    def getParent(self, child_id):
        for attr in self.attributes.values():
            res = attr.getParent(child_id)
            if res is not None: return res
        return None

    def getFocusParent(self):
        for attr in self.attributes.values():
            res = attr.getFocusParent()
            if res is not None: return res
        return None

    def hasID(self, current_type, first_free_id):
        if self.type == current_type and \
           self.attributes["id"].value == first_free_id:
            return True
        for attr in self.attributes.values():
            if attr.hasID(current_type, first_free_id):
                return True
        return False