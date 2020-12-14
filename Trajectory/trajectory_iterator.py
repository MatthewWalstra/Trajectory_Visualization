"""CS 108 Trajectory Visualization Project

Contains a class for iterating over a trajectory

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/TimedView.java
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/TrajectoryIterator.java

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

from Util.util import epsilon_equals, limit2
from Geometry.trajectory_point import TrajectoryPoint

class TrajectoryIterator:
    """Class for iterating over a trajectory"""

    def __init__(self, trajectory):
        """Constructs an instance of TrajectoryIterator"""
        self.trajectory = trajectory
        self.reset()

    def sample(self, t):
        """Returns interpolated trajectory point based on t"""
        if t >= self.end_t:
            return self.trajectory.points[self.trajectory.trajectory_length() - 1]
        if t <= self.start_t:
            return self.trajectory.points[0]
        for i in range(1, self.trajectory.trajectory_length()):
            s = self.trajectory.points[i]
            if s.t >= t:
                prev_s = self.trajectory.points[i - 1]
                if epsilon_equals(s.t, prev_s.t):
                    return s
                return prev_s.interpolate(s, (t - prev_s.t) / (s.t - prev_s.t))

    def is_done(self):
        """Returns if the trajectory is done iterating"""
        return self.remaining_progress() == 0.0
    
    def remaining_progress(self):
        """Returns remaining progress"""
        return max(0.0, self.end_t - self.progress)

    def advance(self, additional_progress):
        """Returns the current sample after moving forward by additional_progress"""
        self.progress = limit2(additional_progress, self.start_t, self.end_t)
        self.current_sample = self.sample(self.progress)
        return self.current_sample
    
    def reset(self):
        """Resets trajectory iterator"""
        if not len(self.trajectory.points) == 0:
            self.start_t = self.trajectory.points[0].t
            self.end_t = self.trajectory.points[self.trajectory.trajectory_length() - 1].t

            self.current_sample = self.sample(self.start_t)
            self.progress = self.start_t
        else: 
            self.start_t = 0
            self.end_t = 0
            self.current_sample = TrajectoryPoint()
            self.progress = 0
