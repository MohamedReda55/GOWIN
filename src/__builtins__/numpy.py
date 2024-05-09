from ..utils.utils import definition
from ..interpreter.number import Number
from ..interpreter.list import CustomList

@definition(return_type='list', arg_types=None)
def multiplyarr(arr1,arr2):
    # fmt, *params = args
    
   
    # message = ', '.join([element.get() for element in array.value])
    # print(arr1,arr2)
    arr1=[element.get() for element in arr1]
    arr2=[element.get() for element in arr2]
    
    result=CustomList(value=[])
    if len(arr1)!=len(arr2) :
        
        return result
    else:
        for i in range(len(arr1)):
                result.append(Number('int',arr1[i]*arr2[i]))
                
    return result
                
        

@definition(return_type='int', arg_types=None)
def sumarr(arr):
    # fmt, *params = args
    
   
    # message = ', '.join([element.get() for element in array.value])
    array_int=[element.get() for element in arr]
    result = sum(array_int)
    # print(message)
    return result