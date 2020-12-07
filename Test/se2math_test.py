"""CS 108 Trajectory Visualization Project

Unittests for Geometry

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/test/java/com/team254/lib/geometry/TestSE2Math.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/test/cpp/lib/Geometry/SE2MathTest.cpp

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
from Geometry.rotation import Rotation, from_degrees, from_radians
from Geometry.trajectory_point import TrajectoryPoint
from Geometry.translation import Translation
from Geometry.twist import Twist

class SE2MathTest(unittest.TestCase):
    """Class to test Geometry"""

    def test_rotation(self):
        """Tests a Rotation"""
       
        # Test Constructors
        rot = Rotation()
        self.assertAlmostEqual(1, rot.cos_angle)
        self.assertAlmostEqual(0, rot.sin_angle)
        self.assertAlmostEqual(0, rot.get_degrees())
        self.assertAlmostEqual(0, rot.get_radians())

        rot = Rotation(1.0, 1.0, True)
        self.assertAlmostEqual(math.sqrt(2.0)/2.0, rot.cos_angle)
        self.assertAlmostEqual(math.sqrt(2.0)/2.0, rot.sin_angle)
        self.assertAlmostEqual(45, rot.get_degrees())
        self.assertAlmostEqual(math.pi/4, rot.get_radians())

        rot = from_radians(math.pi / 2.0)
        self.assertAlmostEqual(0, rot.cos_angle)
        self.assertAlmostEqual(1, rot.sin_angle)
        self.assertAlmostEqual(90, rot.get_degrees())
        self.assertAlmostEqual(math.pi/2.0, rot.get_radians())

        rot = from_degrees(270.0)
        self.assertAlmostEqual(0, rot.cos_angle)
        self.assertAlmostEqual(-1.0, rot.sin_angle)
        self.assertAlmostEqual(-90, rot.get_degrees())
        self.assertAlmostEqual(- math.pi/2, rot.get_radians())

        # Test inverse
        inverse = rot.inverse()
        self.assertAlmostEqual(0, inverse.cos_angle)
        self.assertAlmostEqual(1.0, inverse.sin_angle)
        self.assertAlmostEqual(90, inverse.get_degrees())
        self.assertAlmostEqual(math.pi/2, inverse.get_radians())

        rot = from_degrees(1.0)
        inverse = rot.inverse()
        self.assertAlmostEqual(rot.cos_angle, inverse.cos_angle)
        self.assertAlmostEqual(-rot.sin_angle, inverse.sin_angle)
        self.assertAlmostEqual(-1, inverse.get_degrees())

        # Test rotate
        rot1 = from_degrees(45)
        rot2 = from_degrees(45)
        rot3 = rot1.rotate(rot2)
        self.assertAlmostEqual(0, rot3.cos_angle)
        self.assertAlmostEqual(1.0, rot3.sin_angle)
        self.assertAlmostEqual(90, rot3.get_degrees())
        self.assertAlmostEqual(math.pi/2, rot3.get_radians())

        rot1 = Rotation()
        rot2 = from_degrees(21.45)
        rot3 = rot2.rotate(rot2.inverse())
        self.assertAlmostEqual(rot1.cos_angle, rot3.cos_angle)
        self.assertAlmostEqual(rot1.sin_angle, rot3.sin_angle)
        self.assertAlmostEqual(rot1.get_degrees(), rot3.get_degrees())

        # Test interpolation
        rot1 = from_degrees(45)
        rot2 = from_degrees(135)
        rot3 = rot1.interpolate(rot2, .5)
        self.assertAlmostEqual(90, rot3.get_degrees())

        rot3 = rot1.interpolate(rot2, .75)
        self.assertAlmostEqual(112.5, rot3.get_degrees())

        rot1 = from_degrees(45)
        rot2 = from_degrees(45)
        rot3 = rot1.interpolate(rot2, .5)
        self.assertAlmostEqual(45, rot3.get_degrees())
    
    def test_translation(self):
        """Tests a Translation"""

        # Test constructors
        trans = Translation()
        self.assertAlmostEqual(0, trans.x)
        self.assertAlmostEqual(0, trans.y)
        self.assertAlmostEqual(0, trans.norm())

        trans = Translation(3.0, 4.0)
        self.assertAlmostEqual(3.0, trans.x)
        self.assertAlmostEqual(4.0, trans.y)
        self.assertAlmostEqual(5.0, trans.norm())

        # Test inversion
        trans1 = Translation(3.152, 4.1666)
        trans2 = trans1.inverse()
        self.assertAlmostEqual(-trans1.x, trans2.x)
        self.assertAlmostEqual(-trans1.y, trans2.y)
        self.assertAlmostEqual(trans1.norm(), trans2.norm())

        # Test rotate
        trans = Translation(2.0, 0.0)
        rot = from_degrees(90.)
        trans1 = trans.rotate(rot)
        self.assertAlmostEqual(0.0, trans1.x)
        self.assertAlmostEqual(2.0, trans1.y)
        self.assertAlmostEqual(trans.norm(), trans1.norm())

        rot = from_degrees(-45)
        trans1 = trans.rotate(rot)
        self.assertAlmostEqual(math.sqrt(2.0), trans1.x)
        self.assertAlmostEqual(-math.sqrt(2.0), trans1.y)
        self.assertAlmostEqual(trans.norm(), trans1.norm())

        # Test translate
        trans1 = Translation(2.0, 1.0)
        trans2 = Translation(-2.0, 0.0)
        trans3 = trans1.translate(trans2)
        self.assertAlmostEqual(0.0, trans3.x)
        self.assertAlmostEqual(1.0, trans3.y)
        self.assertAlmostEqual(1, trans3.norm())

        # Test inverse
        trans = Translation()
        trans1 = Translation(2.16612, -23.55)
        trans2 = trans1.translate(trans1.inverse())
        self.assertAlmostEqual(trans.x, trans2.x)
        self.assertAlmostEqual(trans.y, trans2.y)
        self.assertAlmostEqual(trans.norm(), trans2.norm())

        # Test interpolation
        trans = Translation(0.0, 1.0)
        trans1 = Translation(10.0, -1.0)
        trans2 = trans.interpolate(trans1, .75)
        self.assertAlmostEqual(7.5, trans2.x)
        self.assertAlmostEqual(-.5, trans2.y)

    def test_pose(self):
        """Tests pose methods"""

        # Tests Constructor        
        pose = Pose()
        self.assertAlmostEqual(0, pose.translation.x)
        self.assertAlmostEqual(0, pose.translation.y)
        self.assertAlmostEqual(0, pose.rotation.get_degrees())
        self.assertAlmostEqual(0, pose.curvature)
        self.assertAlmostEqual(0, pose.dCurvature)

        pose = Pose(Translation(3.0, 4.0), from_degrees(45), .5, .1)
        self.assertAlmostEqual(3, pose.translation.x)
        self.assertAlmostEqual(4, pose.translation.y)
        self.assertAlmostEqual(45, pose.rotation.get_degrees())
        self.assertAlmostEqual(.5, pose.curvature)
        self.assertAlmostEqual(.1, pose.dCurvature)

        pose = to_pose(4.0, 3.0, -45, .4, -.2)
        self.assertAlmostEqual(4, pose.translation.x)
        self.assertAlmostEqual(3, pose.translation.y)
        self.assertAlmostEqual(-45, pose.rotation.get_degrees())
        self.assertAlmostEqual(.4, pose.curvature)
        self.assertAlmostEqual(-.2, pose.dCurvature)

        # Test transform
        pose1 = to_pose(3.0, 4.0, 90.0, .4, .2)
        pose2 = to_pose(1.0, 0.0, 0.0)
        pose3 = pose1.transform(pose2)
        self.assertAlmostEqual(3, pose3.translation.x)
        self.assertAlmostEqual(5, pose3.translation.y)
        self.assertAlmostEqual(90, pose3.rotation.get_degrees())
        self.assertAlmostEqual(.4, pose3.curvature)
        self.assertAlmostEqual(.2, pose3.dCurvature)

        pose1 = to_pose(3.0, 4.0, 90.0)
        pose2 = to_pose(1.0, 0.0, -90.0)
        pose3 = pose1.transform(pose2)
        self.assertAlmostEqual(3, pose3.translation.x)
        self.assertAlmostEqual(5, pose3.translation.y)
        self.assertAlmostEqual(0, pose3.rotation.get_degrees())
        self.assertAlmostEqual(0, pose3.curvature)
        self.assertAlmostEqual(0, pose3.dCurvature)

        # Test inverse
        identity = Pose()
        pose1 = to_pose(3.12123424, 8.286395, 93.1235, .5, .3)
        pose2 = pose1.transform(pose1.inverse())
        self.assertAlmostEqual(identity.translation.x, pose2.translation.x)
        self.assertAlmostEqual(identity.translation.y, pose2.translation.y)
        self.assertAlmostEqual(identity.rotation.get_degrees(), pose3.rotation.get_degrees())
        self.assertAlmostEqual(.5, pose2.curvature)
        self.assertAlmostEqual(.3, pose2.dCurvature)

        # Test interpolation
        # Movement from pose1 to pose2 along a circle with radius 10 centered at (3, -6)
        pose1 = to_pose(3.0, 4.0, 90.0, .5, .1)
        pose2 = to_pose(13.0, -6.0, 0.0, 1.0, .2)
        pose3 = pose1.interpolate(pose2, .5)
        expected_angle_radians = math.pi / 4.0
        self.assertAlmostEqual(3 + 10.0 * math.cos(expected_angle_radians), pose3.translation.x)
        self.assertAlmostEqual(-6 + 10.0 * math.sin(expected_angle_radians), pose3.translation.y)
        self.assertAlmostEqual(expected_angle_radians, pose3.rotation.get_radians())
        self.assertAlmostEqual(.75, pose3.curvature)
        self.assertAlmostEqual(.15, pose3.dCurvature)

        pose1 = to_pose(3.0, 4.0, 90.0)
        pose2 = to_pose(13.0, -6.0, 0.0)
        pose3 = pose1.interpolate(pose2, .75)
        expected_angle_radians = math.pi / 8.0
        self.assertAlmostEqual(3 + 10.0 * math.cos(expected_angle_radians), pose3.translation.x)
        self.assertAlmostEqual(-6 + 10.0 * math.sin(expected_angle_radians), pose3.translation.y)
        self.assertAlmostEqual(expected_angle_radians, pose3.rotation.get_radians())
        self.assertAlmostEqual(0.0, pose3.curvature)
        self.assertAlmostEqual(0.0, pose3.dCurvature)

        # Test distance
        self.assertAlmostEqual(math.pi * 5, pose1.distance(pose2))

        # Test mirror
        pose = to_pose(4.0, 3.0, -45, .4, -.2)
        pose1 = pose.mirror()
        self.assertAlmostEqual(4, pose1.translation.x)
        self.assertAlmostEqual(-3, pose1.translation.y)
        self.assertAlmostEqual(45, pose1.rotation.get_degrees())
        self.assertAlmostEqual(-.4, pose1.curvature)
        self.assertAlmostEqual(.2, pose1.dCurvature)

        # Test is_collinear
        pose1 = to_pose(3.0, 4.0, 90.0)
        pose2 = to_pose(13.0, -6.0, 0.0)
        self.assertFalse(pose1.is_collinear(pose2))

        pose1 = to_pose(3.0, 4.0, 90.0)
        pose2 = to_pose(3.0, 6.0, 90.0)
        self.assertTrue(pose1.is_collinear(pose2))

    def test_twist(self):
        """Tests Twist methods"""

        # Test constructor
        twist = Twist(1.0, 0.0, 0.0)
        pose = Pose()
        pose = pose.exp(twist)
        self.assertAlmostEqual(1.0, pose.translation.x)
        self.assertAlmostEqual(0.0, pose.translation.y)
        self.assertAlmostEqual(0.0, pose.rotation.get_degrees())

        # Test scaled
        pose = pose.exp(twist.scaled(2.5))
        self.assertAlmostEqual(2.5, pose.translation.x)
        self.assertAlmostEqual(0.0, pose.translation.y)
        self.assertAlmostEqual(0.0, pose.rotation.get_degrees())

        # Test logarithm
        pose = to_pose(2.0, 2.0, 90.0)
        twist = pose.log(pose)
        self.assertAlmostEqual(math.pi, twist.dx)
        self.assertAlmostEqual(0.0, twist.dy)
        self.assertAlmostEqual(math.pi / 2, twist.dtheta)

        # Test exponentiation: inverse of logarithm
        pose1 = pose.exp(twist)
        self.assertAlmostEqual(pose1.translation.x, pose.translation.x)
        self.assertAlmostEqual(pose1.translation.y, pose.translation.y)
        self.assertAlmostEqual(pose1.rotation.get_degrees(), pose.rotation.get_degrees())

    def test_trajectory_point(self):
        """Tests TrajectoryPoint"""

        # Test constructor
        traj = TrajectoryPoint()
        self.assertAlmostEqual(0, traj.pose.translation.x)
        self.assertAlmostEqual(0, traj.pose.translation.y)
        self.assertAlmostEqual(0, traj.pose.rotation.get_degrees())
        self.assertAlmostEqual(0, traj.pose.curvature)
        self.assertAlmostEqual(0, traj.pose.dCurvature)
        self.assertAlmostEqual(0, traj.t)
        self.assertAlmostEqual(0, traj.velocity)
        self.assertAlmostEqual(0, traj.acceleration)
        self.assertAlmostEqual(0, traj.index_floor)
        self.assertAlmostEqual(0, traj.index_ceil)

        traj1 = TrajectoryPoint(to_pose(0, 0, 0), 0, 0, 1, 6, 6)
        self.assertAlmostEqual(0, traj1.pose.translation.x)
        self.assertAlmostEqual(0, traj1.pose.translation.y)
        self.assertAlmostEqual(0, traj1.pose.rotation.get_degrees())
        self.assertAlmostEqual(0, traj1.pose.curvature)
        self.assertAlmostEqual(0, traj1.pose.dCurvature)
        self.assertAlmostEqual(0, traj1.t)
        self.assertAlmostEqual(0, traj1.velocity)
        self.assertAlmostEqual(1, traj1.acceleration)
        self.assertAlmostEqual(6, traj1.index_floor)
        self.assertAlmostEqual(6, traj1.index_ceil)

        traj2 = TrajectoryPoint(to_pose(.5, 0, 0), 1, 1, 0, 7, 7)
        self.assertAlmostEqual(.5, traj2.pose.translation.x)
        self.assertAlmostEqual(0, traj2.pose.translation.y)
        self.assertAlmostEqual(0, traj2.pose.rotation.get_degrees())
        self.assertAlmostEqual(0, traj2.pose.curvature)
        self.assertAlmostEqual(0, traj2.pose.dCurvature)
        self.assertAlmostEqual(1, traj2.t)
        self.assertAlmostEqual(1, traj2.velocity)
        self.assertAlmostEqual(0, traj2.acceleration)
        self.assertAlmostEqual(7, traj2.index_floor)
        self.assertAlmostEqual(7, traj2.index_ceil)

        traj3 = traj1.interpolate(traj2, .5)
        self.assertAlmostEqual(.125, traj3.pose.translation.x)
        self.assertAlmostEqual(0, traj3.pose.translation.y)
        self.assertAlmostEqual(0, traj3.pose.rotation.get_degrees())
        self.assertAlmostEqual(0, traj3.pose.curvature)
        self.assertAlmostEqual(0, traj3.pose.dCurvature)
        self.assertAlmostEqual(.5, traj3.t)
        self.assertAlmostEqual(.5, traj3.velocity)
        self.assertAlmostEqual(1, traj3.acceleration)
        self.assertAlmostEqual(6, traj3.index_floor)
        self.assertAlmostEqual(7, traj3.index_ceil)

        # Test Reverse interpolation
        traj3 = traj2.interpolate(traj1, .5)
        self.assertAlmostEqual(.125, traj3.pose.translation.x)
        self.assertAlmostEqual(0, traj3.pose.translation.y)
        self.assertAlmostEqual(0, traj3.pose.rotation.get_degrees())
        self.assertAlmostEqual(0, traj3.pose.curvature)
        self.assertAlmostEqual(0, traj3.pose.dCurvature)
        self.assertAlmostEqual(.5, traj3.t)
        self.assertAlmostEqual(.5, traj3.velocity)
        self.assertAlmostEqual(1, traj3.acceleration)
        self.assertAlmostEqual(6, traj3.index_floor)
        self.assertAlmostEqual(7, traj3.index_ceil)

if __name__ == '__main__':
    unittest.main()