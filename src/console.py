from file import ext
from datetime import datetime

class formating:
    purple:str = "\u001b[35m"
    red:str = "\u001b[31m"
    yellow:str = "\u001b[33m"
    green:str = "\u001b[32m"
    blue:str = "\u001b[34m"
    white:str = "\u001b[37m"
    inverted:str = "\033[7m"
    italic:str = "\033[3m"
    bold:str = "\033[1m"
    clear:str = "\u001b[0m"
    
enabledLevel:set = {
    "fatal",
    "error",
    "warn",
    "info",
    "debug",
    "trace",
}

broadcast_logfiles = []
logfiles = []

def add_logfile(filepath:str, broadcast:bool=False) -> None:
    try:
        with open(f"{filepath}{ext.log}", "w") as file:
            file.write("")
        
        if broadcast == True:
            broadcast_logfiles.append(open(f"{filepath}{ext.log}", "a"))
        else:
            logfiles.append(open(f"{filepath}{ext.log}", "a"))
        trace(f"Log file '{filepath}{ext.log}' selected.")
    except FileNotFoundError:
        error(f"Directory doesn't exist. Logger is disabled.")

def print_logfile(level:str, msg:str, logfiles:list[str]) -> None:
    if level not in enabledLevel:
        return
    
    for logfile in logfiles:
        logfile.write(f"({datetime.now().strftime('%H:%M:%S.%f')[:-3]}) [{level.upper()}]: {msg}\n")

def print_console(level:str, msg:str, formatings:list[formating]) -> None:
    if level not in enabledLevel:
        return
    
    print(f"{''.join(form for form in formatings)}[{level.upper()}]: {msg}{formating.clear}")

def fatal(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("fatal", msg, [formating.red,formating.inverted,formating.bold])
    print_logfile("fatal", msg, logfiles)

def error(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("error", msg, [formating.red,formating.bold])
    print_logfile("error", msg, logfiles)

def warn(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("warn", msg, [formating.yellow])
    print_logfile("warn", msg, logfiles)

def info(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("info", msg, [formating.green])
    print_logfile("info", msg, logfiles)

def debug(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("debug", msg, [formating.blue])
    print_logfile("debug", msg, logfiles)

def trace(msg:str, logfiles=broadcast_logfiles) -> None:
    print_console("trace", msg, [formating.white, formating.italic])
    print_logfile("trace", msg, logfiles)