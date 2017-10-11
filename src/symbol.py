class Symbol(object):
    
    def __init__(self, word, _type):
        self.type = _type
        self.word = word
    
    def __repr__(self):
        return "{} - {}".format(self.word, self.type)