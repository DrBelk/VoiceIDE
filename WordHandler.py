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
        # TODO: change the focus if where object is defined and found
        # load old command context, not just = operator to keep self.focus as pointer
        self.context.clear()
        self.context.extend(self.history.getCurrContext())
        if self.action == CommandType.CREATE:
            self.focus.append(self.what)

    def try_apply(self, p):
        if "INFN" in p.tag:
            self.parseAction(p)
        elif {"NOUN", "accs"} in p.tag:
            self.parseObjectType(p)
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

    def parseObjectType(self, p):
        # parse new object
        self.what.type = languageType.getType(p.normal_form)
        assert self.what.type != languageType.NODEF, "Unknown object type!"
        # change abstract class to special one
        self.what = languageType.getClass(self.what.type, self.what.attributes)

    def parseName(self, p):
        # parse name of the object
        if "name" in self.what.attributes:
            if not self.what.attributes["name"].value:
                self.what.attributes["name"].value = p.normal_form.lower()
            else:
                self.what.attributes["name"].value += p.normal_form[0].title() + p.normal_form[1:].lower()
