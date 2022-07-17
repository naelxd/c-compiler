from lexer import Lexer
from lexer_types import TokenTypes, UNARY_OPERATORS
from parser_types import *

class Parser:
    def __init__(self, text):
        self._text = text
        self._tokens = Lexer(text)

    def get_tree(self) -> Program:
        functions = self._parse_function()
        program = Program(functions)
        return program

    def _parse_function(self) -> Function:
        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.intToken:
            raise 'Bad syntax'

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.identifierToken:
            raise 'Bad syntax'
        name = token.text

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.openparToken:
            raise 'Bad syntax'

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.closeparToken:
            raise 'Bad syntax'

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.openbraceToken:
            raise 'Bad syntax'

        statement = self._parse_statement()

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.closebraceToken:
            raise 'Bad syntax'

        return Function(name, statement)

    def _parse_statement(self) -> Return:
        token = self._tokens.get_next_token()
        if token.token_type == TokenTypes.returnToken:
        
            expression = self._parse_exp()

            token = self._tokens.get_next_token()
            if token.token_type != TokenTypes.semicolonToken:
                raise 'Bad syntax'

            return Return(expression)

        raise 'Bad syntax'

    def _parse_exp(self) -> Constant | UnaryOperator:
        token = self._tokens.get_next_token()
        if token.token_type == TokenTypes.numberToken:
            return Constant(token.value)

        elif token.token_type in UNARY_OPERATORS:
            return UnaryOperator(token.text, self._parse_exp()) 
        else:
            raise 'Bad syntax'

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
    check_parser('nested_ops.c')
