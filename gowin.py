import argparse
from src.interpreter.interpreter import Interpreter


parser = argparse.ArgumentParser("GOWIN Interpreter")

parser.add_argument("-f","--file", help="filename to run", type=str)
args = parser.parse_args()
if not args.file:
    raise FileNotFoundError()

Cfile=args.file
with open(Cfile, 'r') as file:
        code = file.read()
        Interpreter.run(code)