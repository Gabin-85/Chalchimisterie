class path:
    bin:str = "../bin/"
    test:str = "../test/"
    tilemap:str = "../resources/tilemaps/"
    background:str = "../resources/backgrounds/"

class ext:
    data:str = ".json"
    text:str = ".txt"
    image:str = ".png"
    log:str = ".log"

class formating:
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

consoleLevel:set = {
    "fatal",
    "error",
    "warn",
    "info",
    "debug",
    "trace",
}