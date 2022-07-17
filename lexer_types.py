from typing import NamedTuple
from enum import Enum

class TokenTypes(Enum):
    numberToken = 'numberToken'
    identifierToken = 'identifierToken'
    plusToken = '+'
    minusToken = '-'
    mulToken = '*'
    divToken = '/'
    bitwiseToken = '~'
    lognegToken = '!'
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
UNARY_OPERATORS = [TokenTypes.minusToken, TokenTypes.bitwiseToken,
                    TokenTypes.lognegToken]

class Token(NamedTuple):
    token_type: TokenTypes
    start: int
    text: str
    value: int | None

