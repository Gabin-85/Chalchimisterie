from datetime import datetime

class date:
    
    @staticmethod
    def get_date() -> tuple[int]:
        """
        Get the current date

        Return:
            tuple[int] : The current date DD MM YYYY
        """
        return datetime.now().day, datetime.now().month, datetime.now().year
    
    @staticmethod
    def get_time() -> tuple[int]:
        """
        Get the current date
        
        Return:
            tuple[int] : The current formatted hour HH MM SS MS
        """
        return datetime.now().hour, datetime.now().minute, datetime.now().second, datetime.now().microsecond
    
    @staticmethod
    def get_epoch() -> float:
        """
        Get the current date

        Return:
            float : The current epoch time (in seconds)
        """
        return datetime.now().timestamp()

class clock:

    time_shift:int = int(datetime.now().timestamp() * 1000000)

    @staticmethod
    def get_mics() -> int:
        """
        Get the clock time

        Return:
            int : The clock time in microseconds (µs)
        """
        return int(datetime.now().timestamp() * 1000000) - clock.time_shift
    
    @staticmethod
    def get_ms() -> int:
        """
        Get the clock time

        Return:
            int : The clock time in milliseconds (ms)
        """
        return int(datetime.now().timestamp() * 1000) - clock.time_shift // 1000

    @staticmethod
    def get_sec() -> int:
        """
        Get the clock time

        Return:
            int : The clock time in seconds (s)
        """
        return int(datetime.now().timestamp()) - clock.time_shift // 1000000

class Chrono:

    def __init__(self, unit:str = "mics"):
        """
        Create a chronometer

        Args:
            unit (str): The unit of the time ( s | ms | mics )
        """
        self.is_running =  True 
        self.startup = int(datetime.now().timestamp() * 1000000)
        self.elapsed = 0
        self.removed = 0
        match unit:
            case "s":
                self.unit_multiplier = 1000000
            case "ms":
                self.unit_multiplier = 1000
            case _:
                self.unit_multiplier = 1

    def update(self):
        """
        Update the chronometer
        """
        if not self.is_running:
            self.start()
            self.stop()
        self.elapsed = int(datetime.now().timestamp() * 1000000) - self.startup - self.removed

    def get_elapsed(self) -> int:
        """
        Get the current elapsed time

        Return:
            int : The elapsed time
        """
        self.update()
        return self.elapsed // self.unit_multiplier
    
    def get_removed(self) -> int:
        """
        Get the current removed time

        Return:
            int : The removed time
        """
        self.update()
        return self.removed // self.unit_multiplier
            
    
    def start(self):
        """
        Start/resume the chronometer
        """
        if not self.is_running:
            self.is_running = True
            old_elapsed = self.elapsed
            self.update()
            self.removed += self.elapsed - old_elapsed

    def stop(self):
        """
        Stop the chronometer
        """
        if self.is_running:
            self.is_running = False
    
class Timer:

    def __init__(self, timing:int, unit:str = "mics"):
        """
        Setting up the timer with the right unit ( s | ms | mics )

        Args:
            timing (int): The targeted time
            unit (str): The unit of the time ( s | ms | mics )
        """
        self.is_running = True
        self.startup = int(datetime.now().timestamp() * 1000000)
        self.elapsed = 0
        self.removed = 0
        match unit:
            case "s":
                self.multiplier = 1000000
            case "ms":
                self.multiplier = 1000
            case _:
                self.multiplier = 1
        self.target = timing * self.multiplier

    def update(self) -> int:
        """
        Update the timer if it's running.

        Return:
            int : The remaining time
        """
        if not self.is_running:
            self.start()
            self.stop()
        self.elapsed = int(datetime.now().timestamp() * 1000000) - self.startup - self.removed

    def get_elapsed(self) -> int:
        """
        Get the current elapsed time
        """
        self.update()
        return self.elapsed // self.multiplier
    
    def get_removed(self) -> int:
        """
        Get the current removed time
        """
        self.update()
        return self.removed // self.multiplier
    
    def get_remaining(self) -> int:
        """
        Get the current remaining time
        
        Return:
            int : The remaining time
        """
        self.update()
        return (self.target - self.elapsed) // self.multiplier
    
    def check(self) -> bool:
        """
        Check if the timer is finished

        Return:
            bool : True if the timer is finished, False otherwise
        """
        self.update()
        return self.target < self.elapsed

    def start(self):
        """
        Start/resume the timer
        """
        self.is_running = True
        old_elapsed = self.elapsed
        self.update()
        self.removed += self.elapsed - old_elapsed

    def stop(self):
        """
        Stop the timer
        """
        self.is_running = False
    
def wait(time:int, unit:str = "mics"):
    """
    Make the program wait for a certain amount of time

    Args:
        time (int): The time to wait
        unit (str): The unit of the time ( s | ms | mics )
    """
    timer = Timer(time, unit)
    while timer.check() == False:
        pass