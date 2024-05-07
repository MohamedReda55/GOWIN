from src.interpreter.interpreter import Interpreter

Cfile="test_2.c"
with open(Cfile, 'r') as file:
        code = file.read()
        Interpreter.run(code)