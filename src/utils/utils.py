from functools import wraps
import pickle
import importlib
import types
def import_module(libname):
    """ Function import module using string representation """

    return importlib.import_module(libname)

def copy_function(fn, new_name):
    """
    Returns a copy of the function with a new name.
    """
    new_fn = types.FunctionType(fn.__code__, fn.__globals__, new_name, fn.__defaults__, fn.__closure__)
    new_fn.return_type = getattr(fn, 'return_type', None)
    new_fn.arg_types = getattr(fn, 'arg_types', [])
    return new_fn
def get_functions(module):
    """ Function returns all functions defined in some module """
    lib = import_module(module)
    
    for func_name in dir(lib):
        func = getattr(lib, func_name)
        if callable(func) and not func_name.startswith('__') and func.__module__.endswith(module):
            if func_name=="printf":
                new_function = copy_function(func, "اطبع")
                yield new_function

            yield func

def restorable(fn):
    """ Decorator reset object state after calling function """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        state = pickle.dumps(self.__dict__)
        result = fn(self, *args, **kwargs)
        self.__dict__ = pickle.loads(state)
        return result
    return wrapper


def definition(return_type=None, arg_types=[]):
    """ Decorator used for definition of builtin function """
    def wrapper_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.return_type = return_type
        wrapper.arg_types = arg_types
        return wrapper
    return wrapper_decorator


def get_name(name):
    """ Calculate name using nex sequence value"""
    if name[-2:].isdigit():
        return '{}{:02d}'.format(
            name[:-2],
            int(name[-2:]) + 1
        )
    else:
        return '{}{:02d}'.format(
            name,
            1
        )


class MessageColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'






