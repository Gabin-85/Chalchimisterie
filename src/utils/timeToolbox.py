# Time handler
# It's a tool box that gives functions to manage time, chronometer, timer and clock.
from datetime import datetime
from time import sleep

class Date:

    def __init__(self):
        # Setting up the date
        self.update()

    def update(self):
        """
        Update the date.
        """
        self.updated_date = datetime.now()
    
    def get_date(self):
        """
        Get the current date (datetime format).
        """
        self.update()
        return self.updated_date
    
    def get_unix(self):
        """
        Get the current unix timestamp.        
        """
        self.update()
        return int(self.updated_date.timestamp()*1000000)
    
    def get_formated_time(self):
        """
        Get the current time (str format) in the format "HH:MM:SS:MS".
        """
        self.update()
        return self.updated_date.strftime("%H:%M:%S:%f")
    
    def __type__(self):
        return "Date"

class Clock:

    def __init__(self, start_time:int = None, start_time_type:str = "ms"):
        # Setting up the clock
        self.update()
        if start_time == None:
            self.start_time = 0
        else:
            match start_time_type:
                case "s":
                    self.start_time = int(self.updated_date.timestamp() * 1000000 - start_time * 1000000)
                case "ms":
                    self.start_time = int(self.updated_date.timestamp() * 1000000 - start_time * 1000)
                case "unix":
                    self.start_time = int(self.updated_date.timestamp() * 1000000 - start_time)

    def update(self):
        """
        Update the clock.
        """
        self.updated_date = datetime.now()

    def get_sec(self):
        """
        Get the clock in seconds.        
        """
        self.update()
        return int(self.updated_date.timestamp() - (self.start_time//1000000))

    def get_msec(self):
        """
        Get the clock in milliseconds.        
        """
        self.update()
        return int(self.updated_date.timestamp() * 1000  - (self.start_time//1000))

    def get_misc(self):
        """
        Get the clock in microseconds.       
        """
        self.update()
        return int(self.updated_date.timestamp() * 1000000 - self.start_time)
    
    def __type__(self):
        return "Clock"

# Creating the date and clock objects
date = Date()
clock = Clock(0)

class Chrono:

    def __init__(self, unit:str = "ms"):
        # Setting up the chronometer
        self.reset(unit)
        self.running = True

    def update(self):
        """
        Update the chronometer if it is running.
        """
        if self.running:
            match self.unit:
                case "s":
                    self.updated_time = clock.get_sec()
                case "ms":
                    self.updated_time = clock.get_msec()
                case "unix":
                    self.updated_time = clock.get_misc()
                case _:
                    return False


    def elapsed_time(self):
        """
        Get the current chronometer time.
        """
        self.update()
        return self.updated_time - self.start_time - self.removed
    
    def start(self):
        """
        Resume the chronometer.
        """
        self.running = True
        old_time = self.updated_time
        self.update()
        self.removed += self.updated_time - old_time
        del old_time

    def stop(self):
        """
        Stop the chronometer.
        """
        self.running = False

    def reset(self, unit:str = "ms"):
        """
        Set or reset the chronometer unit, time and snapshot.
        """
        self.unit = unit
        match unit:
                case "s":
                    self.start_time = clock.get_sec()
                case "ms":
                    self.start_time = clock.get_msec()
                case "unix":
                    self.start_time = clock.get_misc()
                case _:
                    return False
        self.updated_time = self.start_time
        self.removed = 0
        self.snapshot = []

    def isrunning(self):
        """
        Check if the chronometer is running.
        """
        return self.running
    
    def set_snapshot(self):
        """
        Save a chronometer snapshot.
        """
        self.snapshot.append(self.elapsed_time())
    
    def get_snapshot(self, index:int = -1):
        """
        Get a chronometer snapshot.
        """
        if index == "all":
            return self.snapshot
        return self.snapshot[index]
    
    def del_snapshot(self, index:int = -1):
        """
        Delete a chronometer snapshot.
        """
        if index == "all":
            self.snapshot = []
        else:
            del self.snapshot[index]

    def __type__(self):
        return "Chrono"

class Timer:

    def __init__(self, time:int, unit:str = "ms"):
        # Setting up the timer
        self.reset(time, unit)
        self.running = True

    def update(self):
        """
        Update the timer if it is running.
        """
        if self.running:
            match self.unit:
                case "s":
                    self.updated_time = clock.get_sec()
                case "ms":
                    self.updated_time = clock.get_msec()
                case "unix":
                    self.updated_time = clock.get_misc()
                case _:
                    return False

    def remaining_time(self):
        """
        Get the remaining time of the timer.
        """
        self.update()
        return self.remaining - (self.updated_time - (self.start_time + self.removed))
    
    def check(self):
        """
        Check if the timer is finished.
        """
        return self.remaining_time() <= 0
    
    def elapsed_time(self):
        """
        Get the current timer active time (not as usefull as the remaining time).
        """
        self.update()
        return self.updated_time - self.start_time - self.removed

    def start(self):
        """
        Resume the timer.
        """
        self.running = True
        old_time = self.updated_time
        self.update()
        self.removed += self.updated_time - old_time
        del old_time

    def stop(self):
        """
        Stop the timer.
        """
        self.running = False

    def reset(self, time:int, unit:str = "ms"):
        """
        Set or reset the timer unit and time.
        """
        self.unit = unit
        match unit:
                case "s":
                    self.start_time = clock.get_sec()
                case "ms":
                    self.start_time = clock.get_msec()
                case "unix":
                    self.start_time = clock.get_misc()
                case _:
                    return False
        self.updated_time = self.start_time
        self.remaining = time
        self.removed = 0

    def isrunning(self):
        """
        Check if the timer is running.
        """
        return self.running
    
    def __type__(self):
        return "Timer"
    
def delay(time:int, unit:str = "ms"):
    """
    Delay the program for a given time.
    """
    match unit:
        case "s":
            sleep(time)
        case "ms":
            sleep(time/1000)
        case "unix":
            sleep(time/1000000)