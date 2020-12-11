"""CS 108 Trajectory Visualization Project

Manages json IO for Trajectory class

JSON Tutorial: https://www.programiz.com/python-programming/json

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import json

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file

from Trajectory.trajectory import Trajectory
from Geometry.pose import Pose, to_pose

class JsonIO:
    """Manages json IO for Trajectory class"""

    def __init__(self, path="Trajectory/", name="Saved_Trajectories.json"):
        """Constructs object -- default path is ../Trajectory/Saved_Trajectories.json"""
        self.file_name = path + name

    def load_trajectories(self):
        """Returns list of trajectories from file_name"""
        
        # Initialize data lists
        trajectories = []
        data = {}

        # Read file
        with open(self.file_name, "r") as f:
            data = json.load(f)
        
        # Convert data from dicts/lists to Trajectories
        # Structure:
        # "{"Name1": [
        #       [reverse, start_velocity, end_velocity, max_velocity, max_abs_acceleration, max_centr_acceleration],
        #       [[p1x, p1y, p1theta], [p2x, p2y, p2theta], ... ]
        #       ],
        #   "Name2": [...], 
        # }"
        for name in data.keys():
            #Easier to work with
            tmp_props = data[name][0]
            tmp_poses = data[name][1]
            
            poses = []
            for p in tmp_poses:
                poses.append(to_pose(p[0], p[1], p[2]))

            trajectories.append(Trajectory(name, poses, tmp_props[0], tmp_props[1], tmp_props[2], tmp_props[3], tmp_props[4], tmp_props[5], tmp_props[6]))
        
        return trajectories

    def save_trajectories(self, trajectories):
        """Saves list of trajectories to JSON"""
        data = {}
        for trajectory in trajectories:
            data[trajectory.name] = [self.properties_to_json(trajectory), self.points_to_json(trajectory)]
        
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def properties_to_json(self, trajectory):
        """Helper method to convert Trajectory properties to list"""
        return [trajectory.current, trajectory.reverse, trajectory.start_velocity, 
            trajectory.end_velocity, trajectory.max_velocity, 
            trajectory.max_abs_acceleration, trajectory.max_centr_acceleration]

    def points_to_json(self, trajectory):
        """Helper method to convert Trajectory points to list"""

        data = []

        # Add each point as a list
        for p in trajectory.poses:
            tmp = [p.translation.x, p.translation.y, p.rotation.get_degrees()]
            data.append(tmp)

        return data

if __name__ == "__main__":
    poses = []
    poses.append(to_pose())
    poses.append(to_pose(100, 300, 40))
    poses.append(to_pose(320, 350, 135))
    poses.append(to_pose(90, -100, -180))
    poses.append(to_pose(400, 50, 90))

    trajectory = Trajectory