"""CS 108 Trajectory Visualization Project

Container class for a trajectory and helper methods

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/TimedView.java
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/TrajectoryView.java


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

from Geometry.trajectory_point import TrajectoryPoint
from Geometry.pose import Pose

from Spline.quintic_hermite_spline import QuinticHermiteSpline, optimize_spline, create_quintic_splines

from Trajectory.trajectory_util import parameterize_splines, time_parameterize_trajectory

def mirror_trajectory(trajectory):
    """Returns a trajectory mirrored about y = 0"""
    poses = []

    # Mirror each pose and return a new trajectory
    for p in trajectory.poses:
        poses.append(p.mirror())

    return Trajectory(poses, reverse = trajectory.reverse, start_velocity=trajectory.start_velocity, end_velocity=trajectory.end_velocity, max_velocity=trajectory.max_velocity, max_abs_acceleration=trajectory.max_abs_acceleration)

class Trajectory:
    """Trajectory container class"""

    generation_time = 0
    drive_time = 0
    length = 0
    
    update_splines = True
    parameterizeable = False

    def __init__(self, poses=[], points=[], reverse=False, start_velocity=0, end_velocity=0, max_velocity=120, max_abs_acceleration=180):
        """Constructs a Trajectory object"""

        self.poses = poses
        self.splines = []
        self.points = points
        self.reverse = reverse
        self.start_velocity = start_velocity
        self.end_velocity = end_velocity
        self.max_velocity = max_velocity
        self.max_abs_acceleration = max_abs_acceleration

        if len(self.poses) != 0:
            self.parameterizeable = True
            self.update_splines = True
            self.reparameterize_splines()

    def reparameterize_splines(self):
        """Re-calculates and re-paramterizes splines if necessary"""

        pose_length_invalid = len(self.poses) == 0
        spline_length_invalid = len(self.splines) == 0

        # TODO: add better error handling
        if (pose_length_invalid and spline_length_invalid) or (not self.parameterizeable):
            raise ValueError("Can't reparameterize splines if len of poses and splines equals 0.")

        # If valid start timer and reparameterize splines
        start_time = time.perf_counter()
        if self.update_splines:
            self.splines = create_quintic_splines(self.poses)
            self.update_splines = False

        self.points = parameterize_splines(self.splines)

        # Add timer to generation time
        self.generation_time += time.perf_counter() - start_time

    def optimize_splines(self):
        """Optimizes splines"""

        pose_length_invalid = len(self.poses) == 0
        spline_length_invalid = len(self.splines) == 0

        # TODO: add better error handling
        if (pose_length_invalid and spline_length_invalid) or (not self.parameterizeable):
            raise ValueError("Can't optimize splines if len of poses and splines equals 0.")

        # Update generation time and optimize splines
        start_time = time.perf_counter()
        optimize_spline(self.splines)
        self.generation_time += time.perf_counter() - start_time
        
        # Don't reset splines to default
        self.update_splines = False
        self.reparameterize_splines()
        

    def time_parameterize_splines(self):
        """Calculates the velocity, acceleration and time for each state"""
        
        # Time parameterize and add time to generation time
        start_time = time.perf_counter()
        time_parameterize_trajectory(self.reverse, self.points, self.start_velocity, self.end_velocity, self.max_velocity, self.max_abs_acceleration)
        self.generation_time += time.perf_counter() - start_time

    def update_poses(self, poses):
        """Mutator to update list of poses"""
        self.poses = poses

        # Reset generation time and reparameterize splines
        self.generation_time = 0.0
        self.update_splines = True
        self.reparameterize_splines()
    
    def update_pose(self, pose, index):
        """Mutator to update a single pose at index"""
        self.poses[index] = pose

        # Reset generation time and reparameterize splines
        self.generation_time = 0.0
        self.update_splines = True
        self.reparameterize_splines()

    def trajectory_length(self):
        """Returns the index length of the Trajectory"""
        return len(self.points)



    


