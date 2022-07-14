from typing import NamedTuple
from lexer import Lexer
from lexer_types import TokenTypes

class Node(NamedTuple):
    node_type: str
    name: str | int | None
    child: tuple | None

class Parser:
    def __init__(self, text):
        self._text = text
        self._tokens = Lexer(text)

    def get_tree(self) -> Node:
        program = Node('Program', None, self._parce_function())
        return program

    def _parce_function(self) -> Node:
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

        statement = self._parce_statement()

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.closebraceToken:
            raise 'Bad syntax'

        return Node('Function', name, statement)

    def _parce_statement(self) -> Node:
        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.returnToken:
            raise 'Bad syntax'

        expression = self._parce_exp()

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.semicolonToken:
            raise 'Bad syntax'

        return Node('Statement', 'return', expression)

    def _parce_exp(self) -> Node:
        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.numberToken:
            raise 'Bad syntax'

        return Node('Expression', token, None)

def check_parser(filename):
    s = open(filename).read()

    parser = Parser(s)

    child = parser.get_tree()
    ind = ''
    while child != None:
        print(ind, child)
        ind += '    '
        child = child.child

if __name__ == '__main__':
    check_parser('return_2.c')
