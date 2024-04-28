# This is a file that gives functions to print.
# It has 6 levels (FATAL, ERROR, WARN, INFO, DEBUG and TRACE) of log/print handling.
import colorama
import json

# Fast functions (function that use the console class to be used elsewere)
def fatal(msg): console.fatal(msg)
def error(msg): console.error(msg)
def warn(msg):  console.warn(msg)
def info(msg):  console.info(msg)
def debug(msg): console.debug(msg)
def trace(msg): console.trace(msg)

class consoleHandler:

    def __init__(self, parameter_file_path):
        """Init the console"""

        # Set the option file to the log_active variable in the parameter.
        self.log_active = json.load(open(parameter_file_path))["log_active"]

        # Colors and heading messages
        colorama.init(autoreset=True)
        self.FATAL = colorama.Fore.WHITE + colorama.Back.RED + "[FATAL]: "
        self.ERROR = colorama.Fore.RED + colorama.Back.BLACK + "[ERROR]: "
        self.WARN  = colorama.Fore.YELLOW + colorama.Back.BLACK + "[WARN] : "
        self.INFO  = colorama.Fore.BLUE + colorama.Back.BLACK + "[INFO] : "
        self.DEBUG = colorama.Fore.GREEN + colorama.Back.BLACK + "[DEBUG]: "
        self.TRACE = colorama.Fore.WHITE + colorama.Back.BLACK + "[TRACE]: "

        self.info("Console initialized.")

    def quit(self):
        """Quit the console"""
        self.info("Console quit.")
        colorama.deinit()

    # Logs functions
    def fatal(self, msg):
        if self.log_active["fatal"] == True:
            print(self.FATAL + str(msg))
    def error(self, msg):
        if self.log_active["error"] == True:
            print(self.ERROR + str(msg))
    def warn(self, msg):
        if self.log_active["warn"] == True:
            print(self.WARN + str(msg))
    def info(self, msg):
        if self.log_active["info"] == True:
            print(self.INFO + str(msg))
    def debug(self, msg):
        if self.log_active["debug"] == True:
            print(self.DEBUG + str(msg))
    def trace(self, msg):
        if self.log_active["trace"] == True:
            print(self.TRACE + str(msg))

# Set the console object
console = consoleHandler("assets/storage/options.json")