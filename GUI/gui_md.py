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
from kivy.properties import StringProperty, ListProperty


from kivy.core.window import Window
Window.size = (1920, 1080) # Adjust for your monitor resolution, esc to exit
Window.fullscreen = True
# https://stackoverflow.com/questions/21891217/issue-setting-kivy-to-fullscreen



from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationLayout
from kivymd.uix.list import OneLineAvatarIconListItem, MDList
from kivymd.theming import ThemableBehavior

from Geometry.pose import to_pose, Pose
from Trajectory.trajectory import Trajectory

KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: 'Custom'
    on_release: self.parent.set_color_item(self)

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
                                
                                radius: [25, 25, 25, 25]
                                md_bg_color: app.theme_cls.bg_darkest
                                
                                RelativeLayout:
                                    pos: -740, -10
                                    
                                    Image:
                                        source: "Images/2020-field.png"
                                        size_hint: 2.2, 2.2
                                        
                                                                        
                            MDFloatLayout:
                                size: (100,100)
                                size_hint: 0, .55
                                radius: [25, 25, 25, 25]
                                md_bg_color: app.theme_cls.bg_darkest
                            
                                GridLayout:
                                    rows: 2
                                    cols: 1
                                    padding: [10,-10,-10,10]

                                    MDFloatLayout:
                                        size_hint: 0, .25
                                        radius: [25, 25, 25, 25]
                                        md_bg_color: app.theme_cls.primary_dark
                                        RelativeLayout:
                                            pos: 20, 300
                                            GridLayout:
                                                rows: 1
                                                cols: 6
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

                                                MDSlider:
                                                    min: 0
                                                    max: 100
                                                    value: 0
                                                    hint: False
                                                    color: 1,1,1,1
                                                    

                                                TooltipMDIconButton:
                                                    icon: "flip-vertical"
                                                    tooltip_text: "Mirror Trajectory"
                                                    on_press: app.mirror_trajectory()

                                                TooltipMDIconButton:
                                                    icon: "plus"
                                                    tooltip_text: "Add Point" 
                                                    on_press: app.add_point()
                                                
                                    # Placeholder until I add Points
                                    MDFloatLayout:
                                        
                                        radius: [25, 25, 25, 25]
                                        canvas.after:
                                            Color:
                                                rgba: app.theme_cls.accent_color
                                            Line:
                                                points: app.points
                                                width: 1.7
                                        


                        
                        MDFloatLayout:
                            
                            size_hint: .5, 0
                            radius: [25, 25, 25, 25]
                            md_bg_color: app.theme_cls.bg_darkest

                            TooltipMDFloatingActionButton:
                                icon: "plus"
                                md_bg_color: app.theme_cls.primary_dark
                                pos: (1835,30)
                                shift_y: 200
                                tooltip_text: "Add Trajectory"
                                on_press: app.add_trajectory()

                        

                        


        
        MDNavigationDrawer:
            id: nav_drawer
            
            ContentNavigationDrawer:
                id: content_drawer
'''

class ItemDrawer(OneLineAvatarIconListItem):
    icon = StringProperty()

class ContentNavigationDrawer(BoxLayout):
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
        icons_item = {
            "Trajectory 1": "chart-bell-curve-cumulative",
            "Trajectory 2": "chart-bell-curve-cumulative",
            "Trajectory 3": "chart-bell-curve-cumulative",
            "Trajectory 4": "chart-bell-curve-cumulative",
            "Trajectory 5": "chart-bell-curve-cumulative",
            "Trajectory 6": "chart-bell-curve-cumulative",
        }

        for icon_name in icons_item.keys():
            self.screen.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icons_item[icon_name], text=icon_name)
            )

        for item in self.screen.ids.content_drawer.ids.md_list.children:
            self.screen.ids.content_drawer.ids.md_list.set_color_item(item)

        self.points = self.trajectory_to_list(self.trajectory)
        

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
    


MainApp().run()