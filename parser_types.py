from typing import NamedTuple

class Constant(NamedTuple):
    value: int

class UnaryOperator(NamedTuple):
    operator: str
    child: Constant

class BinaryOperator(NamedTuple):
    operator: str
    child1: Constant | UnaryOperator
    child2: Constant | UnaryOperator

class Return(NamedTuple):
    child: Constant 

class Function(NamedTuple):
    name: str
    child: Return

class Program(NamedTuple):
    child: list[Function] | Function
