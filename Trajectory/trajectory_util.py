"""CS 108 Trajectory Visualization Project

Module for generating a trajectory

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/spline/SplineGenerator.java
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/trajectory/timing/TimingUtil.java

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math

from Geometry.pose import Pose
from Geometry.rotation import Rotation
from Geometry.translation import Translation
from Geometry.trajectory_point import TrajectoryPoint

from Util.util import epsilon_equals, EPSILON

MAXDX = 2.0 # inches
MAXDY = 0.05 # inches
MAXDTHETA = 0.1 # radians
MINSAMPLESIZE = 1

# TODO: add as label variable
MAXCENTRIPETALACCELERATION = 120

def parameterize_spline(spline, max_dx=MAXDX, max_dy=MAXDY, max_dtheta=MAXDTHETA, t0=0, t1=1):
    """Parameterizes a single spline: returns a list of TrajectoryPoints"""
    rv = []
    rv.append(TrajectoryPoint(spline.get_pose(0.0)))
    dt = (t1 - t0)
    for t in range(1):
        get_segment_arc(spline, rv, t / MINSAMPLESIZE, (t + dt) / MINSAMPLESIZE, max_dx, max_dy, max_dtheta)
    return rv

def parameterize_splines(splines, max_dx=MAXDX, max_dy=MAXDY, max_dtheta=MAXDTHETA):
    """Paramaterizes a list of splines: returns a list TrajectoryPoints"""
    
    rv = []
    if len(splines) == 0:
        return rv
    
    # Add first point because later the first point is removed for each spline
    rv.append(TrajectoryPoint(splines[0].get_pose(0.0)))
    for s in splines:
        
        # Parameterize spline and remove first point to avoid repeats
        samples = parameterize_spline(s, max_dx, max_dy, max_dtheta)
        samples.pop(0)
        rv.extend(samples)
    return rv
    

def get_segment_arc(spline, points, t0, t1, max_dx, max_dy, max_dtheta):
    """Recursively adds a TrajectoryPoint to the list if the transformation is less than the max allowable"""
    p0 = spline.get_point(t0)
    p1 = spline.get_point(t1)
    r0 = spline.get_heading(t0)
    r1 = spline.get_heading(t1)

    transformation = Pose(Translation(p1.x - p0.x, p1.y - p0.y).rotate(r0.inverse()), r1.rotate(r0.inverse())) 
    twist = Pose().log(transformation)
    
    # Recursively divide segment arc in half until twist is smaller than max
    if (twist.dy > max_dy or twist.dx > max_dx or twist.dtheta > max_dtheta): 
        get_segment_arc(spline, points, t0, (t0 + t1) / 2.0, max_dx, max_dy, max_dtheta)
        get_segment_arc(spline, points, (t0 + t1) / 2.0, t1, max_dx, max_dy, max_dtheta)
    else:
        points.append(TrajectoryPoint(spline.get_pose(t1)))

def time_parameterize_trajectory(reverse, trajectory_points, start_velocity, end_velocity, max_velocity, max_abs_acceleration):
    """Time parameterizes given TrajectoryPoints"""
    
    # Forward pass
    predecessor = trajectory_points[0]
    predecessor.distance = 0.0
    predecessor.velocity = start_velocity
    predecessor.min_acceleration = -max_abs_acceleration
    predecessor.max_acceleration = max_abs_acceleration

    for i in range(1, len(trajectory_points)):
        
        # Update state
        state = trajectory_points[i]

        ds = state.pose.distance(predecessor.pose)
        state.distance = ds + predecessor.distance


        # Enforce global max velocity and reachable velocity by acceleration limit
        state.velocity = min(max_velocity, math.sqrt(predecessor.velocity * predecessor.velocity + 2.0 * predecessor.max_acceleration * ds))

        # Enforce velocity constraints
        state.velocity = min(get_max_velocity(state, max_velocity), state.velocity)

        state.max_acceleration = max_abs_acceleration
        state.min_acceleration = -max_abs_acceleration

        predecessor = state
    
    # Backwards pass
    successor = trajectory_points[len(trajectory_points) - 1]
    successor.velocity = end_velocity
    successor.min_acceleration = -max_abs_acceleration
    successor.max_acceleration = max_abs_acceleration
    for i in range(len(trajectory_points)-2, 0, -1):
        state = trajectory_points[i]
        ds = state.distance - successor.distance

        # calculate new max velocity (will only lower the velocity)
        new_max_velocity = math.sqrt(successor.velocity * successor.velocity + 2.0 * successor.min_acceleration * ds)
        if (new_max_velocity >= state.velocity):
            successor = state
            continue

        state.velocity = new_max_velocity

        successor = state

    t = 0.0
    s = 0.0
    v = 0.0
    for i in range(len(trajectory_points)):
        state = trajectory_points[i]
        ds = state.distance - s
        accel = 0.0
        dt = 0.0

        if (i > 0):
            accel = (state.velocity * state.velocity - v * v) / (2.0 * ds)
            trajectory_points[i - 1].acceleration = (-accel if reverse else accel)
            if (abs(accel) > EPSILON):
                dt = (state.velocity - v) / accel
            elif (abs(v) > EPSILON):
                dt = ds / v
            else:
                dt = 0
        t += dt

        v = state.velocity
        s = state.distance

        state.t = t
        state.velocity = -v if reverse else v
        state.acceleration = -accel if reverse else accel
        state.index_floor = i
        state.index_ceil = i

def get_max_velocity(trajectory_point, max_velocity):
    """Returns the max velocity for a given trajectory state"""
    return min(get_max_drivetrain_velocity(trajectory_point, max_velocity), get_max_centripetal_velocity(trajectory_point))

def get_max_drivetrain_velocity(trajectory_point, max_velocity):
    """Returns the max absolute velocity for a tank drive"""
    
    # Going straight
    if epsilon_equals(trajectory_point.pose.curvature, 0.0):
        return max_velocity
    
    # Turning in place
    if math.isinf(trajectory_point.pose.curvature):
        return 0.0

    # right speed if left at max velocity
    right_left_max = max_velocity * (trajectory_point.pose.curvature + 1) / (1.0 - trajectory_point.pose.curvature)
    if abs(right_left_max) <= max_velocity:
        return (max_velocity + right_left_max) / 2.0 

    # left speed if right at max velocity
    left_right_max = max_velocity * (1 - trajectory_point.pose.curvature) / (1.0 + trajectory_point.pose.curvature)
    return (max_velocity + left_right_max) / 2.0
        

def get_max_centripetal_velocity(trajectory_point):
    """Returns max centripetal velocity"""
    if epsilon_equals(trajectory_point.pose.curvature, 0.0):
        return 1e4
    return math.sqrt(abs(MAXCENTRIPETALACCELERATION / trajectory_point.pose.curvature))