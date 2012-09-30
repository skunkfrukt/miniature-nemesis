import pyglet
import math
import collider
import random
from common import AnimatedSprite, GameObject, Projectile
from pyglet.window import key

MIN_Y, MAX_Y = 0, 275


status_severity = {
        'ok': 0,
        'rise': 3,
        'tumble': 2,
        'trip': 1,
        'stun': 4,
        'dead': 999
        }


class Actor(GameObject):
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

    def __init__(self):
        GameObject.__init__(self)
        self.collider = None
        self.direction = (0, 0)
        self.speed = (0.0, 0.0)
        self.stun_time = 0.0
        self.status = 'ok'
    
    def play(self, animation):
        self.sprite.play(animation)
                  
    def update_speed(self, dt):
        if self.status == 'ok':
            dirx, diry = self.direction
            tx, ty = 100 + dirx * self.max_speed, diry * self.max_speed
            self.approach_target_speed(dt, (tx, ty))
        elif self.status == 'rise':
            if self.stun_time <= 0:
                self.apply_status('ok')
        elif self.status == 'tumble':
            if self.speed[0] < 1:
                self.apply_status('rise')
            else:
                self.approach_target_speed(dt, (0,0))
        elif self.status == 'trip':
            if self.stun_time <= 0:
                self.apply_status('tumble')
        elif self.status == 'stun':
            if self.stun_time <= 0:
                self.speed = (100, 0)
                self.apply_status('ok')
        self.stun_time -= dt
        
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
        self.y = min(max(self.y, MIN_Y), MAX_Y)
        self.sprite.x = self.x - stage_offset
        self.sprite.y = self.y
        self.collider.move(self.x, self.y)
        self.animate()
        
    def animate(self):
        pass
        
    def handle_collision(self, other):
        if not other.collision_effect:
            return
        effect, strength = other.collision_effect
        if status_severity[effect] <= status_severity[self.status]:
            return False
        else:
            return self.apply_status(effect, strength)
            
    def apply_status(self, effect, strength=0):
        if effect == 'ok':
            self.stun_time = 0.0
        elif effect == 'rise':
            self.stun_time = 0.3
            self.speed = (0, 0)
        elif effect == 'tumble':
            self.stun_time = 1
            self.speed = (self.max_speed * 2, 0)
        elif effect == 'trip':
            self.stun_time = 0.2
            # self.speed = (0,0)
        elif effect == 'stun':
            self.stun_time = strength
            self.speed = (-100, 0)
        elif effect == 'dead':
            self.speed = (0, 0)
        else:
            return False
        self.status = effect
        return True
            
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
                
    @property
    def width(self):
        return self.sprite.width
        
    def reset(self, x, y):
        GameObject.reset(self, x, y)
        self.apply_status('ok')
        
    def fire_projectile(self, projectile_cls, speed, target=None):
        origin_x = self.x - 320
        origin_y = random.randint(0, 360)
        if target is not None:
            target_x, target_y = target.x, target.y
        else:
            target_x = self.x  # origin_x + 1
            target_y = self.y  # origin_y
        self.dispatch_event('on_projectile_fired',
                projectile_cls, origin_x, origin_y,
                target_x, target_y, speed)

Actor.register_event_type('on_projectile_fired')


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
        Actor.__init__(self)
        self.set_sprite(AnimatedSprite(self.animations, default='run'))
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
        
    def move(self, dt, stage_offset):
        dirx, diry = self.direction
        Actor.move(self, dt, stage_offset)
                
    def animate(self):
        dirx, diry = self.direction
        if self.status == 'stun':
            self.play('hurt')
        elif self.status == 'trip':
            self.play('trip')
        elif self.status == 'tumble':
            self.play('tumble')
        elif self.status == 'rise':
            self.play('rise')
        elif self.status == 'ok':
            if dirx > 0:
                self.play('sprint')
            elif dirx < 0 and self.speed[0] > -self.max_speed:
                self.play('stop')
            else:
                self.play('run')


class Peasant(Actor):
    _image = pyglet.resource.image('img/sprites/anim_peasant-a_minimal.png')
    _frame_data = {
            'idle': ((0, 2), 1.1, True),
            'run': ((2, 4), 0.2, True),
            'notice': ((4, 6), 1.2, True),
            'aim': ((6, 8), 1.2, False),
            'throw': ((8, 9), 1.2, False)
            }
    animations = Actor.make_animations(_image, 9, _frame_data)
    
    max_speed = 60.0
    acceleration = (150, 300)
    collision_effect = ('trip', 0.5)

    def __init__(self):
        Actor.__init__(self)
        self.set_sprite(AnimatedSprite(self.animations, default='idle'))
        self.collider = collider.Collider(0,0,30,20)
        self.speed = (random.randint(0,1)*random.randint(0, self.max_speed), 0)
        
    def update_speed(self, dt):
        x, y = self.speed
        if x > 0:
            self.sprite.play('run')
        else:
            self.sprite.play('idle')
            


class Pebble(Projectile):
    _image = pyglet.resource.image('img/sprites/missile_pebble_minimal.png')
    _frame_data = {'thrown': ((0, 3), 0.2, True)}
    animations = Actor.make_animations(_image, 3, _frame_data)
    collision_effect = ('trip', 1.0)
    
    def __init__(self):
        Projectile.__init__(self)
        self.set_sprite(AnimatedSprite(self.animations, default='thrown'))
        self.collider = collider.Collider(0,0,1,1)
    