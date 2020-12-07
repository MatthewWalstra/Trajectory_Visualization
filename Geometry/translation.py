"""CS 108 Trajectory Visualization Project

Class that contains an (x,y) translation and helper methods

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/geometry/Translation2d.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Geometry/Translation2D.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math
#from Geometry.rotation import Rotation



class Translation:
    """Contains an (x,y translation)"""

    def __init__(self, x=0, y=0):
        """Constructs a Translation object"""
        self.x = x
        self.y = y

    def norm(self):
        """Returns the normal of the x and y coordinates"""
        return math.hypot(self.x, self.y)

    def translate(self, other):
        """Returns a Translation of this object by other"""
        return Translation(self.x + other.x, self.y + other.y)

    def rotate(self, rotation):
        """Returns a Translation of this object rotated by a Rotation"""
        return Translation(self.x * rotation.cos_angle - self.y * rotation.sin_angle, self.x * rotation.sin_angle + self.y * rotation.cos_angle)

    def inverse(self):
        """Returns the inverse of this Translation"""
        return Translation(-self.x, -self.y)
    
    def distance(self, other):
        """Returns the distance between two translation points"""
        return self.inverse().translate(other).norm()

    def extrapolate(self, other, x):
        """Returns a Translation extrapolated from self and other"""
        return Translation(x * (other.x - self.x) + self.x, x * (other.y - self.y) + self.y)

    def interpolate(self, other, x):
        """Returns a Translation interpolated between self and other (x is from 0-1)"""
        if x <= 0.0:
            return self
        elif x >= 1.0:
            return other

        return self.extrapolate(other, x)

    def cross(self, other):
        """Returns the cross product of Translation self and other"""
        return self.x * other.y - self.y * other.x

    def __str__(self):
        """Returns Translation as a string"""
        return "{:.6f}, {:.6f}, ".format(self.x, self.y)
    
if __name__ == "__main__":
    pass
    

    

