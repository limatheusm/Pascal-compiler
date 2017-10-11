import sys
import traceback

from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable
from pct import Pct


class SyntacticAnalyzer(object):
    
    def __init__ (self, list_tokens):
        self.list_tokens = list_tokens
        self.index = -1
        self.symbolTable = SymbolTable() # Semantico
        self.pct = Pct()
        self.scope = 0 # Semantico
    
    # name_func' == name_func__

    def program(self):

        if self.nextToken().token == 'program':
            self.symbolTable.beginScope() # Semantico
            if self.nextToken().tokenType == 'Identificador':
                self.symbolTable.addSymbol(self.getCurrentToken().token, 'program')  # Semantico
                if self.nextToken().token == ';':
                    self.var_declarations() 
                    self.subprograms_declarations()
                    self.composed_commands()
                    if self.nextToken().token == '.':
                        self.symbolTable.endScope() # Semantico
                        print('Sucesso')
                    else:
                        self.getCurrentToken()
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
                self.symbolTable.addSymbol(self.getCurrentToken().token, 'procedure') # Semantico
                self.symbolTable.beginScope() # Semantico
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
            self.scope += 1 # Semantico
            self.options_commands()
            if self.nextToken().token == 'end':
                self.scope -= 1 # Semantico
                if not self.scope: # Semantico
                    self.symbolTable.endScope()
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
            # Recupera o tipo da variavel que recebe
            type_id = self.symbolTable.searchSymbol(self.getCurrentToken().token).type # Semantico [Verificacao de Tipos]
            if type_id == 'program':
                sys.exit('ERRO! O nome do programa nao pode ser usado em comandos e expressoes')

            if self.nextToken().token == ':=':
                self.expression() 
                # Verifica compatibilidade de tipos do resultado com o identificador
                self.verifyTypesId(type_id, self.pct.top())
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
                # Verifica o tipo resultado
                if self.pct.top() == 'boolean': # Semantico [Verificacao de Tipos]
                    self.pct.pop() # Ok!
                else:
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: tipo do if nao eh booleano'.format(self.getCurrentToken().line))
                if self.nextToken().token == 'then':
                    self.command()
                    self.part_else()
                    return
                else:
                    self.syntaxError('then')
            elif aux.token == 'while':
                self.expression()
                if self.pct.top() == 'boolean': # Semantico
                    self.pct.pop() # Ok!
                else:
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: tipo do while nao eh booleano'.format(self.getCurrentToken().line))
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
            self.verifyScope(self.getCurrentToken()) # Semantico [Tabela De Simbolos]
            return True
        else:
            self.index -= 1
            return False
    
    ## return
    def activation_procedure(self):
        if self.nextToken().tokenType == 'Identificador':
            self.verifyScope(self.getCurrentToken()) # Semantico [Tabela de Simbolos]
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
                # Confere os tipos # Semantico
                if not self.pct.reduce_pct_relational():
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: Comparando variaveis com tipos diferentes de integer ou real'.format(self.getCurrentToken().line))
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
            op = self.getCurrentToken().token
            self.term()
            self.simple_expression__()
            # Semantico [Verificacao de Tipos]
            if op == 'or':
                if not self.pct.reduce_pct_logical():
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: Op logicas com tipos diferentes de boolean'.format(self.getCurrentToken().line))
            else:
                if not self.pct.reduce_pct_arithmetic():
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: Op aritimeticas com tipos diferentes de integer ou real'.format(self.getCurrentToken().line))
    
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

    ## return
    def term(self):
        if self.factor():
            self.term__()
            return True
        else:
            return False
    
    def term__(self):
        if self.op_multiplicative():
            op = self.getCurrentToken().token
            self.factor()
            self.term__()
            # Confere os tipos # Semantico
            if op == 'and':
                if not self.pct.reduce_pct_logical():
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: Op logicas com tipos diferentes de boolean'.format(self.getCurrentToken().line))
            else:
                if not self.pct.reduce_pct_arithmetic():
                    sys.exit('ERROR linha {}! Incompatibilidade de tipos: Op aritimeticas com tipos diferentes de integer ou real'.format(self.getCurrentToken().line))
            

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
            self.verifyScope(self.getCurrentToken()) # Semantico [Tabela de Simbolos]
            # Recupera o simbolo corrente dentro da tabela de simbolos e empilha seu tipo na pct
            self.pct.push(self.symbolTable.searchSymbol(self.getCurrentToken().token).type) # Semantico [Verificacao de Tipos]
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
            self.pct.push('integer') # Semantico [Verificacao de Tipos]
            return True
        elif aux.tokenType == 'Numero Real':
            self.pct.push('real') # Semantico [Verificacao de Tipos]
            return True
        elif aux.token == 'true':
            self.pct.push('boolean') # Semantico [Verificacao de Tipos]
            return True
        elif aux.token == 'false':
            self.pct.push('boolean') # Semantico [Verificacao de Tipos]
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
            self.verifyScope(self.getCurrentToken()) # Semantico
            self.list_identifiers__()
            return True
        else:
            self.index -= 1
            return False

    def list_identifiers__(self):
        if self.nextToken().token == ',':
            if self.nextToken().tokenType == 'Identificador':
                self.verifyScope(self.getCurrentToken()) # Semantico
                self.list_identifiers__()
            else:
                self.syntaxError('Identificador')
        else:
            self.index -= 1
    
    def _type(self):
        if self.nextToken().token in ['integer', 'boolean', 'real']:
            self.symbolTable.setType(self.getCurrentToken().token) # Semantico
        else:
            self.syntaxError('Tipo')

    
    # Help Functions
    def verifyTypesId(self, type_id, pct_top):
        line = self.getCurrentToken().line
        if type_id == "integer" and pct_top == "real":
            sys.exit('ERRO linha {}! Incompatibilidade de tipos: Adicionando real em uma variavel inteira'.format(line))
        elif type_id in ['integer','real'] and pct_top == "boolean":
            sys.exit('ERRO linha {}! Incompatibilidade de tipos: Adicionando boolean em uma variavel {}'.format(line, type_id))
        elif pct_top in ['integer','real'] and type_id == "boolean":
            sys.exit('ERRO linha {}! Incompatibilidade de tipos: Adicionando {} em uma variavel boolean'.format(line, pct_top))
        
        self.pct.pop() # Apos verificar id, retira da pilha, zerando assim a pilha
        
    def verifyScope(self, symbol):
        if self.scope:
            if not self.symbolTable.searchSymbol(symbol.token):
                sys.exit('Erro linha {}! Simbolo {} nao declarado'.format(symbol.line, symbol.token))
        else:
            if not self.symbolTable.addSymbol(symbol.token, '?'):
                sys.exit('Erro linha {}! Simbolo {} ja foi declarado no mesmo escopo'.format(symbol.line, symbol.token))

    def nextToken(self):
        if (self.index + 1) < len(self.list_tokens):
            self.index += 1
            #print(self.list_tokens[self.index])
            #self.showStack()
            return self.list_tokens[self.index]
        else:
            sys.exit("out range")
    
    def syntaxError(self, expected):
        ct = self.getCurrentToken()
        sys.exit('Syntax error, "{}" expected but "{}" found in line {}'.format(expected, ct.token, ct.line))
    
    def getCurrentToken(self):
        #print '[getCurrentToken]: {}'.format(self.list_tokens[self.index])
        return self.list_tokens[self.index]

    def showStack(self):
        print("########")
        for line in traceback.format_stack():
            print(line)
        print("########")


file_path = '../program.txt'
p = open(file_path, "r").read()
lex = LexicalAnalyzer(p).parse()
SyntacticAnalyzer(lex).program()