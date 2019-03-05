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
        #TODO: maybe we are intrested not only in the type
        if self.type == object.type:
            # check if there is some attribute with given sound
            does_given_sound_represent_attribute = False
            for attr in self.attributes.values():
                if attr.isWordThisAttribute(attribute_sound):
                    does_given_sound_represent_attribute = True
                    searched_attr = attr.value
                    break
            if does_given_sound_represent_attribute:
                # TODO: check all defined attributes like a name
                # this implementation is wrong because of body attribure that is changing
                is_all_attributes_equal = True
                #for search_object_attr in object.attributes.values():
                #    if search_object_attr.value and \
                #       search_object_attr.value != self.attributes[search_object_attr.name].value:
                #        is_all_attributes_equal = False
                #        break
                if is_all_attributes_equal:
                    return searched_attr
        for attr in self.attributes.values():
            res = attr.searchObject(attribute_sound, object)
            if res is not None: return res
        return None

    def get_attr_id_name_and_id_parent(self, searched_id):
        # check if any attr has provided id
        for attr in self.attributes.values():
            if searched_id == id(attr.value):
                return (self, attr.sounds[0])
        for attr in self.attributes.values():
            res = attr.get_attr_id_name_and_id_parent(searched_id)
            if res is not None: return res
        return None