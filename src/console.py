from datetime import datetime
import file, error

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
    "fault",
    "warn",
    "info",
    "debug",
    "trace",
}

default_logfiles = []
logfiles = []

def add_logfile(filepath:str, default:bool=True) -> None:
    file.create(f"{filepath}{file.ext.log}", "-- Logfile created --\n")    
    if default == True:
        default_logfiles.append(f"{filepath}{file.ext.log}")
    else:
        logfiles.append(f"{filepath}{file.ext.log}")

def dump_logfile(filepath:str) -> None|error.Error:
    if file.write(filepath) == error.group.not_found:
        return error.Error(error.group.not_found, f"The logfile '{filepath}' was not added through add_logfile()")

def dump_all_logfiles() -> None:
    for logfile in logfiles+default_logfiles:
        if error.is_error(dump_logfile(logfile)):
            fault(f"The logfile '{logfile}' was unable to be written")


def print_logfile(level:str, msg:str, logfiles:list) -> None:
    if level not in enabledLevel:
        return
    for logfile in logfiles:
        file.files[logfile] += f"({datetime.now().strftime('%H:%M:%S.%f')[:-3]}) [{level.upper()}]: {msg}\n"

def print_console(level:str, msg:str, formatings:list[formating]) -> None:
    if level not in enabledLevel:
        return
    print(f"{''.join(form for form in formatings)}[{level.upper()}]: {msg}{formating.clear}")


def fatal(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("fatal", msg, logfiles)
        return
    print_console("fatal", msg, [formating.red,formating.inverted,formating.bold])
    print_logfile("fatal", msg, default_logfiles)

def fault(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("fault", msg, logfiles)
        return
    print_console("fault", msg, [formating.red,formating.bold])
    print_logfile("fault", msg, default_logfiles)

def warn(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("warn", msg, logfiles)
        return
    print_console("warn", msg, [formating.yellow])
    print_logfile("warn", msg, default_logfiles)

def info(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("info", msg, logfiles)
        return
    print_console("info", msg, [formating.green])
    print_logfile("info", msg, default_logfiles)

def debug(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("debug", msg, logfiles)
        return
    print_console("debug", msg, [formating.blue])
    print_logfile("debug", msg, default_logfiles)

def trace(msg:str, logfiles:list=None) -> None:
    if logfiles != None:
        print_logfile("trace", msg, logfiles)
        return
    print_console("trace", msg, [formating.white, formating.italic])
    print_logfile("trace", msg, default_logfiles)