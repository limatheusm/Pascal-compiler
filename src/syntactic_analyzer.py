import sys
import traceback

from lexical_analyzer import LexicalAnalyzer


class SyntacticAnalyzer(object):
    
    def __init__ (self, list_tokens):
        self.list_tokens = list_tokens
        self.index = -1
    
    # name_func' == name_func__

    def program(self):

        if self.nextToken().token == 'program':
            if self.nextToken().tokenType == 'Identificador':
                if self.nextToken().token == ';':
                    self.var_declarations() 
                    self.subprograms_declarations()
                    self.composed_commands()
                    if self.nextToken().token == '.':
                        print('Sucesso')
                    else:
                        self.syntaxError('.')
                else:
                    self.syntaxError(";")
            else:
                self.syntaxError("Identificador")
        else:
            self.syntaxError("program")
    
    def var_declarations(self):
        if self.nextToken().token == 'var':
            self.list_var_declarations()
        else:
            self.index -= 1
    
    def subprograms_declarations(self):
        self.subprograms_declarations__()
    
    def subprograms_declarations__(self):
        if self.subprogram_declaration():
            if self.nextToken().token == ';':
                self.subprograms_declarations__()
            else:
                self.syntaxError(';')
        else:
            pass
    
    def subprogram_declaration(self):
        if self.nextToken().token == 'procedure':
            if self.nextToken().tokenType == 'Identificador':
                self.arguments()
                if self.nextToken().token == ';':
                    self.var_declarations()
                    self.subprograms_declarations()
                    self.composed_commands()
                    return True
                else:
                    self.syntaxError(';')
            else:
                self.syntaxError('Identificador')
        else:
            self.index -= 1
            return False
    
    def arguments(self):
        if self.nextToken().token == '(':
            self.list_parameters()
            if self.nextToken().token == ')':
                pass
            else:
                self.syntaxError(')')
        else:
            self.index -= 1

    def list_parameters(self):
        self.list_identifiers() # pode ser nulo
        if self.nextToken().token == ':':
            self._type()
            self.list_parameters__()
        else:
            self.syntaxError(':')
    
    def list_parameters__(self):
        if self.nextToken().token == ';':
            self.list_identifiers()
            if self.nextToken().token == ':':
                self._type()
                self.list_parameters__()
            else:
                self.syntaxError(':')
        else:
            self.index -= 1
    
    ## return
    def composed_commands(self):
        if self.nextToken().token == 'begin':
            self.options_commands()
            if self.nextToken().token == 'end':
                return True
            else:
                self.syntaxError('end')
        else:
            self.index -= 1
            return False
    
    def options_commands(self):
        self.list_commands()

    def list_commands(self):
        self.command()
        self.list_commands__()
    
    def list_commands__(self):
        if self.nextToken().token == ';':
            self.command()
            self.list_commands__()
        else:
            self.index -= 1
    
    ## return
    def command(self):
        if self.variable():
            if self.nextToken().token == ':=':
                self.expression()
                return
            else:
                self.syntaxError(':=')

        elif self.activation_procedure():
            pass
        elif self.composed_commands():
            pass
        else:
            aux = self.nextToken()
            
            if aux.token == 'if':
                self.expression()
                if self.nextToken().token == 'then':
                    self.command()
                    self.part_else()
                    return
                else:
                    self.syntaxError('then')
            elif aux.token == 'while':
                self.expression()
                if self.nextToken().token == 'do':
                    self.command()
                    return
                else:
                    self.syntaxError('do')
            else:
                self.index -= 1
                return False

    ## return
    def variable(self):
        if self.nextToken().tokenType == 'Identificador':
            return True
        else:
            self.index -= 1
            return False
    
    ## return
    def activation_procedure(self):
        if self.nextToken().tokenType == 'Identificador':
            if self.nextToken().token == '(':
                self.list_expressions()
                if self.nextToken().token == ')':
                    return True
                else:
                    self.syntaxError(')')
            else:
                self.index -= 1 
                return True
        else:
            self.index -= 1
            return False
            
    def expression(self):
        if self.simple_expression():
            if self.op_relational():
                self.simple_expression()
        else:
            self.syntaxError('Expressao')

    def simple_expression(self):
        if self.term():
            self.simple_expression__() #
            return True
        elif self.signal():
            self.term()
            self.simple_expression__()
            return True
        else:
            return False

    def simple_expression__(self):
        if self.op_aditive():
            self.term()
            self.simple_expression__()
    
    ## return
    def op_relational(self):
        if self.nextToken().tokenType == 'Operador Relacional':
            return True
        else:
            self.index -= 1
            return False
    
    ## return
    def op_aditive(self):
        if self.nextToken().tokenType == 'Operador Aditivo':
            return True
        else:
            self.index -= 1
            return False
    
    ## return
    def op_multiplicative(self):
        if self.nextToken().tokenType == 'Operador Multiplicativo':
            return True
        else:
            self.index -= 1
            return False
        pass

    ## return
    def term(self):
        if self.factor():
            self.term__()
            return True
        else:
            return False
    
    def term__(self):
        if self.op_multiplicative():
            self.factor()
            self.term__()

    ## return
    def signal(self):
        if self.nextToken().token in "+-":
            return True
        else:
            self.index -= 1
            return False
    
    ## return
    def factor(self):
        aux = self.nextToken()
        if aux.tokenType == 'Identificador':
            if self.nextToken().token == '(':
                self.list_expressions()
                if self.nextToken().token == ')':
                    return True
                else:
                    self.syntaxError(')')
            else:
                self.index -= 1
                return True
        elif aux.tokenType == 'Numero Inteiro':
            return True
        elif aux.tokenType == 'Numero Real':
            return True
        elif aux.token == 'true':
            return True
        elif aux.token == 'false':
            return True
        elif aux.token == '(':
            self.expression()
            if self.nextToken().token == ')':
                return True
            else:
                self.syntaxError(')')
        elif aux.token == 'not':
            self.factor()
            return True
        else:
            self.index -= 1
            return False
    
    def list_expressions(self):
        self.expression()
        self.list_expressions__()
    
    def list_expressions__(self):
        if self.nextToken().token == ',':
            self.expression()
            self.list_expressions__()
        else:
            self.index -= 1
    
    def part_else(self):
        if self.nextToken().token == 'else':
            self.command()
        else:
            self.index -= 1

    def list_var_declarations(self):
        if self.list_identifiers():
            if self.nextToken().token == ':':
                self._type()
                if self.nextToken().token == ';':
                    self.list_var_declarations__()
                else:
                    self.syntaxError(';')
            else:
                self.syntaxError(':')
        else:
            self.syntaxError('Indentificador')

    def list_var_declarations__(self):
        if self.list_identifiers():
            if self.nextToken().token == ':':
                self._type()
                if self.nextToken().token == ';':
                    self.list_var_declarations__()
                else:
                    self.syntaxError(';')
            else:
                self.syntaxError(':')

    def list_identifiers(self):
        if self.nextToken().tokenType == 'Identificador':
            self.list_identifiers__()
            return True
        else:
            self.index -= 1
            return False

    def list_identifiers__(self):
        if self.nextToken().token == ',':
            if self.nextToken().tokenType == 'Identificador':
                self.list_identifiers__()
            else:
                self.syntaxError('Identificador')
        else:
            self.index -= 1
    
    def _type(self):
        if self.nextToken().token in ['integer', 'boolean', 'real']:
            pass
        else:
            self.syntaxError('Tipo')

    # Help Functions
    def nextToken(self):
        if (self.index + 1) < len(self.list_tokens):
            self.index += 1
            #print(self.list_tokens[self.index])
            #self.showStack()
            return self.list_tokens[self.index]
        else:
            sys.exit("out range")
    
    def syntaxError(self, token):
        sys.exit("Erro de sintaxe! Faltou adicionar {}".format(token))

    def showStack(self):
        print("########")
        for line in traceback.format_stack():
            print(line)
        print("########")


file_path = '../program.txt'
p = open(file_path, "r").read()
lex = LexicalAnalyzer(p).parse()
SyntacticAnalyzer(lex).program()
