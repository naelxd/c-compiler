from enum import Enum
from typing import NamedTuple

class TokenTypes(Enum):
    numberToken = 'numberToken'
    identifierToken = 'identifierToken'
    plusToken = 'plusToken'
    minusToken = 'minusToken'
    mulToken = 'mulToken'
    divToken = 'divToken'
    returnToken = 'returnToken'
    openbraceToken = 'openbraceToken'
    closebraceToken = 'closebraceToken'
    openparToken = 'openparToken'
    closeparToken = 'closeparToken'
    semicolonToken = 'semicolonToken'
    intToken = 'intToken'
    errorToken = 'errorToken'
    end = '\0'


class Token(NamedTuple):
    token_type: TokenTypes
    start: int
    text: str
    value: int | None


class Lexer:
    def __init__(self, text):
        self._text = text
        self._position = 0

    def get_next_token(self) -> Token:
        self._pass_indents()
        
        if self._is_end():
            return Token(TokenTypes.end, self._position, '\0', None)

        '''
        if (self._text[self._position] == ' ' or
                self._text[self._position] =='\n' or
                self._text[self._position] =='\t'):
            self._position += 1
        
        if self._text[self._position].isdigit():
            start = self._position

            while (self._position != len(self._text) and 
                    self._text[self._position].isdigit()):
                self._position += 1

            text = self._text[start: self._position]
            value = int(text)

            return Token(TokenTypes.numberToken, start, text, value)
        '''
        if self._text[self._position] == '+':
            self._position += 1
            return Token(TokenTypes.plusToken, self._position - 1, '+', None)
        elif self._text[self._position] == '-':
            self._position += 1
            return Token(TokenTypes.minusToken, self._position - 1, '-', None)
        elif self._text[self._position] == '*':
            self._position += 1
            return Token(TokenTypes.mulToken, self._position - 1, '*', None)
        elif self._text[self._position]  == '/':
            self._position += 1
            return Token(TokenTypes.divToken, self._position - 1, '/', None)
        elif self._text[self._position]  == '{':
            self._position += 1
            return Token(TokenTypes.openbraceToken, self._position - 1, '{', None)
        elif self._text[self._position]  == '}':
            self._position += 1
            return Token(TokenTypes.closebraceToken, self._position - 1, '}', None)
        elif self._text[self._position]  == '(':
            self._position += 1
            return Token(TokenTypes.openparToken, self._position - 1, '(', None)
        elif self._text[self._position]  == ')':
            self._position += 1
            return Token(TokenTypes.closeparToken, self._position - 1, ')', None)
        elif self._text[self._position]  == ';':
            self._position += 1
            return Token(TokenTypes.semicolonToken, self._position - 1, ';', None)
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


if __name__ == '__main__':
    s = open('return_2.c').read()
    
    lexer = Lexer(s)
    
    token = lexer.get_next_token()

    while token.token_type != TokenTypes.end:
        print(token.token_type.value, token.text, token.value)
        token = lexer.get_next_token()


