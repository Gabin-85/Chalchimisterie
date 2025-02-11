class category:
    not_found:int = 0
    already_done:int = 1
    unsupported:int = 2
    pygame_uninitialize:int = 3

class Error:

    def __init__(self, type:category, msg:str=""):
        self.type:str = type
        self.msg:str = msg

    def __str__(self):
        return self.msg
    
    def __eq__(self, value):
        return self.type == value
    
def is_error(*variables) -> bool:
    for variable in variables:
        if type(variable) == Error:
            return True
        if type(variable) == list:
            for element in variable:
                if type(element) == Error:
                    return True
    return False