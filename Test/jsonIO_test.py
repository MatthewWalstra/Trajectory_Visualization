"""CS 108 Trajectory Visualization Project

Unittests for jsonIO

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file

from Trajectory.trajectory import Trajectory
from Geometry.pose import Pose, to_pose
from Util.jsonIO import JsonIO


class jsonIOTest(unittest.TestCase):
    """Unittests for jsonIO"""

    def test_save_load(self):
        """Tests saving and loading: Trajectory should be the same"""

        poses = []
        poses.append(to_pose())
        poses.append(to_pose(100, 300, 40))
        poses.append(to_pose(320, 350, 135))
        poses.append(to_pose(90, -100, -180))
        poses.append(to_pose(400, 50, 90))

        trajectory = Trajectory("Trajectory1", poses, True,  True, 10, 20, 30, 40, 50)
        tmp = Trajectory("White_Line_Shot", poses, False, True, 10, 20, 30, 40, 50)

        trajectories = [tmp, trajectory]

        IO = JsonIO(path="Test/", name="jsonIO_unittest.json")

        IO.save_trajectories(trajectories)

        trajectory2 = IO.load_trajectories()[0]

        self.assertEqual(trajectory.name, trajectory2.name)
        self.assertEqual(trajectory.reverse, trajectory2.reverse)
        self.assertEqual(trajectory.current, trajectory2.current)

        self.assertAlmostEqual(trajectory.start_velocity, trajectory2.start_velocity)
        self.assertAlmostEqual(trajectory.end_velocity, trajectory2.end_velocity)
        self.assertAlmostEqual(trajectory.max_velocity, trajectory2.max_velocity)
        self.assertAlmostEqual(trajectory.max_abs_acceleration, trajectory2.max_abs_acceleration)
        self.assertAlmostEqual(trajectory.max_centr_acceleration, trajectory2.max_centr_acceleration)

        for i in range(len(trajectory.poses)):
            with self.subTest(i=i):
                self.assertAlmostEqual(trajectory.poses[i].translation.x, trajectory2.poses[i].translation.x)
                self.assertAlmostEqual(trajectory.poses[i].translation.y, trajectory2.poses[i].translation.y)
                self.assertAlmostEqual(trajectory.poses[i].rotation.get_degrees(), trajectory2.poses[i].rotation.get_degrees())


if __name__ == "__main__":
    unittest.main()
