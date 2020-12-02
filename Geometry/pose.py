"""CS 108 Trajectory Visualization Project

Class that contains a 2D position, angle, and helper methods

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/geometry/Pose2d.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Geometry/Pose2D.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math

from Geometry.translation import Translation
from Geometry.rotation import Rotation, from_degrees
from Geometry.twist import Twist
from Util.util import EPSILON, interpolate, epsilon_equals


def to_pose(x=0.0, y=0.0, degrees=0.0, curvature=0.0, dCurvature=0.0):
    """Helper function to create a Pose from (x, y, degrees)"""
    return Pose(Translation(x,y), from_degrees(degrees), curvature, dCurvature)

class Pose:
    """Class containing a 2D position"""

    def __init__(self, translation=Translation(), rotation=Rotation(), curvature=0.0, dCurvature=0.0):
        """Constructs a Pose object"""
        self.translation = translation
        self.rotation = rotation
        self.curvature = curvature
        self.dCurvature = dCurvature

    def exp(self, delta):
        """Lie Algebra Exponential map: returns Pose (transform from one Pose to the next)"""

        sin_theta = math.sin(delta.dtheta)
        cos_theta = math.cos(delta.dtheta)
        s = c = 0
        if abs(delta.dtheta) < EPSILON:
            s = 1.0 - 1.0 / 6.0 * delta.dtheta * delta.dtheta
            c = .5 * delta.dtheta
        else:
            s = sin_theta / delta.dtheta
            c = (1.0 - cos_theta) / delta.dtheta
        
        return Pose(Translation(delta.dx * s - delta.dy * c, delta.dx * c + delta.dy * s),
            Rotation(cos_theta, sin_theta, False))

    def log(self, transform):
        """Inverse of exp: returns Twist (Twist from Pose and transformation)"""
        dtheta = transform.rotation.get_radians()
        half_dtheta = .5 * dtheta
        cos_minus_one = transform.rotation.cos_angle - 1.0
        halfdtheta_by_tan_halfdtheta = 0
        if abs(cos_minus_one) < EPSILON:
            halfdtheta_by_tan_halfdtheta = 1.0 - 1.0 / 12.0 * dtheta * dtheta
        else:
            halfdtheta_by_tan_halfdtheta = -(half_dtheta * transform.rotation.sin_angle) / cos_minus_one
        
        tmp_rot = Rotation(halfdtheta_by_tan_halfdtheta, -half_dtheta, False)
        tmp_trans = transform.translation.rotate(tmp_rot)

        return Twist(tmp_trans.x, tmp_trans.y, dtheta)
        
    def transform(self, other):
        """Returns self transformed by other"""
        return Pose(self.translation.translate(other.translation.rotate(self.rotation)), self.rotation.rotate(other.rotation), self.curvature, self.dCurvature)

    def inverse(self):
        """Returns the inverse of self"""
        tmp_rot = self.rotation.inverse()
        return Pose(self.translation.inverse().rotate(tmp_rot), tmp_rot)
    
    def normal(self):
        """Returns the normal of self"""
        return Pose(self.translation, self.rotation.inverse())
    
    def interpolate(self, other, x):
        """Returns interpolation of self and other"""
        if x <= 0.0:
            return self
        elif x >= 1.0:
            return other
        tmp = self.log(self.inverse().transform(other))
        tmp_pose = self.transform(self.exp(tmp.scaled(x)))
        tmp_pose.curvature = interpolate(self.curvature, other.curvature, x)
        tmp_pose.dCurvature = interpolate(self.dCurvature, other.dCurvature, x)
        return tmp_pose

    def distance(self, other):
        """Returns the distance between self and other"""
        return self.log(self.inverse().transform(other)).norm()

    def mirror(self):
        """Returns mirrored point about y = 0"""
        return Pose(Translation(self.translation.x, -self.translation.y), self.rotation.inverse(),-self.curvature, -self.dCurvature)
    
    def is_collinear(self, other):
        """returns True if self and other are collinear (lie on the same line)"""
        if not self.rotation.isParallel(other.rotation):
            return False
        
        tmp = self.log(self.inverse().transform(other))
        return epsilon_equals(tmp.dy, 0.0) and epsilon_equals(tmp.dtheta, 0.0)
