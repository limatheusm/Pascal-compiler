class Token(object):

    def __init__(self, token, tokenType, line):
        self.token = token
        self.tokenType = tokenType
        self.line = line

    def __str__(self):
        return "{}\t\t{}\t\t{}".format(self.token, self.tokenType, self.line)
