import pymorphy2
from abstractObject import abstractObject

class WordHandler(object):
    """Handles words"""

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.abstract = abstractObject()
        self.context = 

    def sendWord(self, word):
        """Processes a word from any word generator depending on the current state"""
        print('[sendWord] hanlde word:', word)
        parse = self.morph.parse(word)
        
        for parse_variant in parse:
            if self.try_apply(parse_variant):
                if "INFN" in parse_variant.tag:
                    self.completePast()
                    break


    def try_apply(self, p):
        if "INFN" in p.tag:
            self.parseAction(p)
            return True
        if "NOUN" in p.tag:
            parseObjectType(p)
            return True
        return False

    def completePast(self):
        self.abstract = abstractObject()
        

    def parseAction(self, p):
        pass

    def parseObjectType(self, p):
        pass





