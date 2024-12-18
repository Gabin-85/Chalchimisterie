from utils.time import date
from args import path, ext, formating, consoleLevel

class logger():

    filepath:str = None
    
    @staticmethod
    def select(filename:str) -> None:
        """
        Select the log file and clear it
        
        Args:
            filename (str): The name of the log file (in bin/)
        """
        try:
            open(f"{path.bin}{filename}{ext.log}", "w").write("")
            logger.filepath = f"{path.bin}{filename}{ext.log}"
            console.info(f"Log file '{filename}{ext.log}' selected")
        except FileNotFoundError:
            console.error(f"The logging directory is invalid. Logger is disabled.")

    @staticmethod
    def add(msg) -> None:
        """
        Add a line to the log file

        Args:
            msg (any): The message
        """
        if not logger.filepath:
            return
        open(logger.filepath, "a").write(f"({"{}:{}:{}:{}".format(*date.get_time())}) {msg}\n")

class console():

    @staticmethod
    def fatal(msg) -> None:
        """
        Print a FATAL message.

        Args:
            msg (any): The message
        """
        if consoleLevel.fatal == False:
            return
        print(f"{formating.red}{formating.inverted}{formating.bold}[FATAL]: {msg}{formating.clear}")
        logger.add(f"[FATAL]: {msg}")

    @staticmethod
    def error(msg) -> None:
        """
        Print an ERROR message.

        Args:
            msg (any): The message
        """
        if consoleLevel.error == False:
            return
        print(f"{formating.red}{formating.bold}[ERROR]: {msg}{formating.clear}")
        logger.add(f"[ERROR]: {msg}")

    @staticmethod
    def warn(msg) -> None:
        """
        Print a WARN message.

        Args:
            msg (any): The message
        """
        if consoleLevel.warn == False:
            return
        print(f"{formating.yellow}[WARN] : {msg}{formating.clear}")
        logger.add(f"[WARN] : {msg}")

    @staticmethod
    def info(msg) -> None:
        """
        Print an INFO message.

        Args:
            msg (any): The message
        """
        if consoleLevel.info == False:
            return
        print(f"{formating.green}[INFO] : {msg}{formating.clear}")
        logger.add(f"[INFO] : {msg}")
    
    @staticmethod
    def debug(msg) -> None:
        """
        Print a DEBUG message.

        Args:
            msg (any): The message
        """
        if consoleLevel.debug == False:
            return
        print(f"{formating.blue}[DEBUG]: {msg}{formating.clear}")
        logger.add(f"[DEBUG]: {msg}")

    @staticmethod
    def trace(msg) -> None:
        """
        Print a TRACE message.

        Args:
            msg (any): The message
        """
        if consoleLevel.trace == False:
            return
        print(f"{formating.white}[TRACE]: {formating.italic}{msg}{formating.clear}")
        logger.add(f"[TRACE]: {msg}")