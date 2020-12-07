"""CS 108 Trajectory Visualization Project

Class that contains the delta between two Poses, velocities, or accelerations

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/geometry/Twist2d.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Geometry/Twist2D.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math

class Twist:
    """Contains the delta between poses velocities or accelerations"""

    def __init__(self, dx=0, dy=0, dtheta=0):
        """Constructs a Twist object"""
        self.dx = dx
        self.dy = dy
        self.dtheta = dtheta
    
    def scaled(self, scale):
        """Returns a scaled Twist"""
        return Twist(self.dx * scale, self.dy * scale, self.dtheta * scale)

    def norm(self):
        """Returns the magnitude of the Twist"""
        if (self.dy == 0.0):
            return abs(self.dx)
        return math.hypot(self.dx, self.dy)

    def derive(self, initial, dt):
        """Returns the derivative between (self and initial) / dt"""
        ddx = (self.dx - initial.dx) / dt
        ddy = (self.dy - initial.dy) / dt
        ddt = (self.dtheta - initial.dtheta) / dt
        return Twist(ddx, ddy, ddt)

    def __str__(self):
        """Returns Twist as a string"""
        return "{:.6f}, {:.6f}, {:.6f}, ".format(self.dx, self.dy, self.dtheta)

    