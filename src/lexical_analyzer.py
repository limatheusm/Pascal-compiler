import sys
from token import Token
from stack import Stack

class LexicalAnalyzer(object):

    def __init__(self, program):
        self.program = program
        self.keywords = ['program', 'var', 'integer', 'real', 'boolean', 'procedure',
                         'begin', 'end', 'if', 'then', 'else', 'while', 'not', 'do']
        self.relational_operators = ['=', '<', '>', '>=', '<=', '<>']
        self.additive_operators = ['+', '-', 'or']
        self.multiplicative_operators = ['*', '/', 'and']
        self.delimiters = [',', '.', ';', ':', ':=', ')', '(']
        self.tokens = []

    def parse(self):

        i = 0
        size = len(self.program)
        line = 1
        stackComment = Stack()
        print ('---------------------------')
        print (self.program)
        print ('---------------------------')
        while i < size:
            token = ''
            currentType = 'null'

            
            #Verificar String numerica int
            if self.program[i].isdigit():
                currentType = 'Numero Inteiro'
                while i < size and self.program[i].isdigit():
                    token += self.program[i]
                    i += 1
                #Verificar Numero Real
                if i < size and self.program[i] == '.':
                    currentType = 'Numero Real'
                    token += self.program[i]
                    i += 1
                    while i < size and self.program[i].isdigit():
                        token += self.program[i]
                        i += 1
                # numero complexo 23i+12 23i+
                elif i < size and self.program[i] == 'i':
                    tempToken = ''
                    tempToken += token
                    tempToken += self.program[i] #23
                    # verifica se realmente eh complexo
                    if i < size - 2 and (self.program[i+1] in '-+') and self.program[i+2].isdigit():
                        currentType = 'Numero Complexo'
                        i += 1 # Coloca i
                        token = tempToken
                        token += self.program[i]
                        i += 1 # comeca a ler numeros
                        while i < size and self.program[i].isdigit():
                            token += self.program[i]
                            i += 1

                        
            # Verificar Identificador ou Palavra Chave ou Operador (or, and)
            elif self.program[i].isalpha():
                currentType = 'Identificador'
                while i < size and (self.program[i].isalpha() or self.program[i].isdigit() or self.program[i] == '_'):
                    token += self.program[i]
                    i += 1
                if token in self.keywords:
                    currentType = 'Palavra Reserv.'
                elif token in self.multiplicative_operators:
                    currentType = 'Operador Mult'
                elif token in self.additive_operators:
                    currentType = 'Operador Adit.'

            # Verificar comentario de linha
            elif i < size - 1 and self.program[i] == '/' and self.program[i+1] == '/':
                while i < size:
                    i += 1
                    if i >= size:
                        break
                    if self.program[i] == '\n':
                        i += 1
                        line += 1
                        break
                

            # Verificar Operadores
            elif self.program[i] in self.relational_operators:
                currentType = 'Operador Rel.'
                if self.program[i] == '<' or self.program[i] == '>':
                    token += self.program[i]
                    i += 1
                    if i < size and self.program[i] == '=':
                        token += self.program[i]
                        i += 1
                    elif i < size and self.program[i-1] == '<' and self.program[i] == '>':
                        token += self.program[i]
                        i += 1
                else:
                    token += self.program[i]
                    i += 1
            elif self.program[i] in self.additive_operators:
                currentType = 'Operador Adit.'
                token += self.program[i]
                i += 1
            elif self.program[i] in self.multiplicative_operators:
                currentType = 'Operador Mult'
                token += self.program[i]
                i += 1

            # Verificar Delimitadores
            elif self.program[i] in self.delimiters:
                currentType = 'Delimitador'
                if self.program[i] == ':' and i < size - 1 and self.program[i+1] == '=':
                    currentType = 'Atribuicao'
                    token += self.program[i] + self.program[i+1]
                    i += 2
                else:
                    token += self.program[i]
                    i += 1
            
            # # Verificar Comentarios
            elif self.program[i] == '{':
                lineComment = line
                while self.program[i] != '}':
                    i += 1
                    if i >= size:
                        sys.exit("Erro - Faltou fechar comentario aberto na linha {}".format(lineComment))
                    if self.program[i] == '\n':
                        line += 1
                i += 1
            
            # elif self.program[i] == '{':
            #     # Empilha elemento
            #     stackComment.push(self.program[i])
            #     i += 1
            #     while i < size:                    
            #         if self.program[i] == '\n':
            #             line += 1
            #         if not stackComment.isempty():
            #             if self.program[i] == '{':
            #                 stackComment.push(self.program[i])
            #             elif self.program[i] == '}':
            #                 # Desempilha
            #                 stackComment.pop()
            #         else:
            #             break
            #         i += 1
            #     if not stackComment.isempty():
            #         sys.exit("Erro - Comentario aberto e nao fechado - linha {}".format(line))
            #     i += 1

            # Erro de comentario
            elif self.program[i] is '}':
                sys.exit("Erro - Comentario fechado e nao aberto - linha {}".format(line))

            # Contagem de Linhas
            elif self.program[i] == '\n':
                i += 1
                line += 1

            #Verificar simbolos fora da linguagem
            elif not self.program[i].isspace():
                sys.exit("Erro linha {} - Simbolo {} nao pertence a linguagem".format(line, self.program[i]))

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
