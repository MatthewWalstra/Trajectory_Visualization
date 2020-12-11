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

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file


from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty


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
from Trajectory.trajectory import Trajectory

from Util.util import limit2
from Util.jsonIO import JsonIO

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
            on_press: app.trash()
            tooltip_text: "Delete"

    VerticalContainer:
        id: left_container

        GridLayout:
            rows: 1
            cols: 2

            TooltipMDIconButton:
                id: up
                icon: "arrow-up"
                on_press: app.up()
                tooltip_text: "Move Up"

            TooltipMDIconButton:
                id: down
                icon: "arrow-down"
                on_press: app.down()
                tooltip_text: "Move Down"
            
        
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
                                                    on_active: app.on_checkbox_active(*args)
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
                            
                            MDGridLayout:
                                rows: 2
                                cols: 2
                                spacing: 10
                                padding: 10
                                size_hint: 1, .6

                                StatLabel:
                                    id: generation
                                    text: "Generation Time"
                                    value: "0"
                                    
                                StatLabel:
                                    id: drive
                                    text: "Drive Time"
                                    value: "0"

                                StatLabel:
                                    id: length
                                    text: "Trajectory Length"
                                    value: "0"
                                    
                                StatLabel:
                                    id: current_vel
                                    text: "Current Velocity"
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

        self.prev_x = x
        self.prev_y = y
        self.prev_theta = theta

    def update_x(self):
        """Updates x"""
        try:
            # TODO: Update actual Trajectory List
            value = float(self.children[2].text)
            # https://stackoverflow.com/questions/32162180/how-can-i-refer-to-kivys-root-widget-from-python

            print("{}, {:.2f}".format(self.get_index(), value))

            MDApp.get_running_app().current_trajectory.poses[self.get_index()].translation.x = value 
            
            
            
        except ValueError:
            self.children[2].text = self.prev_x
            pass
        self.prev_x = self.children[2].text
        
    
    def update_y(self):
        """Updates y"""
        try:
            # TODO: Update actual Trajectory List
            value = float(self.children[1].text)
            MDApp.get_running_app().current_trajectory.poses[self.get_index()].translation.y = value 
            print("{}, {:.2f}".format(self.get_index(), value))
        except ValueError:
            self.children[1].text = self.prev_y
            pass
        self.prev_y = self.children[1].text
    
    def update_theta(self):
        """Updates theta"""
        try:
            # TODO: Update actual Trajectory List
            value = float(self.children[0].text)
            MDApp.get_running_app().current_trajectory.poses[self.get_index()].rotation = from_degrees(value) 
            print("{}, {:.2f}".format(self.get_index(), value))
            
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
        if self.current_item == instance_item:
            return
        self.remove_widget(instance_item)

        # TODO: update, so delete current and moves previous to current 

class MainApp(MDApp):
    """Main app class"""

    poses = [to_pose(300, 800, 45), to_pose(400, 900, -45), to_pose(200, 500, 180.0)]
    trajectory = Trajectory(poses=poses)
    points = ListProperty()
    reverse = StringProperty("Forward Trajectory")
    jsonIO = JsonIO()

    trajectories = []
    current_trajectory = Trajectory()

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
        
        # Match poses
        self.update_poses()


    def on_stop(self):
        """Save Settings before leaving"""
        self.jsonIO.save_trajectories(self.trajectories)

    def trajectory_to_list(self, trajectory):
        point_list = []
        for point in trajectory.points:
            point_list.append(point.pose.translation.x)
            point_list.append(point.pose.translation.y)
        return point_list

    def optimize_trajectory(self):
        print("Optimize Trajectory")
    
    def mirror_trajectory(self):
        print("Mirror Trajectory")

    def animate_trajectory(self):
        print("Animate Trajectory")

    def add_point(self):
        print("Add Point")

    def add_trajectory(self):
        print("Add Trajectory")
    
    def down(self):
        print("down")
    
    def up(self):
        print("up")
    
    def trash(self):
        print("trash")
    
    def on_checkbox_active(self, checkbox, value):
        """https://kivymd.readthedocs.io/en/latest/components/selection-controls/"""
        
        self.reverse = "Reverse Trajectory" if checkbox.active else "Forward Trajectory"
        print(self.reverse) 

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
            c.ids.left_container.initial_update(str(self.current_trajectory.poses[i].translation.x), str(self.current_trajectory.poses[i].translation.y), str(self.current_trajectory.poses[i].rotation.get_degrees()))
        
    


MainApp().run()