class GameObject(object):
    '''Superclass of all objects that are drawn on stage.'''
    def __init__(self):
        self.dead = True
        self.x, self.y = 0, 0
        
    def kill(self):
        self.dead = True
        
    def reset(self, x, y):
        self.x, self.y = x, y
        self.dead = False
        
        
class Point(object):
    '''A point in 2D space.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y