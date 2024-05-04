# from src.lexical_analysis.lexar import Lexer
from src.lexical_analysis.lexar import *
from src.syntax_analysis.parser import *
from src.semantic_analysis.analyzer import *
from src.interpreter.interpreter import *

def handle_string_exp(lexer_obj):
        token = lexer_obj.get_next_token
        previous_token=token
        yield token
        while True:
            token = lexer_obj.get_next_token
            # print(token.type,previous_token.type,token,previous_token)
            
            if token.type==COMMA and previous_token.type in [COMMA,EOF]:
                
                lexer_obj.error(message="SyntaxError: invalid syntax. Expected value between commas.")

            if token.type == COMMA:
                previous_token=token
                continue
            if token.type ==EOF:
                if previous_token.type==COMMA:
                    lexer_obj.error(message="SyntaxError: invalid syntax. Expected value between commas.")
                
                break
            previous_token=token
            yield token
            
            

    

# t=Lexer("['1','2',3,\"hello\",test,(5+5)]")
# t=Lexer("void main(){{int equation = {};}}".format("10"))


# parser = Parser(t)
# tree = parser.parse()
# # print(tree)
# SemanticAnalyzer.analyze(tree)
# status = Interpreter().interpret_with_memory(tree)
# print(status.value)
# for token in handle_string_exp(t):
#     # print(token)
#     pass

print(Interpreter().handle_equations("5*56"))