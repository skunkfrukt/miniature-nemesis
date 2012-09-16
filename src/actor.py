import pyglet
import math
import collider
from pyglet.window import key

class Actor(pyglet.sprite.Sprite):
    max_speed = 0.0
    acceleration = (100, 100)
    
    @classmethod
    def make_animations(cls, image, number_of_frames, frame_data):
        """Makes an animation set for an Actor subclass.
        
        Keyword arguments:
        image -- the image to be used as a sprite sheet
        number_of_frames
        frame_data -- data on how to process the sprite sheet
        
        The frame data is given in the form of a dictionary,
        where the keys are the names of the animations, and the
        values are tuples following this formula:
            ((fa, fz), speed, loop),
        where fa and fz are the start and end index of the frames
        to be used, speed is the duration of each frame, and
        loop is a boolean value determining whether to loop the
        animation.
        
        """
        fis = pyglet.image.Animation.from_image_sequence
        grid = pyglet.image.ImageGrid(image, 1, number_of_frames)
        animations = {}
        for name, template in frame_data.items():
            animations[name] = fis(grid[slice(*template[0])], *template[1:])
        return animations

    def __init__(self, animations=None, default=None):
        if animations is not None:
            self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        pyglet.sprite.Sprite.__init__(self, self.animations[default])
        self.current_animation = default
        self.direction = (0, 0)
        self.speed = (0, 0)
        self.stun_time = 0.0
    
    def play(self, animation):
        if animation == self.current_animation:
            return
        elif animation in self.animations:
            self.image = self.animations[animation]
            self.current_animation = animation
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))
                  
    def update_speed(self, dt):
        if self.stun_time <= 0:
            dirx, diry = self.direction
            tx, ty = dirx * self.max_speed, diry * self.max_speed
            self.approach_target_speed(dt, (tx, ty))
        else:
            self.stun_time -= dt
            self.speed = (-160, 0)
        if self.stun_time > 0:
            print "STUN: %d" % self.stun_time 
        else: print self.speed
        
    def approach_target_speed(self, dt, target=(0, 0)):
        dx, dy = self.speed
        tx, ty = target
        ax, ay = self.acceleration
        if tx < dx:
            dx -= ax * dt
            dx = max(dx, tx)
        elif tx > dx:
            dx += ax * dt
            dx = min(dx, tx)
        if ty < dy:
            dy -= ay * dt
            dy = max(dy, ty)
        elif ty > dy:
            dy += ay * dt
            dy = min(dy, ty)
        self.speed = (dx, dy)
            
    
    def update_position(self, dt):
        dx, dy = self.speed
        self.x += dx * dt
        self.y += dy * dt
        
    def handle_collision(self, other):
        if not other.collision_effect:
            return
        effect, strength = other.collision_effect
        if effect == 'stun' and strength > self.stun_time:
            self.stun_time = strength
            self.play('hurt')


class Hero(Actor):
    _image = pyglet.resource.image('img/sprites/anim_hero_minimal.png')
    _frame_data = {
            'idle': ((0, 2), 0.12, True),
            'run': ((2, 4), 0.12, True),
            'sprint': ((4, 6), 0.12, True),
            'stop': ((6, 8), 0.12, True),
            'hurt': ((8, 10), 0.12, False)
            }
    animations = Actor.make_animations(_image, 10, _frame_data)
    
    max_speed = 80.0
    acceleration = (200, 400)

    def __init__(self):
        Actor.__init__(self, default='run')

    def fixSpeed(self, keys):
        dirx = 0
        diry = 0
        if keys[key.W] or keys[key.UP]:
            diry += 1
        if keys[key.S] or keys[key.DOWN]:
            diry -= 1
        if keys[key.A] or keys[key.LEFT]:
            dirx -= 1
        if keys[key.D] or keys[key.RIGHT]:
            dirx += 1
        self.direction = (dirx, diry)
        if self.stun_time > 0:
            self.play('hurt')
        elif dirx > 0:
            self.play('sprint')
        elif dirx < 0 and self.speed[0] > -self.max_speed:
            self.play('stop')
        else:
            self.play('run')


class Peasant(Actor):
    _image = pyglet.resource.image('img/sprites/anim_peasant-a_minimal.png')
    _frame_data = {
            'idle': ((0, 2), 1.2, True),
            'run': ((2, 4), 1.2, True),
            'notice': ((4, 6), 1.2, True),
            'aim': ((6, 8), 1.2, False),
            'throw': ((8, 9), 1.2, False)
            }
    animations = Actor.make_animations(_image, 9, _frame_data)


class Woodpecker(Actor):
    _image = pyglet.resource.image('img/sprites/anim_woodpecker_minimal.png')
    _frame_data = {'fly': ((0, 2), 0.1, True)}
    animations = Actor.make_animations(_image, 2, _frame_data)

    max_speed = 100
    acceleration = (50, 50)

    def __init__(self):
        Actor.__init__(self, default='fly')
        self.target_speed = (0, 0)
        
    def set_aim(x, y):
        self.aim = (x, y)
        
