# This is a system that gives functions to print.
# It has 6 levels (FATAL, ERROR, WARN, INFO, DEBUG and TRACE) of log/print handling.
from utils.timeToolbox import date
import colorama
import os
import json

# Fast functions (function that use the console class to be used elsewere)
def fatal(msg): console.fatal(msg)
def error(msg): console.error(msg)
def warn(msg):  console.warn(msg)
def info(msg):  console.info(msg)
def debug(msg): console.debug(msg)
def trace(msg): console.trace(msg)

class consoleHandler:

    def __init__(self):
        """Init the console system"""

        self.log_option = json.load(open("assets/storage/options.json"))["log_option"]
        # Activate or not live functions
        self.live_active = self.log_option["live_active"]
        self.log_active = self.log_option["log_active"]
        # Set or not the colors
        self.live_colors = self.log_option["colors"]
        # Create or not the prefix
        self.live_prefix = self.log_option["live_prefix"]
        self.log_prefix = self.log_option["log_prefix"]
        # Create or not the time
        self.live_time = self.log_option["live_time"]
        self.log_time = self.log_option["log_time"]
        self.logs = []

        # Colors and heading messages
        colorama.init(autoreset=True)
        if self.live_colors:
            self.FATAL_COLOR = colorama.Fore.WHITE + colorama.Back.RED
            self.ERROR_COLOR = colorama.Fore.RED + colorama.Back.BLACK
            self.WARN_COLOR  = colorama.Fore.YELLOW + colorama.Back.BLACK
            self.INFO_COLOR  = colorama.Fore.GREEN + colorama.Back.BLACK
            self.DEBUG_COLOR = colorama.Fore.BLUE + colorama.Back.BLACK
            self.TRACE_COLOR = colorama.Fore.WHITE + colorama.Back.BLACK
        else:
            self.FATAL_COLOR = ""
            self.ERROR_COLOR = ""
            self.WARN_COLOR  = ""
            self.INFO_COLOR  = ""
            self.DEBUG_COLOR = ""
            self.TRACE_COLOR = ""

        if self.live_prefix:
            self.FATAL_LIVE_PREFIX = "[FATAL]: "
            self.ERROR_LIVE_PREFIX = "[ERROR]: "
            self.WARN_LIVE_PREFIX = "[WARN] : "
            self.INFO_LIVE_PREFIX = "[INFO] : "
            self.DEBUG_LIVE_PREFIX = "[DEBUG]: "
            self.TRACE_LIVE_PREFIX = "[TRACE]: "
        else:
            self.FATAL_LIVE_PREFIX = ""
            self.ERROR_LIVE_PREFIX = ""
            self.WARN_LIVE_PREFIX = ""
            self.INFO_LIVE_PREFIX = ""
            self.DEBUG_LIVE_PREFIX = ""
            self.TRACE_LIVE_PREFIX = ""

        if self.log_prefix:
            self.FATAL_LOG_PREFIX = "[FATAL]: "
            self.ERROR_LOG_PREFIX = "[ERROR]: "
            self.WARN_LOG_PREFIX = "[WARN] : "
            self.INFO_LOG_PREFIX = "[INFO] : "
            self.DEBUG_LOG_PREFIX = "[DEBUG]: "
            self.TRACE_LOG_PREFIX = "[TRACE]: "
        else:
            self.FATAL_LOG_PREFIX = ""
            self.ERROR_LOG_PREFIX = ""
            self.WARN_LOG_PREFIX = ""
            self.INFO_LOG_PREFIX = ""
            self.DEBUG_LOG_PREFIX = ""
            self.TRACE_LOG_PREFIX = ""


        self.info("Console system initialized.")

    def quit(self):
        """Quit the console system"""

        self.info("Console system quit.")
        # Create logs
        with open("logs.log", "w") as f:
            f.write("\n".join(self.logs))
        
        colorama.deinit()

    # Logs functions
    def fatal(self, msg):
        if self.live_active["fatal"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.FATAL_LIVE_PREFIX + str(msg))
            else:
                print(self.FATAL_COLOR + self.FATAL_LIVE_PREFIX + str(msg))
        if self.log_active["fatal"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.FATAL_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.FATAL_LOG_PREFIX + str(msg))
            
    def error(self, msg):
        if self.live_active["error"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.ERROR_LIVE_PREFIX + str(msg))
            else:
                print(self.ERROR_COLOR + self.ERROR_LIVE_PREFIX + str(msg))
        if self.log_active["error"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.ERROR_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.ERROR_LOG_PREFIX + str(msg))
            
    def warn(self, msg):
        if self.live_active["warn"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.WARN_LIVE_PREFIX + str(msg))
            else:
                print(self.WARN_COLOR + self.WARN_LIVE_PREFIX + str(msg))
        if self.log_active["warn"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.WARN_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.WARN_LOG_PREFIX + str(msg))
            
    def info(self, msg):
        if self.live_active["info"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.INFO_LIVE_PREFIX + str(msg))
            else:
                print(self.INFO_COLOR + self.INFO_LIVE_PREFIX + str(msg))
        if self.log_active["info"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.INFO_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.INFO_LOG_PREFIX + str(msg))

    def debug(self, msg):
        if self.live_active["debug"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.DEBUG_LIVE_PREFIX + str(msg))
            else:
                print(self.DEBUG_COLOR + self.DEBUG_LIVE_PREFIX + str(msg))
        if self.log_active["debug"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.DEBUG_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.DEBUG_LOG_PREFIX + str(msg))

    def trace(self, msg):
        if self.live_active["trace"]:
            if self.live_time:
                print("("+date.get_formated_time()+") "+self.TRACE_LIVE_PREFIX + str(msg))
            else:
                print(self.TRACE_COLOR + self.TRACE_LIVE_PREFIX + str(msg))
        if self.log_active["trace"]:
            if self.log_time:
                self.logs.append("("+date.get_formated_time()+") "+self.TRACE_LOG_PREFIX + str(msg))
            else:
                self.logs.append(self.TRACE_LOG_PREFIX + str(msg))

# Set the console object
console = consoleHandler()