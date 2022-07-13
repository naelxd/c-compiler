from enum import Enum
from typing import NamedTuple

class TokenTypes(Enum):
    numberToken = 'numberToken'
    identifierToken = 'identifierToken'
    plusToken = '+'
    minusToken = '-'
    mulToken = '*'
    divToken = '/'
    openbraceToken = '{'
    closebraceToken = '}'
    openparToken = '('
    closeparToken = ')'
    semicolonToken = ';'
    returnToken = 'return'
    intToken = 'int'
    errorToken = 'errorToken'
    end = '\0'

TOKEN_VALUES = [t.value for t in TokenTypes]

class Token(NamedTuple):
    token_type: TokenTypes
    start: int
    text: str
    value: int | None

class Node(NamedTuple):
    name: str | int
    child: tuple | None

class Lexer:
    ''' Lexer for code on C '''
    def __init__(self, text):
        self._text = text
        self._position = 0

    def get_next_token(self) -> Token:
        self._pass_indents()
        
        if self._is_end():
            return Token(TokenTypes.end, self._position, '\0', None)

        if self._text[self._position] in TOKEN_VALUES:
            text = self._text[self._position]
            self._position += 1
            return Token(TokenTypes(text), self._position - 1, text, None)
        elif self._text[self._position:self._position+3] == 'int':
            self._position += 3
            return Token(TokenTypes.intToken, self._position - 3, 'int', None)
        elif self._text[self._position:self._position+6] == 'return':
            self._position += 6
            return Token(TokenTypes.returnToken, self._position - 6, 'return', None)
        elif self._text[self._position].isdigit():
            start = self._position

            while (not self._is_end() and 
                    self._text[self._position].isdigit()):
                self._position += 1

            text = self._text[start:self._position]
            value = int(text)

            return Token(TokenTypes.numberToken, start, text, value)
        elif self._text[self._position].isidentifier():
            start = self._position

            while (not self._is_end() and
                    self._text[self._position] != ' ' and
                    self._text[self._position] not in 
                    ['}', '{', '(', ')', ';', '+', '-', '*', '/']):
                self._position += 1

            text = self._text[start:self._position]

            return Token(TokenTypes.identifierToken, start, text, None)

    def _pass_indents(self) -> None:
        while (not self._is_end() and 
                self._text[self._position] in [' ', '\n', '\t']):
            self._position += 1

    def _is_end(self) -> bool:
        return self._position == len(self._text)

class Parser:
    def __init__(self, text):
        self._text = text
        self._tokens = Lexer(text)

    def get_tree(self) -> Node:
        program = Node('Program', self._parce_function())
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

        return Node(name, statement)

    def _parce_statement(self) -> Node:
        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.returnToken:
            raise 'Bad syntax'

        expression = self._parce_exp()

        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.semicolonToken:
            raise 'Bad syntax'

        return Node('statement', expression)

    def _parce_exp(self) -> Node:
        token = self._tokens.get_next_token()
        if token.token_type != TokenTypes.numberToken:
            raise 'Bad syntax'

        return Node(token.value, None)

def check_lexer(filename):
    s = open(filename).read()
    
    lexer = Lexer(s)
    
    token = lexer.get_next_token()

    while token.token_type != TokenTypes.end:
        print(token.token_type, token.text, token.value)
        token = lexer.get_next_token()

if __name__ == '__main__':
    s = open('return_2.c').read()

    parser = Parser(s)

    child = parser.get_tree()
    while child != None:
        print(child)
        child = child.child
