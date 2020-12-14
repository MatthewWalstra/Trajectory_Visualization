from kivy.lang import Builder

from kivymd.app import MDApp

from kivy.graphics import Line, Color, Ellipse, Point

KV = '''


Screen:

   
'''


class TestCard(MDApp):
    point_list = [100,100, 300,300, 300,500]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        self.screen = Builder.load_string(KV)

        with self.screen.canvas.after:
            Color(self.theme_cls.primary_color[0],self.theme_cls.primary_color[1],self.theme_cls.primary_color[2],self.theme_cls.primary_color[3])
            radius = 50 / 8
            for i in range(len(self.point_list) // 2):
                
                Line(circle=(self.point_list[2 * i], self.point_list[2 * i + 1], radius), width= 1.1, color=self.theme_cls.primary_color)
                
                
                Ellipse(size=(radius,radius), pos=(self.point_list[2 * i] - radius/2, self.point_list[2 * i + 1] - radius/2))
                
        return self.screen


TestCard().run()