from .memory import *
from .number import Number
from .string import CustomString
from .list import CustomList

from ..lexical_analysis.lexar import Lexer
from ..lexical_analysis.token_type import *
from ..syntax_analysis.parser import Parser
from ..syntax_analysis.tree import *
from ..semantic_analysis.analyzer import SemanticAnalyzer
from ..utils.utils import get_functions, MessageColor

import re


class Interpreter(NodeVisitor):

    def __init__(self):
        self.memory = Memory()

    def load_libraries(self, tree):
        for node in filter(lambda o: isinstance(o, IncludeLibrary), tree.children):
            functions = get_functions('src.__builtins__.{}'.format(
                node.library_name
            ))
            
            for function in functions:
                if function.__name__=="printf":

                    self.memory["اطبع"] = function

                self.memory[function.__name__] = function

    def load_functions(self, tree):
        for node in filter(lambda o: isinstance(o, FunctionDecl), tree.children):
            self.memory[node.func_name] = node

    def visit_Program(self, node):
        for var in filter(lambda self: not isinstance(self, (FunctionDecl, IncludeLibrary)), node.children):
            self.visit(var)

    def visit_VarDecl(self, node):
        self.memory.declare(node.var_node.value)

    def visit_FunctionDecl(self, node):
        for i, param in enumerate(node.params):
            self.memory[param.var_node.value] = self.memory.stack.current_frame.current_scope._values.pop(i)
        return self.visit(node.body)

    def visit_FunctionBody(self, node):
        for child in node.children:
            if isinstance(child, ReturnStmt):
                return self.visit(child)
            self.visit(child)

    def visit_Expression(self, node):
        expr = None
        for child in node.children:
            expr = self.visit(child)
        return expr

    def visit_FunctionCall(self, node):
    
        args = [self.visit(arg) for arg in node.args]
        if node.name == 'scanf':
            args.append(self.memory)

        if isinstance(self.memory[node.name], Node):
            self.memory.new_frame(node.name)

            for i, arg in enumerate(args):
                self.memory.declare(i)
                self.memory[i] = arg
                

            res = self.visit(self.memory[node.name])
            self.memory.del_frame()
            return res
        else:
            if self.memory[node.name].return_type == "str":
                return CustomString(self.memory[node.name](*args))
            elif self.memory[node.name].return_type == "list":
                return CustomList(self.memory[node.name](*args))
            
            return Number(self.memory[node.name].return_type, self.memory[node.name](*args))

    def visit_UnOp(self, node):
        if node.prefix:
            if node.op.type == AND_OP:
                return node.expr.value
            elif node.op.type == INC_OP :
                self.memory[node.expr.value] += Number('int', 1)
                return self.memory[node.expr.value]
            elif node.op.type == DEC_OP:
                self.memory[node.expr.value] -= Number('int', 1)
                return self.memory[node.expr.value]
            elif node.op.type == SUB_OP:
                return Number('int', -1) * self.visit(node.expr)
            elif node.op.type == ADD_OP:
                return self.visit(node.expr)
            elif node.op.type == LOG_NEG:
                res = self.visit(node.expr)
                return res._not()
            else:
                res = self.visit(node.expr)
                return Number(node.op.value, res.value)
        else:
            if node.op.type == INC_OP :
                var = self.memory[node.expr.value]
                self.memory[node.expr.value] += Number('int', 1)
                return var
            elif node.op.type == DEC_OP:
                var = self.memory[node.expr.value]
                self.memory[node.expr.value] -= Number('int', 1)
                return var

        return self.visit(node.expr)

    def visit_CompoundStmt(self, node):
        self.memory.new_scope()

        for child in node.children:
            self.visit(child)

        self.memory.del_scope()

    def visit_ReturnStmt(self, node):
        return self.visit(node.expression)

    def visit_Num(self, node):
        
        if node.token.type == INTEGER_CONST:
            return Number(ttype="int", value=node.value)
        elif node.token.type == CHAR_CONST:
            return Number(ttype="char", value=node.value)
        else:
            return Number(ttype="float", value=node.value)

    def visit_Var(self, node):
        return self.memory[node.value]

    def visit_Assign(self, node):
        var_name = node.left.value
        if node.op.type == ADD_ASSIGN:
            self.memory[var_name] += self.visit(node.right)
        elif node.op.type == SUB_ASSIGN:
            self.memory[var_name] -= self.visit(node.right)
        elif node.op.type == MUL_ASSIGN:
            self.memory[var_name] *= self.visit(node.right)
        elif node.op.type == DIV_ASSIGN:
            self.memory[var_name] /= self.visit(node.right)
        else:
            self.memory[var_name] = self.visit(node.right)
        return self.memory[var_name]

    def visit_NoOp(self, node):
        pass
    def visit_List(self,node):
        values_li=[]
        for token in node.values:
            if token.token.type==ID:
                values_li.append(self.visit_Var(token.value))
            elif token.token.type in [INTEGER_CONST,CHAR_CONST,FLOAT,REAL_CONST]:
                
                values_li.append(self.visit_Num(token))
            elif token.token.type == STRING:
                values_li.append(self.visit_String(token))
            elif token.token.type == LIST:
                values_li.append(self.visit_List(token))
        
        return CustomList(values_li)
    def visit_BinOp(self, node):
        if node.op.type == ADD_OP:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == SUB_OP:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL_OP:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV_OP:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MOD_OP:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == LT_OP:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GT_OP:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LE_OP:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GE_OP:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == EQ_OP:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NE_OP:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == LOG_AND_OP:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == LOG_OR_OP:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == AND_OP:
            return self.visit(node.left) & self.visit(node.right)
        elif node.op.type == OR_OP:
            return self.visit(node.left) | self.visit(node.right)
        elif node.op.type == XOR_OP:
            return self.visit(node.left) ^ self.visit(node.right)

    def visit_String(self, node):
        return CustomString(node.value)

    def visit_IfStmt(self, node):
        if self.visit(node.condition):
            self.visit(node.tbody)
        else:
            self.visit(node.fbody)
    def visit_SwitchStmt(self,node):
        
        var = node.condition
        var_value=self.visit(var)
        case_children=node.case_children
        for case in case_children:
            case_exp=self.visit(case.condition)
            if case_exp.value == var_value.value:
                self.visit(case.body)
                return
        if node.default_body != None:
            self.visit(node.default_body)
            
            
        
    # def visit_CaseStmt(self,node):
    #     return self.visit()
    def visit_WhileStmt(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_ForStmt(self, node):
        self.visit(node.setup)
        while self.visit(node.condition):
            self.visit(node.body)
            self.visit(node.increment)

    def interpret(self, tree):
        self.load_libraries(tree)
        self.load_functions(tree)
        self.visit(tree)
        self.memory.new_frame('main')
        try:
            node = self.memory['رئيسية']
        except:
            node = self.memory['main']
        
        res = self.visit(node)
        self.memory.del_frame()
        return res
    def interpret_with_memory(self,tree,var_name="equation"):
        self.load_libraries(tree)
        self.load_functions(tree)
        self.visit(tree)
        self.memory.new_frame('main')
        node = self.memory['main']
        res = self.visit(node)
        memory_scope=self.memory.stack.current_frame.current_scope
        self.memory.del_frame()
        return memory_scope.get(var_name)
    
    def handle_equations(self,equation):
        expression="void main(){{int equation = {};}}".format(equation)
        t=Lexer(expression)
        parser = Parser(t)
        tree = parser.parse()
        # print(tree)
        SemanticAnalyzer.analyze(tree)
        var = self.interpret_with_memory(tree=tree,var_name="equation")
        return var.value
    
    
    @staticmethod
    def run(program):

        try:
            lexer = Lexer(program)
            parser = Parser(lexer)
            tree = parser.parse()
            # get_tree(tree)
            SemanticAnalyzer.analyze(tree)
            # get_tree(tree)
            
            status = Interpreter().interpret(tree)
        except Exception as message:
            print("{}[{}] {} {}".format(
                MessageColor.FAIL,
                type(message).__name__,
                message,
                MessageColor.ENDC
            ))
            status = -1
        print()
        print(MessageColor.OKBLUE + "Process terminated with status {}".format(status) + MessageColor.ENDC)
    
    @staticmethod
    def run_debug(program):

       
            lexer = Lexer(program)
            parser = Parser(lexer)
            tree = parser.parse()
            SemanticAnalyzer.analyze(tree)
            # Interpreter.get_tree(tree)
            
            status = Interpreter().interpret(tree)
        
    @staticmethod
    def run_interactive():
        program_memory="#include <stdio.h>\nvoid main(){"
        status=-1
        while True:
            try:
                program = input(f"{MessageColor.OKGREEN}GOWIN>{MessageColor.ENDC}")
                if program == '':
                    continue
                if program.lower() == 'quit':
                    break
                program_memory=remove_printf(program_memory)
                program_memory+=program
                
                lexer = Lexer(program_memory+"}")
                parser = Parser(lexer)
                tree = parser.parse()
                SemanticAnalyzer.analyze(tree)
                status = Interpreter().interpret(tree)
                print()
                # print(MessageColor.OKBLUE + "Process terminated with status {}".format(status) + MessageColor.ENDC)
            except KeyboardInterrupt:
                print("\nInterrupted by user. Exiting...")
                break
            except Exception as message:
                print("{}[{}] {} {}".format(
                    MessageColor.FAIL,
                    type(message).__name__,
                    message,
                    MessageColor.ENDC
                ))
                program_memory="#include <stdio.h>\nvoid main(){"
                status = -1
        print()
        print(MessageColor.OKBLUE + "Process terminated with status {}".format(status) + MessageColor.ENDC)
        
   
    
        



def remove_printf(code):
    return re.sub(r'printf\([^;]*;\s*', '', code)

def print_children(node, level=0):
    print(' ' * level*2 + 'Node:', type(node).__name__)
    if hasattr(node, 'children'):
        for child in node.children:
            print_children(child, level + 1)
    if hasattr(node, 'body') and hasattr(node.body, 'children'):
        for child in node.body.children:
            print_children(child, level + 1)
            


def get_tree(tree):
    for child in tree.children:
            print_children(child)

def remove_functions(node):
    if hasattr(node, 'children'):
        for child in node.children:
            if isinstance(child, FunctionCall):
                if child.name in ["printf","printarr"]:
                    node.children.remove(child)
            else:
                    remove_functions(child)
                    
    return node