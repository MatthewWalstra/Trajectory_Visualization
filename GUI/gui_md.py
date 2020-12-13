"""CS 108 Trajectory Visualization Project

Contains a class for the main gui

Themes
https://kivymd.readthedocs.io/en/latest/themes/theming/

Navigation bar
https://kivymd.readthedocs.io/en/latest/components/navigation-drawer/

Anchor Layout
https://www.reddit.com/r/kivy/comments/94wqzk/toolbar_stuck_at_bottom_of_screen/


@author: Matthew Walstra (mjw64)
@date: Fall, 2020
"""

from random import uniform, randint

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file


from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock

from kivy.core.window import Window
Window.size = (1920, 1080) # Adjust for your monitor resolution, esc to exit
Window.fullscreen = True
# https://stackoverflow.com/questions/21891217/issue-setting-kivy-to-fullscreen



from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationLayout
from kivymd.uix.list import OneLineAvatarIconListItem, MDList, IRightBodyTouch, ILeftBodyTouch, ILeftBody
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout

from Geometry.pose import to_pose, Pose
from Geometry.rotation import from_degrees
from Trajectory.trajectory import Trajectory, mirror_trajectory

from Util.util import limit2
from Util.jsonIO import JsonIO
from Util.time_delayed_boolean import TimeDelayedBoolean

RADIUS = 15

KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: 'Custom'
    text_color: app.theme_cls.text_color
    on_release: app.set_active_trajectory(self)

    IconLeftWidget:
        id: l_icon
        icon: root.icon
        theme_text_color: 'Custom'
        text_color: root.text_color

    IconRightWidget:
        id: r_icon
        icon: "window-close"
        theme_text_color: 'Custom'
        text_color: root.text_color
        on_press: root.parent.remove_child(root)

<TooltipMDIconButton@MDIconButton+MDTooltip>
<TooltipMDFloatingActionButton@MDFloatingActionButton+MDTooltip>
<TooltipMDCheckbox@MDCheckbox+MDTooltip>
<TooltipMDSwitch@MDSwitch+MDTooltip>

<PointDrawer>:
    on_size:
        self.ids._right_container.width = right_container.width
        self.ids._right_container.x = right_container.width

        self.ids._left_container.width = 900

    _no_ripple_effect: True
        
    
    RightContainer:
        id: right_container

        TooltipMDIconButton:
            id: delte
            icon: "trash-can"
            on_press: app.delete_point(self.parent)
            tooltip_text: "Delete"

    VerticalContainer:
        id: left_container

        GridLayout:
            rows: 1
            cols: 2

            MDIconButton:
                id: up
                icon: "arrow-up"
                on_press: app.up(self.parent.parent)

            MDIconButton:
                id: down
                icon: "arrow-down"
                on_press: app.down(self.parent.parent)
            
        
        MDTextField:
            id: x_coord
            text: self.parent.prev_x
            on_text_validate: self.parent.update_x() 
            hint_text: "X:"
            color_mode: "custom"
            line_color_focus: 1,1,1,1
            
        MDTextField:
            id: y_coord
            text: self.parent.prev_y
            on_text_validate: self.parent.update_y() 
            hint_text: "Y:"
            color_mode: "custom"
            line_color_focus: 1,1,1,1
        
        MDTextField:
            id: theta
            text: self.parent.prev_theta
            on_text_validate: self.parent.update_theta() 
            hint_text: "Heading (Degrees):"
            color_mode: "custom"
            line_color_focus: 1,1,1,1    
    

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDLabel:
        text: "Saved Trajectories"
        font_style: "H4"
        size_hint_y: .05
        height: "36dp"
        halign: "center"
        theme_text_color: "Custom" 
        text_color: app.theme_cls.accent_color
        underline: True

    ScrollView:

        DrawerList:
            id: md_list

