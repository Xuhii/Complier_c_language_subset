from SentenceParser.expression_model import *
class TokenStack:
    def __init__(self, tokenList:list):
        self.data =  tokenList + [Symbol('$')]
        self.pointer = 0
    def __str__(self):
        return str(self.data)
    def next(self):
        self.pointer = (self.pointer + 1)%len(self.data)
    def initiallize(self):
        self.pointer = 0
    def cur(self):
        return self.data[self.pointer]
    
    # TODO
    # Use to Test
    @classmethod
    def bystr(cls, s:str):
        L = s.split(" ")
        return cls(list(map(lambda x:Symbol(x), L)))
    @classmethod
    def byword(cls, data):
        def _f(x):
            return Symbol(x[1], val=x[2], pos=x[0])
        return cls(list(map(_f, data)))
