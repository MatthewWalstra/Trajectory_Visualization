"""CS 108 Trajectory Visualization Project

Contains helper functions

Inspired by: 
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Util/Util.cpp
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Util/Units.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

EPSILON = 1E-12


def limit2(v, min_v, max_v):
    "Returns limited value of v between min_v and max_v"
    # TODO: ValueError if min_v > max_v
    
    if v <= min_v:
        return min_v
    elif v >= max_v:
        return max_v
    return v

def limit(v, lim):
    "Returns limited value of v: + or - lim"
    return limit2(v, -lim, lim)

def interpolate(a, b, x):
    """Returns interpolation between two data points"""
    x = limit2(x, 0.0, 1.0)
    return a + (b-a) * x

def epsilon_equals(a, b, epsilon = EPSILON):
    """Returns True if two floats are equal"""
    return (a - epsilon <= b) and (a + epsilon >= b)




    
    
    