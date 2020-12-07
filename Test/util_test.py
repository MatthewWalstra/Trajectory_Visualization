"""CS 108 Trajectory Visualization Project

Unittests for util

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

from Util.util import limit2, limit, interpolate, epsilon_equals

class UtilTest(unittest.TestCase):
    """Class to test util"""

    def test_util(self):
        """Tests util methods"""

        # Test limit2
        self.assertAlmostEqual(1.0, limit2(1.0, -2.0, 4.0))
        self.assertAlmostEqual(-0.0, limit2(1.0, -2.0, -0.0))
        self.assertAlmostEqual(-2.0, limit2(-5.0, -2.0, -0.0))

        # Test limit
        self.assertAlmostEqual(1.0, limit(1.0, 4.0))
        self.assertAlmostEqual(4.0, limit(6.0, 4.0))
        self.assertAlmostEqual(-3.0, limit(-5.0, 3.0))

        # Test interpolate
        self.assertAlmostEqual(1.0, interpolate(.0, 4.0, .25))
        self.assertAlmostEqual(1.0, interpolate(-1, 4.0, .4))
        self.assertAlmostEqual(1.0, interpolate(4.0, 0.0, .75))

        # Test epsilon_equals
        self.assertTrue(epsilon_equals(1, 1.5, .5))
        self.assertTrue(epsilon_equals(2, 1.5, .5))
        self.assertFalse(epsilon_equals(1, 1.5))

if __name__ == '__main__':
    unittest.main()