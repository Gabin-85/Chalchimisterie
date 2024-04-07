# This is a tool box that gives functions to print.
# It has 6 levels (FATAL, ERROR, WARN, INFO, DEBUG and TRACE) of log/print handling.
import colorama
import json

class consoleHandler:

    def __init__(self):
        global log_active
        log_active = json.load(open("storage/options.json"))["log_active"]
        colorama.init(autoreset=True)

    def quit():
        colorama.deinit()
        
class log_level:
    # Colors and heading messages
    FATAL = colorama.Fore.WHITE + colorama.Back.RED + "[FATAL]: "
    ERROR = colorama.Fore.RED + colorama.Back.BLACK + "[ERROR]: "
    WARN  = colorama.Fore.YELLOW + colorama.Back.BLACK + "[WARN] : "
    INFO  = colorama.Fore.BLUE + colorama.Back.BLACK + "[INFO] : "
    DEBUG = colorama.Fore.GREEN + colorama.Back.BLACK + "[DEBUG]: "
    TRACE = colorama.Fore.WHITE + colorama.Back.BLACK + "[TRACE]: "


# Logs functions
def fatal(msg):
    if log_active["fatal"] == True:
        print(log_level.FATAL + str(msg))
def error(msg):
    if log_active["error"] == True:
        print(log_level.ERROR + str(msg))
def warn(msg):
    if log_active["warn"] == True:
        print(log_level.WARN + str(msg))
def info(msg):
    if log_active["info"] == True:
        print(log_level.INFO + str(msg))
def debug(msg):
    if log_active["debug"] == True:
        print(log_level.DEBUG + str(msg))
def trace(msg):
    if log_active["trace"] == True:
        print(log_level.TRACE + str(msg))