<StatLabel>:
    orientation: "vertical"
    size_hint: 1, 1
    md_bg_color: app.theme_cls.bg_dark
    radius: [6, 6, 6, 6]

    MDBoxLayout:
        size_hint: 1, .3
        md_bg_color: app.theme_cls.bg_normal
        radius: [6, 6, 6, 6]
        spacing: 10
        padding: 10
        
        MDLabel:
            id: title
            text: self.parent.parent.text
            theme_text_color: "Custom"
            text_color: app.theme_cls.opposite_bg_darkest
            halign: "left"
            valign: "center"
            
            
    MDLabel:
        id: value
        text: self.parent.value
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        halign: "center"
        font_style: "H3"

<SliderLayout>:
    orientation: "vertical"
    padding: 20,1
    MDLabel:
        id: title
        text: self.parent.text
        theme_text_color: "Custom"
        text_color: app.theme_cls.opposite_bg_darkest
        halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        spacing: 20
        padding: 20
        MDSlider:
            id: slider
            size_hint: 6,1
            value: self.parent.parent.value
            min: self.parent.parent.min_v
            max: self.parent.parent.max_v
            hint: False
            show_off: False
             

        RelativeLayout:
            
            MDTextField:
                id: text
                pos: 0, -12.5
                text: "{:.4f}".format(self.parent.parent.parent.ids.slider.value)
                #size_hint: .4, 1
                on_text_validate: self.parent.parent.parent.test()
                color_mode: "custom"
                line_color_focus: app.theme_cls.opposite_bg_dark
                halign: "center"

