from parser import Parser

class AssemblyGenerator:
    def __init__(self, text):
        self._text = text
        self._tree = Parser(text).get_tree()
    
    def generate_file(self, name='result.s') -> None:
        with open(name, 'w') as f:
            f.write(self._generate_code())

    def _generate_code(self) -> str:
        while self._tree != None:
            if self._tree.node_type == 'Function':
                name = self._tree.name
                return self._generate_function(name)
            self._tree = self._tree.child

    def _generate_function(self, name) -> str:
        s = f' .globl {name}\n{name}:\n{self._generate_statement()}'
        return s

    def _generate_statement(self) -> str:
        while self._tree.node_type != 'Statement':
            self._tree = self._tree.child
        if self._tree.name == 'return':
            self._tree = self._tree.child
            if self._tree.node_type == 'Expression':
                return f' movl\t${self._tree.name.value}, %eax\n ret\n'

def check_generator(input_file, result_filename):
    s = open(input_file).read()

    gen = AssemblyGenerator(s) 

    gen.generate_file(result_filename)

if __name__ == '__main__':
    check_generator('return_2.c', 'check.s')
