from symbol import Symbol

class SymbolTable(object):
    
    def __init__(self):
        self.data = []
        self.mark = '$'
    
    def push(self, symbol):		
       self.data.append(symbol)	
    
    def isempty(self):		
        return not self.data
    
    def pop(self):		
       if not self.isempty():	
           return self.data.pop(-1)

    def beginScope(self):
        self.push(Symbol(self.mark, 'mark'))
        self.printStack('beginScope')
    
    def endScope(self):
        # Elimina todos as entradas da pilha ate
        # encontrar a mark, que tambem eh eliminado
        i = -1
        if self.isempty():            
            return 

        while self.data[i].word != self.mark:
            self.pop()
        self.pop() # retira a marca
        #self.printStack('endScope')      

    def searchSymbol(self, symbol):
        #print '[searchSymbol]: {}'.format(symbol)
        for s in self.data[::-1]:
            if s.word == symbol:
                return s
        return False

    def addSymbol(self, symbol, _type):
        i = -1
        if self.isempty():
            self.push(symbol)
            return 

        # verificar se ja existe o simbolo no escopo
        while self.data[i].word != self.mark and self.data[i].word != symbol:
            i -= 1

        if self.data[i].word == self.mark:
            self.push(Symbol(symbol, _type))
            #self.printStack('addSymbol')
            return True
        else:
            return False
    
    def printStack(self, procedure):
        print '[{}]: {}'.format(procedure, self.data)
    
    def setType(self, _type):
        for index, value in enumerate(self.data):
            if value.type == '?':
                self.data[index].type = _type
        #self.printStack('setType')