Screen:
    NavigationLayout:
        ScreenManager:
            Screen:
                GridLayout:
                    rows: 2
                    cols: 1

                    MDToolbar:
                        title: "Trajectory Visualization"
                        elevation: 10
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["window-close", lambda x: app.close_application()]]
                    
                    GridLayout:
                        rows: 1
                        cols: 2
                        padding: [10,10,10,10]

                        GridLayout:
                            rows: 2
                            cols: 1
                            padding: [0,0,10,0]
                            spacing: [0,10]

                            MDFloatLayout:
                                size: (100,100)
                                
                                radius: [6, 6, 6, 6]
                                md_bg_color: app.theme_cls.bg_darkest
                                
                                RelativeLayout:
                                    pos: -740, -10
                                    
                                    Image:
                                        source: "Images/2020-field.png"
                                        size_hint: 2.2, 2.2
                                        
                                                                        
                            MDFloatLayout:
                                size: (100,100)
                                size_hint: 0, .55
                                radius: [6, 6, 6, 6]
                                md_bg_color: app.theme_cls.bg_darkest
                            
                                GridLayout:
                                    rows: 2
                                    cols: 1
                                    padding: [10,-10,-10,15]

                                    MDFloatLayout:
                                        size_hint: 1, .25
                                        radius: [6, 6, 6, 6]
                                        md_bg_color: app.theme_cls.primary_dark
                                        RelativeLayout:
                                            pos: 20, 300
                                            GridLayout:
                                                rows: 1
                                                cols: 7
                                                padding: [20, 0, 20, 0]
                                                spacing: [15,0]

                                                MDTextField:
                                                    hint_text: "Trajectory Title"
                                                    color_mode: "custom"
                                                    line_color_focus: 1,1,1,1
                                                    on_text_validate: app.update_name(self)

                                                TooltipMDIconButton:
                                                    icon: "sync"
                                                    tooltip_text: "Optimize Trajectory"
                                                    on_press: app.optimize_trajectory()
                                                    
                                                TooltipMDIconButton:
                                                    icon: "animation-play"
                                                    tooltip_text: "Run Animation"
                                                    on_press: app.animate_trajectory()

                                                RelativeLayout:
                                                    MDSlider:
                                                        pos: 0, -7.5
                                                        min: 0
                                                        max: 100
                                                        value: 0
                                                        hint: False
                                                        color: 1,1,1,1
                                                        show_off: False
                                                    

                                                TooltipMDIconButton:
                                                    icon: "flip-vertical"
                                                    tooltip_text: "Mirror Trajectory"
                                                    on_press: app.mirror_trajectory()

                                                TooltipMDSwitch:
                                                    id: reverse
                                                    on_active: app.update_reverse(*args)
                                                    tooltip_text: app.reverse


                                                TooltipMDIconButton:
                                                    icon: "plus"
                                                    tooltip_text: "Add Point" 
                                                    on_press: app.add_point()
                                                
                                    ScrollView:
                                        MDList:
                                            id: point_list
                            
                            
                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint: .5, 0
                            radius: [6, 6, 6, 6]
                            md_bg_color: app.theme_cls.bg_darkest
                            canvas.after:
                                Color:
                                    rgba: app.theme_cls.accent_color
                                Line:
                                    points: app.points
                                    width: 1.7
                                Color:
                                    rgba: app.theme_cls.accent_dark
                                Point:
                                    points: app.control_points
                                    pointsize: 4
                            
                            MDGridLayout:
                                rows: 2
                                cols: 2
                                spacing: 10
                                padding: 10
                                size_hint: 1, .6

                                StatLabel:
                                    id: generation
                                    text: "Generation Time (s)"
                                    value: "0"
                                    
                                StatLabel:
                                    id: drive
                                    text: "Drive Time (s)"
                                    value: "0"

                                StatLabel:
                                    id: length
                                    text: "Trajectory Length (in)"
                                    value: "0"
                                    
                                StatLabel:
                                    id: current_vel
                                    text: "Current Velocity (in/s)"
                                    value: "0"
                                    
                            MDBoxLayout:
                                orientation: "vertical"    
                                size_hint: 1, 1
                                SliderLayout:
                                    id: max_vel
                                    text: "Max Velocity (in/s)"
                                    value: 120
                                    min_v: 0
                                    max_v: 200
                                
                                SliderLayout:
                                    id: max_accel
                                    text: "Max Acceleration (in/s^2)"
                                    value: 180
                                    min_v: 0
                                    max_v: 200

                                SliderLayout:
                                    id: max_centr_accel
                                    text: "Max Centripetal Acceleration (in/s^2)"
                                    value: 120
                                    min_v: 0
                                    max_v: 200

                                SliderLayout:
                                    id: start_vel
                                    text: "Start Velocity (in/s)"
                                    value: 0
                                    min_v: -root.ids.max_vel.ids.slider.value
                                    max_v: root.ids.max_vel.ids.slider.value
                                SliderLayout:
                                    id: end_vel
                                    text: "End Velocity (in/s)"
                                    value: 0
                                    min_v: -root.ids.max_vel.ids.slider.value
                                    max_v: root.ids.max_vel.ids.slider.value

                            
                                RelativeLayout:
                                    TooltipMDFloatingActionButton:
                                        icon: "plus"
                                        
                                        md_bg_color: app.theme_cls.accent_dark
                                        pos: (555,20)
                                        shift_y: 200
                                        tooltip_text: "Add Trajectory"
                                        on_press: app.add_trajectory()

                        

                        


        
        MDNavigationDrawer:
            id: nav_drawer
            
            ContentNavigationDrawer:
                id: content_drawer
