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

        def getWhereAndName(context, searched_id):
            for object in context:
                res = object.getAttrIdAndSound(searched_id)
                if res is not None: return res
            return None

        def getParent(context, child_id):
            for object in context:
                res = object.getParent(child_id)    
                if res is not None: return res
            # if res is None parent is context
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

        # если фокус не на самом контексте, мы теряем ссылку, поэтому найдем на какой объект ссылается фокус и присвоим self.where его
        # нам это нужно делать до перезаписи контекста историей

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
            if find_res is not None:
                self.focus = moveFocus(_from = self.focus,
                                       _to = find_res)

        if self.action == CommandType.CREATE:
            self.focus.append(self.what)
        if self.action == CommandType.DELETE:
            # find WHAT object in the context
            find_res = findInContext(self.context, None, self.what)
            if find_res is not None:
                parent = getParent(self.context, id(find_res))
                assert isinstance(parent, list), "DELETE find res is not a list"
                for object in parent:
                    if id(find_res) == id(object):
                        parent.remove(object)

        # to keep FOCUS the last in the object array
        self.focus = moveFocus(_from = self.focus,
                                _to = self.focus)

    def try_apply(self, p):
        if "INFN" in p.tag:
            self.parseAction(p)
        elif {"NOUN", "accs"} in p.tag:
            self.parseWhatObject(p)
        elif {"NOUN", "gent"} in p.tag:
            self.parseWhereObject(p)
        elif "VERB" in p.tag:
            pass # can be part of "наследуется от"
        elif "LATN" in p.tag:
            self.parseName(p)
        else:
            print("Unknown tag: ", p.tag)
            return False
        return True

    def parseAction(self, p):
        if self.action != CommandType.UNDO and self.action != CommandType.REDO:
            self.completePast()

        # parse new action
        self.action = CommandType.getAction(p.word)
        assert self.action != CommandType.NODEF, "Unknown infinitive verb!"

        # check if action is editor command
        if self.action == CommandType.REDO:
            self.context.clear()
            self.context.extend(self.history.redo())
        if self.action == CommandType.UNDO:
            self.context.clear()
            self.context.extend(self.history.undo())

    def parseWhatObject(self, p):
        if self.action == CommandType.CREATE or self.action == CommandType.DELETE:
            # parse new object
            self.what.type = languageType.getType(p.normal_form)
            assert self.what.type != languageType.NODEF, "Unknown WHAT object type!"
            # change abstract class to special one
            self.what = languageType.getClass(self.what.type, self.what.attributes)
        if self.action == CommandType.CHANGE:
            self.what.type = languageType.getType(p.normal_form)
            if self.what.type == languageType.NODEF: # we have an attribute name
                self.what = p.normal_form
            
            # configure WHERE object
            # MULTI: изменить what(родителей (ВП), тело(ВП))  where(класса potato)             ВП         MOVE FOCUS

            # BOOL: сделать what(метод getPotato) bool(статическим)             ВП ПРИЛ    CHANGE ATTRIBUTE
            # STR: изменить what attribute (имя) where(класса) Name на newName  ВП         CHANGE ATTRIBUTE

    def parseWhereObject(self, p):
        self.where.type = languageType.getType(p.normal_form)
        assert self.where.type != languageType.NODEF, "Unknown WHERE object type!"
        # change abstract class to special one
        self.where = languageType.getClass(self.where.type, self.where.attributes)
        self.is_where_mode = True

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
