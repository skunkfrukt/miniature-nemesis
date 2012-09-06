import pyglet

class Stage:
    def __init__(self, id):
        self.id = id
        self.offset = 0
        self.bg = pyglet.resource.image('png/testbg.png')

class Prop:
    def __init__(self, id):
        self.id = id