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
from Geometry.rotation import from_degrees

from Spline.quintic_hermite_spline import QuinticHermiteSpline, optimize_spline, create_quintic_splines

from Trajectory.trajectory_util import parameterize_splines, time_parameterize_trajectory

def mirror_trajectory(trajectory):
    """Returns a trajectory mirrored about y = 0"""
    poses = []

    # Mirror each pose and return a new trajectory
    for p in trajectory.poses:
        poses.append(p.mirror())

    return Trajectory(name=trajectory.name + "-Mirrored", poses=poses, current=False, reverse = trajectory.reverse, start_velocity=trajectory.start_velocity, end_velocity=trajectory.end_velocity, max_velocity=trajectory.max_velocity, max_abs_acceleration=trajectory.max_abs_acceleration)

class Trajectory:
    """Trajectory container class"""

    generation_time = 0
    drive_time = 0
    length = 0
    
    update_splines = True
    optimized = False

    def __init__(self, name="", poses=[], current=False, reverse=False, start_velocity=0, end_velocity=0, max_velocity=120, max_abs_acceleration=180, max_centr_acceleration=120):
        """Constructs a Trajectory object"""

        self.current = current
        self.name = name
        self.poses = poses
        self.splines = []
        self.reverse = reverse
        self.start_velocity = start_velocity
        self.end_velocity = end_velocity
        self.max_velocity = max_velocity
        self.max_abs_acceleration = max_abs_acceleration
        self.max_centr_acceleration = max_centr_acceleration

        if len(self.poses) != 0:
            self.update_splines = True
            self.reparameterize_splines()

    def reparameterize_splines(self):
        """Re-calculates and re-paramterizes splines if necessary"""

        pose_length_invalid = len(self.poses) == 0
        spline_length_invalid = len(self.splines) == 0

        # TODO: add better error handling
        if (pose_length_invalid and spline_length_invalid):
            raise ValueError("Can't reparameterize splines if len of poses and splines equals 0.")

        # If valid, start timer and reparameterize splines
        start_time = time.perf_counter()
        if self.update_splines or not self.optimized:
            self.splines = create_quintic_splines(self.poses)
            self.update_splines = False

        self.points = parameterize_splines(self.splines)

        # Add timer to generation time
        self.generation_time += time.perf_counter() - start_time
        self.time_parameterize_splines()

    def optimize_splines(self):
        """Optimizes splines"""

        if self.optimized:
            return

        pose_length_invalid = len(self.poses) == 0
        spline_length_invalid = len(self.splines) == 0

        # TODO: add better error handling
        if (pose_length_invalid and spline_length_invalid):
            raise ValueError("Can't optimize splines if len of poses and splines equals 0.")

        # Update generation time and optimize splines
        start_time = time.perf_counter()
        optimize_spline(self.splines)
    
        self.generation_time += time.perf_counter() - start_time
        
        # Don't reset splines to default
        self.optimized = True
        self.reparameterize_splines()
        

    def time_parameterize_splines(self):
        """Calculates the velocity, acceleration and time for each state"""
        
        # Time parameterize and add time to generation time
        start_time = time.perf_counter()
        time_parameterize_trajectory(self.reverse, self.points, self.start_velocity, self.end_velocity, self.max_velocity, self.max_abs_acceleration, self.max_centr_acceleration)
        self.generation_time += time.perf_counter() - start_time

        self.drive_time = self.points[len(self.points) - 1].t
        self.length = self.points[len(self.points) - 1].distance

    def add_pose(self, pose):
        """Mutator to add pose to end"""
        self.poses.append(pose)

        self.reset()

    def move_pose(self, index, delta):
        """Mutator to move pose up or down"""
        #https://www.geeksforgeeks.org/python-program-to-swap-two-elements-in-a-list/
        self.poses[index],self.poses[index - delta] = self.poses[index - delta],self.poses[index]

        self.reset()

    def remove_pose(self, index):
        """Mutator to add pose to end"""
        self.poses.pop(index)

        self.reset()

    
    def update_pose(self, index, value, key):
        """Mutator to update a single value at index"""
        if key == "x":
            self.poses[index].translation.x = value
        elif key == "y":
            self.poses[index].translation.y = value
        if key == "theta":
            self.poses[index].rotation = from_degrees(value)

        self.reset()
        

    def trajectory_length(self):
        """Returns the index length of the Trajectory"""
        return len(self.points)

    def reset(self):
        """Helper function that resets Trajectory generation"""

        # Reset generation time and reparameterize splines
        self.generation_time = 0.0
        self.update_splines = True
        self.optimized = False
        self.reparameterize_splines()


    



