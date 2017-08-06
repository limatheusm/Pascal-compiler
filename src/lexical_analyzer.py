import sys

class Token(object):
    
    def __init__(self, token, tokenType, line):
        self.token = token
        self.tokenType = tokenType
        self.line = line

    def __str__(self):
        return "{}\t\t{}\t\t{}".format(self.token, self.tokenType, self.line)

class LexicalAnalyzer(object):
    
    def __init__(self, program):
        self.program = program
        self.keywords = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 
                         'begin', 'end', 'if', 'then', 'else', 'while', 'not', 'do']
        self.operators = ['+', '-', '*', '/', '=', '<', '>', '>=', '<=', 'and', 'or', '<>']
        self.delimiters = [',', '.', ';', ':', ':=', ')', '(']
        self.tokens = []

    def parse(self):        
        
        i = 0        
        size = len(self.program)
        line = 1
        print ('---------------------------')
        print (self.program)
        print ('---------------------------')
        while i < size:
            token = ''
            currentType = 'null'

            #Verificar String numerica int
            if self.program[i].isdigit():                
                currentType = 'Numero Inteiro'
                while self.program[i].isdigit():
                    token += self.program[i]
                    i += 1                
                #Verificar Numero Real
                if self.program[i] == '.' and self.program[i+1].isdigit():
                    currentType = 'Numero Real'
                    token += self.program[i]
                    i += 1
                    while self.program[i].isdigit():
                        token += self.program[i]
                        i += 1               
            
            # Verificar Identificador ou Palavra Chave ou Operador (or, and)
            elif self.program[i].isalpha():
                currentType = 'Identificador'                
                while self.program[i].isalpha() or self.program[i].isdigit() or self.program[i] == '_':
                    token += self.program[i]
                    i += 1                    
                if token in self.keywords:
                    currentType = 'Palavra Chave'
                elif token in self.operators:
                    currentType = 'Operador'

            # Verificar Operadores
            elif self.program[i] in self.operators:
                currentType = 'Operador'                
                if self.program[i] == '<' or self.program[i] == '>':
                    token += self.program[i]
                    i += 1
                    if self.program[i] == '=':
                        token += self.program[i]
                        i += 1
                    elif self.program[i-1] == '<' and self.program[i] == '>':
                        token += self.program[i]
                        i += 1
                else:
                    token += self.program[i]
                    i += 1
            
            # Verificar Delimitadores
            elif self.program[i] in self.delimiters:
                currentType = 'Delimitador'
                if self.program[i] == ':' and self.program[i+1] == '=':
                    token += self.program[i] + self.program[i+1]
                    i += 2
                else:
                    token += self.program[i]
                    i += 1
            
            # Verificar Comentarios
            elif self.program[i] == '{':
                while self.program[i] != '}':
                    i += 1
                i += 1
                
            # Erro de comentario
            elif self.program[i] is '}':
				sys.exit("Erro linha {} - Faltou abrir comentario".format(line))

            # Contagem de Linhas
            elif self.program[i] == '\n':
                i += 1
                line += 1

            else:
                i += 1 

            if token:
                self.tokens.append(Token(token, currentType, line)) 

        print('\nToken\t\tClassificacao\t\tLinha\n')
        for s in self.tokens:
            print(s)  

#file_name = sys.argv[1]
file_name = '../program.txt'
p = open(file_name, "r").read()
LexicalAnalyzer(p).parse()
