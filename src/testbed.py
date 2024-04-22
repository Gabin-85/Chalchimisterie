# This is a testbed
# It is used to test part of the game without launching it.
from utils.timeHandler import date, clock, Chrono, Timer
from utils.consoleHandler import *

# Actually testing timeHandler and consoleHandler at the same time.

console = consoleHandler()

def test_time_classes():
    # Test the Clock and Date classes
    debug("Current time in date: " + str(date.get_date()))
    debug("Current time in unix: " + str(date.get_unix()))
    debug("Current clock in unix: " + str(clock.get_misc()))

    # Test the Chrono class
    chrono = Chrono()
    chrono.start()
    if chrono.removed == 0:
        debug("Passed")
    else:
        error("Failed")
    chrono.stop()
    if chrono.elapsed_time() == 0:
        debug("Passed")
    else:
        error("Failed")

    # Test the Timer class
    timer = Timer(2)
    timer.stop()
    if timer.elapsed_time() == 0:
        debug("Passed")
    else:
        error("Failed")
    timer.start()
    while timer.check() == False:
        debug("Remaining time: " + str(timer.remaining_time()))
    if timer.check() == True and timer.elapsed_time() == 2:
        debug("Passed")
    else:
        error("Failed")

    debug("End Test")

test_time_classes()

console.quit()