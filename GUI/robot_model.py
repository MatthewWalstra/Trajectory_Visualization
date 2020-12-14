from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout

KV = '''
<RobotModel>:
    
    origin: 500, 500
    angle: 0
    scalar: 4.7
    wheel: 2.5, 1.25
    pos_scalar: 4
    radius: root.scalar / 5, root.scalar / 5
    vel_length: 2.7 #2.7
    accel_length: 2.7 #2.7
    accel_angle: 45
    vector_scalar: .3
    triangle_scalar: 1.5
    center_scalar: 1.6

    canvas.after:
        
        Rotate:
            id: rot
            angle: app.angle
            axis: 0,0,1
            origin: root.origin
        
        #Color:
        #    rgba: app.theme_cls.bg_light
        
        #Point:
        #    points: root.origin
        #    pointsize: 22.5
        
        Color: 
            rgba: app.theme_cls.opposite_bg_darkest
        # Wheels
        # Front Left
        RoundedRectangle:
            pos: root.origin[0] + (root.pos_scalar - root.wheel[0] * 3 / 4) * root.scalar, root.origin[1] + (root.pos_scalar - root.wheel[1] / 2) * root.scalar
            size: root.wheel[0] * root.scalar, root.wheel[1] * root.scalar
            radius: root.radius
        
        # Back Left
        RoundedRectangle:
            pos: root.origin[0] - (root.pos_scalar + root.wheel[0] / 4) * root.scalar, root.origin[1] + (root.pos_scalar - root.wheel[1] / 2) * root.scalar
            size: root.wheel[0] * root.scalar, root.wheel[1] * root.scalar
            radius: root.radius
        
        # Front Right
        RoundedRectangle:
            pos: root.origin[0] + (root.pos_scalar - root.wheel[0] * 3 / 4) * root.scalar, root.origin[1] - (root.pos_scalar + root.wheel[1] / 2) * root.scalar
            size: root.wheel[0] * root.scalar, root.wheel[1] * root.scalar
            radius: root.radius

        # Back Right
        RoundedRectangle:
            pos: root.origin[0] - (root.pos_scalar + root.wheel[0] / 4) * root.scalar, root.origin[1] - (root.pos_scalar + root.wheel[1] / 2) * root.scalar
            size: root.wheel[0] * root.scalar, root.wheel[1] * root.scalar
            radius: root.radius

        #Center
        Ellipse:
            pos: root.origin[0] - root.scalar * root.center_scalar / 2, root.origin[1] - root.scalar * root.center_scalar / 2
            size: root.scalar * root.center_scalar, root.scalar * root.center_scalar

        #Color: 
        #    rgba: app.theme_cls.primary_color
        #Point:
        #    points: root.origin[0] + root.pos_scalar * root.scalar, root.origin[1] + root.pos_scalar * root.scalar, root.origin[0], root.origin[1], root.origin[0] + root.pos_scalar * root.scalar, root.origin[1] - root.pos_scalar * root.scalar, root.origin[0] - root.pos_scalar * root.scalar, root.origin[1] + root.pos_scalar * root.scalar, root.origin[0] - root.pos_scalar * root.scalar, root.origin[1] - root.pos_scalar * root.scalar,
        #    pointsize: root.scalar / 4

        # Vectors
        # Velocity
        Color:
            rgba: app.theme_cls.primary_dark
        Triangle:
            points: (root.origin[0] + root.vel_length * root.scalar - root.radius[0] + 1.5 * root.scalar, root.origin[1] + root.scalar * root.vector_scalar * root.triangle_scalar, root.origin[0] + root.vel_length * root.scalar - root.radius[0] + 1.5 * root.scalar, root.origin[1] - root.scalar * root.vector_scalar * root.triangle_scalar, root.origin[0] + root.vel_length * root.scalar - root.radius[0] + + root.scalar * root.vector_scalar * root.triangle_scalar * 2 + 1.5 * root.scalar, root.origin[1])
            #radius: root.radius

        RoundedRectangle: 
            pos: root.origin[0] + 1.5 * root.scalar, root.origin[1] - (root.wheel[1] * root.scalar * root.vector_scalar) / 2
            size: root.vel_length * root.scalar, root.wheel[1] * root.scalar * root.vector_scalar
            radius: root.radius

        # Acceleration
        Rotate:
            id: rot
            angle: root.accel_angle
            axis: 0,0,1
            origin: root.origin
        Color:
            rgba: app.theme_cls.accent_dark
        Triangle:
            points: (root.origin[0] + root.scalar * root.vector_scalar * root.triangle_scalar, root.origin[1] + root.accel_length * root.scalar - root.radius[1] + 1.5 * root.scalar, root.origin[0] - root.scalar * root.vector_scalar * root.triangle_scalar, root.origin[1] + root.accel_length * root.scalar - root.radius[1] + 1.5 * root.scalar, root.origin[0], root.origin[1] + root.accel_length * root.scalar - root.radius[1] + root.scalar * root.vector_scalar * root.triangle_scalar * 2 + 1.5 * root.scalar)
            

        RoundedRectangle: 
            pos:  root.origin[0] - (root.wheel[1] * root.scalar * root.vector_scalar) / 2, root.origin[1] + 1.5 * root.scalar
            size: root.wheel[1] * root.scalar * root.vector_scalar, root.accel_length * root.scalar
            radius: root.radius

'''

class RobotModel(MDFloatLayout):
    """Draws Robot Model"""

if __name__ == "__main__":
    class MainApp(MDApp):
        def build(self):
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Cyan"
            self.theme_cls.theme_style = "Dark"
            self.screen = Builder.load_string(KV)
            return self.screen

        

    MainApp().run()