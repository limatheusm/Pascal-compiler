# Pilha de Controle de Tipos

class Pct(object):

    def __init__(self):
        self.data = []
    
    def isempty(self):		
        return not self.data

    def push(self, symbol):		
        self.data.append(symbol)
        self.print_stack('push')
    
    def pop(self):		
       if not self.isempty():
           ret = self.data.pop(-1)
           self.print_stack('pop')
           return ret

    def update_pct(self, result):
        self.pop()
        self.pop()
        self.push(result)
    
    def print_stack(self, procedure):
        print '[{}]: {}'.format(procedure, self.data)
    
    def reduce_pct_arithmetic(self):
        top = self.data[-1]
        subTop = self.data[-2]

        if top == "integer" and subTop == "integer":
            self.update_pct("integer")
        elif top == "integer" and subTop == "real":
            self.update_pct("real")
        elif top == "real" and subTop == "integer":
            self.update_pct("real")
        elif top == "real" and subTop == "real":
            self.update_pct("real")
        else:
            print top +' - '+ subTop
            return False
        return True
    
    def reduce_pct_relational(self):
        top = self.data[-1]
        subTop = self.data[-2]
        types = ['integer', 'real']
        if top in types and subTop in types:
            self.update_pct("boolean")
        else:
            print top +' - '+ subTop
            return False
        return True
    
    def reduce_pct_logical(self):
        top = self.data[-1]
        subTop = self.data[-2]

        if top == "boolean" and subTop == "boolean":
            self.update_pct("boolean")
            return True
        print top +' - '+ subTop
        return False

    def top(self):
        return self.data[-1]
