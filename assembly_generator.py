from parser import Parser

class AssemblyGenerator:
    def __init__(self, text):
        self._text = text
        self._tree = Parser(text).get_tree()
    
    def generate_file(self, name='result.s') -> None:
        with open(name, 'w') as f:
            f.write(self._generate_code())

    def _generate_code(self) -> str:
        self._tree = self._tree.child
        name = self._tree.name
        return self._generate_function(name)

    def _generate_function(self, name) -> str:
        self._tree = self._tree.child
        s = f' .globl {name}\n{name}:\n{self._generate_statement()}'
        return s

    def _generate_statement(self) -> str:
        if type(self._tree).__name__ == 'Return':
            self._tree = self._tree.child
            if type(self._tree).__name__ == 'Constant':
                return f' movl\t${self._tree.value}, %eax\n ret\n'

def check_generator(input_file):
    s = open(input_file).read()

    gen = AssemblyGenerator(s) 

    print(gen._generate_code())

if __name__ == '__main__':
    check_generator('return_2.c')
