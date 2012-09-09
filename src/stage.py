import pyglet
import gui

class Stage:
    
    def __init__(self, id, color=(0,0,0,0), obstacles=[]):
        self.id = id
        self.offset = 0
        obstacles.sort(key=lambda obj: obj.x)
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)
        

class Prop(pyglet.sprite.Sprite):
    def __init__(self, image):
        pyglet.sprite.Sprite.__init__(self, image)


class Rock(Prop):
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        Prop.__init__(self, self._image)
