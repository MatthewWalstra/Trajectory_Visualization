"""CS 108 Trajectory Visualization Project

Class Containing a time delayed boolean: returns true if value passed in is equivalent for a certain amount of time

Inspired by: 
https://github.com/SCsailors/2020RobotCode/blob/Limelight-PNP/src/main/cpp/lib/Util/TimeDelayedBoolean.cpp


@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import time

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file

from Util.util import epsilon_equals

class TimeDelayedBoolean:
    """Delayed boolean if values are equal for a certain amount of time"""

    def __init__(self, initial_value, timeout):
        """Constructs object"""
        self.timeout = timeout
        self.prev_value = initial_value
        self.start_time = time.perf_counter()
        self.first = False

    def update(self, value):
        """Returns True once if equivalent for a set amount of time"""
        
        # Not the same, so reset timer, update prev_value, and return False
        if (not epsilon_equals(value, self.prev_value)):
            self.start_time = time.perf_counter()
            self.prev_value = value
            self.first = True
            return False

        dt = time.perf_counter() - self.start_time
        return_value = False
    
        if (dt >= self.timeout) and (self.first):
            # First time over the set time, set false to not repeat
            self.first = False
            return_value = True
        
        self.prev_value = value
        return return_value
            

