from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import IRightBodyTouch, ILeftBodyTouch, OneLineAvatarIconListItem

KV = '''
<TooltipMDIconButton@MDIconButton+MDTooltip>

<item>:
    
    on_size:
        self.ids._right_container.width = container.width + 50
        self.ids._right_container.x = container.width - 200

        self.ids._left_container.width = 600
        self.ids._left_container.x = 100
    _no_ripple_effect: True
    LContainer:
        id: left_container
        #MDIconButton:
        #    icon: "arrow-down"
        #    on_press: app.down()
        
        
        RelativeLayout:
            pos: 300, 0
            MDTextField:
                pos: 50, 0
                hint_text: "X-Coordinate:"
                #helper_text: "X-Coordinate:"
                #helper_text_mode: "persistent"
                color_mode: "custom"
                line_color_focus: 1,1,1,1
        
        RelativeLayout:
            pos: 300, 0
            MDTextField:
                pos: 150, 0
                hint_text: "Y-Coordinate:"
                #helper_text: "Y-Coordinate:"
                #helper_text_mode: "persistent"
                color_mode: "custom"
                line_color_focus: 1,1,1,1
        
        RelativeLayout:
            pos: 300, 0
            MDTextField:
                pos: 300, 0
                hint_text: "Theta (degrees):"
                #helper_text: "X-Coordinate:"
                #helper_text_mode: "persistent"
                color_mode: "custom"
                line_color_focus: 1,1,1,1
        

        #MDIconButton: 
        #    icon: "arrow-up"
        #    on_press: app.up()

    Container:
        id: container

        TooltipMDIconButton:
            icon: "arrow-up"
            on_press: app.up()
            tooltip_text: "Move Up"

        TooltipMDIconButton:
            icon: "arrow-down"
            on_press: app.down()
            tooltip_text: "Move Down"
        
        MDIconButton:
            icon: "trash-can"
            on_press: app.trash()
        
        

ScrollView:
    MDList:
        id: point_list        
'''

class item(OneLineAvatarIconListItem):
    pass

class LContainer(ILeftBodyTouch, MDGridLayout):
    size_hint = 50,0
    cols = 3
    rows = 1

class Container(IRightBodyTouch, MDGridLayout):
    adaptive_width = True
    cols = 3
    rows = 1


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        for i in range(20):
            self.root.ids.point_list.add_widget(
                item()
            )

    def down(self):
        print("down")
    
    def up(self):
        print("up")
    
    def trash(self):
        print("trash")


MainApp().run()