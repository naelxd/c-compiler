from lexer_types import *

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
            
            if text in TOKEN_VALUES:
                return Token(TokenTypes(text), start, text, None)

            return Token(TokenTypes.identifierToken, start, text, None)

    def _pass_indents(self) -> None:
        while (not self._is_end() and 
                self._text[self._position] in [' ', '\n', '\t']):
            self._position += 1

    def _is_end(self) -> bool:
        return self._position == len(self._text)

def check_lexer(filename):
    s = open(filename).read()
    
    lexer = Lexer(s)
    
    token = lexer.get_next_token()

    while token.token_type != TokenTypes.end:
        print(token.token_type, token.text, token.value)
        token = lexer.get_next_token()

if __name__ == '__main__':
    check_lexer('return_2.c')
