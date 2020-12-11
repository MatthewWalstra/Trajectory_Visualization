from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDFloatingActionButton:
    icon: "plus"
    md_bg_color: app.theme_cls.opposite_bg_dark
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

MainApp().run()