"""CS 108 Trajectory Visualization Project

Unittests for Spline

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/test/java/com/team254/lib/spline/QuinticHermiteOptimizerTest.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/test/cpp/lib/Spline/QuinticHermiteSplineTest.cpp
https://github.com/SCsailors/2020RobotCode/blob/master/src/test/cpp/lib/Spline/QuinticSplineTest.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import unittest
import math
import time

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file


from Spline.quintic_hermite_spline import QuinticHermiteSpline, optimize_spline, fit_parabola, create_quintic_spline
from Geometry.translation import Translation
from Geometry.rotation import Rotation, from_degrees
from Geometry.pose import Pose, to_pose

class SplineTest(unittest.TestCase):
    """Unittests for Spline folder"""

    def test_fit_parabola(self):
        """Tests fit_parabola"""

        # Symmetric downwards parabola (vertex x coordinate at 0)
        x = fit_parabola(Translation(-2.0, 2.0), Translation(0.0, 4.0), Translation(2.0, 2.0))

        self.assertAlmostEqual(0, x)

    def test_spline_construction(self):
        """Tests Quintic Hermite Spline construction"""

        s = create_quintic_spline()

        self.assertAlmostEqual(0, s.get_start_pose().translation.x)
        self.assertAlmostEqual(0, s.get_start_pose().translation.y)
        self.assertAlmostEqual(0, s.get_start_pose().rotation.get_degrees())

        self.assertAlmostEqual(0, s.get_end_pose().translation.x)
        self.assertAlmostEqual(0, s.get_end_pose().translation.y)
        self.assertAlmostEqual(0, s.get_end_pose().rotation.get_degrees())

        self.assertAlmostEqual(0, s.get_velocity(0))
        self.assertAlmostEqual(0, s.get_curvature(0))
        self.assertAlmostEqual(0, s.get_dCurvature(0))
        self.assertAlmostEqual(0, s.get_heading(0).get_degrees())
        self.assertAlmostEqual(0, s.get_point(0).x)
        self.assertAlmostEqual(0, s.get_point(0).y)
        self.assertAlmostEqual(0, s.get_pose(0).translation.x)
        self.assertAlmostEqual(0, s.get_pose(0).translation.y)
        self.assertAlmostEqual(0, s.get_pose(0).rotation.get_degrees())

        self.assertAlmostEqual(0, s.get_velocity(1))
        self.assertAlmostEqual(0, s.get_curvature(1))
        self.assertAlmostEqual(0, s.get_dCurvature(1))
        self.assertAlmostEqual(0, s.get_heading(1).get_degrees())
        self.assertAlmostEqual(0, s.get_point(1).x)
        self.assertAlmostEqual(0, s.get_point(1).y)
        self.assertAlmostEqual(0, s.get_pose(1).translation.x)
        self.assertAlmostEqual(0, s.get_pose(1).translation.y)
        self.assertAlmostEqual(0, s.get_pose(1).rotation.get_degrees())

        s = create_quintic_spline(p1=to_pose(3.0, 4.0, 90.0))
        self.assertAlmostEqual(0, s.get_start_pose().translation.x)
        self.assertAlmostEqual(0, s.get_start_pose().translation.y)
        self.assertAlmostEqual(0, s.get_start_pose().rotation.get_degrees())

        self.assertAlmostEqual(3.0, s.get_end_pose().translation.x)
        self.assertAlmostEqual(4.0, s.get_end_pose().translation.y)
        self.assertAlmostEqual(90.0, s.get_end_pose().rotation.get_degrees())

        self.assertAlmostEqual(6.0, s.get_velocity(0))
        self.assertAlmostEqual(0, s.get_curvature(0))
        #self.assertAlmostEqual(0, s.get_dCurvature(0))
        self.assertAlmostEqual(0, s.get_heading(0).get_degrees())
        self.assertAlmostEqual(0, s.get_point(0).x)
        self.assertAlmostEqual(0, s.get_point(0).y)
        self.assertAlmostEqual(0, s.get_pose(0).translation.x)
        self.assertAlmostEqual(0, s.get_pose(0).translation.y)
        self.assertAlmostEqual(0, s.get_pose(0).rotation.get_degrees())

        self.assertAlmostEqual(6.0, s.get_velocity(1))
        self.assertAlmostEqual(0, s.get_curvature(1))
        #self.assertAlmostEqual(0, s.get_dCurvature(1))
        self.assertAlmostEqual(90, s.get_heading(1).get_degrees())
        self.assertAlmostEqual(3, s.get_point(1).x)
        self.assertAlmostEqual(4, s.get_point(1).y)
        self.assertAlmostEqual(3, s.get_pose(1).translation.x)
        self.assertAlmostEqual(4, s.get_pose(1).translation.y)
        self.assertAlmostEqual(90, s.get_pose(1).rotation.get_degrees())
    
    def test_optimization(self):
        """Tests Spline optimization"""

        # Optimization test 1
        p1 = to_pose(0.0, 100.0, 270.0)
        p2 = to_pose(50.0, 0.0, 0.0)
        p3 = to_pose(100.0, 100.0, 90.0)
        
        splines = []
        splines.append(create_quintic_spline(p1, p2))
        splines.append(create_quintic_spline(p2, p3))

        start_time = time.perf_counter()
        self.assertTrue(optimize_spline(splines) < 0.014)
        print("Optimization time: {:.6}s".format(time.perf_counter() - start_time))
        
        # Optimization test 2
        p4 = to_pose(degrees=90.0)
        p5 = to_pose(0.0, 50.0, 0.0)
        p6 = to_pose(100.0, 0.0, 90.0)
        p7 = to_pose(100.0, 100.0, 0.0)
        splines1 = []
        splines1.append(create_quintic_spline(p4, p5))
        splines1.append(create_quintic_spline(p5, p6))
        splines1.append(create_quintic_spline(p6, p7))

        start_time = time.perf_counter()
        self.assertTrue(optimize_spline(splines1) < 0.16)
        print("Optimization time: {:.6}s".format(time.perf_counter() - start_time))

        # Optimization test 3
        p8 = to_pose()
        p9 = to_pose(50.0, 0.0, 0.0)
        p10 = to_pose(100.0, 50.0, 45.0)
        p11 = to_pose(150.0, 0.0, 270.0)
        p12 = to_pose(150.0, -50.0, 270.0)
        
        splines2 = []
        splines2.append(create_quintic_spline(p8, p9))
        splines2.append(create_quintic_spline(p9, p10))
        splines2.append(create_quintic_spline(p10, p11))
        splines2.append(create_quintic_spline(p11, p12))

        start_time = time.perf_counter()
        self.assertTrue(optimize_spline(splines1) < 0.16)
        print("Optimization time: {:.6}s".format(time.perf_counter() - start_time))


if __name__ == '__main__':
    unittest.main()
