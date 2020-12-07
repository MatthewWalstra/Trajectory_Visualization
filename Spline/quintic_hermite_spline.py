"""CS 108 Trajectory Visualization Project

Class contains quintic hermite spline and helper methods

Inspired by: 
https://github.com/Team254/FRC-2018-Public/blob/master/src/main/java/com/team254/lib/spline/QuinticHermiteSpline.java
https://github.com/SCsailors/2020RobotCode/blob/master/src/main/cpp/lib/Splines/QuinticHermiteSpline.cpp

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import math

from Geometry.pose import Pose, to_pose
from Geometry.rotation import Rotation, from_degrees
from Geometry.translation import Translation

from Util.util import epsilon_equals

MAXITERATIONS = 100
EPSILON = 1E-5
STEPSIZE = 1.0
MINDELTA = .001

def create_quintic_splines(poses):
    """Helper function that returns a list of QuinticHermiteSplines"""
    splines = []
    for i in range(len(poses) - 1):
        splines.append(create_quintic_spline(poses[i], poses[i + 1]))

    return splines

def create_quintic_spline(p0=Pose(), p1=Pose()):
    """Helper function to return a QuinticHermiteSpline object from 2 Poses"""
    scale = 1.2 * p0.translation.distance(p1.translation)
    return QuinticHermiteSpline(p0.translation.x, p1.translation.x, p0.rotation.cos_angle * scale, p1.rotation.cos_angle * scale, 0, 0, 
        p0.translation.y, p1.translation.y, p0.rotation.sin_angle * scale, p1.rotation.sin_angle * scale, 0, 0)

def sum_dCurvature2(splines):
    """Returns the sum of the dCurvature2 for a list of splines"""
    total = 0.0
    for s in splines:
        total += s.sum_dCurvature2()
    return total

def optimize_spline(splines):
    """Returns optimized dCurvature2 and optimizes """
    count = 0
    prev = sum_dCurvature2(splines)
    while (count < MAXITERATIONS):

        # Run optimization iteration and recalculate dCurvature2
        run_optimization_iteration(splines)
        current = sum_dCurvature2(splines)

        # Exit if delta is less than MINDELTA
        if ( (prev - current) < MINDELTA ):
            return current
        
        prev = current
        count += 1
    return prev

def run_optimization_iteration(splines):
    """Runs one optimization iteration on list of splines"""
    if (len(splines) <= 1):
        return
    
    control_points = []
    magnitude = 0.0

    for i in range(len(splines) - 1):

        if (splines[i].get_start_pose().is_collinear(splines[i+1].get_start_pose())) or (splines[i].get_end_pose().is_collinear(splines[i+1].get_end_pose())):
            # Skip optimization if consecutive splines are collinear
            continue

        original = sum_dCurvature2(splines)
        tmp1 = splines[i]
        tmp2 = splines[i+1]

        control_points.append(ControlPoint())

        # Calculate partial derivatives of sum_dCurvature2
        # Partial x
        splines[i] = QuinticHermiteSpline(tmp1.x0, tmp1.x1, tmp1.dx0, tmp1.dx1, tmp1.ddx0, tmp1.ddx1 + EPSILON, tmp1.y0, tmp1.y1, tmp1.dy0, tmp1.dy1, tmp1.ddy0, tmp1.ddy1)
        splines[i + 1] = QuinticHermiteSpline(tmp2.x0, tmp2.x1, tmp2.dx0, tmp2.dx1, tmp2.ddx0 + EPSILON, tmp2.ddx1, tmp2.y0, tmp2.y1, tmp2.dy0, tmp2.dy1, tmp2.ddy0, tmp2.ddy1)
        control_points[i].ddx = (sum_dCurvature2(splines) - original) / EPSILON

        # Partial y
        splines[i] = QuinticHermiteSpline(tmp1.x0, tmp1.x1, tmp1.dx0, tmp1.dx1, tmp1.ddx0, tmp1.ddx1, tmp1.y0, tmp1.y1, tmp1.dy0, tmp1.dy1, tmp1.ddy0, tmp1.ddy1 + EPSILON)
        splines[i + 1] = QuinticHermiteSpline(tmp2.x0, tmp2.x1, tmp2.dx0, tmp2.dx1, tmp2.ddx0, tmp2.ddx1, tmp2.y0, tmp2.y1, tmp2.dy0, tmp2.dy1, tmp2.ddy0 + EPSILON, tmp2.ddy1)
        control_points[i].ddy = (sum_dCurvature2(splines) - original) / EPSILON

        # Reset splines
        splines[i] = tmp1
        splines[i+1] = tmp2
        magnitude += control_points[i].ddx * control_points[i].ddx + control_points[i].ddy * control_points[i].ddy
    
    magnitude = math.sqrt(magnitude)

    # Minimize along the direction of the gradient by calculating 3 points along it.
    p2 = Translation(0, sum_dCurvature2(splines)) # Middle point is the current location

    for i in range(len(splines) - 1):
        if (splines[i].get_start_pose().is_collinear(splines[i+1].get_start_pose())) or (splines[i].get_end_pose().is_collinear(splines[i+1].get_end_pose())):
            # Skip optimization if consecutive splines are collinear
            continue

        # Normalize to step size
        control_points[i].ddx *= STEPSIZE / magnitude
        control_points[i].ddy *= STEPSIZE / magnitude

        # Move opposite the gradient by STEPSIZE
        splines[i].ddx1 -= control_points[i].ddx
        splines[i].ddy1 -= control_points[i].ddy

        splines[i + 1].ddx0 -= control_points[i].ddx
        splines[i + 1].ddy0 -= control_points[i].ddy

        # Recompute spline coefficients to account for new 2nd derivatives
        splines[i].compute_coefficients()
        splines[i + 1].compute_coefficients()
    
    p1 = Translation(-STEPSIZE, sum_dCurvature2(splines))

    for i in range(len(splines) - 1):
        if (splines[i].get_start_pose().is_collinear(splines[i+1].get_start_pose())) or (splines[i].get_end_pose().is_collinear(splines[i+1].get_end_pose())):
            # Skip optimization if consecutive splines are collinear
            continue

        # Move in direction of the gradient by 2 * STEPSIZE (return to original position and 1 more)
        splines[i].ddx1 += 2 * control_points[i].ddx
        splines[i].ddy1 += 2 * control_points[i].ddy

        splines[i + 1].ddx0 += 2 * control_points[i].ddx
        splines[i + 1].ddy0 += 2 * control_points[i].ddy

        # Recompute spline coefficients to account for new 2nd derivatives
        splines[i].compute_coefficients()
        splines[i + 1].compute_coefficients()

    p3 = Translation(STEPSIZE, sum_dCurvature2(splines))

    step_size = fit_parabola(p1, p2, p3) # Approximate step size to minimize sum_dCurvature2 along the grandient

    for i in range(len(splines) - 1):
        if (splines[i].get_start_pose().is_collinear(splines[i+1].get_start_pose())) or (splines[i].get_end_pose().is_collinear(splines[i+1].get_end_pose())):
            # Skip optimization if consecutive splines are collinear
            continue

        # Normalize to step size (+1 to offset for the final transformation to find p3)
        control_points[i].ddx *= 1 + step_size / STEPSIZE
        control_points[i].ddy *= 1 + step_size / STEPSIZE

        splines[i].ddx1 += control_points[i].ddx
        splines[i].ddy1 += control_points[i].ddy

        splines[i + 1].ddx0 += control_points[i].ddx
        splines[i + 1].ddy0 += control_points[i].ddy

        # Recompute spline coefficients to account for new 2nd derivatives
        splines[i].compute_coefficients()
        splines[i + 1].compute_coefficients()




def fit_parabola(p1, p2, p3):
    """Returns the x-coordinate of the vertex of the parabola"""
    a = p3.x * (p2.y - p1.y) + p2.x * (p1.y - p3.y) + p1.x * (p3.y - p2.y)
    b = p3.x * p3.x * (p1.y - p2.y) + p2.x * p2.x * (p3.y - p1.y) + p1.x * p1.x * (p2.y - p3.y)
    return -b/(2 * a)

class QuinticHermiteSpline:
    """Contains QuinticHermiteSpline"""

    # Variables for optimization

    SAMPLES = 100
    
    def __init__(self, x0=0, x1=0, dx0=0, dx1=0, ddx0=0, ddx1=0, y0=0, y1=0, dy0=0, dy1=0, ddy0=0, ddy1=0):
        """Updates coefficients for optimization and construction"""
        self.x0 = x0
        self.x1 = x1
        self.dx0 = dx0
        self.dx1 = dx1
        self.ddx0 = ddx0
        self.ddx1 = ddx1

        self.y0 = y0
        self.y1 = y1
        self.dy0 = dy0
        self.dy1 = dy1
        self.ddy0 = ddy0
        self.ddy1 = ddy1

        self.compute_coefficients()

    def compute_coefficients(self):
        """Computes Spline coefficients"""
        self.Ax = -6 * self.x0 - 3 * self.dx0 - .5 * self.ddx0 + .5 * self.ddx1 - 3 * self.dx1 + 6 * self.x1
        self.Bx = 15 * self.x0 + 8 * self.dx0 + 1.5 * self.ddx0 - self.ddx1 + 7 * self.dx1 - 15 * self.x1
        self.Cx = -10 * self.x0 - 6 * self.dx0 - 1.5 * self.ddx0 + .5 * self.ddx1 - 4 * self.dx1 + 10 * self.x1
        self.Dx = .5 * self.ddx0
        self.Ex = self.dx0
        self.Fx = self.x0

        self.Ay = -6 * self.y0 - 3 * self.dy0 - .5 * self.ddy0 + .5 * self.ddy1 - 3 * self.dy1 + 6 * self.y1
        self.By = 15 * self.y0 + 8 * self.dy0 + 1.5 * self.ddy0 - self.ddy1 + 7 * self.dy1 - 15 * self.y1
        self.Cy = -10 * self.y0 - 6 * self.dy0 - 1.5 * self.ddy0 + .5 * self.ddy1 - 4 * self.dy1 + 10 * self.y1
        self.Dy = .5 * self.ddy0
        self.Ey = self.dy0
        self.Fy = self.y0

    def get_start_pose(self):
        """Returns start pose of the spline"""
        return Pose(Translation(self.x0, self.y0), Rotation(self.dx0, self.dy0, True))

    def get_end_pose(self):
        """Returns end pose of the spline"""
        return Pose(Translation(self.x1, self.y1), Rotation(self.dx1, self.dy1, True))

    def get_point(self, t):
        """Returns Translation at t (from 0 to 1)"""
        x = (self.Ax * t * t * t * t * t) + (self.Bx * t * t * t * t) + (self.Cx * t * t * t) + (self.Dx * t * t) + (self.Ex * t) + (self.Fx)
        y = (self.Ay * t * t * t * t * t) + (self.By * t * t * t * t) + (self.Cy * t * t * t) + (self.Dy * t * t) + (self.Ey * t) + (self.Fy)
        return Translation(x, y)

    def dx(self, t):
        """Returns derivative of x component at t"""
        return 5 * (self.Ax * t * t * t * t) + 4 * (self.Bx * t * t * t) + 3 * (self.Cx * t * t) + 2 * (self.Dx * t) + (self.Ex)
    
    def dy(self, t):
        """Returns derivative of y component at t"""
        return 5 * (self.Ay * t * t * t * t) + 4 * (self.By * t * t * t) + 3 * (self.Cy * t * t) + 2 * (self.Dy * t) + (self.Ey)

    def ddx(self, t):
        """Returns second derivative of x component at t"""
        return 20 * (self.Ax * t * t * t) + 12 * (self.Bx * t * t) + 6 * (self.Cx * t) + 2 * (self.Dx)

    def ddy(self, t):
        """Returns second derivative of y component at t"""
        return 20 * (self.Ay * t * t * t) + 12 * (self.By * t * t) + 6 * (self.Cy * t) + 2 * (self.Dy)
    
    def dddx(self, t):
        """Returns third derivate of x component at t"""
        return 60 * (self.Ax * t * t) + 24 * (self.Bx * t) + 6 * (self.Cx)

    def dddy(self, t):
        """Returns third derivate of y component at t"""
        return 60 * (self.Ay * t * t) + 24 * (self.By * t) + 6 * (self.Cy)

    def get_velocity(self, t):
        """Returns velocity of the spline at t"""
        return math.hypot(self.dx(t), self.dy(t))
    
    def get_curvature(self, t):
        """Returns the curvature of the spline at t"""

        num = (self.dx(t) * self.ddy(t) - self.ddx(t) * self.dy(t))
        # Checks if dx(t) and dy(t) are zero to avoid ZeroDivisionError
        if epsilon_equals(self.dx(t), 0) and epsilon_equals(self.dy(t), 0):
            return math.inf * (-1.0 if num < 0 else 1.0)
        
        return num / ((self.dx(t) * self.dx(t) + self.dy(t) * self.dy(t)) * math.sqrt(self.dx(t) * self.dx(t) + self.dy(t) * self.dy(t)))

    def get_dCurvature(self, t):
        """Returns dCurvature of the spline at t"""
        
        # Checks if dx(t) and dy(t) are zero to avoid ZeroDivisionError
        if epsilon_equals(self.dx(t), 0) and epsilon_equals(self.dy(t), 0):
            return 0

        dx2dy2 = self.dx(t) * self.dx(t) + self.dy(t) * self.dy(t)
        num = (self.dx(t) * self.dddy(t) - self.dddx(t) * self.dy(t)) * dx2dy2 - 3 * (self.dx(t) * self.ddy(t) - self.ddx(t) * self.dy(t)) * (self.dx(t) * self.ddx(t) + self.dy(t) * self.ddy(t))
        return num/(dx2dy2 * dx2dy2 * math.sqrt(dx2dy2))

    def get_dCurvature2(self, t):
        """Returns dCurvature_ds squared at t"""
        return self.get_dCurvature(t) * self.get_dCurvature(t)

    def get_heading(self, t):
        """Returns heading of the spline at t"""
        return Rotation(self.dx(t), self.dy(t), True)

    def get_pose(self, t):
        """Returns pose of the spline at t"""
        
        # Avoid ZeroDivisionError
        dCurvature_ds = 0 if epsilon_equals(self.get_velocity(t), 0) else self.get_dCurvature(t) / self.get_velocity(t)
        
        return Pose(self.get_point(t), self.get_heading(t), self.get_curvature(t), dCurvature_ds)

    def sum_dCurvature2(self):
        """Returns the sum of the dCurvature2 of a spline for optimization"""
        dt = 1.0 / self.SAMPLES
        total = 0.0
        for i in range(self.SAMPLES):
            total += dt * self.get_dCurvature2(i * dt)
        return total

class ControlPoint:
    """ControlPoint for optimization"""
    ddx = 0
    ddy = 0
    def __init__(self):
        """Constructs a ControlPoint object"""
        pass