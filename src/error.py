class Err:
    
    def __init__(self, type:str, msg:str, helper:str=None):
        self.type = type
        self.msg = msg
        self.helper = helper

    def __eq__(self, value:str):
        return self.type == value
    
    def __repr__(self):
        if self.helper:
            return  f"ErrorType(type={self.type!r}, msg={self.msg!r}, [+HELPER])"
        return  f"ErrorType(type={self.type!r}, msg={self.msg!r})"

    def __str__(self):
        if self.helper:
            return f"Error {self.type} <- {self.msg}\n{self.helper}"
        return f"Error {self.type} <- {self.msg}"