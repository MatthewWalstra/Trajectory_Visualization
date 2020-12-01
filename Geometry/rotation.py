"""CS 108 Trajectory Visualization Project

Class that contains a rotation angle and helper methods

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/geometry/Rotation2d.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Geometry/Rotation2D.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right, F5 works regardless

import Util.utility

class Rotation:
    """Class that contains a rotation"""

    def __init__(self, x=1.0, y=0.0, normalize=False):
        """Constructs Rotation object"""
        self.cos_angle = x
        self.sin_angle = y
        self.normalize = normalize
        
        if normalize:
            magnitude = math.hypot(x, y)
            if (magnitude):
                pass