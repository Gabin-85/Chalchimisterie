from utils.time import date
from args import pathLocation, fileExtension, asciiColorFormat, consoleLevel

class logger():

    filepath:str = None
    
    @staticmethod
    def select(filename:str):
        """
        Select the log file and clear it
        
        Args:
            filename (str): The name of the file
        """
        try:
            open(f"{pathLocation.bin}{filename}{fileExtension.log}", "w").write("")
            logger.filepath = f"{pathLocation.bin}{filename}{fileExtension.log}"
            console.info(f"Log file '{filename}{fileExtension.log}' selected")
        except FileNotFoundError:
            console.error(f"The logging directory is invalid. Logger is disabled.")

    @staticmethod
    def add(msg:str) -> bool:
        """
        Add a line to the logs

        Args:
            msg (str): The message to add

        Return:
            bool : True if the log was added, False otherwise
        """
        if not logger.filepath:
            return False
        open(logger.filepath, "a").write(f"({date.get_time()}) {msg}\n")
        return True

class console():

    @staticmethod
    def exception(msg):
        """
        Print an EXCEPTION message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.exception == False: return
        print(f"{asciiColorFormat.purple}{asciiColorFormat.bold}[EXCEPT]: {asciiColorFormat.italic}{msg}{asciiColorFormat.clear}")
        logger.add(f"[EXCEPT]: {msg}")

    @staticmethod
    def fatal(msg):
        """
        Print a FATAL message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.fatal == False: return
        print(f"{asciiColorFormat.red}{asciiColorFormat.inverted}{asciiColorFormat.bold}[FATAL]: {msg}{asciiColorFormat.clear}")
        logger.add(f"[FATAL]: {msg}")

    @staticmethod
    def error(msg):
        """
        Print an ERROR message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.error == False: return
        print(f"{asciiColorFormat.red}{asciiColorFormat.bold}[ERROR]: {msg}{asciiColorFormat.clear}")
        logger.add(f"[ERROR]: {msg}")

    @staticmethod
    def warn(msg):
        """
        Print a WARN message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.warn == False: return
        print(f"{asciiColorFormat.yellow}[WARN] : {msg}{asciiColorFormat.clear}")
        logger.add(f"[WARN] : {msg}")

    @staticmethod
    def info(msg):
        """
        Print an INFO message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.info == False: return
        print(f"{asciiColorFormat.green}[INFO] : {msg}{asciiColorFormat.clear}")
        logger.add(f"[INFO] : {msg}")
    
    @staticmethod
    def debug(msg):
        """
        Print a DEBUG message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.debug == False: return
        print(f"{asciiColorFormat.blue}[DEBUG]: {msg}{asciiColorFormat.clear}")
        logger.add(f"[DEBUG]: {msg}")

    @staticmethod
    def trace(msg):
        """
        Print a TRACE message.

        Args:
            msg (str): The message to print
        """
        if consoleLevel.trace == False: return
        print(f"{asciiColorFormat.white}[TRACE]: {asciiColorFormat.italic}{msg}{asciiColorFormat.clear}")
        logger.add(f"[TRACE]: {msg}")