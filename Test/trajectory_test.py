"""CS 108 Trajectory Visualization Project

Unittests for Trajectory

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import unittest
import math

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file

from Geometry.pose import Pose, to_pose
from Geometry.trajectory_point import TrajectoryPoint

from Trajectory.trajectory import Trajectory, mirror_trajectory
from Trajectory.trajectory_iterator import TrajectoryIterator
from Trajectory.trajectory_util import time_parameterize_trajectory, parameterize_splines

class TractoryTest(unittest.TestCase):
    """Class to test Trajectories"""

    def test_trajectory(self):
        """Tests Trajectory class"""

        poses = []
        poses.append(to_pose())
        poses.append(to_pose(50, 100, 90))
        poses.append(to_pose(100, 150, 0))

        traj = Trajectory(poses=poses, reverse = False)

        self.assertAlmostEqual(3, len(traj.poses))
        self.assertAlmostEqual(2, len(traj.splines))

        with open("Trajectory_Test.csv", "w") as file:
            traj.update_pose(to_pose(50, 75, 135), 1)
            traj.time_parameterize_splines()
            for t in traj.points:
                file.write(t.__str__() + "\n")

        with open("Trajectory_Test.csv", "a") as file:
            traj.optimize_splines()
            traj.time_parameterize_splines()
            for t in traj.points:
                file.write(t.__str__() + "\n")
        

    def test_trajectory_iterator(self):
        """Tests Trajectory iterator class""" 

        poses = []
        poses.append(to_pose())
        poses.append(to_pose(36.0, 0.0, 0.0))
        poses.append(to_pose(60.0, 100.0, 0.0))
        poses.append(to_pose(160.0, 100.0, 0.0))
        poses.append(to_pose(200.0, 70.0, 45.0))

        traj = Trajectory(poses=poses)
        traj.time_parameterize_splines()
        iterator = TrajectoryIterator(traj)
        print(iterator.end_t)  
        with open("Trajectory_Iterator_Test.csv", "w") as file:
            t = 0.1
            while not iterator.is_done():
                sample = iterator.advance(t)
                file.write(sample.__str__() + "\n")
        

if __name__ == '__main__':
    unittest.main()