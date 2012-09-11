import pyglet
import gui

class Stage:
    
    def __init__(self, id, color=(0,0,0,0), obstacles={}):
        self.id = id
        self.offset = 0
        self.obstacles = obstacles
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)
        

class Prop(pyglet.sprite.Sprite):
    def __init__(self, image):
        pyglet.sprite.Sprite.__init__(self, image)


class Rock(Prop):
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        Prop.__init__(self, self._image)
        
        
village_stage = {
        'props': [
                (Rock, 100, 100), (Rock, 200, 50), (Rock, 300, 200),
                (Rock, 740, 150), (Rock, 900, 0), (Rock, 1234, 250),
                (Rock, 1500, 100), (Rock, 1500, 50), (Rock, 1650, 200),
                (Rock, 1730, 150), (Rock, 1900, 0), (Rock, 2012, 250),
                (Rock, 2130, 100), (Rock, 2200, 50), (Rock, 2222, 200),
                (Rock, 2500, 150), (Rock, 2600, 0), (Rock, 2700, 250),
                (Rock, 2710, 100), (Rock, 2720, 50), (Rock, 2730, 200),
                (Rock, 2800, 150), (Rock, 3000, 0), (Rock, 3210, 250),
                (Rock, 3333, 100), (Rock, 3456, 50), (Rock, 3579, 200),
                (Rock, 4000, 150), (Rock, 4567, 0), (Rock, 5000, 250),
        ]
}
