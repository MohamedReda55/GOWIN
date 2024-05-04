"""
This module file supports basic functions from stdio.h library
"""

from ..utils.utils import definition
from ..interpreter.number import Number
from ..interpreter.list import CustomList


@definition(return_type='int', arg_types=None)
def printf(*args):
    """ basic printf function
    example:
        printf("%d %d", 1, 2);
    """
    fmt, *params = args
    param_list=[]
    for param in params:
        if type(param) ==CustomList:
            param_list.extend(param)
            continue
        param_list.append(param)

    message = fmt % tuple([param.value for param in param_list])
    result = len(message)
    
    print(message, end='')
    return result

@definition(return_type='int', arg_types=None)
def printarr(*args):
    # fmt, *params = args
    array,*params=args
   
    # message = ', '.join([element.get() for element in array.value])
    message=[element.get() for element in array]
    result = len(message)
    print(message)
    return result


@definition(return_type='int', arg_types=None)
def printstring(*args):
    array,*params=args
    
    message = ''.join(element.replace("'","") for element in array)
    result = len(message)
    print(message)
    return result
@definition(return_type='int', arg_types=None)
def scanf(*args):
    """ basic printf function
        example:
            scanf("%d %d", 'a', 'b');
        """

    import re
    def cast(flag):
        if flag[-1] == 'd':
            return 'int'
        raise Exception('You are not allowed to use \'{}\' other type'.format(flag))

    fmt, *params, memory = args
    fmt = re.sub(r'\s+', '', fmt)
    all_flags = re.findall('%[^%]*[dfi]', fmt)
    if len(all_flags) != len(params):
        raise Exception('Format of scanf function takes {} positional arguments but {} were given'.format(
            len(all_flags),
            len(params)
        ))
    elements = []
    while len(elements) < len(all_flags):
        str = input()
        elements.extend(str.split())
    for flag, param, val in zip(all_flags, params, elements):
        memory[param] = Number(cast(flag), val)

    return len(elements)

@definition(return_type='str', arg_types=None)
def openfile(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return ''

@definition(return_type='char', arg_types=[])
def getchar():
    import sys
    return ord(sys.stdin.read(1))


