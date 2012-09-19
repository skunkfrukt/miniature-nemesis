import pyglet
import math
import collider
from pyglet.window import key

class AnimatedSprite(pyglet.sprite.Sprite):
    def __init__(self, animations=None, default=None):
        self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        pyglet.sprite.Sprite.__init__(self, self.animations[default])
        
    def play(self, animation):
        if animation == self.current_animation:
            return
        elif animation in self.animations:
            self.image = self.animations[animation]
            self.current_animation = animation
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))


class Actor(object):
    max_speed = 0.0
    acceleration = (100, 100)
    
    @classmethod
    def make_animations(cls, image, number_of_frames, frame_data):
        fis = pyglet.image.Animation.from_image_sequence
        grid = pyglet.image.ImageGrid(image, 1, number_of_frames)
        animations = {}
        for name, template in frame_data.items():
            animations[name] = fis(grid[slice(*template[0])], *template[1:])
        return animations

    def __init__(self, animations=None, default=None):
        self.sprite = AnimatedSprite(animations, default)
        self.sprite.current_animation = default
        self.collider = None
        self.direction = (0, 0)
        self.speed = (0.0, 0.0)
        self.stun_time = 0.0
    
    def play(self, animation):
        self.sprite.play(animation)
                  
    def update_speed(self, dt):
        if self.stun_time <= 0:
            dirx, diry = self.direction
            tx, ty = 100 + dirx * self.max_speed, diry * self.max_speed
            self.approach_target_speed(dt, (tx, ty))
        else:
            self.stun_time -= dt
            self.speed = (-60, 0)
        if self.stun_time > 0:
            print "STUN: %.2f" % self.stun_time 
        # else: print self.speed
        
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
    
    def move(self, dt, stage_offset):
        self.update_speed(dt)
        dx, dy = self.speed
        self.x += dx * dt
        self.y += dy * dt
        self.sprite.x = self.x - stage_offset
        self.sprite.y = self.y
        self.collider.x = self.x + 10
        self.collider.y = self.y
        
    def handle_collision(self, other):
        if not other.collision_effect:
            return
        effect, strength = other.collision_effect
        if effect == 'stun' and strength > self.stun_time:
            self.stun_time = strength
            self.play('hurt')
            
    def collide(self, other):
        if not (self.collider and other.collider):
            return False
        else:
            collision = self.collider.collide(other.collider)
            if collision:
                self.handle_collision(other)
            return collision
        
    def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group


class Hero(Actor):
    _image = pyglet.resource.image('img/sprites/anim_hero.png')
    _frame_data = {
            'idle': ((0, 2), 0.12, True),
            'run': ((2, 4), 0.12, True),
            'sprint': ((4, 6), 0.12, True),
            'stop': ((6, 8), 0.12, True),
            'hurt': ((8, 10), 0.12, False),
            'trip': ((10, 11), 0.12, False),
            'tumble': ((11, 13), 0.12, True),
            'rise': ((13, 14), 0.12, False)
            }
    animations = Actor.make_animations(_image, 14, _frame_data)
    
    max_speed = 80.0
    acceleration = (200, 400)

    def __init__(self):
        Actor.__init__(self, self.animations, default='run')
        self.collider = collider.Collider(0,0,30,20)

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
        
