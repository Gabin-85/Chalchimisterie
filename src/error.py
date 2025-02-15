class group:
    not_found:int = 0
    already_done:int = 1
    unsupported:int = 2
    unespected_state:int = 3
    pygame_uninitialize:int = 4

class Error:

    def __init__(self, group:group, msg:str=""):
        self.group:str = group
        self.msg:str = msg

    def __eq__(self, value):
        return self.group == value
    
    def __str__(self):
        return self.msg
    
def is_error(variable) -> bool:
    if type(variable) == Error:
        return True
    return False

def is_group(variable, group:group) -> bool:
    if is_error(variable) and variable == group:
        return True
    return False