# This is a system that gives functions to print.
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
        self.logs = []

        # Colors and heading messages
        colorama.init(autoreset=True)
        self.FATAL_COLOR = colorama.Fore.WHITE + colorama.Back.RED
        self.FATAL_PREFIX = "[FATAL]: "
        self.ERROR_COLOR = colorama.Fore.RED + colorama.Back.BLACK
        self.ERROR_PREFIX = "[ERROR]: "
        self.WARN_COLOR  = colorama.Fore.YELLOW + colorama.Back.BLACK
        self.WARN_PREFIX = "[WARN] : "
        self.INFO_COLOR  = colorama.Fore.GREEN + colorama.Back.BLACK
        self.INFO_PREFIX = "[INFO] : "
        self.DEBUG_COLOR = colorama.Fore.BLUE + colorama.Back.BLACK
        self.DEBUG_PREFIX = "[DEBUG]: "
        self.TRACE_COLOR = colorama.Fore.WHITE + colorama.Back.BLACK
        self.TRACE_PREFIX = "[TRACE]: "

        self.info("Console initialized.")

    def quit(self):
        """Quit the console"""

        self.info("Console quit.")

        # Create logs
        with open("output/logs.log", "w") as f:
            f.write("\n".join(self.logs))
        
        colorama.deinit()

    # Logs functions
    def fatal(self, msg):
        if self.log_active["fatal"] == True:
            print(self.FATAL_COLOR + self.FATAL_PREFIX + str(msg))
            self.logs.append(self.FATAL_PREFIX + str(msg))
    def error(self, msg):
        if self.log_active["error"] == True:
            print(self.ERROR_COLOR + self.ERROR_PREFIX + str(msg))
            self.logs.append(self.ERROR_PREFIX + str(msg))
    def warn(self, msg):
        if self.log_active["warn"] == True:
            print(self.WARN_COLOR + self.WARN_PREFIX + str(msg))
            self.logs.append(self.WARN_PREFIX + str(msg))
    def info(self, msg):
        if self.log_active["info"] == True:
            print(self.INFO_COLOR + self.INFO_PREFIX + str(msg))
            self.logs.append(self.INFO_PREFIX + str(msg))
    def debug(self, msg):
        if self.log_active["debug"] == True:
            print(self.DEBUG_COLOR + self.DEBUG_PREFIX + str(msg))
            self.logs.append(self.DEBUG_PREFIX + str(msg))
    def trace(self, msg):
        if self.log_active["trace"] == True:
            print(self.TRACE_COLOR + self.TRACE_PREFIX + str(msg))
            self.logs.append(self.TRACE_PREFIX + str(msg))

# Set the console object
console = consoleHandler("assets/storage/options.json")