"""CS 108 Trajectory Visualization Project

Class with state data generated by the trajectory planner

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/timing/TimedState.java

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

from Util.util import interpolate, epsilon_equals

from Geometry.pose import Pose, to_pose

class TrajectoryPoint:
    """State data generated by the trajectory planner"""

    def __init__(self, pose=Pose(), time=0, velocity=0, acceleration=0, index_floor=0, index_ceil=0):
        """Constructs a TrajectoryPoint instance"""
        self.pose = pose
        self.t = time
        self.velocity = velocity
        self.acceleration = acceleration
        self.index_floor = index_floor
        self.index_ceil = index_ceil

    def interpolate(self, other, x):
        """Returns interpolatation between self and other"""
        new_t = interpolate(self.t, other.t, x)
        delta_t = new_t - self.t

        # Going for 2nd pass through timed states
        if delta_t < 0.0:
            return other.interpolate(self, 1.0 - x)

        # Constant acceleration formulas
        reversing = self.velocity < 0.0 or (epsilon_equals(0.0, self.velocity) and self.acceleration < 0.0)
        new_v = self.velocity + self.acceleration * delta_t
        new_s = (-1.0 if reversing else 1.0) * (self.velocity * delta_t + .5 * self.acceleration * delta_t * delta_t)

        return TrajectoryPoint(self.pose.interpolate(other.pose, new_s / self.pose.distance(other.pose)), new_t, new_v, self.acceleration, self.index_floor, other.index_ceil)
