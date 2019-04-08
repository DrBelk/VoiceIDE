import pymorphy2

from abstractObject import *
from attribute import *
from CommandType import CommandType
from ContextHistory import ContextHistory
from languageType import languageType
from helpFunctions import (contextList2str, str2)

class WordHandler(object):
    """Handles words"""

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()  # we do not need to clear parser for every command
        self.history = ContextHistory()         # we do not need to clear history for every command
        self.action = CommandType.NODEF         # just init value

        # init context object (consists an array of all the code objects) and focus
        self.context = [languageType.getClass(languageType.FOCUS)]
        self.focus = self.context
        # init other objects that should be reinited every command
        self.completePast()

    def completePast(self):
        """Completes previous command"""
        self.what = abstractObject(languageType.NODEF) # represent an object of action
        self.where = abstractObject(languageType.NODEF) # represent an place in an object where the action happens
        self.history.addContext(self.context)
        self.is_where_mode = False
        self.isBinaryTrue = True
        self.what_type_part = ''
        self.where_type_part = ''

        self.editing_attribute_type = None
        self.nextIsNewValue = False
        self.editing_attribute_new_value = None

    def sendWord(self, word):
        """Processes a word from any word generator depending on the current state"""
        print('[sendWord] hanlde word:', word)
        # request of empty word means no changes
        if not word:
            return contextList2str(self.context)
        parse = self.morph.parse(word)
        
        handled = False
        for parse_variant in parse:
            if self.try_apply(parse_variant):
                handled = True
                break

        if not handled:
            pass # take a word from English line
        else:
            self.updateContext()

        return contextList2str(self.context)

    def updateContext(self):
        def findInContext(context, what, where):
            for object in context:
                res = object.searchObject(attribute_sound = what, 
                                          object = where)
                if res is not None: return res
            return None

        def getParent(context, child_id):
            for object in context:
                res = object.getParent(child_id)    
                if res is not None: return res
            return context

        def getFocusParent(context):
            for object in context:
                res = object.getFocusParent()    
                if res is not None: return res
            return context

        def moveFocus(_from, _to):
            for object in _from:
                if object.type == languageType.FOCUS:
                    _from.remove(object)
                    break
            _to.append(languageType.getClass(languageType.FOCUS))
            return _to

        def deleteObj(_from, del_id):
            for object in _from:
                if del_id == id(object):
                    parent.remove(object)

        # load old command context, not just = operator to keep self.focus as pointer
        self.context.clear()
        self.context.extend(self.history.getCurrContext())

        # find focus
        self.focus = getFocusParent(self.context)

        # if focus is going to be changed
        if self.where.type != languageType.NODEF:
            assert isinstance(self.what, str), "WHAT object is not a string"
            # we expect attribute name in WHAT object
            find_res = findInContext(self.context, self.what, self.where)
            if isinstance(find_res, multiAttribute):
                self.focus = moveFocus(_from = self.focus,
                                       _to = find_res.value)
            elif find_res is not None:
                if self.editing_attribute_new_value:
                    find_res.value = self.editing_attribute_new_value
                else:
                    self.editing_attribute_type = type(find_res.value)

        elif isinstance(self.what, str) and self.what in ["контекст", "корень"]:
            self.focus = moveFocus(_from = self.focus,
                                   _to = self.context)

        if self.action == CommandType.CREATE:
            self.focus.append(self.what)
        elif self.action == CommandType.DELETE:
            # find WHAT object in the context
            find_res = findInContext(self.context, None, self.what)
            if find_res is not None:
                parent = getParent(self.context, id(find_res))
                assert isinstance(parent, list), "DELETE find res is not a list"
                deleteObj(parent, id(find_res))
        elif self.action == CommandType.CHANGE:
            if not isinstance(self.what, str) and self.what.type != languageType.NODEF:
                find_res = findInContext(self.context, None, self.what)
                if find_res is not None:
                    parent = getParent(self.context, id(find_res))
                    assert isinstance(parent, list), "CHANGE find res is not a list"
                    deleteObj(parent, id(find_res))
                    parent.append(self.what)

        # to keep FOCUS be the last in the object array
        self.focus = moveFocus(_from = self.focus,
                                _to = self.focus)

    def try_apply(self, p):
        if "INFN" in p.tag:
            return self.parseAction(p)
        elif self.nextIsNewValue: # should be before any other but verb
            return self.setAttributeValue(p)
        elif not isinstance(self.what, str) and self.what.type == languageType.PART:
            return self.parseWhatObject(p)
        elif {"NOUN", "accs"} in p.tag:
            return self.parseWhatObject(p)
        elif {"NOUN", "gent"} in p.tag:
            return self.parseWhereObject(p)
        elif {"PRCL"} in p.tag:
            return self.parseNot(p)
        elif {"PREP"} in p.tag:
            return self.parsePrep(p)
        elif {"ADJF", "ablt"} in p.tag:
            return self.parseWhatBinary(p)
        elif {"LATN"} in p.tag:
            return self.parseName(p)
        else:
            print("Unknown tag: ", p.tag)
            return False
        return True

    def setAttributeValue(self, p):
        def parseInteger(p):
            self.editing_attribute_new_value = int(p.word)
        def parseString(p):
            if {"LATN"} in p.tag:
                if not self.editing_attribute_new_value:
                    self.editing_attribute_new_value = p.normal_form.lower()
                else:
                    self.editing_attribute_new_value += p.normal_form[0].title() + p.normal_form[1:].lower()
            else:
                self.editing_attribute_new_value = p.normal_form.lower()

        # if the attribute is found
        if self.editing_attribute_type:
            if self.editing_attribute_type is int:
                parseInteger(p)
            elif self.editing_attribute_type is str:
                parseString(p)
        return True

    def parsePrep(self, p):
        # find att
        if p.word == "на" and self.action == CommandType.CHANGE:
            self.nextIsNewValue = True
            self.is_where_mode = False
        return True

    def parseNumbr(self, p):
        # find att
        if p.word == "на" and self.action == CommandType.CHANGE:
            self.nextIsNewValue = True
            self.is_where_mode = False
        return True

    def parseNot(self, p):
        if p.word == "не":
            self.isBinaryTrue = False
        return True

    def parseWhatBinary(self, p):
        return self.what.setBinary(p.normal_form, self.isBinaryTrue)

    def parseAction(self, p):
        if self.action != CommandType.UNDO and self.action != CommandType.REDO:
            self.completePast()

        # parse new action
        self.action = CommandType.getAction(p.word)
        if self.action == CommandType.NODEF:
            print("Unknown infinitive verb!")
            return False

        # check if action is editor command
        if self.action == CommandType.REDO:
            self.context.clear()
            self.context.extend(self.history.redo())
        if self.action == CommandType.UNDO:
            self.context.clear()
            self.context.extend(self.history.undo())
            return True

    def parseWhatObject(self, p):
        def getTypePart():
            self.what.type = languageType.getType(self.what_type_part + p.normal_form)
                
            if self.what.type == languageType.NODEF:
                print("Unknown WHAT object type!")
                return False
            # change abstract class to special one
            if self.what.type != languageType.PART:
                self.what_type_part = ""
                self.what = languageType.getClass(self.what.type, self.what.attributes)
            else:
                self.what_type_part += p.normal_form + " "
        if self.action == CommandType.CREATE or self.action == CommandType.DELETE:
            # parse new object
            getTypePart()
        if self.action == CommandType.CHANGE:
            getTypePart()
            if self.what.type == languageType.NODEF: # we have an attribute name
                self.what = p.normal_form
        return True

    def parseWhereObject(self, p):
        self.where.type = languageType.getType(self.where_type_part + p.normal_form)
        if self.where.type == languageType.NODEF:
            print("Unknown WHERE object type!")
            return False
        # change abstract class to special one
        if self.where.type != languageType.PART:
            self.where_type_part = ""
            self.where = languageType.getClass(self.where.type, self.where.attributes)
            self.is_where_mode = True
        else:
            self.where_type_part += p.normal_form + " "
        return True

    def parseName(self, p):
        # Find out what object we should change
        if self.is_where_mode:
            object = self.where
        else:
            object = self.what

        # parse the name of the object
        if "name" in object.attributes:
            if not object.attributes["name"].value:
                object.attributes["name"].value = p.normal_form.lower()
            else:
                object.attributes["name"].value += p.normal_form[0].title() + p.normal_form[1:].lower()
        return True
