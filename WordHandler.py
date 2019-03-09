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
        self.context = []
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
        def findWhereInContext(context, what, where):
            for object in context:
                res = object.searchObject(what, where)
                if res is not None: return res
            return None

        def restoreWhereAndName(context, searched_id):
            for object in context:
                res = object.get_attr_id_name_and_id_parent(searched_id)
                if res is not None: return res
            return None

        # change the focus if where object is defined
        if self.where.type != languageType.NODEF:
            # we expect attribute name in WHAT object
            attr_name = self.what
        elif self.focus is not self.context:
            # load WHERE object to restore focus reference
            (self.where, attr_name) = restoreWhereAndName(self.context, id(self.focus))

        assert self.focus is not None, "Focus is None!"

        # если фокус не на самом контексте, мы теряем ссылку, поэтому найдем на какой объект ссылается фокус и присвоим self.where его
        # нам это нужно делать до перезаписи контекста историей

        # load old command context, not just = operator to keep self.focus as pointer
        self.context.clear()
        self.context.extend(self.history.getCurrContext())
        
        # check if WHERE object is finally defined enough
        if self.where.type != languageType.NODEF:
            find_res = findWhereInContext(self.context, attr_name, self.where)
            if find_res is not None:
                self.focus = find_res
                self.where = abstractObject(languageType.NODEF) # clear temporary used WHERE object

        if self.action == CommandType.CREATE:
            self.focus.append(self.what)
        

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
        if self.action == CommandType.CREATE:
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
