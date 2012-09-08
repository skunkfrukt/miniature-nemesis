import pyglet
import gui

class Stage:
    
    def __init__(self, id, color=(0,0,0,0)):
        self.id = id
        self.offset = 0
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)

class Prop:
    def __init__(self):
        pass

class Rock(Prop):
    def __init__(self):
        pass
