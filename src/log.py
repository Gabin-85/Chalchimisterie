import printer

cache:str = ""
printback:bool = True

def set_file(path:str):
    global file
    with open(path, "w") as file:
        file.write("--File Created--\n")
    file = open(path, "a")

def add(msg:str)->None:
    global cache
    if printback and __debug__:
        print(msg)
    cache += msg + "\n"

def flush():
    global cache, file
    if cache == "":
        return
    file.write(cache)
    cache = ""

def error(msg): add(printer.color.red+printer.format.bold+msg+printer.format.clear)
def warn(msg): add(printer.color.yellow+msg+printer.format.clear)
def info(msg): add(printer.color.green+msg+printer.format.clear)