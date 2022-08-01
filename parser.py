from lexer import Lexer
from lexer_types import TokenTypes, UNARY_OPERATORS, BINARY_OPERATORS
from parser_types import *

class Parser:
    def __init__(self, text):
        self._text = text
        self._lexer = Lexer(text)
        self._token = None
        self._in_un_op = False

    def get_tree(self) -> Program:
        functions = self._parse_function()
        program = Program(functions)
        return program

    def _parse_function(self) -> Function:
        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.intToken:
            raise Exception

        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.identifierToken:
            raise Exception
        name = self._token.text

        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.openparToken:
            raise Exception

        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.closeparToken:
            raise Exception

        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.openbraceToken:
            raise Exception

        statement = self._parse_statement()

        self._token = self._lexer.get_next_token()
        if self._token.token_type != TokenTypes.closebraceToken:
            raise Exception

        return Function(name, statement)

    def _parse_statement(self) -> Return:
        self._token = self._lexer.get_next_token()
        if self._token.token_type == TokenTypes.returnToken:
        
            expression = self._parse_exp()

            if self._token.token_type != TokenTypes.semicolonToken:
                raise Exception

            return Return(expression)

        raise Exception

    def _parse_exp(self) -> Constant | UnaryOperator:
        self._token = self._lexer.get_next_token()
        if self._token.token_type == TokenTypes.numberToken:
            constant = Constant(self._token.value)
            self._token = self._lexer.get_next_token()
            if self._token.token_type in BINARY_OPERATORS:
                if not self._in_un_op:
                    return BinaryOperator(self._token.text, constant,
                            self._parse_exp())
            return constant
        elif self._token.token_type in UNARY_OPERATORS:
            self._in_un_op = True
            unary_operator = UnaryOperator(self._token.text, self._parse_exp())
            return unary_operator 
        else:
            raise Exception

def check_parser(filename):
    s = open(filename).read()

    parser = Parser(s)

    child = parser.get_tree()
    ind = ''
    while type(child).__name__ != 'Constant':
        print(ind, child)
        ind += '    '
        child = child.child

if __name__ == '__main__':
    check_parser('add.c')
