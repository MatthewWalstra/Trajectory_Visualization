import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# Number of os.path.dirname dependent on number of subfolders: goes up 1 directory each time
# Uncomment top line if you want to use the run button in the top right
# F5 works because of adding Trajectory_Visualization directory to PYTHONPATH in .env file


from kivy.lang import Builder

from kivy.properties import NumericProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from Util.util import limit2

KV = '''
<StatLabel>:
    orientation: "vertical"
    size_hint: 1, 1
    #size: self.minimum_size
    md_bg_color: app.theme_cls.bg_dark
    radius: [6, 6, 6, 6]

    MDBoxLayout:
        size_hint: 1, .5
        #size: self.minimum_size
        md_bg_color: app.theme_cls.bg_normal
        radius: [6, 6, 6, 6]
        spacing: 200
        padding: 50
        
        MDLabel:
            id: title
            text: "Generation Time"
            theme_text_color: "Custom"
            text_color: app.theme_cls.opposite_bg_darkest
            halign: "left"
            
            
    MDLabel:
        id: value
        text: "420"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        halign: "center"
        font_style: "H3"

<SliderLayout>:
    orientation: "vertical"
    padding: 10
    MDLabel:
        id: title
        text: "Max Velocity (in/s)"
        theme_text_color: "Custom"
        text_color: app.theme_cls.opposite_bg_darkest
        halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        spacing: 40
        padding: 20
        MDSlider:
            id: slider
            size_hint: 10,1
            value: self.parent.parent.value
            min: 0
            max: 200
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
                
            


MDBoxLayout:
    orientation: "vertical"
    md_bg_color: app.theme_cls.bg_darkest
    MDGridLayout:
        rows: 2
        cols: 2
        spacing: 20
        padding: 10

        StatLabel:
            id: generation
        StatLabel:
            id: drive
        StatLabel:
            id: length
        StatLabel:
            id: current_vel
    MDBoxLayout:
        orientation: "vertical"    
        SliderLayout:
            value: 40
        SliderLayout:
        SliderLayout:
        SliderLayout:
        SliderLayout:

'''

class StatLabel(MDBoxLayout):
    text = StringProperty("Base")
    value = NumericProperty(420)
    pass

class SliderLayout(MDBoxLayout):
    value = NumericProperty()

    text = StringProperty("Base")
    min_v = NumericProperty(0)
    max_v = NumericProperty(200)
    
    def test(self):
        prev_value = self.value
        try:
            value = limit2(float(self.ids.text.text), self.ids.slider.min, self.ids.slider.max)
            self.value =  value
            self.ids.text.text = str(value)
        except ValueError:
            self.value = prev_value
            self.ids.text.text = str(prev_value)
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

MainApp().run()