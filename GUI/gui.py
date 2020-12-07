"""CS 108 Trajectory Visualization Project

Contains a class for the main gui

@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import ListProperty

from kivy.lang import Builder

from Geometry.pose import to_pose, Pose
from Trajectory.trajectory import Trajectory


Builder.load_string('''

<PointWidget>
    cols = 7

<RootWidget>
    rows:2
    cols:2
    Image:
        source: "Images/2020-Field.png"
        size_hint: .5, .5
        canvas.after:
            Color:
                rgba: .204, .8, 1.0, 1.0
            Line:
                points: root.points
                width: 1.7  
             

        
    Button:
        text: 'Hello1'
        size_hint: .1, .1
        on_press: root.points = [400, 400, 300, 200, 200, 400, 300, 300, 400, 500]
    Button:
        text: 'Hello2'
        size_hint: .1, .1
        on_press: root.points = [500, 500, 500, 100, 200, 0, 300, 300, 400, 700]
    Button:
        text: 'Hello3'
        size_hint: .1, .1
        on_press: root.points = root.trajectory_to_list(root.trajectory)
        

''')

class RootWidget(GridLayout):
    #points = ListProperty([(500, 500),
    #                      [500, 100, 200, 0],
    #                      [300, 300, 400, 700]])
    points = ListProperty([500, 500, 500, 100, 200, 0, 300, 300, 400, 700])
    poses = [to_pose(300, 300, 45), to_pose(400, 500, 90), to_pose(600, 500, 0.0)]
    trajectory = Trajectory(poses=poses)

    def trajectory_to_list(self, trajectory):
        point_list = []
        for point in trajectory.points:
            point_list.append(point.pose.translation.x)
            point_list.append(point.pose.translation.y)
        return point_list




class MainApp(App):

    def build(self):
        root = RootWidget()
        
        return root

if __name__ == '__main__':
    MainApp().run()