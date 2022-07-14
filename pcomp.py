import sys
from assembly_generator import AssemblyGenerator

text = open(sys.argv[1]).read()

gen = AssemblyGenerator(text)

if len(sys.argv) == 3:
    gen.generate_file(sys.argv[2])
else:
    gen.generate_file()
