class pathLocation:
    bin:str = "../bin/"
    tilemap_image:str = "../resources/tilemap_image/"
    tilemap_config:str = "../resources/tilemap_config/"
    layer_image:str = "../resources/layer_image/"
    layer_config:str = "../resources/layer_config/"
    level_config:str = "../resources/level_config/"

class fileExtension:
    data:str = ".json"
    text:str = ".txt"
    image:str = ".png"
    log:str = ".log"

class asciiColorFormat:
    purple = "\u001b[35m"
    red = "\u001b[31m"
    yellow = "\u001b[33m"
    green = "\u001b[32m"
    blue = "\u001b[34m"
    white = "\u001b[37m"
    inverted = "\033[7m"
    italic = "\033[3m"
    bold = "\033[1m"
    clear = "\u001b[0m"

class consoleLevel:
    exception:bool = True
    fatal:bool     = True
    error:bool     = True
    warn:bool      = True
    info:bool      = True
    debug:bool     = True
    trace:bool     = True