'''

class VerticalContainer(ILeftBody, MDGridLayout):
    #adaptive_width = True
    #orientation = "horizontal"
    cols = 4
    rows = 1
    spacing = [30, 0]

    prev_x = StringProperty("0")
    prev_y = StringProperty("0")
    prev_theta = StringProperty("0")

    def initial_update(self, x, y, theta):
        """initial update to PointDrawer"""

        self.prev_x = "{:.3f}".format(x)
        self.prev_y = "{:.3f}".format(y)
        self.prev_theta = "{:.3f}".format(theta)

    def update_x(self):
        """Updates x"""
        try:
            value = float(self.children[2].text)
            value = limit2(value, 0 + RADIUS, 629.25 - RADIUS)
            self.children[2].text = "{:.3f}".format(value)
            # https://stackoverflow.com/questions/32162180/how-can-i-refer-to-kivys-root-widget-from-python
            MDApp.get_running_app().current_trajectory.update_pose(self.get_index(), value, "x") 
            MDApp.get_running_app().update_points()
            
        except ValueError:
            self.children[2].text = self.prev_x
            pass
        self.prev_x = self.children[2].text
        
    
    def update_y(self):
        """Updates y"""
        try:
            value = float(self.children[1].text)
            value = limit2(value, -161.625 + RADIUS, 161.625 - RADIUS)
            self.children[1].text = "{:.3f}".format(value)
            MDApp.get_running_app().current_trajectory.update_pose(self.get_index(), value, "y") 
            MDApp.get_running_app().update_points()
        except ValueError:
            self.children[1].text = self.prev_y
            pass
        self.prev_y = self.children[1].text
    
    def update_theta(self):
        """Updates theta"""
        try:
            value = float(self.children[0].text)
            self.children[0].text = "{:.3f}".format(value)
            MDApp.get_running_app().current_trajectory.update_pose(self.get_index(), value, "theta")
            MDApp.get_running_app().update_points()
        except ValueError:
            self.children[0].text = self.prev_theta
            pass
        self.prev_theta = self.children[0].text

    def get_index(self):
        """Returns the index of the point"""
        c_list = MDApp.get_running_app().screen.ids.point_list.children 
        i = len(c_list) - 1
        for c in c_list:    
            if c.ids.left_container == self:
                return i
            i -= 1
        
    

class RightContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

    def get_index(self):
        """Returns the index of the point"""
        c_list = MDApp.get_running_app().screen.ids.point_list.children 
        i = len(c_list) - 1
        for c in c_list:    
            if c.ids.right_container == self:
                return i
            i -= 1

class PointDrawer(OneLineAvatarIconListItem):

    
    pass
    

class PointNavigationDrawer(MDBoxLayout):
    pass

class ItemDrawer(OneLineAvatarIconListItem):
    icon = StringProperty()
    def get_index(self):
        """Returns index in list"""

        c_list = MDApp.get_running_app().screen.ids.content_drawer.ids.md_list.children 
        i = len(c_list) - 1
        for c in c_list:    
            if c == self:
                return i
            i -= 1

class ContentNavigationDrawer(BoxLayout):
    pass

class StatLabel(MDBoxLayout):
    text = StringProperty("Base")
    value = StringProperty("420")
    pass

class SliderLayout(MDBoxLayout):
    value = NumericProperty()

    text = StringProperty("Base")
    min_v = NumericProperty(0)
    max_v = NumericProperty(200)
    
    def test(self):
        prev_value = self.ids.slider.value
        
        try:
            value = limit2(float(self.ids.text.text), self.ids.slider.min, self.ids.slider.max)
            self.ids.slider.value =  value
            self.ids.text.text = "{:.4f}".format(value)
        except ValueError:
            #self.value = prev_value
            self.ids.text.text = "{:.4f}".format(prev_value)
    pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Changes color of tapped item"""
        # https://kivymd.readthedocs.io/en/latest/components/navigation-drawer/

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        self.current_item = instance_item
    
    def remove_child(self, instance_item):
        """Removes Given Item from the list"""
        if len(self.children) == 1:
            return

        index = instance_item.get_index()
        MDApp.get_running_app().trajectories.pop(index)
        
        self.remove_widget(instance_item)

        if (not instance_item.text_color == self.theme_cls.text_color):
            index = len(self.children) - (1 if index == 0 else index)
            MDApp.get_running_app().set_active_trajectory(self.children[index])

class MainApp(MDApp):
    """Main app class"""

    poses = [to_pose(300, 800, 45), to_pose(400, 900, -45), to_pose(200, 500, 180.0)]
    trajectory = Trajectory(poses=poses)
    points = ListProperty()
    control_points = ListProperty()
    reverse = StringProperty("Forward Trajectory")
    jsonIO = JsonIO()

    trajectories = []
    current_trajectory = Trajectory()

    timeout = .5
    max_vel = TimeDelayedBoolean(0, timeout)
    max_accel = TimeDelayedBoolean(0, timeout)
    max_centr_accel = TimeDelayedBoolean(0, timeout)
    start_vel = TimeDelayedBoolean(0, timeout)
    end_vel = TimeDelayedBoolean(0, timeout)

    prev_reverse = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        """Builds app and sets theme"""
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        return self.screen

    def close_application(self):
        """Callback for closing window"""

        #https://stackoverflow.com/questions/32425831/how-to-exit-a-kivy-application-using-a-button
        self.get_running_app().stop()

    def on_start(self):
        """Runs at start of application: Initializes stuff"""

        # Load Trajectories
        self.trajectories = self.jsonIO.load_trajectories()
        
        # Set Current Trajectory
        update = True
        for t in self.trajectories:
            if t.current:
                self.current_trajectory = t
                update = False

        if update and len(self.trajectories) > 0:
            self.current_trajectory = self.trajectories[0]

        # Add each trajectory
        for trajectory in self.trajectories:
            self.screen.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon="chart-bell-curve-cumulative", text=trajectory.name)
            )

        # Highlight correct Trajectory in drawerlist
        length = len(self.screen.ids.content_drawer.ids.md_list.children) - 1
        item = self.screen.ids.content_drawer.ids.md_list.children[length - self.get_current_index()]
        self.screen.ids.content_drawer.ids.md_list.set_color_item(item)
        
        self.set_constraints()
        self.set_reverse()
        # Sync GUI and Mathematical Poses
        self.update_poses()

        # Schedule saving trajectories every 500 ms
        Clock.schedule_interval(self.save_trajectories, .5)

        # Schedule updating constraints
        Clock.schedule_interval(self.update_constraints, .5)


    def on_stop(self):
        """Save Settings before leaving"""
        self.jsonIO.save_trajectories(self.trajectories)

    def save_trajectories(self, dt):
        """Save Trajectories to JSON Periodically"""
        self.jsonIO.save_trajectories(self.trajectories)

    def update_points(self):
        """Updates trajectory lines"""
        point_list = []
        for point in self.current_trajectory.points:
            point_list.append(self.translate_x(point.pose.translation.x))
            point_list.append(self.translate_y(point.pose.translation.y))
        self.points = point_list
        
        control_points = []
        for pose in self.current_trajectory.poses:
            control_points.append(self.translate_x(pose.translation.x))
            control_points.append(self.translate_y(pose.translation.y))
        self.control_points = control_points

    def translate_x(self, x):
        """Returns x translation from inches to pixels"""
        return x * 1.5 + 174
    
    def translate_y(self, y):
        """Returns y translation from inches to pixels"""
        return y * 1.5 + 689.5

    def update_name(self, instance):
        """Updates name of current trajectory"""
        # Update trajectory name
        self.current_trajectory.name = instance.text

        # Update GUI name
        length = len(self.screen.ids.content_drawer.ids.md_list.children) - 1
        self.screen.ids.content_drawer.ids.md_list.children[length - self.get_current_index()].text = instance.text

    def optimize_trajectory(self):
        """Callback for optimizing current trajectory"""
        self.current_trajectory.optimize_splines()

        self.update_stats()
        # Update points to match optimization
        self.update_points()
    
    def mirror_trajectory(self):
        """Mirrors current Trajectory and adds it as a new trajectory"""
        self.add_trajectory(mirror_trajectory(self.current_trajectory))

    def animate_trajectory(self):
        print("Animate Trajectory")

    def add_point(self):
        """Adds a point to current trajectory"""
        dx = [50.0, 120.0]
        dy = [-30.0, 30.0]
        dt = [-20.0, 20.0]
        # Generate semi - random point (Previous point + dx, dy, dt)
        pose = self.current_trajectory.poses[len(self.current_trajectory.poses) - 1].transform(to_pose(uniform(dx[0], dx[1]), uniform(dy[0], dy[1]), uniform(dt[0], dt[1])))
        pose.translation.x = limit2(pose.translation.x, 15, 614.25)
        pose.translation.y = limit2(pose.translation.y, -146.625, 146.625)

        # Add new point to trajectory
        self.current_trajectory.add_pose(pose)

        # Add new point to GUI
        self.screen.ids.point_list.add_widget(PointDrawer())
        self.screen.ids.point_list.children[0].ids.left_container.initial_update(pose.translation.x, pose.translation.y, pose.rotation.get_degrees())

        
        # Re-draw points to include new pose
        self.update_points()

    def add_trajectory(self, trajectory = None):
        """Adds a trajectory to the trajectory list"""
        
        if trajectory == None:
            # Find a valid trajectory name (Format: Trajectory1, Trajectory2, ... Trajectory100)
            name = "Trajectory" + str(1)
            valid = False
            for i in range(100):
                name = "Trajectory" + str(i + 1)
                valid = False
                for t in self.trajectories:
                    if t.name == name:
                        valid = False
                        break
                    valid = True
                if valid:
                    break
            
            trajectory = Trajectory(name=name, poses=self.random_points(), 
                current=False, reverse=self.current_trajectory.reverse, start_velocity=self.current_trajectory.start_velocity, 
                end_velocity=self.current_trajectory.end_velocity, max_velocity=self.current_trajectory.max_velocity, 
                max_abs_acceleration=self.current_trajectory.max_abs_acceleration, 
                max_centr_acceleration=self.current_trajectory.max_centr_acceleration)

        # Add Trajectory to graphical list    
        item = ItemDrawer(icon="chart-bell-curve-cumulative", text=trajectory.name)
        self.screen.ids.content_drawer.ids.md_list.add_widget(
                item
            )

        # Add Trajectory to mathematical list
        self.trajectories.append(trajectory)

        self.set_active_trajectory(item)

    def random_points(self):
        """Returns list if multiple of pseudo-random poses, else 1 pose"""
        theta_range = [-20.0, 20.0]
        x_range = [15.0, 120.0]
        y_range = [-100.0, 100.0]
        x_delta = [60.0, 100.0]
        y_delta = [-30.0, 30.0]

        theta1 = uniform(theta_range[0], theta_range[1])
        theta2 = uniform(theta_range[0], theta_range[1])
        x = uniform(x_range[0], x_range[1])
        y = uniform(y_range[0], y_range[1])
    
        dx = uniform(x_delta[0], x_delta[1])
        dy = uniform(y_delta[0], y_delta[1])

        return [to_pose(x, y, theta1), to_pose(x + dx, y + dy, theta2)]

    
    def down(self, instance):
        """Callback that moves a trajectory pose down one"""
        index = instance.get_index()

        if index == len(self.current_trajectory.poses) - 1:
            return
        
        self.current_trajectory.move_pose(index, -1)
        self.update_poses()
    
    def up(self, instance):
        """Callback that moves a trajectory pose up one"""
        index = instance.get_index()

        if index == 0:
            return
        
        self.current_trajectory.move_pose(index, 1)
        self.update_poses()
    
    def delete_point(self, instance):
        """Callback to delete trajectory point"""

        if len(self.current_trajectory.poses) == 2:
            return
        self.current_trajectory.remove_pose(instance.get_index())
        self.update_poses()
        
    
    def update_reverse(self, checkbox, value):
        """https://kivymd.readthedocs.io/en/latest/components/selection-controls/"""
        
        slider_state = checkbox.active

        self.reverse = "Reverse Trajectory" if slider_state else "Forward Trajectory"
        
        if self.prev_reverse != slider_state:
            self.current_trajectory.update_reverse(slider_state)

        self.prev_reverse = slider_state

        self.update_stats()
    
    def set_reverse(self):
        """Sets reverse slider"""
        self.screen.ids.reverse.active = self.current_trajectory.reverse



    def set_active_trajectory(self, selected_instance):
        """Updates Current Trajectory"""
        self.screen.ids.content_drawer.ids.md_list.set_color_item(selected_instance)

        # Set all to False
        for t in self.trajectories:
            t.current = False

        # Update Current Trajectory
        self.current_trajectory = self.trajectories[selected_instance.get_index()]
        self.current_trajectory.current = True
        self.update_poses()

        # Update Constraints
        self.set_constraints()
        self.set_reverse()
        

    def get_current_index(self):
        """Returns index of current trajectory"""
        i = 0
        for t in self.trajectories:
            if t == self.current_trajectory:
                return i
            i += 1
    
    def update_poses(self):
        """Updates displayed poses to match current trajectory""" 
        
        # Remove Children
        self.screen.ids.point_list.clear_widgets()
        
        # Re-add Children
        for p in self.current_trajectory.poses:
            self.screen.ids.point_list.add_widget(PointDrawer())
        
        # Update values
        for i in range(len(self.screen.ids.point_list.children)):
            c = self.screen.ids.point_list.children[len(self.screen.ids.point_list.children) - i - 1]
            c.ids.left_container.initial_update(self.current_trajectory.poses[i].translation.x, self.current_trajectory.poses[i].translation.y, self.current_trajectory.poses[i].rotation.get_degrees())
        
        self.update_stats()
        self.update_points()

    def update_stats(self):
        """Updates Generation, drive, and length"""
        self.screen.ids.generation.value = "{:.7f}".format(self.current_trajectory.generation_time)
        self.screen.ids.drive.value = "{:.3f}".format(self.current_trajectory.drive_time)
        self.screen.ids.length.value = "{:.3f}".format(self.current_trajectory.length)

    def update_constraints(self, dt):
        """Periodically called to update trajectory Constraints"""

        # Temporarily Save Values
        max_velocity = self.screen.ids.max_vel.ids.slider.value
        max_acceleration = self.screen.ids.max_accel.ids.slider.value
        max_centr_acceleration = self.screen.ids.max_centr_accel.ids.slider.value
        start_velocity = self.screen.ids.start_vel.ids.slider.value
        end_velocity = self.screen.ids.end_vel.ids.slider.value

        # Check and Update if Necessary
        if self.max_vel.update(max_velocity):
            self.current_trajectory.update_constraint(max_velocity, 0)
        if self.max_accel.update(max_acceleration):
            self.current_trajectory.update_constraint(max_acceleration, 1)
        if self.max_centr_accel.update(max_centr_acceleration):
            self.current_trajectory.update_constraint(max_centr_acceleration, 2)
        if self.start_vel.update(start_velocity):
            self.current_trajectory.update_constraint(start_velocity, 3)
        if self.end_vel.update(end_velocity):
            self.current_trajectory.update_constraint(end_velocity, 4)
        
        self.update_stats()

    def set_constraints(self):
        """Sets constraints"""
        max_velocity = self.current_trajectory.max_velocity
        max_acceleration = self.current_trajectory.max_abs_acceleration
        max_centr_acceleration = self.current_trajectory.max_centr_acceleration
        start_velocity = self.current_trajectory.start_velocity
        end_velocity = self.current_trajectory.end_velocity

        self.max_vel = TimeDelayedBoolean(max_velocity, self.timeout)
        self.max_accel = TimeDelayedBoolean(max_acceleration, self.timeout)
        self.max_centr_accel = TimeDelayedBoolean(max_centr_acceleration, self.timeout)
        self.start_vel = TimeDelayedBoolean(start_velocity, self.timeout)
        self.end_vel = TimeDelayedBoolean(end_velocity, self.timeout)

        self.screen.ids.max_vel.ids.slider.value = max_velocity
        self.screen.ids.max_accel.ids.slider.value = max_acceleration
        self.screen.ids.max_centr_accel.ids.slider.value = max_centr_acceleration
        self.screen.ids.start_vel.ids.slider.value = start_velocity
        self.screen.ids.end_vel.ids.slider.value = end_velocity


MainApp().run()