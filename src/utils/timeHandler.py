# Here is the time handler
# It's a tool box that gives functions to manage time, chronometer, timer and clock.
from datetime import datetime

class Clock_functions :

    def __init__(self):
        # Setting up the clock
        self.clock = datetime.now()

    def update(self):
        """
        Update the clock.
        """
        self.clock = datetime.now()
    
    def get_date(self):
        """
        Get the current date (datetime format).
        """
        self.update()
        return self.clock
    
    def get_year(self):
        """
        Get the current years.
        """
        self.update()
        return self.clock.year
    
    def get_month(self):
        """
        Get the current month.
        """
        self.update()
        return self.clock.month
    
    def get_day(self):
        """
        Get the current day.
        """
        self.update()
        return self.clock.day

    def get_hour(self):
        """
        Get the current hour.
        """
        self.update()
        return self.clock.hour

    def get_min(self):
        """
        Get the current minute.        
        """
        self.update()
        return self.clock.minute
    
    def get_sec(self):
        """
        Get the current second.        
        """
        self.update()
        return self.clock.minute

    def get_time_in_sec(self):
        """
        Get the current time in seconds.        
        """
        self.update()
        return int(self.clock.timestamp())

    def get_time_in_ms(self):
        """
        Get the current time in milliseconds.        
        """
        self.update()
        return int(self.clock.timestamp() * 1000)

    def get_time_in_unix(self):
        """
        Get the current time in microseconds (in unix time).       
        """
        self.update()
        return int(self.clock.timestamp() * 1000000)

# Create the first clock
clock = Clock_functions()

class Chrono :

    def __init__(self, unit = "ms"):
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
                    self.chrono_now = clock.get_time_in_sec()
                case "ms":
                    self.chrono_now = clock.get_time_in_ms()
                case "unix":
                    self.chrono_now = clock.get_time_in_unix()
                case _:
                    return False


    def get_time(self):
        """
        Get the current choronometer time.
        """
        self.update()
        return self.chrono_now - self.chrono_start - self.removed
    
    def start(self):
        """
        Resume the chronometer.
        """
        self.running = True
        self.removed -= self.chrono_now - self.get_time()

    def stop(self):
        """
        Stop the chronometer.
        """
        self.running = False

    def reset(self, unit = "ms"):
        """
        Set or reset the chronometer unit, time and snapshot.
        """
        self.unit = unit
        match unit:
                case "s":
                    self.chrono_start = clock.get_time_in_sec()
                case "ms":
                    self.chrono_start = clock.get_time_in_ms()
                case "unix":
                    self.chrono_start = clock.get_time_in_unix()
                case _:
                    return False
        self.chrono_now = self.chrono_start
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
        self.snapshot.append(self.get_time())
    
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

class Timer :

    def __init__(self, time, unit = "ms"):
        # Setting up the timer
        self.reset(time, unit)
        self.running = True

    def update(self, unit:str):
        """
        Update the timer if it is running.
        """
        if self.running:
            match unit:
                case "s":
                    self.timer_now = clock.get_time_in_sec()
                case "ms":
                    self.timer_now = clock.get_time_in_ms()
                case "unix":
                    self.timer_now = clock.get_time_in_unix()
                case _:
                    return False

    def remaining_time(self, unit:str = "ms"):
        """
        Get the remaining time of the timer.
        """
        self.update(unit)
        return self.remaining - (self.timer_now - self.timer_start + self.removed)
    
    def check(self):
        """
        Check if the timer is finished.
        """
        return self.remaining_time() <= 0
    
    def get_time(self):
        """
        Get the current timer active time (not as usefull as the remaining time).
        """
        self.update(self.unit)
        return self.timer_now - self.timer_start - self.removed

    def start(self):
        """
        Resume the timer.
        """
        self.running = True
        self.removed -= self.timer_now - self.get_time()

    def stop(self):
        """
        Stop the timer.
        """
        self.running = False

    def reset(self, time, unit = "ms"):
        """
        Set or reset the timer unit and time.
        """
        self.unit = unit
        match unit:
                case "s":
                    self.timer_start = clock.get_time_in_sec()
                case "ms":
                    self.timer_start = clock.get_time_in_ms()
                case "unix":
                    self.timer_start = clock.get_time_in_unix()
                case _:
                    return False
        self.timer_now = self.timer_start
        self.remaining = time
        self.removed = 0

    def isrunning(self):
        """
        Check if the timer is running.
        """
        return self.running