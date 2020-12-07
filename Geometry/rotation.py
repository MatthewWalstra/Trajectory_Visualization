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
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file

from Util.util import EPSILON, epsilon_equals
from Geometry.translation import Translation

def from_radians(radians):
    """Returns a Rotation object with specified angle in radians"""
    return Rotation(math.cos(radians), math.sin(radians), False)

def from_degrees(degrees):
    """Returns a Rotation object with specified angle in degrees"""
    return from_radians(math.radians(degrees))

class Rotation:
    """Class that contains a rotation"""

    def __init__(self, x=1.0, y=0.0, normalize=False):
        """Constructs Rotation object"""
        self.normalize = normalize
        
        if normalize:
            magnitude = math.hypot(x, y)
            if (magnitude > EPSILON):
                self.sin_angle = y / magnitude
                self.cos_angle = x / magnitude
            else:
                self.sin_angle = 0
                self.cos_angle = 1
        else:
            self.cos_angle = x
            self.sin_angle = y

    def rotate(self, other):
        """Returns a Rotation of this rotated by other"""
        return Rotation(self.cos_angle * other.cos_angle - self.sin_angle * other.sin_angle, self.cos_angle * other.sin_angle + self.sin_angle * other.cos_angle, True)
    
    def get_radians(self):
        """Returns the magnitude of the rotation in radians"""
        return math.atan2(self.sin_angle, self.cos_angle)
    
    def get_degrees(self):
        """Returns the magnitude of the rotation in degrees"""
        return math.degrees(self.get_radians())

    def inverse(self):
        """Returns the inverse of the rotation"""
        return Rotation(self.cos_angle, -self.sin_angle)

    def interpolate(self, other, x):
        """Returns the interpolation between two Rotations: this and other"""
        if x <= 0.0:
            return self
        if x >= 1.0:
            return other
        angle_diff = self.inverse().rotate(other).get_radians()
        return self.rotate(from_radians(angle_diff * x))

    def isParallel(self, other):
        """Returns True if two rotations are parallel (cross product of 0)"""
        return epsilon_equals(self.to_translation().cross(other.to_translation()), 0)

    def to_translation(self):
        """Returns Rotation as a translation"""
        return Translation(self.cos_angle, self.sin_angle)

    def __str__(self):
        """Returns Rotation as a string"""
        return "{:.6f}, ".format(self.get_degrees())

        

