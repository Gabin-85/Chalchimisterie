# This is a log system that is used in the game.
# DO NOT used all functions in this file before logs_init().
#
# It has 6 levels (FATAL, ERROR, WARN, INFO, DEBUG and TRACE) of log/print handling.
# You can active or unactive various functions by initializing the logs.
import colorama
log_active = {}
logs = ""

colorama.init(autoreset=True)
class log_level:
    # Colors and heading messages
    FATAL = colorama.Fore.WHITE + colorama.Back.RED + "[FATAL]: "
    ERROR = colorama.Fore.RED + colorama.Back.BLACK + "[ERROR]: "
    WARN  = colorama.Fore.YELLOW + colorama.Back.BLACK + "[WARN] : "
    INFO  = colorama.Fore.BLUE + colorama.Back.BLACK + "[INFO] : "
    DEBUG = colorama.Fore.GREEN + colorama.Back.BLACK + "[DEBUG]: "
    TRACE = colorama.Fore.WHITE + colorama.Back.BLACK + "[TRACE]: "


# Logs functions
def FATAL(msg):
    if log_active["fatal"] == True:
        print(log_level.FATAL + str(msg))
def ERROR(msg):
    if log_active["error"] == True:
        print(log_level.ERROR + str(msg))
def WARN(msg):
    if log_active["warn"] == True:
        print(log_level.WARN + str(msg))
def INFO(msg):
    if log_active["info"] == True:
        print(log_level.INFO + str(msg))
def DEBUG(msg):
    if log_active["debug"] == True:
        print(log_level.DEBUG + str(msg))
def TRACE(msg):
    if log_active["trace"] == True:
        print(log_level.TRACE + str(msg))

def logs_init(active:dict):
    global log_active
    log_active = active
    INFO("Logs initialized")